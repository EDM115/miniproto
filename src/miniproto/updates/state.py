"""Frozen persisted update cursor models and bounded duplicate/entity state helpers."""

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
    """Return the current timezone-aware UTC time for cursor and entity defaults."""
    return datetime.now(UTC)


def coerce_update_datetime(value: datetime | int | float | str | None) -> datetime:
    """Coerce supported update timestamps, preserving aware datetime timezones.

    Args:
        value: A datetime, Unix timestamp, ISO 8601 string or ``None`` for the current UTC time.

    Returns:
        A timezone-aware datetime; aware values retain their timezone and naive values are treated as UTC.

    Raises:
        ValueError: If a string is not accepted by ``datetime.fromisoformat``.
        TypeError: If ``value`` has an unsupported type.
    """
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
    """Persistent, normalized peer data learned while processing updates.

    Attributes:
        id: Telegram peer identifier.
        kind: Peer category used as part of the cache key.
        access_hash: Optional hash needed to construct an input peer or channel.
        username: Optional username observed in update entities.
        phone: Optional phone number observed in a user entity.
        title: Optional display title or user full name.
        complete: Whether the source was a full entity allowed to clear absent aliases.
        updated_at: Observation timestamp; aware input retains its timezone and naive input assumes UTC.
    """

    id: int
    kind: PeerKind
    access_hash: int | None = None
    username: str | None = None
    phone: str | None = None
    title: str | None = None
    complete: bool = False
    updated_at: datetime = field(default_factory=utc_now)

    def to_peer_cache_entry(self) -> PeerCacheEntry:
        """Convert this reference to the session peer-cache representation."""
        raw: dict[str, object] = {"title": self.title} if self.title else {}
        if self.complete:
            raw["_miniproto_complete"] = True
        return PeerCacheEntry(
            id=self.id,
            kind=self.kind,
            access_hash=self.access_hash,
            username=self.username,
            phone=self.phone,
            updated_at=self.updated_at,
            raw=raw or None,
        )


@dataclass(frozen=True, slots=True)
class ChannelUpdateCursor:
    """Persisted PTS cursor for one channel's independent update stream.

    Attributes:
        channel_id: Telegram channel identifier.
        pts: Most recently applied channel PTS, defaulting to zero.
        date: Timestamp associated with this channel state; aware input retains its timezone.
    """

    channel_id: int
    pts: int = 0
    date: datetime = field(default_factory=utc_now)


@dataclass(frozen=True, slots=True)
class UpdateCursor:
    """Immutable global and per-channel update state persisted in a session record.

    ``duplicate_keys`` retains a bounded recent-history window for best-effort duplicate suppression. ``entities`` supplies access hashes needed for channel gap recovery.

    Attributes:
        pts: Global persistent timestamp.
        qts: Secret-chat persistent timestamp.
        seq: Global sequence number.
        date: Global-state timestamp; aware input retains its timezone and naive input assumes UTC.
        channel_cursors: Independent channel PTS states.
        entities: Peer references observed while processing updates.
        duplicate_keys: Recent raw-update identity keys.
    """

    pts: int = 0
    qts: int = 0
    seq: int = 0
    date: datetime = field(default_factory=utc_now)
    channel_cursors: tuple[ChannelUpdateCursor, ...] = ()
    entities: tuple[EntityReference, ...] = ()
    duplicate_keys: tuple[str, ...] = ()

    @classmethod
    def from_record(cls, record: SessionRecord, *, duplicate_window: int = DEFAULT_DUPLICATE_WINDOW) -> UpdateCursor:
        """Build a cursor from persisted session state and bounded update metadata.

        Args:
            record: Session record containing update state, peer cache and metadata.
            duplicate_window: Maximum recent duplicate keys to restore.

        Returns:
            A cursor containing global state, channel cursors, cached entities and the newest retained keys.
        """
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
        """Convert the global cursor fields to the session model's ``UpdateState``."""
        return UpdateState(pts=self.pts, qts=self.qts, seq=self.seq, date=self.date)

    def with_state(
        self,
        *,
        pts: int | None = None,
        qts: int | None = None,
        seq: int | None = None,
        date: datetime | int | float | str | None = None,
    ) -> UpdateCursor:
        """Return a cursor with selected global state fields replaced.

        ``date`` accepts the same representations as ``coerce_update_datetime``; omitted fields retain their current values.

        Args:
            pts: Optional replacement global persistent timestamp.
            qts: Optional replacement secret-chat timestamp.
            seq: Optional replacement global sequence number.
            date: Optional datetime/string/Unix timestamp; aware values retain their timezone.
        """
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
        """Return the channel cursor or a zero-PTS cursor when this channel is not known.

        Args:
            channel_id: Telegram channel identifier to look up.
        """
        for cursor in self.channel_cursors:
            if cursor.channel_id == channel_id:
                return cursor
        return ChannelUpdateCursor(channel_id=channel_id)

    def with_channel_state(
        self, channel_id: int, *, pts: int, date: datetime | int | float | str | None = None
    ) -> UpdateCursor:
        """Return a cursor with one channel's PTS state replaced or added.

        Args:
            channel_id: Telegram channel identifier whose cursor is updated.
            pts: Replacement channel persistent timestamp.
            date: Optional channel datetime/string/Unix timestamp; aware values retain their timezone.
        """
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
        """Return a cursor with incoming entities merged by peer kind and identifier.

        Args:
            entities: Entity references observed in newly processed update data.
        """
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
        """Return a cursor with the supplied persisted duplicate-key sequence.

        Args:
            duplicate_keys: Recent update identity keys to persist in order.
        """
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
    """Bounded insertion-ordered set for duplicate suppression across persisted update state.

    Args:
        keys: Existing keys restored from session metadata.
        max_size: Positive maximum number of keys retained, defaulting to 2048.

    Raises:
        ValueError: If ``max_size`` is not positive.
    """

    def __init__(self, keys: Iterable[str] = (), *, max_size: int = DEFAULT_DUPLICATE_WINDOW) -> None:
        """Restore optional keys while retaining only the most recent ``max_size`` distinct values.

        Args:
            keys: Existing persisted duplicate keys to restore.
            max_size: Positive maximum count retained in the duplicate window.
        """
        if max_size <= 0:
            raise ValueError("duplicate tracker max_size must be positive")
        self.max_size = max_size
        self._keys: deque[str] = deque()
        self._seen: set[str] = set()
        for key in keys:
            self.add(key)

    def __contains__(self, key: object) -> bool:
        """Return whether ``key`` is currently retained by the duplicate window.

        Args:
            key: Candidate object to test for duplicate membership.
        """
        return key in self._seen

    def add(self, key: str) -> None:
        """Remember a new key, evicting the oldest retained key when the window is full.

        Args:
            key: Raw update identity key to retain.
        """
        if key in self._seen:
            return
        self._keys.append(key)
        self._seen.add(key)
        while len(self._keys) > self.max_size:
            removed = self._keys.popleft()
            self._seen.discard(removed)

    def keys(self) -> tuple[str, ...]:
        """Return retained keys from oldest to newest for session persistence."""
        return tuple(self._keys)


def update_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    """Return a shallow copy of the nested update metadata or an empty mapping.

    Args:
        metadata: Session metadata mapping that may contain update-specific fields.
    """
    value = metadata.get(UPDATE_METADATA_KEY)
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def metadata_with_duplicate_keys(
    metadata: Mapping[str, Any], keys: Iterable[str], channel_cursors: Iterable[ChannelUpdateCursor] = ()
) -> dict[str, Any]:
    """Return metadata updated with duplicate keys and, when supplied, channel cursors.

    Empty ``channel_cursors`` leave an existing serialized channel mapping unchanged.

    Args:
        metadata: Session metadata mapping to copy and update.
        keys: Recent raw-update keys to store for duplicate suppression.
        channel_cursors: Optional channel cursor states to serialize.
    """
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
    """Deserialize well-formed channel cursors from update metadata, skipping invalid entries.

    Args:
        metadata: Nested update metadata containing optional serialized channel cursors.
    """
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
    """Merge normalized entity references by peer identity using peer-cache merge policy.

    Args:
        existing: Current normalized entity references.
        incoming: Newly observed entity references.
    """
    peers = merge_peer_entries(
        (entity.to_peer_cache_entry() for entity in existing), (entity.to_peer_cache_entry() for entity in incoming)
    )
    return {(peer.kind, peer.id): entity_reference_from_peer(peer) for peer in peers}


def merge_peer_cache_entries(
    existing: Iterable[PeerCacheEntry], entities: Iterable[EntityReference]
) -> tuple[PeerCacheEntry, ...]:
    """Merge update entities into existing session peer-cache entries.

    Args:
        existing: Current session peer-cache entries.
        entities: Update entities to merge into the cache.
    """
    return merge_peer_entries(existing, (entity.to_peer_cache_entry() for entity in entities))


def entity_reference_from_peer(peer: PeerCacheEntry) -> EntityReference:
    """Convert a persisted peer-cache entry to its update-state representation.

    Args:
        peer: Persisted session peer-cache entry to project.
    """
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
