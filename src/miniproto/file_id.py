"""Stable, local ``mpf1_`` file identifiers for reusable Telegram media references."""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any, Literal, TypeGuard

from miniproto.raw import types
from miniproto.types import Media

FileIdKind = Literal["document", "photo"]
FILE_ID_PREFIX = "mpf1_"
MAX_FILE_ID_LENGTH = 64 * 1024
MAX_FILE_REFERENCE_LENGTH = 16 * 1024
_SIGNED_INT64_MIN = -(1 << 63)
_SIGNED_INT64_MAX = (1 << 63) - 1


@dataclass(frozen=True, slots=True)
class DecodedFileId:
    """Decoded local file-id fields used to recreate a media location or input media.

    Attributes:
        kind: Encoded media kind, either ``"document"`` or ``"photo"``.
        id: Telegram document or photo ID.
        access_hash: Telegram access hash required for reuse.
        file_reference: Telegram file reference required for reuse.
        dc_id: Optional data-center ID retained as metadata.
        size: Optional known media size retained as metadata.
        file_name: Optional document filename retained as metadata.
        mime_type: Optional MIME type retained as metadata.
        thumb_size: Input-location thumbnail size, defaulting to the empty size.
    """

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
        """Build a ``Media`` value retaining the encoded file location.

        Returns:
            A media value with the file reference, access hash, and matching input location.
        """
        location: object
        if self.kind == "photo":
            location = types.InputPhotoFileLocation(
                id=self.id, access_hash=self.access_hash, file_reference=self.file_reference, thumb_size=self.thumb_size
            )
        else:
            location = types.InputDocumentFileLocation(
                id=self.id, access_hash=self.access_hash, file_reference=self.file_reference, thumb_size=self.thumb_size
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
        """Build the matching Telegram input-media object.

        Args:
            spoiler: Request Telegram's spoiler presentation for the media.
            ttl_seconds: Optional self-destruct timer forwarded to Telegram.
            video_cover: Optional document video-cover input object.
            video_timestamp: Optional document video start timestamp.

        Returns:
            ``InputMediaPhoto`` for photo IDs or ``InputMediaDocument`` for document IDs.
        """
        if self.kind == "photo":
            return types.InputMediaPhoto(
                spoiler=spoiler,
                id=types.InputPhoto(id=self.id, access_hash=self.access_hash, file_reference=self.file_reference),
                ttl_seconds=ttl_seconds,
            )
        return types.InputMediaDocument(
            spoiler=spoiler,
            id=types.InputDocument(id=self.id, access_hash=self.access_hash, file_reference=self.file_reference),
            video_cover=video_cover,
            video_timestamp=video_timestamp,
            ttl_seconds=ttl_seconds,
        )


def is_file_id(value: object) -> TypeGuard[str]:
    """Return whether a value has the miniproto file-id prefix.

    Args:
        value: Arbitrary candidate value.

    Returns:
        ``True`` only for strings beginning with ``mpf1_``.
    """
    return isinstance(value, str) and value.startswith(FILE_ID_PREFIX)


def encode_file_id(media: Media | object) -> str:
    """Encode supported Telegram media or input locations into a local file ID.

    Args:
        media: A ``Media`` value, supported generated media object, or input file location.

    Returns:
        Canonical URL-safe ``mpf1_`` identifier containing the reusable location fields.

    Raises:
        TypeError: If the media cannot supply a supported reusable location.
        ValueError: If an extracted field cannot be encoded.
    """
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
    """Best-effort variant of :func:`encode_file_id`.

    Args:
        media: Candidate media, or ``None``.

    Returns:
        The encoded local ID, or ``None`` for absent or unsupported media.
    """
    if media is None:
        return None
    try:
        return encode_file_id(media)
    except (TypeError, ValueError):
        return None


def decode_file_id(file_id: str) -> DecodedFileId:
    """Decode an ``mpf1_`` file ID without contacting Telegram.

    Args:
        file_id: Local identifier produced by :func:`encode_file_id`.

    Returns:
        Parsed reusable media fields.

    Raises:
        ValueError: If the prefix, payload encoding, or required fields are invalid.
    """
    if not is_file_id(file_id):
        raise ValueError("not a miniproto file id")
    if len(file_id) > MAX_FILE_ID_LENGTH:
        raise ValueError("miniproto file id exceeds the encoded size limit")
    try:
        payload = json.loads(_b64_decode(file_id.removeprefix(FILE_ID_PREFIX)).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError("invalid miniproto file id payload") from exc
    if not isinstance(payload, dict):
        raise ValueError("invalid miniproto file id payload")
    kind = _decode_kind(payload.get("k"))
    return DecodedFileId(
        kind=kind,
        id=_required_int(payload, "id", minimum=1, maximum=_SIGNED_INT64_MAX),
        access_hash=_required_int(payload, "ah", minimum=_SIGNED_INT64_MIN, maximum=_SIGNED_INT64_MAX),
        file_reference=_decode_file_reference(_required_str(payload, "fr")),
        dc_id=_optional_int(payload.get("dc"), name="dc", minimum=1, maximum=(1 << 31) - 1),
        size=_optional_int(payload.get("s"), name="s", minimum=0, maximum=_SIGNED_INT64_MAX),
        file_name=_optional_str(payload.get("n")),
        mime_type=_optional_str(payload.get("mt")),
        thumb_size=_optional_str(payload.get("ts")) or "",
    )


def media_from_file_id(file_id: str) -> Media:
    """Decode a local file ID into a reusable ``Media`` value.

    Args:
        file_id: Local identifier produced by :func:`encode_file_id`.

    Returns:
        Media retaining the ID's input location and metadata.
    """
    return decode_file_id(file_id).to_media()


def input_media_from_file_id(
    file_id: str,
    *,
    spoiler: bool = False,
    ttl_seconds: int | None = None,
    video_cover: object | None = None,
    video_timestamp: int | None = None,
) -> object:
    """Decode a file ID into Telegram input media.

    Args:
        file_id: Local identifier produced by :func:`encode_file_id`.
        spoiler: Request spoiler presentation; defaults to ``False``.
        ttl_seconds: Optional self-destruct timer.
        video_cover: Optional cover input for document media.
        video_timestamp: Optional start timestamp for document media.

    Returns:
        Matching generated input-media object.
    """
    return decode_file_id(file_id).to_input_media(
        spoiler=spoiler, ttl_seconds=ttl_seconds, video_cover=video_cover, video_timestamp=video_timestamp
    )


def _decoded_from_media(media: Media | object) -> DecodedFileId:
    """Extract reusable fields from supported public media shapes.

    Args:
        media: Media wrapper, generated media object, or supported input location.
    """
    if isinstance(media, Media):
        if media.location is not None:
            location = _decoded_from_location(
                media.location, size=media.size, file_name=media.file_name, mime_type=media.mime_type, dc_id=media.dc_id
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
    """Convert a supported generated input location into decoded file-id fields.

    Args:
        location: Generated document or photo input location.
        size: Optional retained media size.
        file_name: Optional retained document filename.
        mime_type: Optional retained MIME type.
        dc_id: Optional retained data-center ID.
    """
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
    """Map the compact serialized kind marker to its public kind name.

    Args:
        value: Decoded compact JSON kind marker.
    """
    if value == "d":
        return "document"
    if value == "p":
        return "photo"
    raise ValueError("unsupported miniproto file id kind")


def _required_int(payload: dict[str, Any], key: str, *, minimum: int, maximum: int) -> int:
    """Read a required integer-like JSON payload field.

    Args:
        payload: Decoded file-ID JSON object.
        key: Required compact field name.
        minimum: Smallest accepted integer value.
        maximum: Largest accepted integer value.
    """
    value = payload.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"miniproto file id is missing {key}")
    if not minimum <= value <= maximum:
        raise ValueError(f"miniproto file id {key} is outside the accepted range")
    return value


def _required_str(payload: dict[str, Any], key: str) -> str:
    """Read a non-empty required string JSON payload field.

    Args:
        payload: Decoded file-ID JSON object.
        key: Required compact field name.
    """
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"miniproto file id is missing {key}")
    return value


def _optional_int(value: object, *, name: str, minimum: int, maximum: int) -> int | None:
    """Normalize an optional payload value to an integer.

    Args:
        value: Decoded optional JSON value.
        name: Compact field name used in validation errors.
        minimum: Smallest accepted integer value.
        maximum: Largest accepted integer value.
    """
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        raise ValueError(f"miniproto file id {name} is outside the accepted range")
    return value


def _optional_str(value: object) -> str | None:
    """Normalize an optional payload value to a non-empty string.

    Args:
        value: Decoded optional JSON value.
    """
    return value if isinstance(value, str) and value else None


def _b64_encode(raw: bytes) -> str:
    """Encode bytes using URL-safe base64 without padding.

    Args:
        raw: Bytes to encode.
    """
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64_decode(encoded: str) -> bytes:
    """Decode an unpadded URL-safe base64 string.

    Args:
        encoded: URL-safe base64 text without required padding.
    """
    try:
        raw = encoded.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("invalid URL-safe base64 text") from exc
    try:
        return base64.b64decode(raw + b"=" * (-len(raw) % 4), altchars=b"-_", validate=True)
    except ValueError as exc:
        raise ValueError("invalid URL-safe base64 text") from exc


def _decode_file_reference(encoded: str) -> bytes:
    """Decode and size-limit one file-reference bearer value.

    Args:
        encoded: Strict URL-safe base64 file-reference text.
    """
    value = _b64_decode(encoded)
    if len(value) > MAX_FILE_REFERENCE_LENGTH:
        raise ValueError("miniproto file id file reference exceeds the size limit")
    return value


def _document_file_name(attributes: tuple[object, ...]) -> str | None:
    """Find a document filename attribute, when present.

    Args:
        attributes: Generated document attribute objects.
    """
    for attribute in attributes:
        if isinstance(attribute, types.DocumentAttributeFilename):
            return attribute.file_name
    return None


def _largest_photo_size(sizes: tuple[object, ...]) -> int | None:
    """Return the largest integer ``size`` attribute among photo sizes.

    Args:
        sizes: Generated photo-size objects.
    """
    candidates: list[int] = []
    for size in sizes:
        value = getattr(size, "size", None)
        if isinstance(value, int):
            candidates.append(value)
    return max(candidates) if candidates else None


def _largest_photo_thumb_size(sizes: tuple[object, ...]) -> str:
    """Return the thumbnail type associated with the largest usable photo size.

    Args:
        sizes: Generated photo-size objects.
    """
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
