from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from miniproto.crypto.mtproto import media_ctr_crypt
from miniproto.raw import functions, types


class CdnError(RuntimeError):
    pass


type RawInvoker = Callable[..., Awaitable[object]]


@dataclass(frozen=True, slots=True)
class CdnRedirect:
    dc_id: int
    file_token: bytes
    encryption_key: bytes
    encryption_iv: bytes
    file_hashes: tuple[object, ...]
    raw: types.UploadFileCdnRedirect


async def get_cdn_file_part(
    invoke: RawInvoker,
    redirect: CdnRedirect,
    *,
    offset: int,
    limit: int,
    request_timeout: float | None = None,
) -> bytes:
    while True:
        result = await invoke(
            functions.UploadGetCdnFile(file_token=redirect.file_token, offset=offset, limit=limit),
            request_timeout=request_timeout,
        )
        if isinstance(result, types.UploadCdnFileReuploadNeeded):
            await invoke(
                functions.UploadReuploadCdnFile(
                    file_token=redirect.file_token, request_token=result.request_token
                ),
                request_timeout=request_timeout,
                retry=True,
            )
            continue
        if isinstance(result, types.UploadCdnFile):
            return decrypt_cdn_chunk(
                result.bytes, key=redirect.encryption_key, iv=redirect.encryption_iv, offset=offset
            )
        raise CdnError(f"unsupported CDN file response: {type(result).__name__}")


def cdn_redirect_from_raw(result: object) -> CdnRedirect | None:
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


__all__ = [
    "CdnError",
    "CdnRedirect",
    "cdn_redirect_from_raw",
    "decrypt_cdn_chunk",
    "get_cdn_file_part",
]
