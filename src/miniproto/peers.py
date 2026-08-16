"""Resolve, normalize, and persist Telegram peers with revision-aware indexes."""

from __future__ import annotations

import asyncio
import inspect
import time
from collections.abc import Awaitable, Callable, Iterable, Mapping
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol, cast

from miniproto.config import ClientConfig
from miniproto.errors import NotFound, RpcError, Unauthorized, classify_rpc_error
from miniproto.invoke import load_session_record
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, SessionRecord, UserIdentity
from miniproto.session.peer_merge import (
    PeerEntryMapMerge,
    PeerKey,
    merge_peer_entries,
    merge_peer_entry_map_with_metadata,
)
from miniproto.session.storage import SessionStorage
from miniproto.types import Peer, PeerKind, User

USERNAME_CACHE_TTL = timedelta(hours=24)


class PeerInvoker(Protocol):
    """Callable capable of executing a raw Telegram request synchronously or asynchronously."""

    def __call__(self, raw_request: object, /) -> Awaitable[object] | object:
        """Execute ``raw_request`` and return its direct or awaitable result.

        Args:
            raw_request: Raw Telegram function object to invoke.
        """
        ...


OwnerKeys = PeerKey | tuple[PeerKey, ...]


@dataclass(slots=True)
class _PeerIndexBundle:
    """Private canonical peer indexes and their stable insertion ordering.

    Attributes:
        entries_by_key: Canonical entries keyed by kind and ID.
        keys_by_id: Canonical owners grouped by numeric ID.
        owners_by_username: Canonical owners grouped by normalized username.
        owners_by_phone: Canonical owners grouped by normalized digits.
        order_by_key: Stable insertion ordering for tied owners.
        cached_user: Optional durable authenticated identity.
        next_order: Next stable order value for appended entries.
    """

    entries_by_key: dict[PeerKey, PeerCacheEntry]
    keys_by_id: dict[int, OwnerKeys]
    owners_by_username: dict[str, OwnerKeys]
    owners_by_phone: dict[str, OwnerKeys]
    order_by_key: dict[PeerKey, int]
    cached_user: UserIdentity | None
    next_order: int


class PeerCache:
    """Revision-aware session peer cache with local and remote resolution paths."""

    def __init__(self, config: ClientConfig, storage: SessionStorage, invoker: PeerInvoker) -> None:
        """Bind client configuration, mutable session storage, and raw invocation.

        Args:
            config: Client configuration whose DC identifies loaded session state.
            storage: Session storage supplying durable auth and peer domains.
            invoker: Raw Telegram request callable for remote peer resolution.
        """
        self._config = config
        self._storage = storage
        self._invoke = invoker
        self._index_lock = asyncio.Lock()
        self._index_bundle = _PeerIndexBundle({}, {}, {}, {}, {}, None, 0)
        self._loaded_auth_revision: int | None = None
        self._loaded_peers_revision: int | None = None
        self._index_rebuilds = 0
        self._canonical_tuple_visits = 0
        self._incremental_reconciliations = 0
        self._incremental_reconciliation_ns = 0

    @property
    def index_stats(self) -> Mapping[str, int]:
        """Return diagnostic rebuild and incremental-reconciliation counters."""
        return {
            "rebuilds": self._index_rebuilds,
            "canonical_tuple_visits": self._canonical_tuple_visits,
            "incremental_reconciliations": self._incremental_reconciliations,
            "incremental_reconciliation_ns": self._incremental_reconciliation_ns,
        }

    async def get_me(self, *, refresh: bool = False) -> User:
        """Return the authenticated user, reading cache unless ``refresh`` is true.

        Args:
            refresh: When true, try ``users.getUsers(inputUserSelf)`` first. If
                its result lacks a self user, return a cached identity when one
                exists; otherwise raise ``Unauthorized``.

        Raises:
            Unauthorized: If Telegram does not return a concrete self user and
                no cached identity is available.
        """
        if not refresh:
            async with self._index_lock:
                await self._ensure_indexes_locked()
                if self._index_bundle.cached_user is not None:
                    return _user_from_identity(self._index_bundle.cached_user)
        result = await self._invoke_raw(functions.UsersGetUsers(id=(types.InputUserSelf(),)))
        users = result if isinstance(result, tuple) else ()
        raw_user = next((item for item in users if isinstance(item, types.User)), None)
        if raw_user is None:
            async with self._index_lock:
                await self._ensure_indexes_locked()
                if self._index_bundle.cached_user is not None:
                    return _user_from_identity(self._index_bundle.cached_user)
            raise Unauthorized("users.getUsers(inputUserSelf) returned no self user")
        user = _user_from_raw_user(raw_user, force_self=True)
        await self._save_entries((_entry_from_user(raw_user, force_self=True),), user=_identity_from_user(user))
        return user

    async def resolve_peer(self, peer: Peer | str | int) -> Peer:
        """Resolve a peer object, numeric ID, phone number, self alias, or username.

        Numeric IDs use cached peers first, then seed from dialogs. Usernames may
        call Telegram after the 24-hour local username cache expires.

        Raises:
            NotFound: If the reference is empty, unknown, or lacks an access hash.
            RpcError: If remote username resolution returns an unexpected result.

        Args:
            peer: Existing peer, signed/numeric ID, self alias, phone, or username.
        """
        if isinstance(peer, Peer):
            return await self._resolve_public_peer(peer)
        if isinstance(peer, int):
            return await self._resolve_numeric_peer(peer)
        value = peer.strip()
        if _is_self_alias(value):
            return (await self.get_me()).peer
        if value.startswith("+"):
            return await self._resolve_phone(value)
        numeric = _maybe_int(value)
        if numeric is not None:
            return await self._resolve_numeric_peer(numeric)
        username = _normalize_username(value)
        if username is None:
            raise NotFound("peer reference is empty")
        return await self._resolve_username(username)

    async def resolve_input_peer(self, peer: Peer | str | int) -> object:
        """Resolve a reference then return the matching MTProto ``InputPeer``.

        Raises:
            NotFound: If resolution fails or the resolved peer needs an uncached hash.

        Args:
            peer: Any reference accepted by :meth:`resolve_peer`.
        """
        return input_peer_from_peer(await self.resolve_peer(peer))

    async def remember_raw_entities(self, raw: object) -> None:
        """Extract peer-bearing raw objects and merge their cache entries durably.

        Args:
            raw: Raw Telegram object, container, or sequence that may expose users/chats.
        """
        entries = tuple(_entries_from_raw(raw))
        if entries:
            await self._save_entries(entries)

    async def _resolve_public_peer(self, peer: Peer) -> Peer:
        """Validate or enrich a supplied peer with its required cached access hash.

        Args:
            peer: Caller-supplied public peer reference.
        """
        if peer.kind == "self":
            if peer.id > 0 and peer.access_hash is not None:
                return peer
            return (await self.get_me()).peer
        if peer.kind == "chat":
            return peer
        if peer.access_hash is not None:
            return peer
        async with self._index_lock:
            await self._ensure_indexes_locked()
            entry = self._index_bundle.entries_by_key.get((peer.kind, peer.id))
        if entry is None or entry.access_hash is None:
            raise NotFound(f"{peer.kind} access hash is not cached")
        return _peer_from_entry(entry)

    async def _resolve_numeric_peer(self, value: int) -> Peer:
        """Resolve numeric IDs locally, seeding dialog peers when needed.

        Each unresolved call seeds dialogs then retries the indexes; no negative
        result is cached, so a later unresolved call can seed dialogs again.

        Args:
            value: Telegram numeric ID using signed chat/channel conventions.
        """
        resolved = await self._resolve_numeric_peer_from_index(value)
        if resolved is not None:
            return resolved
        await self._seed_dialog_peers()
        resolved = await self._resolve_numeric_peer_from_index(value)
        if resolved is not None:
            return resolved
        raise NotFound("numeric peer id is not cached")

    async def _resolve_phone(self, phone: str) -> Peer:
        """Resolve a normalized cached phone number without remote lookup.

        Args:
            phone: User-entered phone reference whose digits are normalized.
        """
        normalized = _normalize_phone(phone)
        async with self._index_lock:
            await self._ensure_indexes_locked()
            owners = self._index_bundle.owners_by_phone.get(normalized or "")
            if owners is not None:
                entry = self._index_bundle.entries_by_key[_owner_tuple(owners)[0]]
                return _peer_from_entry(entry)
            cached_user = self._index_bundle.cached_user
            if cached_user is not None and _normalize_phone(cached_user.phone) == normalized:
                return _user_from_identity(cached_user).peer
        raise NotFound("phone peer is not cached")

    async def _resolve_username(self, username: str) -> Peer:
        """Resolve a fresh cached username or fetch and persist Telegram's answer.

        Args:
            username: Already normalized username without URL or ``@`` syntax.
        """
        async with self._index_lock:
            await self._ensure_indexes_locked()
            cached = self._find_username_entry_locked(username)
        if cached is not None:
            return _peer_from_entry(cached)
        result = await self._invoke_raw(functions.ContactsResolveUsername(username=username))
        if not isinstance(result, types.ContactsResolvedPeer):
            raise RpcError("contacts.resolveUsername returned an unexpected result", request="contacts.resolveUsername")
        entries = tuple(_entries_from_raw(result))
        await self._save_entries(entries)
        resolved = _peer_from_raw_peer(result.peer, entries)
        if resolved is None:
            raise NotFound("resolved username did not include a usable peer")
        return resolved

    async def _seed_dialog_peers(self, *, limit: int = 100) -> None:
        """Populate cache entries from the first ``limit`` unpinned dialogs.

        Args:
            limit: Maximum dialog entries requested from Telegram.
        """
        result = await self._invoke_raw(
            functions.MessagesGetDialogs(
                exclude_pinned=True, offset_date=0, offset_id=0, offset_peer=types.InputPeerEmpty(), limit=limit, hash=0
            )
        )
        entries = tuple(_entries_from_raw(result))
        if entries:
            await self._save_entries(entries)

    async def _invoke_raw(self, request: object) -> object:
        """Invoke a raw request and translate RPC failures to public errors.

        Args:
            request: Raw Telegram function object passed to the configured invoker.
        """
        try:
            result = self._invoke(request)
            return await result if inspect.isawaitable(result) else result
        except RpcError as exc:
            raise classify_rpc_error(exc) from exc

    async def _save_entries(self, entries: Iterable[PeerCacheEntry], *, user: UserIdentity | None = None) -> None:
        """Merge entries atomically and incrementally reconcile compatible indexes.

        Args:
            entries: Newly observed peer cache entries to merge.
            user: Optional authoritative authenticated identity to persist.
        """
        incoming = tuple(entries)
        if not incoming and user is None:
            return
        async with self._index_lock:
            await self._ensure_indexes_locked()
            base_revisions = self._relevant_revisions()
            transformed_record: SessionRecord | None = None
            transformed_entries: dict[PeerKey, PeerCacheEntry] = {}
            transformed_merge: PeerEntryMapMerge | None = None
            own_peers_changed = False
            own_auth_changed = False

            def merge(payload: Mapping[str, Any] | None) -> SessionRecord:
                """Apply this save's peer and identity merge inside storage mutation.

                Args:
                    payload: Current decoded session mapping supplied by storage.
                """
                nonlocal transformed_record, transformed_entries, transformed_merge
                nonlocal own_peers_changed, own_auth_changed
                record = load_session_record(payload, self._config.dc_id)
                transformed_merge = merge_peer_entry_map_with_metadata(record.peers, incoming)
                transformed_entries = transformed_merge.entries
                peers = tuple(transformed_entries.values())
                identity = user or _identity_updated_from_entries(record.user, incoming)
                transformed_record = replace(record, peers=peers, user=identity)
                own_peers_changed = peers != record.peers
                own_auth_changed = identity != record.user
                return transformed_record

            try:
                committed = await self._storage.mutate(merge)
            except asyncio.CancelledError:
                self._loaded_auth_revision = None
                self._loaded_peers_revision = None
                raise
            if transformed_record is None:
                transformed_record = load_session_record(committed, self._config.dc_id)
                transformed_entries = {(entry.kind, entry.id): entry for entry in transformed_record.peers}
            post_revisions = self._relevant_revisions()
            attributable = post_revisions == (
                base_revisions[0] + int(own_auth_changed),
                base_revisions[1] + int(own_peers_changed),
            )
            if not attributable:
                self._publish_rebuild_locked(transformed_record, post_revisions)
                return
            if own_peers_changed:
                if transformed_merge is None:
                    self._publish_rebuild_locked(transformed_record, post_revisions)
                    return
                reconciliation_started = time.perf_counter_ns()
                for key in transformed_merge.affected_keys:
                    if key not in transformed_entries:
                        self._replace_index_entry_locked(key, None)
                for key in transformed_merge.appended_keys:
                    if key in self._index_bundle.order_by_key:
                        self._replace_index_entry_locked(key, None)
                for key in transformed_merge.canonical_affected_keys:
                    self._replace_index_entry_locked(key, transformed_entries[key])
                self._incremental_reconciliations += 1
                self._incremental_reconciliation_ns += time.perf_counter_ns() - reconciliation_started
            if own_auth_changed:
                self._index_bundle.cached_user = transformed_record.user
            self._loaded_auth_revision, self._loaded_peers_revision = post_revisions

    async def _resolve_numeric_peer_from_index(self, value: int) -> Peer | None:
        """Resolve a numeric external ID from the locked canonical indexes.

        Args:
            value: Telegram numeric ID using signed chat/channel conventions.
        """
        async with self._index_lock:
            await self._ensure_indexes_locked()
            bundle = self._index_bundle
            if value < 0:
                preferred_kind, peer_id = _numeric_candidates(value)[0]
                entry = bundle.entries_by_key.get((cast("PeerKind", preferred_kind), peer_id))
                return None if entry is None else _peer_from_entry(entry)
            owners = bundle.keys_by_id.get(value)
            if owners is not None:
                for kind in ("self", "user", "chat", "channel"):
                    for key in _owner_tuple(owners):
                        if key[0] == kind:
                            return _peer_from_entry(bundle.entries_by_key[key])
            if bundle.cached_user is not None and bundle.cached_user.id == value:
                return _user_from_identity(bundle.cached_user).peer
            return None

    def _find_username_entry_locked(self, username: str) -> PeerCacheEntry | None:
        """Return the first non-expired username owner from locked indexes.

        Args:
            username: Normalized username to locate.
        """
        normalized = _normalize_username(username)
        if normalized is None:
            return None
        owners = self._index_bundle.owners_by_username.get(normalized)
        if owners is None:
            return None
        now = datetime.now(UTC)
        for key in _owner_tuple(owners):
            entry = self._index_bundle.entries_by_key[key]
            if now - entry.updated_at <= USERNAME_CACHE_TTL:
                return entry
        return None

    async def _ensure_indexes_locked(self) -> None:
        """Rebuild indexes only from a stable pair of storage domain revisions."""
        while True:
            revisions_before = self._relevant_revisions()
            if revisions_before == (self._loaded_auth_revision, self._loaded_peers_revision):
                return
            payload = await self._storage.load()
            revisions_after = self._relevant_revisions()
            if revisions_before != revisions_after:
                continue
            record = load_session_record(payload, self._config.dc_id)
            self._publish_rebuild_locked(record, revisions_after)
            return

    def _publish_rebuild_locked(self, record: SessionRecord, revisions: tuple[int, int]) -> None:
        """Replace locked indexes from a stable record and record the rebuild.

        Args:
            record: Stable decoded session record to index.
            revisions: Stable auth and peer domain revisions associated with it.
        """
        self._index_bundle = _build_index_bundle(record, self._record_canonical_visit)
        self._loaded_auth_revision, self._loaded_peers_revision = revisions
        self._index_rebuilds += 1

    def _record_canonical_visit(self) -> None:
        """Increment the instrumentation counter for canonical-entry scans."""
        self._canonical_tuple_visits += 1

    def _relevant_revisions(self) -> tuple[int, int]:
        """Return the storage revisions that can invalidate peer indexes."""
        revisions = self._storage.domain_revisions()
        return int(revisions.get("auth", 0)), int(revisions.get("peers", 0))

    def _replace_index_entry_locked(self, key: PeerKey, replacement: PeerCacheEntry | None) -> None:
        """Remove or replace one canonical entry across every locked secondary index.

        Args:
            key: Canonical kind-and-ID key to replace or remove.
            replacement: New entry, or ``None`` to remove the existing entry.
        """
        bundle = self._index_bundle
        current = bundle.entries_by_key.get(key)
        canonical_key = key
        if current is not None:
            id_owners = bundle.keys_by_id.get(current.id)
            if id_owners is not None:
                canonical_key = next((owner for owner in _owner_tuple(id_owners) if owner == key), key)
            _remove_owner(bundle.keys_by_id, current.id, key)
            for username in _entry_usernames(current):
                _remove_owner(bundle.owners_by_username, username, key)
            phone = _normalize_phone(current.phone)
            if phone is not None:
                _remove_owner(bundle.owners_by_phone, phone, key)
        if replacement is None:
            bundle.entries_by_key.pop(key, None)
            bundle.order_by_key.pop(key, None)
            return
        if canonical_key not in bundle.order_by_key:
            bundle.order_by_key[canonical_key] = bundle.next_order
            bundle.next_order += 1
        bundle.entries_by_key[canonical_key] = replacement
        _add_owner(bundle.keys_by_id, replacement.id, canonical_key, bundle.order_by_key)
        for username in _entry_usernames(replacement):
            _add_owner(bundle.owners_by_username, username, canonical_key, bundle.order_by_key)
        phone = _normalize_phone(replacement.phone)
        if phone is not None:
            _add_owner(bundle.owners_by_phone, phone, canonical_key, bundle.order_by_key)


def _build_index_bundle(record: SessionRecord, visit: Callable[[], None]) -> _PeerIndexBundle:
    """Build canonical peer, ID, username, and phone indexes in record order.

    Args:
        record: Session record whose cached peers are indexed.
        visit: Instrumentation callback invoked for each canonical peer entry.
    """
    entries_by_key: dict[PeerKey, PeerCacheEntry] = {}
    keys_by_id: dict[int, OwnerKeys] = {}
    owners_by_username: dict[str, OwnerKeys] = {}
    owners_by_phone: dict[str, OwnerKeys] = {}
    order_by_key: dict[PeerKey, int] = {}
    for order, entry in enumerate(record.peers):
        visit()
        key: PeerKey = (entry.kind, entry.id)
        entries_by_key[key] = entry
        order_by_key[key] = order
        _add_owner(keys_by_id, entry.id, key, order_by_key)
        for username in _entry_usernames(entry):
            _add_owner(owners_by_username, username, key, order_by_key)
        phone = _normalize_phone(entry.phone)
        if phone is not None:
            _add_owner(owners_by_phone, phone, key, order_by_key)
    return _PeerIndexBundle(
        entries_by_key=entries_by_key,
        keys_by_id=keys_by_id,
        owners_by_username=owners_by_username,
        owners_by_phone=owners_by_phone,
        order_by_key=order_by_key,
        cached_user=record.user,
        next_order=len(record.peers),
    )


def _owner_tuple(owners: OwnerKeys) -> tuple[PeerKey, ...]:
    """Normalize compact single-owner and tuple-owner index values.

    Args:
        owners: One peer key or an ordered tuple of peer keys.
    """
    if isinstance(owners[0], str):
        return (cast("PeerKey", owners),)
    return cast("tuple[PeerKey, ...]", owners)


def _add_owner(index: dict[Any, OwnerKeys], value: Any, key: PeerKey, order_by_key: Mapping[PeerKey, int]) -> None:
    """Add a unique owner while retaining canonical insertion ordering.

    Args:
        index: Secondary index to update.
        value: Indexed ID, normalized username, or normalized phone value.
        key: Canonical peer key to add.
        order_by_key: Stable ordering used when more than one owner exists.
    """
    current = index.get(value)
    if current is None:
        index[value] = key
        return
    owners = list(_owner_tuple(current))
    if key in owners:
        return
    owners.append(key)
    owners.sort(key=order_by_key.__getitem__)
    index[value] = tuple(owners)


def _remove_owner(index: dict[Any, OwnerKeys], value: Any, key: PeerKey) -> None:
    """Remove one owner and compact the index representation when possible.

    Args:
        index: Secondary index to update.
        value: Indexed value whose owner is being removed.
        key: Canonical peer key to remove.
    """
    current = index.get(value)
    if current is None:
        return
    owners = tuple(owner for owner in _owner_tuple(current) if owner != key)
    if not owners:
        index.pop(value, None)
    elif len(owners) == 1:
        index[value] = owners[0]
    else:
        index[value] = owners


def _entry_usernames(entry: PeerCacheEntry) -> tuple[str, ...]:
    """Return unique normalized primary and historical usernames for an entry.

    Args:
        entry: Cached peer entry whose primary and raw usernames are inspected.
    """
    values: list[str] = []
    primary = _normalize_username(entry.username or "")
    if primary is not None:
        values.append(primary)
    raw = entry.raw if isinstance(entry.raw, Mapping) else {}
    raw_usernames = raw.get("usernames", ())
    if isinstance(raw_usernames, Iterable) and not isinstance(raw_usernames, str | bytes):
        for raw_username in raw_usernames:
            username = _normalize_username(str(raw_username))
            if username is not None and username not in values:
                values.append(username)
    return tuple(values)


def input_peer_from_peer(peer: Peer) -> object:
    """Convert a resolved peer to its MTProto ``InputPeer`` representation.

    Chats need no hash; users and channels must carry a cached access hash.

    Raises:
        NotFound: If the peer kind is unsupported or its required hash is absent.

    Args:
        peer: Resolved public peer to convert.
    """
    if peer.kind == "self":
        return types.InputPeerSelf()
    if peer.kind == "chat":
        return types.InputPeerChat(chat_id=peer.id)
    if peer.access_hash is None:
        raise NotFound(f"{peer.kind} access hash is not cached")
    if peer.kind == "user":
        return types.InputPeerUser(user_id=peer.id, access_hash=peer.access_hash)
    if peer.kind == "channel":
        return types.InputPeerChannel(channel_id=peer.id, access_hash=peer.access_hash)
    raise NotFound(f"unsupported peer kind: {peer.kind}")


def input_user_from_peer(peer: Peer) -> object:
    """Convert self or a hash-bearing user peer to MTProto ``InputUser``.

    Raises:
        NotFound: If ``peer`` is not self or a user with an access hash.

    Args:
        peer: Self or resolved user peer to convert.
    """
    if peer.kind == "self":
        return types.InputUserSelf()
    if peer.kind != "user" or peer.access_hash is None:
        raise NotFound("input users require a cached user access hash")
    return types.InputUser(user_id=peer.id, access_hash=peer.access_hash)


def input_channel_from_peer(peer: Peer) -> object:
    """Convert a hash-bearing channel peer to MTProto ``InputChannel``.

    Raises:
        NotFound: If ``peer`` is not a channel with an access hash.

    Args:
        peer: Resolved channel peer to convert.
    """
    if peer.kind != "channel" or peer.access_hash is None:
        raise NotFound("input channels require a cached channel access hash")
    return types.InputChannel(channel_id=peer.id, access_hash=peer.access_hash)


def _entries_from_raw(raw: object) -> Iterable[PeerCacheEntry]:
    """Yield cache entries recursively from supported raw Telegram containers.

    Args:
        raw: Raw peer, container, or sequence to inspect recursively.
    """
    if isinstance(raw, types.User):
        yield _entry_from_user(raw)
        return
    if isinstance(raw, types.UserEmpty):
        yield PeerCacheEntry(id=raw.id, kind="user")
        return
    if isinstance(raw, types.Chat | types.ChatForbidden):
        yield _entry_from_chat(raw)
        return
    if isinstance(raw, types.Channel | types.ChannelForbidden):
        yield _entry_from_channel(raw)
        return
    if isinstance(raw, tuple | list):
        for item in raw:
            yield from _entries_from_raw(item)
        return
    for attr in ("users", "chats"):
        for item in _iter_attr(raw, attr):
            yield from _entries_from_raw(item)


def _entry_from_user(user: types.User, *, force_self: bool = False) -> PeerCacheEntry:
    """Create a cache entry from a user, omitting hashes from minimal objects.

    Args:
        user: Raw Telegram user to cache.
        force_self: Mark the entry as self regardless of the raw ``self_`` flag.
    """
    usernames = _raw_usernames(user)
    primary_username = user.username or (usernames[0] if usernames else None)
    return PeerCacheEntry(
        id=user.id,
        kind="self" if force_self or user.self_ else "user",
        access_hash=None if user.min else user.access_hash,
        username=primary_username,
        phone=user.phone,
        raw=_compact_raw(is_bot=user.bot, first_name=user.first_name, last_name=user.last_name, usernames=usernames),
    )


def _entry_from_chat(chat: types.Chat | types.ChatForbidden) -> PeerCacheEntry:
    """Create a title-only cache entry for a basic chat.

    Args:
        chat: Raw basic or forbidden chat to cache.
    """
    return PeerCacheEntry(id=chat.id, kind="chat", raw=_compact_raw(title=chat.title))


def _entry_from_channel(channel: types.Channel | types.ChannelForbidden) -> PeerCacheEntry:
    """Create a channel entry, omitting inaccessible hashes from minimal objects.

    Args:
        channel: Raw channel or forbidden channel to cache.
    """
    return PeerCacheEntry(
        id=channel.id,
        kind="channel",
        access_hash=None if getattr(channel, "min", False) else channel.access_hash,
        username=getattr(channel, "username", None),
        raw=_compact_raw(title=channel.title, usernames=_raw_usernames(channel)),
    )


def _raw_usernames(raw: object) -> list[str]:
    """Collect the primary and alternate raw usernames without duplicates.

    Args:
        raw: Raw Telegram object that may expose username fields.
    """
    values: list[str] = []
    primary = getattr(raw, "username", None)
    if isinstance(primary, str) and primary:
        values.append(primary)
    for item in _iter_attr(raw, "usernames"):
        username = getattr(item, "username", None)
        if isinstance(username, str) and username and username not in values:
            values.append(username)
    return values


def _merge_entries(
    existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]
) -> tuple[PeerCacheEntry, ...]:
    """Merge incoming peer entries using the session's canonical merge policy.

    Args:
        existing: Current canonical peer entries.
        incoming: Newly observed peer entries.
    """
    return merge_peer_entries(existing, incoming)


def _identity_updated_from_entries(
    current: UserIdentity | None, entries: Iterable[PeerCacheEntry]
) -> UserIdentity | None:
    """Refresh matching self-identity fields from newly received cache entries.

    Args:
        current: Existing authenticated identity, if any.
        entries: Newly observed cache entries that may update self fields.
    """
    if current is None:
        return None
    self_entry = next((entry for entry in entries if entry.kind == "self" and entry.id == current.id), None)
    if self_entry is None:
        return current
    raw = dict(self_entry.raw or {})
    return UserIdentity(
        id=current.id,
        access_hash=self_entry.access_hash if self_entry.access_hash is not None else current.access_hash,
        is_bot=bool(raw.get("is_bot", current.is_bot)),
        username=self_entry.username or current.username,
        phone=self_entry.phone or current.phone,
        first_name=_optional_str(raw.get("first_name")) or current.first_name,
        last_name=_optional_str(raw.get("last_name")) or current.last_name,
    )


def _user_from_identity(identity: UserIdentity) -> User:
    """Project durable self-identity storage into the public self user model.

    Args:
        identity: Durable authenticated identity to expose.
    """
    return User(
        id=identity.id,
        access_hash=identity.access_hash,
        is_bot=identity.is_bot,
        username=identity.username,
        phone=identity.phone,
        first_name=identity.first_name,
        last_name=identity.last_name,
        is_self=True,
    )


def _user_from_raw_user(user: types.User, *, force_self: bool = False) -> User:
    """Project a raw Telegram user into the public user model.

    Args:
        user: Raw Telegram user to project.
        force_self: Mark the public user as self regardless of raw state.
    """
    return User(
        id=user.id,
        access_hash=user.access_hash,
        is_bot=user.bot,
        username=user.username,
        phone=user.phone,
        first_name=user.first_name,
        last_name=user.last_name,
        is_self=force_self or user.self_,
        raw=user,
    )


def _identity_from_user(user: User) -> UserIdentity:
    """Project a public user into the durable identity storage model.

    Args:
        user: Public user to persist as an authenticated identity.
    """
    return UserIdentity(
        id=user.id,
        access_hash=user.access_hash,
        is_bot=user.is_bot,
        username=user.username,
        phone=user.phone,
        first_name=user.first_name,
        last_name=user.last_name,
    )


def _peer_from_entry(entry: PeerCacheEntry) -> Peer:
    """Project a cached entry into a public peer reference.

    Args:
        entry: Cached peer entry to project.
    """
    return Peer(id=entry.id, kind=entry.kind, access_hash=entry.access_hash)


def _resolve_numeric_peer_from_record(record: SessionRecord, value: int) -> Peer | None:
    """Resolve an external numeric peer ID from an unindexed session record.

    Args:
        record: Session record whose cached peers are searched.
        value: Telegram numeric ID using signed chat/channel conventions.
    """
    for preferred_kind, peer_id in _numeric_candidates(value):
        entry = _find_entry(record.peers, kind=preferred_kind, id=peer_id) if preferred_kind else None
        if entry is not None:
            return _peer_from_entry(entry)
        if preferred_kind is None:
            selected = _select_entry_by_id(record.peers, peer_id)
            if selected is not None:
                return _peer_from_entry(selected)
            if record.user is not None and record.user.id == peer_id:
                return _user_from_identity(record.user).peer
    return None


def _peer_from_raw_peer(raw_peer: object, entries: Iterable[PeerCacheEntry]) -> Peer | None:
    """Convert a raw peer ID using newly extracted entries for access hashes.

    Args:
        raw_peer: Raw Telegram peer identifier to convert.
        entries: Newly extracted entries supplying peer kind and access hash.
    """
    cached = tuple(entries)
    if isinstance(raw_peer, types.PeerUser):
        entry = _find_entry(cached, kind=None, id=raw_peer.user_id)
        return Peer(
            id=raw_peer.user_id,
            kind=entry.kind if entry is not None else "user",
            access_hash=None if entry is None else entry.access_hash,
        )
    if isinstance(raw_peer, types.PeerChat):
        return Peer(id=raw_peer.chat_id, kind="chat")
    if isinstance(raw_peer, types.PeerChannel):
        entry = _find_entry(cached, kind="channel", id=raw_peer.channel_id)
        return Peer(id=raw_peer.channel_id, kind="channel", access_hash=None if entry is None else entry.access_hash)
    return None


def _find_entry(entries: Iterable[PeerCacheEntry], *, kind: PeerKind | None, id: int) -> PeerCacheEntry | None:
    """Find the first entry matching an ID and optional peer kind.

    Args:
        entries: Entries to scan in source order.
        kind: Required kind, or ``None`` for any kind.
        id: Telegram peer ID to match.
    """
    for entry in entries:
        if entry.id == id and (kind is None or entry.kind == kind):
            return entry
    return None


def _select_entry_by_id(entries: Iterable[PeerCacheEntry], id: int) -> PeerCacheEntry | None:
    """Choose an ID owner with stable self/user/chat/channel precedence.

    Args:
        entries: Entries to consider.
        id: Telegram peer ID shared by candidate entries.
    """
    candidates = tuple(entry for entry in entries if entry.id == id)
    for kind in ("self", "user", "chat", "channel"):
        selected = next((entry for entry in candidates if entry.kind == kind), None)
        if selected is not None:
            return selected
    return None


def _find_username_entry(entries: Iterable[PeerCacheEntry], username: str) -> PeerCacheEntry | None:
    """Find a non-expired matching username entry by scanning a record.

    Args:
        entries: Cached peer entries to scan.
        username: User-entered username to normalize and locate.
    """
    normalized = _normalize_username(username)
    if normalized is None:
        return None
    now = datetime.now(UTC)
    for entry in entries:
        if now - entry.updated_at > USERNAME_CACHE_TTL:
            continue
        if _entry_has_username(entry, normalized):
            return entry
    return None


def _entry_has_username(entry: PeerCacheEntry, username: str) -> bool:
    """Return whether normalized primary or alternate usernames contain a value.

    Args:
        entry: Cached peer entry to inspect.
        username: Normalized username sought in primary or alternate values.
    """
    if _normalize_username(entry.username or "") == username:
        return True
    raw = entry.raw if isinstance(entry.raw, Mapping) else {}
    raw_usernames = raw.get("usernames", ())
    if not isinstance(raw_usernames, Iterable) or isinstance(raw_usernames, str | bytes):
        return False
    return any(_normalize_username(str(item)) == username for item in raw_usernames)


def _numeric_candidates(value: int) -> tuple[tuple[PeerKind | None, int], ...]:
    """Decode Telegram's signed chat and channel ID conventions.

    Args:
        value: User-facing signed or unsigned numeric peer ID.
    """
    if value >= 0:
        return ((None, value),)
    raw = abs(value)
    if raw > 1_000_000_000_000:
        return (("channel", raw - 1_000_000_000_000),)
    return (("chat", raw),)


def _is_self_alias(value: str) -> bool:
    """Return whether a user-facing reference denotes saved messages.

    Args:
        value: User-entered peer alias to normalize and compare.
    """
    return value.strip().casefold() in {"me", "self", "saved messages", "saved_messages"}


def _maybe_int(value: str) -> int | None:
    """Parse an integer reference without exposing conversion errors.

    Args:
        value: User-entered potential numeric peer ID.
    """
    try:
        return int(value)
    except ValueError:
        return None


def _normalize_username(value: str) -> str | None:
    """Canonicalize @handles and t.me URLs, returning ``None`` for empty input.

    Args:
        value: User-entered handle or supported t.me URL.
    """
    rendered = value.strip()
    for prefix in ("https://t.me/", "http://t.me/", "t.me/"):
        if rendered.casefold().startswith(prefix):
            rendered = rendered[len(prefix) :]
            break
    rendered = rendered.removeprefix("@").split("/", 1)[0].strip().casefold()
    return rendered or None


def _normalize_phone(value: str | None) -> str | None:
    """Keep only phone digits, returning ``None`` for absent or digitless values.

    Args:
        value: Optional user-entered phone reference.
    """
    if value is None:
        return None
    digits = "".join(character for character in value if character.isdigit())
    return digits or None


def _iter_attr(raw: object, attr: str) -> tuple[object, ...]:
    """Return tuple or list attributes as a safe immutable iterable.

    Args:
        raw: Object whose attribute is inspected.
        attr: Attribute name expected to contain a tuple or list.
    """
    value = getattr(raw, attr, ())
    if isinstance(value, tuple):
        return cast("tuple[object, ...]", value)
    if isinstance(value, list):
        return tuple(value)
    return ()


def _compact_raw(**values: object) -> Mapping[str, Any] | None:
    """Remove empty optional raw fields, returning ``None`` when none remain.

    Args:
        **values: Named raw fields whose ``None`` and empty values are discarded.
    """
    compacted = {key: value for key, value in values.items() if value not in (None, (), [])}
    return compacted or None


def _optional_str(value: object) -> str | None:
    """Convert a present optional value to string while preserving ``None``.

    Args:
        value: Optional value to render as string.
    """
    return None if value is None else str(value)


__all__ = ["PeerCache", "input_channel_from_peer", "input_peer_from_peer", "input_user_from_peer"]
