from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any, Literal, TypeGuard

from miniproto.raw import types
from miniproto.types import Media

FileIdKind = Literal["document", "photo"]
FILE_ID_PREFIX = "mpf1_"


@dataclass(frozen=True, slots=True)
class DecodedFileId:
    kind: FileIdKind
    id: int
    access_hash: int
    file_reference: bytes
    dc_id: int | None = None
    size: int | None = None
    file_name: str | None = None
    mime_type: str | None = None
    thumb_size: str = ""

    def to_media(self) -> Media:
        location: object
        if self.kind == "photo":
            location = types.InputPhotoFileLocation(
                id=self.id,
                access_hash=self.access_hash,
                file_reference=self.file_reference,
                thumb_size=self.thumb_size,
            )
        else:
            location = types.InputDocumentFileLocation(
                id=self.id,
                access_hash=self.access_hash,
                file_reference=self.file_reference,
                thumb_size=self.thumb_size,
            )
        return Media(
            id=self.id,
            mime_type=self.mime_type,
            size=self.size,
            file_name=self.file_name,
            access_hash=self.access_hash,
            file_reference=self.file_reference,
            dc_id=self.dc_id,
            location=location,
        )

    def to_input_media(
        self,
        *,
        spoiler: bool = False,
        ttl_seconds: int | None = None,
        video_cover: object | None = None,
        video_timestamp: int | None = None,
    ) -> object:
        if self.kind == "photo":
            return types.InputMediaPhoto(
                spoiler=spoiler,
                id=types.InputPhoto(
                    id=self.id, access_hash=self.access_hash, file_reference=self.file_reference
                ),
                ttl_seconds=ttl_seconds,
            )
        return types.InputMediaDocument(
            spoiler=spoiler,
            id=types.InputDocument(
                id=self.id, access_hash=self.access_hash, file_reference=self.file_reference
            ),
            video_cover=video_cover,
            video_timestamp=video_timestamp,
            ttl_seconds=ttl_seconds,
        )


def is_file_id(value: object) -> TypeGuard[str]:
    return isinstance(value, str) and value.startswith(FILE_ID_PREFIX)


def encode_file_id(media: Media | object) -> str:
    decoded = _decoded_from_media(media)
    payload: dict[str, object] = {
        "k": "p" if decoded.kind == "photo" else "d",
        "id": decoded.id,
        "ah": decoded.access_hash,
        "fr": _b64_encode(decoded.file_reference),
    }
    if decoded.dc_id is not None:
        payload["dc"] = decoded.dc_id
    if decoded.size is not None:
        payload["s"] = decoded.size
    if decoded.file_name:
        payload["n"] = decoded.file_name
    if decoded.mime_type:
        payload["mt"] = decoded.mime_type
    if decoded.thumb_size:
        payload["ts"] = decoded.thumb_size
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return FILE_ID_PREFIX + _b64_encode(raw)


def try_encode_file_id(media: Media | object | None) -> str | None:
    if media is None:
        return None
    try:
        return encode_file_id(media)
    except (TypeError, ValueError):
        return None


def decode_file_id(file_id: str) -> DecodedFileId:
    if not is_file_id(file_id):
        raise ValueError("not a miniproto file id")
    try:
        payload = json.loads(_b64_decode(file_id.removeprefix(FILE_ID_PREFIX)).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid miniproto file id payload") from exc
    if not isinstance(payload, dict):
        raise ValueError("invalid miniproto file id payload")
    kind = _decode_kind(payload.get("k"))
    return DecodedFileId(
        kind=kind,
        id=_required_int(payload, "id"),
        access_hash=_required_int(payload, "ah"),
        file_reference=_b64_decode(_required_str(payload, "fr")),
        dc_id=_optional_int(payload.get("dc")),
        size=_optional_int(payload.get("s")),
        file_name=_optional_str(payload.get("n")),
        mime_type=_optional_str(payload.get("mt")),
        thumb_size=_optional_str(payload.get("ts")) or "",
    )


def media_from_file_id(file_id: str) -> Media:
    return decode_file_id(file_id).to_media()


def input_media_from_file_id(
    file_id: str,
    *,
    spoiler: bool = False,
    ttl_seconds: int | None = None,
    video_cover: object | None = None,
    video_timestamp: int | None = None,
) -> object:
    return decode_file_id(file_id).to_input_media(
        spoiler=spoiler,
        ttl_seconds=ttl_seconds,
        video_cover=video_cover,
        video_timestamp=video_timestamp,
    )


def _decoded_from_media(media: Media | object) -> DecodedFileId:
    if isinstance(media, Media):
        if media.location is not None:
            location = _decoded_from_location(
                media.location,
                size=media.size,
                file_name=media.file_name,
                mime_type=media.mime_type,
                dc_id=media.dc_id,
            )
            return location
        if media.access_hash is not None and media.file_reference is not None:
            return DecodedFileId(
                kind="document",
                id=media.id,
                access_hash=media.access_hash,
                file_reference=media.file_reference,
                dc_id=media.dc_id,
                size=media.size,
                file_name=media.file_name,
                mime_type=media.mime_type,
            )
        if media.raw is not None:
            return _decoded_from_media(media.raw)
    if isinstance(media, types.MessageMediaDocument) and media.document is not None:
        return _decoded_from_media(media.document)
    if isinstance(media, types.MessageMediaPhoto) and media.photo is not None:
        return _decoded_from_media(media.photo)
    if isinstance(media, types.Document):
        return DecodedFileId(
            kind="document",
            id=media.id,
            access_hash=media.access_hash,
            file_reference=media.file_reference,
            dc_id=media.dc_id,
            size=media.size,
            file_name=_document_file_name(media.attributes),
            mime_type=media.mime_type,
        )
    if isinstance(media, types.Photo):
        return DecodedFileId(
            kind="photo",
            id=media.id,
            access_hash=media.access_hash,
            file_reference=media.file_reference,
            dc_id=media.dc_id,
            size=_largest_photo_size(media.sizes),
            mime_type="image/jpeg",
            thumb_size=_largest_photo_thumb_size(media.sizes),
        )
    return _decoded_from_location(media)


def _decoded_from_location(
    location: object,
    *,
    size: int | None = None,
    file_name: str | None = None,
    mime_type: str | None = None,
    dc_id: int | None = None,
) -> DecodedFileId:
    if isinstance(location, types.InputDocumentFileLocation):
        return DecodedFileId(
            kind="document",
            id=location.id,
            access_hash=location.access_hash,
            file_reference=location.file_reference,
            dc_id=dc_id,
            size=size,
            file_name=file_name,
            mime_type=mime_type,
            thumb_size=location.thumb_size,
        )
    if isinstance(location, types.InputPhotoFileLocation):
        return DecodedFileId(
            kind="photo",
            id=location.id,
            access_hash=location.access_hash,
            file_reference=location.file_reference,
            dc_id=dc_id,
            size=size,
            file_name=file_name,
            mime_type=mime_type or "image/jpeg",
            thumb_size=location.thumb_size,
        )
    raise TypeError(f"cannot encode file id from {type(location).__name__}")


def _decode_kind(value: object) -> FileIdKind:
    if value == "d":
        return "document"
    if value == "p":
        return "photo"
    raise ValueError("unsupported miniproto file id kind")


def _required_int(payload: dict[str, Any], key: str) -> int:
    value = payload.get(key)
    if value is None:
        raise ValueError(f"miniproto file id is missing {key}")
    return int(value)


def _required_str(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"miniproto file id is missing {key}")
    return value


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str | bytes | bytearray):
        return int(value)
    return int(str(value))


def _optional_str(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _b64_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64_decode(encoded: str) -> bytes:
    return base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))


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
    sized: list[tuple[object, int]] = []
    for size in sizes:
        value = getattr(size, "size", None)
        if isinstance(value, int):
            sized.append((size, value))
    if sized:
        selected, _size = max(sized, key=lambda item: item[1])
        thumb = getattr(selected, "type", "")
        return thumb if isinstance(thumb, str) else ""
    for size in reversed(sizes):
        thumb = getattr(size, "type", "")
        if isinstance(thumb, str):
            return thumb
    return ""


__all__ = [
    "FILE_ID_PREFIX",
    "DecodedFileId",
    "decode_file_id",
    "encode_file_id",
    "input_media_from_file_id",
    "is_file_id",
    "media_from_file_id",
    "try_encode_file_id",
]
