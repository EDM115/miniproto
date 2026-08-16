"""Telegram CDN retrieval, AES-CTR decryption, and ``FileHash``-bounded integrity checks.

The module accepts and returns ordinary immutable ``bytes``. Ciphertext,
plaintext, redirect keys, IVs, and temporary counter buffers are not explicitly
zeroized; callers that require memory sanitization must manage their own process
and buffer-lifetime boundary.
"""

from __future__ import annotations

import hashlib
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from miniproto.crypto.mtproto import media_ctr_crypt
from miniproto.observability import record_metric
from miniproto.raw import functions, types

CDN_HASH_BLOCK_SIZE = 128 * 1024


class CdnError(RuntimeError):
    """Raised when a CDN response cannot be reuploaded, decrypted, or interpreted."""


class CdnIntegrityError(CdnError):
    """Raised when a CDN range lacks valid ``FileHash`` coverage or verification fails.

    This includes missing hash metadata, non-positive declared ``FileHash.limit``,
    a response shorter than that declared limit, and SHA-256 mismatches. The
    declared limit controls exactly how many decrypted bytes form each verified
    range; it is not assumed to be a fixed-size block.
    """


type RawInvoker = Callable[..., Awaitable[object]]


@dataclass(frozen=True, slots=True)
class CdnRedirect:
    """Validated information supplied by Telegram when a file moves to its CDN.

    Attributes:
        dc_id: CDN data-center identifier.
        file_token: Opaque token authorizing CDN file and hash requests.
        encryption_key: 32-byte AES-CTR key for CDN ciphertext; retained as immutable bytes and not zeroized.
        encryption_iv: 16-byte initial counter block for CDN ciphertext; retained as immutable bytes and not zeroized.
        file_hashes: Hash metadata supplied with the redirect.
        raw: Original raw Telegram redirect object.
    """

    dc_id: int
    file_token: bytes
    encryption_key: bytes
    encryption_iv: bytes
    file_hashes: tuple[object, ...]
    raw: types.UploadFileCdnRedirect


async def get_cdn_file_part(
    invoke: RawInvoker, redirect: CdnRedirect, *, offset: int, limit: int, request_timeout: float | None = None
) -> bytes:
    """Fetch, decrypt, and hash-verify one CDN file range.

    Args:
        invoke: Async raw-RPC invoker bound to the appropriate data center.
        redirect: CDN credentials and encryption metadata returned by Telegram.
        offset: Byte offset of the requested range and CTR stream.
        limit: Maximum ciphertext/plaintext bytes to retrieve.
        request_timeout: Optional per-RPC timeout in seconds.

    Returns:
        The decrypted, integrity-verified bytes returned for the requested range.

    Raises:
        CdnIntegrityError: The range lacks coverage, has an invalid/short declared
            hash range, or its digest mismatches.
        CdnError: Telegram returns an unsupported CDN response.
        asyncio.CancelledError: The caller cancels the awaited transfer.
    """
    while True:
        result = await invoke(
            functions.UploadGetCdnFile(file_token=redirect.file_token, offset=offset, limit=limit),
            request_timeout=request_timeout,
        )
        if isinstance(result, types.UploadCdnFileReuploadNeeded):
            await invoke(
                functions.UploadReuploadCdnFile(file_token=redirect.file_token, request_token=result.request_token),
                request_timeout=request_timeout,
                retry=True,
            )
            continue
        if isinstance(result, types.UploadCdnFile):
            payload = decrypt_cdn_chunk(
                result.bytes, key=redirect.encryption_key, iv=redirect.encryption_iv, offset=offset
            )
            await verify_cdn_part(invoke, redirect, offset=offset, data=payload, request_timeout=request_timeout)
            return payload
        raise CdnError(f"unsupported CDN file response: {type(result).__name__}")


async def verify_cdn_part(
    invoke: RawInvoker,
    redirect: CdnRedirect,
    *,
    offset: int,
    data: bytes,
    known_hashes: dict[int, types.FileHash] | None = None,
    request_timeout: float | None = None,
) -> None:
    """Verify a decrypted CDN chunk against Telegram's 128 KiB SHA-256 file hashes.

    Args:
        invoke: Async raw-RPC invoker used to request missing CDN hash metadata.
        redirect: CDN token and redirect-provided hash metadata for this file.
        offset: File offset of the first byte in ``data``.
        data: Already-decrypted CDN bytes to validate; bytes are not zeroized.
        known_hashes: Optional mutable offset-to-hash cache shared by the caller.
            Redirect hashes seed a new cache when it is omitted.
        request_timeout: Optional per-RPC timeout in seconds for missing hash fetches.

    Raises:
        CdnIntegrityError: Any byte lacks a valid complete hash block, hash metadata
            is invalid, or a SHA-256 digest mismatches.
        asyncio.CancelledError: The awaited metadata request is cancelled.

    Hashes delivered with the redirect seed the lookup; uncovered blocks are
    fetched from the master DC with ``upload.getCdnFileHashes``. Every byte of
    ``data`` must be covered by a verified hash. Each raw ``FileHash.limit``
    defines the exact number of bytes sliced and hashed for its offset, so a
    short chunk cannot be treated as a partial successful block.
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
        data: Ciphertext bytes for a contiguous CDN response; immutable buffers are not zeroized.
        key: Exactly 32 bytes of AES key material; immutable buffers are not zeroized.
        iv: Exactly 16 bytes forming the initial CTR counter; immutable buffers are not zeroized.
        offset: Non-negative file offset of ``data``; defaults to ``0``.

    Returns:
        Plaintext bytes of the same length as ``data``.

    Raises:
        ValueError: ``key``, ``iv``, or ``offset`` violates CDN cryptographic constraints.
    """
    if len(key) != 32:
        raise ValueError("CDN encryption key must be 32 bytes")
    if len(iv) != 16:
        raise ValueError("CDN encryption IV must be 16 bytes")
    if offset < 0:
        raise ValueError("CDN offset must not be negative")
    block_offset, byte_offset = divmod(offset, 16)
    counter = (int.from_bytes(iv, "big") + block_offset) % (1 << 128)
    counter_iv = counter.to_bytes(16, "big")
    if byte_offset:
        return media_ctr_crypt(b"\x00" * byte_offset + data, key, counter_iv)[byte_offset:]
    return media_ctr_crypt(data, key, counter_iv)


def _file_hash_map(file_hashes: tuple[object, ...]) -> dict[int, types.FileHash]:
    """Index valid file-hash objects by their starting offsets.

    Args:
        file_hashes: Redirect-provided raw hash candidates to filter and index.
    """
    hashes: dict[int, types.FileHash] = {}
    for item in _iter_file_hashes(file_hashes):
        hashes.setdefault(int(item.offset), item)
    return hashes


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
