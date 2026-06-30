from __future__ import annotations

import asyncio
import inspect
import io
import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, cast

from miniproto.media.cdn import cdn_redirect_from_raw, get_cdn_file_part
from miniproto.media.upload import DEFAULT_CHUNK_SIZE, ProgressCallback
from miniproto.raw import functions, types
from miniproto.types import Media

type Destination = str | os.PathLike[str] | BinaryIO | None


class MediaDownloadError(RuntimeError):
    pass


type RawInvoker = Callable[..., Awaitable[object]]


@dataclass(frozen=True, slots=True)
class MediaDownloadResult:
    bytes_downloaded: int
    offset: int
    destination: Path | BinaryIO | None = None
    data: bytes | None = None
    raw_location: object | None = None


@dataclass(slots=True)
class _DestinationHandle:
    handle: BinaryIO
    path: Path | None
    should_close: bool
    remove_on_cancel: bool
    existing_bytes: int
    get_data: Callable[[], bytes | None]


async def download_file(
    invoke: RawInvoker,
    location: object,
    destination: Destination = None,
    *,
    offset: int = 0,
    limit: int | None = None,
    part_size: int = DEFAULT_CHUNK_SIZE,
    resume: bool = False,
    progress: ProgressCallback | None = None,
    precise: bool = False,
    cdn_supported: bool = True,
    total_size: int | None = None,
    request_timeout: float | None = None,
    max_buffer_size: int | None = None,
) -> MediaDownloadResult:
    _validate_download_options(offset, limit, part_size, max_buffer_size)
    destination_handle = _open_destination(destination, resume=resume)
    current_offset = offset + destination_handle.existing_bytes
    downloaded = destination_handle.existing_bytes
    remaining = None if limit is None else max(0, limit - destination_handle.existing_bytes)
    callback_total = limit if limit is not None else total_size
    try:
        while remaining is None or remaining > 0:
            request_limit = part_size if remaining is None else min(part_size, remaining)
            result = await invoke(
                functions.UploadGetFile(
                    precise=precise,
                    cdn_supported=cdn_supported,
                    location=location,
                    offset=current_offset,
                    limit=request_limit,
                ),
                request_timeout=request_timeout,
            )
            payload = await _payload_from_get_file_result(
                invoke,
                result,
                offset=current_offset,
                limit=request_limit,
                request_timeout=request_timeout,
            )
            if remaining is not None and len(payload) > remaining:
                payload = payload[:remaining]
            if not payload:
                break
            destination_handle.handle.write(payload)
            downloaded += len(payload)
            current_offset += len(payload)
            if remaining is not None:
                remaining -= len(payload)
            await _call_progress(progress, downloaded, callback_total)
            if len(payload) < request_limit:
                break
        if destination_handle.should_close:
            destination_handle.handle.close()
        data = destination_handle.get_data()
        return MediaDownloadResult(
            bytes_downloaded=downloaded,
            offset=offset,
            destination=destination_handle.path or destination_handle.handle,
            data=data,
            raw_location=location,
        )
    except asyncio.CancelledError:
        if destination_handle.should_close:
            destination_handle.handle.close()
        if destination_handle.remove_on_cancel and destination_handle.path is not None:
            destination_handle.path.unlink(missing_ok=True)
        raise
    except BaseException:
        if destination_handle.should_close:
            destination_handle.handle.close()
        raise


async def download_media(
    invoke: RawInvoker, media: object, destination: Destination = None, **kwargs: Any
) -> MediaDownloadResult:
    location = download_location_from_media(media)
    total_size = kwargs.pop("total_size", None)
    if total_size is None and isinstance(media, Media):
        total_size = media.size
    return await download_file(invoke, location, destination, total_size=total_size, **kwargs)


def download_location_from_media(media: object) -> object:
    if isinstance(media, Media):
        if media.location is not None:
            return media.location
        if media.raw is not None:
            return download_location_from_media(media.raw)
    if _is_input_file_location(media):
        return media
    if isinstance(media, types.Message):
        return download_location_from_media(media.media)
    if isinstance(media, types.MessageMediaDocument) and media.document is not None:
        return download_location_from_media(media.document)
    if isinstance(media, types.Document):
        return types.InputDocumentFileLocation(
            id=media.id,
            access_hash=media.access_hash,
            file_reference=media.file_reference,
            thumb_size="",
        )
    if isinstance(media, types.MessageMediaPhoto) and media.photo is not None:
        return download_location_from_media(media.photo)
    if isinstance(media, types.Photo):
        thumb_size = _largest_photo_thumb_size(media.sizes)
        return types.InputPhotoFileLocation(
            id=media.id,
            access_hash=media.access_hash,
            file_reference=media.file_reference,
            thumb_size=thumb_size,
        )
    raise MediaDownloadError(f"cannot resolve download location from {type(media).__name__}")


def media_from_raw(raw: object) -> Media | None:
    if isinstance(raw, Media):
        return raw
    if raw is None:
        return None
    if isinstance(raw, types.Message):
        return media_from_raw(raw.media)
    if isinstance(raw, types.UpdateShortSentMessage):
        return media_from_raw(raw.media)
    if isinstance(raw, types.MessageMediaDocument) and isinstance(raw.document, types.Document):
        return _media_from_document(raw.document, raw=raw)
    if isinstance(raw, types.Document):
        return _media_from_document(raw, raw=raw)
    if isinstance(raw, types.MessageMediaPhoto) and isinstance(raw.photo, types.Photo):
        return _media_from_photo(raw.photo, raw=raw)
    if isinstance(raw, types.Photo):
        return _media_from_photo(raw, raw=raw)
    if _is_input_file_location(raw):
        return Media(id=0, raw=raw, location=raw)
    return None


async def _payload_from_get_file_result(
    invoke: RawInvoker, result: object, *, offset: int, limit: int, request_timeout: float | None
) -> bytes:
    redirect = cdn_redirect_from_raw(result)
    if redirect is not None:
        return await get_cdn_file_part(
            invoke, redirect, offset=offset, limit=limit, request_timeout=request_timeout
        )
    if isinstance(result, types.UploadFile):
        return result.bytes
    raise MediaDownloadError(f"unsupported upload.getFile response: {type(result).__name__}")


def _media_from_document(document: types.Document, *, raw: object) -> Media:
    file_name = _document_file_name(document.attributes)
    location = types.InputDocumentFileLocation(
        id=document.id,
        access_hash=document.access_hash,
        file_reference=document.file_reference,
        thumb_size="",
    )
    return Media(
        id=document.id,
        mime_type=document.mime_type,
        size=document.size,
        file_name=file_name,
        raw=raw,
        access_hash=document.access_hash,
        file_reference=document.file_reference,
        dc_id=document.dc_id,
        location=location,
    )


def _media_from_photo(photo: types.Photo, *, raw: object) -> Media:
    size = _largest_photo_size(photo.sizes)
    thumb_size = _largest_photo_thumb_size(photo.sizes)
    location = types.InputPhotoFileLocation(
        id=photo.id,
        access_hash=photo.access_hash,
        file_reference=photo.file_reference,
        thumb_size=thumb_size,
    )
    return Media(
        id=photo.id,
        mime_type="image/jpeg",
        size=size,
        raw=raw,
        access_hash=photo.access_hash,
        file_reference=photo.file_reference,
        dc_id=photo.dc_id,
        location=location,
    )


def _document_file_name(attributes: tuple[object, ...]) -> str | None:
    for attribute in attributes:
        if isinstance(attribute, types.DocumentAttributeFilename):
            return attribute.file_name
    return None


def _largest_photo_size(sizes: tuple[object, ...]) -> int | None:
    candidates: list[int] = []
    for size in sizes:
        value = getattr(size, "size", None)
        if isinstance(value, int):
            candidates.append(value)
    return max(candidates) if candidates else None


def _largest_photo_thumb_size(sizes: tuple[object, ...]) -> str:
    sized = [size for size in sizes if isinstance(getattr(size, "size", None), int)]
    if sized:
        selected = max(sized, key=lambda item: cast(int, item.size))
        thumb = getattr(selected, "type", "")
        return thumb if isinstance(thumb, str) else ""
    for size in reversed(sizes):
        thumb = getattr(size, "type", "")
        if isinstance(thumb, str):
            return thumb
    return ""


def _is_input_file_location(value: object) -> bool:
    return getattr(type(value), "RESULT_TYPE", None) == "InputFileLocation"


def _validate_download_options(
    offset: int, limit: int | None, part_size: int, max_buffer_size: int | None
) -> None:
    if offset < 0:
        raise ValueError("offset must not be negative")
    if limit is not None and limit < 0:
        raise ValueError("limit must not be negative")
    if part_size <= 0:
        raise ValueError("part_size must be positive")
    if part_size > DEFAULT_CHUNK_SIZE:
        raise ValueError("part_size must not exceed 512 KiB")
    ceiling = part_size if max_buffer_size is None else max_buffer_size
    if ceiling < part_size:
        raise ValueError("max_buffer_size is lower than the configured download chunk size")


def _open_destination(destination: Destination, *, resume: bool) -> _DestinationHandle:
    if destination is None:
        buffer = io.BytesIO()
        return _DestinationHandle(
            handle=buffer,
            path=None,
            should_close=False,
            remove_on_cancel=False,
            existing_bytes=0,
            get_data=buffer.getvalue,
        )
    if isinstance(destination, str | os.PathLike):
        path = Path(cast(str | os.PathLike[str], destination))
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.stat().st_size if resume and path.exists() else 0
        handle = path.open("ab" if resume else "wb")
        return _DestinationHandle(
            handle=handle,
            path=path,
            should_close=True,
            remove_on_cancel=not resume,
            existing_bytes=existing,
            get_data=lambda: None,
        )
    return _DestinationHandle(
        handle=destination,
        path=None,
        should_close=False,
        remove_on_cancel=False,
        existing_bytes=0,
        get_data=lambda: None,
    )


async def _call_progress(
    progress: ProgressCallback | None, current: int, total: int | None
) -> None:
    if progress is None:
        return
    result = progress(current, total)
    if inspect.isawaitable(result):
        await result


__all__ = [
    "Destination",
    "MediaDownloadError",
    "MediaDownloadResult",
    "download_file",
    "download_location_from_media",
    "download_media",
    "media_from_raw",
]
