from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from miniproto.session.models import PeerCacheEntry, SessionRecord, UpdateState
from miniproto.session.peer_merge import merge_peer_entries
from miniproto.types import PeerKind

UPDATE_METADATA_KEY = "updates"
UPDATE_DUPLICATE_KEYS_KEY = "recent_update_keys"
UPDATE_CHANNELS_KEY = "channels"
DEFAULT_DUPLICATE_WINDOW = 2048


def utc_now() -> datetime:
    return datetime.now(UTC)


def coerce_update_datetime(value: datetime | int | float | str | None) -> datetime:
    if value is None:
        return utc_now()
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
    if isinstance(value, int | float):
        return datetime.fromtimestamp(value, UTC)
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


@dataclass(frozen=True, slots=True)
class EntityReference:
    id: int
    kind: PeerKind
    access_hash: int | None = None
    username: str | None = None
    phone: str | None = None
    title: str | None = None
    updated_at: datetime = field(default_factory=utc_now)

    def to_peer_cache_entry(self) -> PeerCacheEntry:
        return PeerCacheEntry(
            id=self.id,
            kind=self.kind,
            access_hash=self.access_hash,
            username=self.username,
            phone=self.phone,
            updated_at=self.updated_at,
            raw={"title": self.title} if self.title else None,
        )


@dataclass(frozen=True, slots=True)
class ChannelUpdateCursor:
    channel_id: int
    pts: int = 0
    date: datetime = field(default_factory=utc_now)


@dataclass(frozen=True, slots=True)
class UpdateCursor:
    pts: int = 0
    qts: int = 0
    seq: int = 0
    date: datetime = field(default_factory=utc_now)
    channel_cursors: tuple[ChannelUpdateCursor, ...] = ()
    entities: tuple[EntityReference, ...] = ()
    duplicate_keys: tuple[str, ...] = ()

    @classmethod
    def from_record(cls, record: SessionRecord, *, duplicate_window: int = DEFAULT_DUPLICATE_WINDOW) -> UpdateCursor:
        metadata = update_metadata(record.metadata)
        raw_keys = metadata.get(UPDATE_DUPLICATE_KEYS_KEY, ())
        keys = tuple(str(key) for key in raw_keys if isinstance(key, str))[-duplicate_window:]
        return cls(
            pts=record.update_state.pts,
            qts=record.update_state.qts,
            seq=record.update_state.seq,
            date=record.update_state.date,
            channel_cursors=_channel_cursors_from_metadata(metadata),
            entities=tuple(entity_reference_from_peer(peer) for peer in record.peers),
            duplicate_keys=keys,
        )

    def to_update_state(self) -> UpdateState:
        return UpdateState(pts=self.pts, qts=self.qts, seq=self.seq, date=self.date)

    def with_state(
        self,
        *,
        pts: int | None = None,
        qts: int | None = None,
        seq: int | None = None,
        date: datetime | int | float | str | None = None,
    ) -> UpdateCursor:
        return UpdateCursor(
            pts=self.pts if pts is None else pts,
            qts=self.qts if qts is None else qts,
            seq=self.seq if seq is None else seq,
            date=self.date if date is None else coerce_update_datetime(date),
            channel_cursors=self.channel_cursors,
            entities=self.entities,
            duplicate_keys=self.duplicate_keys,
        )

    def channel_cursor(self, channel_id: int) -> ChannelUpdateCursor:
        for cursor in self.channel_cursors:
            if cursor.channel_id == channel_id:
                return cursor
        return ChannelUpdateCursor(channel_id=channel_id)

    def with_channel_state(
        self, channel_id: int, *, pts: int, date: datetime | int | float | str | None = None
    ) -> UpdateCursor:
        updated = ChannelUpdateCursor(
            channel_id=channel_id, pts=pts, date=self.date if date is None else coerce_update_datetime(date)
        )
        cursors = {cursor.channel_id: cursor for cursor in self.channel_cursors}
        cursors[channel_id] = updated
        return UpdateCursor(
            pts=self.pts,
            qts=self.qts,
            seq=self.seq,
            date=self.date,
            channel_cursors=tuple(cursors.values()),
            entities=self.entities,
            duplicate_keys=self.duplicate_keys,
        )

    def with_entities(self, entities: Iterable[EntityReference]) -> UpdateCursor:
        merged = merge_entity_references(self.entities, entities)
        return UpdateCursor(
            pts=self.pts,
            qts=self.qts,
            seq=self.seq,
            date=self.date,
            channel_cursors=self.channel_cursors,
            entities=tuple(merged.values()),
            duplicate_keys=self.duplicate_keys,
        )

    def with_duplicate_keys(self, duplicate_keys: Iterable[str]) -> UpdateCursor:
        return UpdateCursor(
            pts=self.pts,
            qts=self.qts,
            seq=self.seq,
            date=self.date,
            channel_cursors=self.channel_cursors,
            entities=self.entities,
            duplicate_keys=tuple(duplicate_keys),
        )


class DuplicateTracker:
    def __init__(self, keys: Iterable[str] = (), *, max_size: int = DEFAULT_DUPLICATE_WINDOW) -> None:
        if max_size <= 0:
            raise ValueError("duplicate tracker max_size must be positive")
        self.max_size = max_size
        self._keys: deque[str] = deque()
        self._seen: set[str] = set()
        for key in keys:
            self.add(key)

    def __contains__(self, key: object) -> bool:
        return key in self._seen

    def add(self, key: str) -> None:
        if key in self._seen:
            return
        self._keys.append(key)
        self._seen.add(key)
        while len(self._keys) > self.max_size:
            removed = self._keys.popleft()
            self._seen.discard(removed)

    def keys(self) -> tuple[str, ...]:
        return tuple(self._keys)


def update_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    value = metadata.get(UPDATE_METADATA_KEY)
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def metadata_with_duplicate_keys(
    metadata: Mapping[str, Any], keys: Iterable[str], channel_cursors: Iterable[ChannelUpdateCursor] = ()
) -> dict[str, Any]:
    updated = dict(metadata)
    update_values = update_metadata(updated)
    update_values[UPDATE_DUPLICATE_KEYS_KEY] = list(keys)
    cursors = tuple(channel_cursors)
    if cursors:
        update_values[UPDATE_CHANNELS_KEY] = {
            str(cursor.channel_id): {"pts": cursor.pts, "date": cursor.date.isoformat()} for cursor in cursors
        }
    updated[UPDATE_METADATA_KEY] = update_values
    return updated


def _channel_cursors_from_metadata(metadata: Mapping[str, Any]) -> tuple[ChannelUpdateCursor, ...]:
    raw_channels = metadata.get(UPDATE_CHANNELS_KEY)
    if not isinstance(raw_channels, Mapping):
        return ()
    cursors: list[ChannelUpdateCursor] = []
    for raw_channel_id, raw_cursor in raw_channels.items():
        if not isinstance(raw_cursor, Mapping):
            continue
        try:
            channel_id = int(raw_channel_id)
            pts = int(raw_cursor.get("pts", 0))
        except (TypeError, ValueError):
            continue
        cursors.append(
            ChannelUpdateCursor(channel_id=channel_id, pts=pts, date=coerce_update_datetime(raw_cursor.get("date")))
        )
    return tuple(cursors)


def merge_entity_references(
    existing: Iterable[EntityReference], incoming: Iterable[EntityReference]
) -> dict[tuple[PeerKind, int], EntityReference]:
    peers = merge_peer_entries(
        (entity.to_peer_cache_entry() for entity in existing), (entity.to_peer_cache_entry() for entity in incoming)
    )
    return {(peer.kind, peer.id): entity_reference_from_peer(peer) for peer in peers}


def merge_peer_cache_entries(
    existing: Iterable[PeerCacheEntry], entities: Iterable[EntityReference]
) -> tuple[PeerCacheEntry, ...]:
    return merge_peer_entries(existing, (entity.to_peer_cache_entry() for entity in entities))


def entity_reference_from_peer(peer: PeerCacheEntry) -> EntityReference:
    title = None
    if isinstance(peer.raw, Mapping):
        raw_title = peer.raw.get("title")
        title = None if raw_title is None else str(raw_title)
    return EntityReference(
        id=peer.id,
        kind=peer.kind,
        access_hash=peer.access_hash,
        username=peer.username,
        phone=peer.phone,
        title=title,
        updated_at=peer.updated_at,
    )
