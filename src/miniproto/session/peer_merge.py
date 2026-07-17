from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from miniproto.session.models import PeerCacheEntry
from miniproto.types import PeerKind

PeerKey = tuple[PeerKind, int]


@dataclass(frozen=True, slots=True)
class PeerEntryMapMerge:
    entries: dict[PeerKey, PeerCacheEntry]
    affected_keys: tuple[PeerKey, ...]
    canonical_affected_keys: tuple[PeerKey, ...]
    appended_keys: tuple[PeerKey, ...]


def merge_peer_entry(current: PeerCacheEntry, incoming: PeerCacheEntry) -> PeerCacheEntry:
    raw = dict(current.raw or {})
    raw.update(dict(incoming.raw or {}))
    return PeerCacheEntry(
        id=incoming.id,
        kind=incoming.kind,
        access_hash=incoming.access_hash if incoming.access_hash is not None else current.access_hash,
        username=incoming.username or current.username,
        phone=incoming.phone or current.phone,
        updated_at=incoming.updated_at,
        raw=raw or None,
    )


def merge_peer_entries(
    existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]
) -> tuple[PeerCacheEntry, ...]:
    return tuple(merge_peer_entry_map(existing, incoming).values())


def merge_peer_entry_map(
    existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]
) -> dict[PeerKey, PeerCacheEntry]:
    return merge_peer_entry_map_with_metadata(existing, incoming).entries


def merge_peer_entry_map_with_metadata(
    existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]
) -> PeerEntryMapMerge:
    incoming_entries = tuple(incoming)
    affected_by_event: dict[PeerKey, None] = {}
    for entry in incoming_entries:
        if entry.kind == "self":
            affected_by_event.setdefault(("user", entry.id), None)
        key = (entry.kind, entry.id)
        affected_by_event.setdefault(key, None)

    affected_set = set(affected_by_event)
    merged: dict[PeerKey, PeerCacheEntry] = {}
    canonical_affected: dict[PeerKey, None] = {}
    for entry in existing:
        key = (entry.kind, entry.id)
        merged[key] = entry
        if key in affected_set:
            canonical_affected.setdefault(key, None)

    appended: dict[PeerKey, None] = {}
    for entry in incoming_entries:
        if entry.kind == "self":
            removed_key: PeerKey = ("user", entry.id)
            merged.pop(removed_key, None)
            canonical_affected.pop(removed_key, None)
            appended.pop(removed_key, None)
        key = (entry.kind, entry.id)
        current = merged.get(key)
        merged[key] = entry if current is None else merge_peer_entry(current, entry)
        if current is None:
            canonical_affected.pop(key, None)
            canonical_affected[key] = None
            appended.pop(key, None)
            appended[key] = None
    return PeerEntryMapMerge(
        entries=merged,
        affected_keys=tuple(affected_by_event),
        canonical_affected_keys=tuple(canonical_affected),
        appended_keys=tuple(appended),
    )


__all__ = [
    "PeerEntryMapMerge",
    "PeerKey",
    "merge_peer_entries",
    "merge_peer_entry",
    "merge_peer_entry_map",
    "merge_peer_entry_map_with_metadata",
]
