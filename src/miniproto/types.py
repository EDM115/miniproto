"""Small immutable public value types produced by high-level client helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

PeerKind = Literal["user", "chat", "channel", "self"]


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp for update defaults."""
    return datetime.now(UTC)


@dataclass(slots=True, frozen=True)
class Peer:
    """Telegram peer reference suitable for high-level client operations.

    Attributes:
        id: Telegram peer identifier.
        kind: Peer category: user, chat, channel or the current account.
        access_hash: Optional Telegram access hash required for some peers.
    """

    id: int
    kind: PeerKind
    access_hash: int | None = None


@dataclass(slots=True, frozen=True)
class User:
    """Normalized Telegram user returned by peer and authorization helpers.

    Attributes:
        id: Telegram user identifier.
        access_hash: Optional hash used to address the user.
        is_bot: Whether the account is a bot.
        username: Optional public username.
        phone: Optional phone number supplied by Telegram.
        first_name: Optional first name.
        last_name: Optional last name.
        is_self: Whether this is the authorized account.
        raw: Optional underlying TL object for low-level inspection.
    """

    id: int
    access_hash: int | None = None
    is_bot: bool = False
    username: str | None = None
    phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_self: bool = False
    raw: object | None = None

    @property
    def peer(self) -> Peer:
        """Return this user as a ``Peer``, preserving its access hash and self identity."""
        return Peer(id=self.id, kind="self" if self.is_self else "user", access_hash=self.access_hash)


@dataclass(slots=True, frozen=True)
class Media:
    """Normalized Telegram media descriptor used for upload and download helpers.

    Attributes:
        id: Telegram media identifier.
        mime_type: Optional declared content type.
        size: Optional byte size.
        file_name: Optional file name.
        raw: Optional underlying TL object.
        access_hash: Optional Telegram media access hash.
        file_reference: Optional opaque reference that Telegram may require to fetch the media.
        dc_id: Optional datacenter that hosts the media.
        location: Optional low-level download location.
    """

    id: int
    mime_type: str | None = None
    size: int | None = None
    file_name: str | None = None
    raw: object | None = None
    access_hash: int | None = None
    file_reference: bytes | None = None
    dc_id: int | None = None
    location: object | None = None

    @property
    def file_id(self) -> str | None:
        """Encode this media as a portable file ID when its fields support that format.

        Returns:
            The encoded ID or ``None`` when the media lacks the information needed for encoding.
        """
        from miniproto.file_id import try_encode_file_id

        return try_encode_file_id(self)


@dataclass(slots=True, frozen=True)
class Message:
    """Normalized Telegram message returned by high-level messaging helpers.

    Attributes:
        id: Telegram message identifier within ``peer``.
        peer: Conversation containing the message.
        text: Parsed message text.
        date: Telegram timestamp.
        media: Optional normalized attachment.
        entities: Parsed text entities.
        raw: Optional underlying TL message.
    """

    id: int
    peer: Peer
    text: str
    date: datetime
    media: Media | None = None
    entities: tuple[object, ...] = ()
    raw: object | None = None


@dataclass(slots=True, frozen=True)
class Update:
    """Base normalized update with a UTC creation timestamp and optional raw payload.

    Attributes:
        date: Time associated with the update, generated as current UTC time when omitted.
        raw: Optional original Telegram TL object retained for low-level inspection.
    """

    date: datetime = field(default_factory=_utc_now)
    raw: object | None = None


@dataclass(slots=True, frozen=True)
class NewMessage(Update):
    """Update emitted for a newly received message.

    Attributes:
        date: Inherited update timestamp, generated as current UTC time when omitted.
        raw: Inherited optional original Telegram TL object.
        message: Normalized message when conversion succeeded.
        metadata: Additional update-specific values.
    """

    message: Message | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
