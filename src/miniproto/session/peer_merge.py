"""Merge durable peer cache entries without discarding richer known metadata."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from miniproto.session.models import PeerCacheEntry
from miniproto.types import PeerKind

PeerKey = tuple[PeerKind, int]


@dataclass(frozen=True, slots=True)
class PeerEntryMapMerge:
    """Merged peer map plus keys needed for incremental index reconciliation.

    Attributes:
        entries: Canonical peer map after applying incoming entries.
        affected_keys: Input keys whose updates may require index reconciliation.
        canonical_affected_keys: Existing canonical keys affected by updates.
        appended_keys: Canonical keys newly appended to the map.
    """

    entries: dict[PeerKey, PeerCacheEntry]
    affected_keys: tuple[PeerKey, ...]
    canonical_affected_keys: tuple[PeerKey, ...]
    appended_keys: tuple[PeerKey, ...]


def merge_peer_entry(current: PeerCacheEntry, incoming: PeerCacheEntry) -> PeerCacheEntry:
    """Prefer fresh fields while retaining existing hashes and populated metadata.

    Args:
        current: Existing canonical peer cache entry.
        incoming: New entry whose populated fields take precedence.
    """
    incoming_raw = dict(incoming.raw or {})
    complete = incoming_raw.get("_miniproto_complete") is True
    raw = {} if complete else dict(current.raw or {})
    raw.update(incoming_raw)
    return PeerCacheEntry(
        id=incoming.id,
        kind=incoming.kind,
        access_hash=incoming.access_hash if incoming.access_hash is not None else current.access_hash,
        username=incoming.username if complete else incoming.username or current.username,
        phone=incoming.phone if complete else incoming.phone or current.phone,
        updated_at=incoming.updated_at,
        raw=raw or None,
    )


def merge_peer_entries(
    existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]
) -> tuple[PeerCacheEntry, ...]:
    """Merge peer collections into canonical map insertion order.

    Args:
        existing: Current peer entries in canonical order.
        incoming: New peer entries to merge.
    """
    return tuple(merge_peer_entry_map(existing, incoming).values())


def merge_peer_entry_map(
    existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]
) -> dict[PeerKey, PeerCacheEntry]:
    """Merge peer collections into a map keyed by kind and Telegram ID.

    Args:
        existing: Current peer entries.
        incoming: New peer entries to merge.
    """
    return merge_peer_entry_map_with_metadata(existing, incoming).entries


def merge_peer_entry_map_with_metadata(
    existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]
) -> PeerEntryMapMerge:
    """Merge entries and report affected, canonical and newly appended keys.

    Self entries replace an equivalent user key, preserving the cache's single
    canonical representation for the authenticated account.

    Args:
        existing: Current peer entries in insertion order.
        incoming: New peer entries whose effects are tracked.
    """
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
