"""Telegram CDN retrieval, AES-CTR decryption and ``FileHash``-bounded integrity checks.

The module accepts and returns immutable ``bytes``. It does not zeroize ciphertext, plaintext, redirect keys, IVs or temporary counter buffers. Callers that require memory sanitization must manage process and buffer lifetimes.
"""

from __future__ import annotations

import hashlib
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from miniproto.crypto.mtproto import media_ctr_crypt
from miniproto.observability import record_metric
from miniproto.raw import functions, types

CDN_HASH_BLOCK_SIZE = 128 * 1024


class CdnError(RuntimeError):
    """Base exception for unsupported CDN responses and integrity failures."""


class CdnIntegrityError(CdnError):
    """Raised when a CDN range lacks valid ``FileHash`` coverage or verification fails.

    This includes missing hash metadata, non-positive ``FileHash.limit``, responses shorter than a declared hash interval, SHA-256 mismatches and intervals that cannot fit a legal CDN request. Each declared limit determines the exact number of decrypted bytes to hash.
    """


type RawInvoker = Callable[..., Awaitable[object]]


@dataclass(frozen=True, slots=True)
class CdnRedirect:
    """Metadata supplied by Telegram when it redirects a file to its CDN.

    Attributes:
        dc_id: CDN data-center identifier.
        file_token: Opaque bearer token for CDN file, hash and reupload requests.
        encryption_key: Expected 32-byte AES-CTR key, validated at decryption, retained as immutable bytes without zeroization.
        encryption_iv: Expected 16-byte IV, validated at decryption. Its first 12 bytes form the counter prefix, the file block offset replaces its final four bytes. Retained without zeroization.
        file_hashes: Hash metadata supplied with the redirect.
        raw: Original raw Telegram redirect object.
    """

    dc_id: int
    file_token: bytes = field(repr=False)
    encryption_key: bytes = field(repr=False)
    encryption_iv: bytes = field(repr=False)
    file_hashes: tuple[object, ...]
    raw: types.UploadFileCdnRedirect = field(repr=False)


async def get_cdn_file_part(
    origin_invoke: RawInvoker,
    cdn_invoke: RawInvoker,
    redirect: CdnRedirect,
    *,
    offset: int,
    limit: int,
    request_timeout: float | None = None,
) -> bytes:
    """Fetch, decrypt and hash-verify one CDN file range.

    Args:
        origin_invoke: Async master-DC invoker used for hashes and reupload authorization.
        cdn_invoke: Async CDN-DC invoker used only for ``upload.getCdnFile``.
        redirect: CDN credentials and encryption metadata returned by Telegram.
        offset: Byte offset of the requested range and CTR stream.
        limit: Maximum plaintext bytes to return. Retrieval covers complete hash intervals and can overfetch aligned ciphertext ranges.
        request_timeout: Optional per-RPC timeout in seconds.

    Returns:
        The requested slice of complete SHA-256-verified plaintext intervals, at most ``limit`` bytes.

    Raises:
        ValueError: ``offset`` or ``limit`` is invalid, or redirect key/IV lengths or the CTR offset violate decryption constraints.
        CdnIntegrityError: The range lacks complete valid hash coverage, its digest mismatches or a hash interval cannot fit a legal CDN request.
        CdnError: Telegram returns an unsupported CDN response.
        asyncio.CancelledError: The caller cancels the awaited transfer.
    """
    if offset < 0 or limit <= 0:
        raise ValueError("CDN offset must be non-negative and limit must be positive")
    requested_end = offset + limit
    hashes = _file_hash_map(redirect.file_hashes)
    cursor = offset
    chunks: list[bytes] = []
    while cursor < requested_end:
        file_hash = _covering_file_hash(hashes, cursor)
        if file_hash is None:
            fetched = await origin_invoke(
                functions.UploadGetCdnFileHashes(file_token=redirect.file_token, offset=cursor),
                request_timeout=request_timeout,
                retry=True,
            )
            record_metric("media.cdn.hash_fetches", 1)
            for item in _iter_file_hashes(fetched):
                hashes.setdefault(int(item.offset), item)
            file_hash = _covering_file_hash(hashes, cursor)
        if file_hash is None:
            raise CdnIntegrityError(f"no CDN file hash covers offset {cursor}")
        hash_offset = int(file_hash.offset)
        hash_limit = int(file_hash.limit)
        if hash_limit <= 0:
            raise CdnIntegrityError(f"invalid CDN file hash limit at offset {hash_offset}")
        wire_offset, wire_limit = _cdn_wire_range(hash_offset, hash_limit)
        while True:
            result = await cdn_invoke(
                functions.UploadGetCdnFile(file_token=redirect.file_token, offset=wire_offset, limit=wire_limit),
                request_timeout=request_timeout,
                dc_id=redirect.dc_id,
            )
            if isinstance(result, types.UploadCdnFileReuploadNeeded):
                await origin_invoke(
                    functions.UploadReuploadCdnFile(file_token=redirect.file_token, request_token=result.request_token),
                    request_timeout=request_timeout,
                    retry=True,
                )
                continue
            if not isinstance(result, types.UploadCdnFile):
                raise CdnError(f"unsupported CDN file response: {type(result).__name__}")
            plaintext = decrypt_cdn_chunk(
                result.bytes, key=redirect.encryption_key, iv=redirect.encryption_iv, offset=wire_offset
            )
            short_read_end = wire_offset + len(plaintext) if len(result.bytes) < wire_limit else None
            break
        block_start = hash_offset - wire_offset
        block = plaintext[block_start : block_start + hash_limit]
        if len(block) != hash_limit:
            raise CdnIntegrityError(
                f"CDN chunk at offset {hash_offset} is not verifiable: got {len(block)} of {hash_limit} hashed bytes"
            )
        if hashlib.sha256(block).digest() != bytes(file_hash.hash):
            record_metric("media.cdn.hash_mismatches", 1)
            raise CdnIntegrityError(f"CDN block SHA-256 mismatch at offset {hash_offset}")
        record_metric("media.cdn.blocks_verified", 1)
        slice_start = cursor - hash_offset
        slice_end = min(hash_limit, requested_end - hash_offset)
        chunks.append(block[slice_start:slice_end])
        cursor = hash_offset + slice_end
        if short_read_end is not None and cursor >= short_read_end:
            break
    return b"".join(chunks)


async def verify_cdn_part(
    invoke: RawInvoker,
    redirect: CdnRedirect,
    *,
    offset: int,
    data: bytes,
    known_hashes: dict[int, types.FileHash] | None = None,
    request_timeout: float | None = None,
) -> None:
    """Verify a decrypted CDN chunk against complete declared SHA-256 hash intervals.

    Args:
        invoke: Async raw-RPC invoker used to request missing CDN hash metadata.
        redirect: CDN token and redirect-provided hash metadata for this file.
        offset: File offset of the first byte in ``data``.
        data: Decrypted bytes beginning at a hash interval's exact offset, bytes are not zeroized.
        known_hashes: Optional mutable offset-to-hash cache shared by the caller, redirect hashes seed a new cache only when it is omitted.
        request_timeout: Optional per-RPC timeout in seconds for missing hash fetches.

    Raises:
        CdnIntegrityError: Any byte lacks a complete declared hash interval, hash metadata is invalid or a SHA-256 digest mismatches.
        asyncio.CancelledError: The awaited metadata request is cancelled.

    Missing metadata is fetched from the master DC with ``upload.getCdnFileHashes``. ``data`` must contain complete consecutive hash intervals, each starting at the declared ``FileHash.offset`` and containing exactly ``FileHash.limit`` bytes. This helper does not retrieve missing plaintext for partial intervals.
    """
    if not data:
        return
    hashes = _file_hash_map(redirect.file_hashes) if known_hashes is None else known_hashes
    position = 0
    while position < len(data):
        block_offset = offset + position
        file_hash = hashes.get(block_offset)
        if file_hash is None:
            fetched = await invoke(
                functions.UploadGetCdnFileHashes(file_token=redirect.file_token, offset=block_offset),
                request_timeout=request_timeout,
                retry=True,
            )
            record_metric("media.cdn.hash_fetches", 1)
            for item in _iter_file_hashes(fetched):
                hashes.setdefault(int(item.offset), item)
            file_hash = hashes.get(block_offset)
        if file_hash is None:
            raise CdnIntegrityError(f"no CDN file hash covers offset {block_offset}")
        hash_limit = int(file_hash.limit)
        if hash_limit <= 0:
            raise CdnIntegrityError(f"invalid CDN file hash limit at offset {block_offset}")
        block = bytes(data[position : position + hash_limit])
        if len(block) != hash_limit:
            raise CdnIntegrityError(
                f"CDN chunk at offset {block_offset} is not verifiable: got {len(block)} of {hash_limit} hashed bytes"
            )
        if hashlib.sha256(block).digest() != bytes(file_hash.hash):
            record_metric("media.cdn.hash_mismatches", 1)
            raise CdnIntegrityError(f"CDN block SHA-256 mismatch at offset {block_offset}")
        record_metric("media.cdn.blocks_verified", 1)
        position += hash_limit


def cdn_redirect_from_raw(result: object) -> CdnRedirect | None:
    """Convert a raw CDN redirect response to stable transfer metadata.

    Args:
        result: Raw result returned by ``upload.getFile``.

    Returns:
        A :class:`CdnRedirect` for a CDN redirect, otherwise ``None``.
    """
    if not isinstance(result, types.UploadFileCdnRedirect):
        return None
    return CdnRedirect(
        dc_id=result.dc_id,
        file_token=result.file_token,
        encryption_key=result.encryption_key,
        encryption_iv=result.encryption_iv,
        file_hashes=tuple(result.file_hashes),
        raw=result,
    )


def decrypt_cdn_chunk(data: bytes, *, key: bytes, iv: bytes, offset: int = 0) -> bytes:
    """Decrypt a CDN ciphertext range with the counter aligned to its file offset.

    Args:
        data: Ciphertext bytes for a contiguous CDN response, immutable buffers are not zeroized.
        key: Exactly 32 bytes of AES key material, immutable buffers are not zeroized.
        iv: Exactly 16 bytes, the first 12 form the counter prefix and the final four are replaced with ``offset // 16``. Immutable buffers are not zeroized.
        offset: Non-negative file byte offset of ``data``, defaults to ``0``, its block index must fit in 32 bits.

    Returns:
        Plaintext bytes of the same length as ``data``.

    Raises:
        ValueError: ``key``, ``iv`` or ``offset`` violates CDN cryptographic constraints.
    """
    if len(key) != 32:
        raise ValueError("CDN encryption key must be 32 bytes")
    if len(iv) != 16:
        raise ValueError("CDN encryption IV must be 16 bytes")
    if offset < 0:
        raise ValueError("CDN offset must not be negative")
    block_offset, byte_offset = divmod(offset, 16)
    if block_offset > 0xFFFFFFFF:
        raise ValueError("CDN offset exceeds the 32-bit counter range")
    counter_iv = iv[:12] + block_offset.to_bytes(4, "big")
    if byte_offset:
        return media_ctr_crypt(b"\x00" * byte_offset + data, key, counter_iv)[byte_offset:]
    return media_ctr_crypt(data, key, counter_iv)


def _file_hash_map(file_hashes: tuple[object, ...]) -> dict[int, types.FileHash]:
    """Index raw ``FileHash`` objects by starting offset, retaining the first duplicate.

    Args:
        file_hashes: Redirect-provided candidates, filtered by type without validating interval bounds or digests.
    """
    hashes: dict[int, types.FileHash] = {}
    for item in _iter_file_hashes(file_hashes):
        hashes.setdefault(int(item.offset), item)
    return hashes


def _covering_file_hash(hashes: dict[int, types.FileHash], offset: int) -> types.FileHash | None:
    """Return the declared hash interval containing one file offset.

    Args:
        hashes: Known file hashes indexed by their starting offsets.
        offset: File position that must be covered.
    """
    for start in sorted(hashes, reverse=True):
        item = hashes[start]
        if start <= offset < start + int(item.limit):
            return item
    return None


def _cdn_wire_range(hash_offset: int, hash_limit: int) -> tuple[int, int]:
    """Return a legal CDN request range covering one complete hash interval.

    Args:
        hash_offset: Start of the Telegram hash interval.
        hash_limit: Complete byte length authenticated by that hash.

    Raises:
        CdnIntegrityError: No 4 KiB-aligned request of at most one MiB covers the interval within a single one-MiB boundary.
    """
    wire_offset = hash_offset - (hash_offset % 4096)
    required = hash_offset + hash_limit - wire_offset
    for candidate in (4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576):
        if candidate >= required and wire_offset // 1048576 == (wire_offset + candidate - 1) // 1048576:
            return wire_offset, candidate
    raise CdnIntegrityError(f"CDN hash interval at offset {hash_offset} crosses a 1 MiB request boundary")


def _iter_file_hashes(value: object) -> tuple[types.FileHash, ...]:
    """Return only supported raw file-hash values from a scalar or sequence.

    Args:
        value: Candidate ``FileHash`` or sequence returned by Telegram.
    """
    if isinstance(value, types.FileHash):
        return (value,)
    if isinstance(value, tuple | list):
        return tuple(item for item in value if isinstance(item, types.FileHash))
    return ()


__all__ = [
    "CDN_HASH_BLOCK_SIZE",
    "CdnError",
    "CdnIntegrityError",
    "CdnRedirect",
    "cdn_redirect_from_raw",
    "decrypt_cdn_chunk",
    "get_cdn_file_part",
    "verify_cdn_part",
]
