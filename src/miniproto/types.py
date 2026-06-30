from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

PeerKind = Literal["user", "chat", "channel", "self"]


def _utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True, frozen=True)
class Peer:
    id: int
    kind: PeerKind
    access_hash: int | None = None


@dataclass(slots=True, frozen=True)
class User:
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
        return Peer(
            id=self.id, kind="self" if self.is_self else "user", access_hash=self.access_hash
        )


@dataclass(slots=True, frozen=True)
class Media:
    id: int
    mime_type: str | None = None
    size: int | None = None
    file_name: str | None = None
    raw: object | None = None
    access_hash: int | None = None
    file_reference: bytes | None = None
    dc_id: int | None = None
    location: object | None = None


@dataclass(slots=True, frozen=True)
class Message:
    id: int
    peer: Peer
    text: str
    date: datetime
    media: Media | None = None
    entities: tuple[object, ...] = ()
    raw: object | None = None


@dataclass(slots=True, frozen=True)
class Update:
    date: datetime = field(default_factory=_utc_now)
    raw: object | None = None


@dataclass(slots=True, frozen=True)
class NewMessage(Update):
    message: Message | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
