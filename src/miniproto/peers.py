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
    def __call__(self, raw_request: object, /) -> Awaitable[object] | object: ...


OwnerKeys = PeerKey | tuple[PeerKey, ...]


@dataclass(slots=True)
class _PeerIndexBundle:
    entries_by_key: dict[PeerKey, PeerCacheEntry]
    keys_by_id: dict[int, OwnerKeys]
    owners_by_username: dict[str, OwnerKeys]
    owners_by_phone: dict[str, OwnerKeys]
    order_by_key: dict[PeerKey, int]
    cached_user: UserIdentity | None
    next_order: int


class PeerCache:
    def __init__(self, config: ClientConfig, storage: SessionStorage, invoker: PeerInvoker) -> None:
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
        return {
            "rebuilds": self._index_rebuilds,
            "canonical_tuple_visits": self._canonical_tuple_visits,
            "incremental_reconciliations": self._incremental_reconciliations,
            "incremental_reconciliation_ns": self._incremental_reconciliation_ns,
        }

    async def get_me(self, *, refresh: bool = False) -> User:
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
        return input_peer_from_peer(await self.resolve_peer(peer))

    async def remember_raw_entities(self, raw: object) -> None:
        entries = tuple(_entries_from_raw(raw))
        if entries:
            await self._save_entries(entries)

    async def _resolve_public_peer(self, peer: Peer) -> Peer:
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
        resolved = await self._resolve_numeric_peer_from_index(value)
        if resolved is not None:
            return resolved
        await self._seed_dialog_peers()
        resolved = await self._resolve_numeric_peer_from_index(value)
        if resolved is not None:
            return resolved
        raise NotFound("numeric peer id is not cached")

    async def _resolve_phone(self, phone: str) -> Peer:
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
        result = await self._invoke_raw(
            functions.MessagesGetDialogs(
                exclude_pinned=True, offset_date=0, offset_id=0, offset_peer=types.InputPeerEmpty(), limit=limit, hash=0
            )
        )
        entries = tuple(_entries_from_raw(result))
        if entries:
            await self._save_entries(entries)

    async def _invoke_raw(self, request: object) -> object:
        try:
            result = self._invoke(request)
            return await result if inspect.isawaitable(result) else result
        except RpcError as exc:
            raise classify_rpc_error(exc) from exc

    async def _save_entries(self, entries: Iterable[PeerCacheEntry], *, user: UserIdentity | None = None) -> None:
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
        self._index_bundle = _build_index_bundle(record, self._record_canonical_visit)
        self._loaded_auth_revision, self._loaded_peers_revision = revisions
        self._index_rebuilds += 1

    def _record_canonical_visit(self) -> None:
        self._canonical_tuple_visits += 1

    def _relevant_revisions(self) -> tuple[int, int]:
        revisions = self._storage.domain_revisions()
        return int(revisions.get("auth", 0)), int(revisions.get("peers", 0))

    def _replace_index_entry_locked(self, key: PeerKey, replacement: PeerCacheEntry | None) -> None:
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
    if isinstance(owners[0], str):
        return (cast("PeerKey", owners),)
    return cast("tuple[PeerKey, ...]", owners)


def _add_owner(index: dict[Any, OwnerKeys], value: Any, key: PeerKey, order_by_key: Mapping[PeerKey, int]) -> None:
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
    if peer.kind == "self":
        return types.InputUserSelf()
    if peer.kind != "user" or peer.access_hash is None:
        raise NotFound("input users require a cached user access hash")
    return types.InputUser(user_id=peer.id, access_hash=peer.access_hash)


def input_channel_from_peer(peer: Peer) -> object:
    if peer.kind != "channel" or peer.access_hash is None:
        raise NotFound("input channels require a cached channel access hash")
    return types.InputChannel(channel_id=peer.id, access_hash=peer.access_hash)


def _entries_from_raw(raw: object) -> Iterable[PeerCacheEntry]:
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
    return PeerCacheEntry(id=chat.id, kind="chat", raw=_compact_raw(title=chat.title))


def _entry_from_channel(channel: types.Channel | types.ChannelForbidden) -> PeerCacheEntry:
    return PeerCacheEntry(
        id=channel.id,
        kind="channel",
        access_hash=None if getattr(channel, "min", False) else channel.access_hash,
        username=getattr(channel, "username", None),
        raw=_compact_raw(title=channel.title, usernames=_raw_usernames(channel)),
    )


def _raw_usernames(raw: object) -> list[str]:
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
    return merge_peer_entries(existing, incoming)


def _identity_updated_from_entries(
    current: UserIdentity | None, entries: Iterable[PeerCacheEntry]
) -> UserIdentity | None:
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
    return Peer(id=entry.id, kind=entry.kind, access_hash=entry.access_hash)


def _resolve_numeric_peer_from_record(record: SessionRecord, value: int) -> Peer | None:
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
    for entry in entries:
        if entry.id == id and (kind is None or entry.kind == kind):
            return entry
    return None


def _select_entry_by_id(entries: Iterable[PeerCacheEntry], id: int) -> PeerCacheEntry | None:
    candidates = tuple(entry for entry in entries if entry.id == id)
    for kind in ("self", "user", "chat", "channel"):
        selected = next((entry for entry in candidates if entry.kind == kind), None)
        if selected is not None:
            return selected
    return None


def _find_username_entry(entries: Iterable[PeerCacheEntry], username: str) -> PeerCacheEntry | None:
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
    if _normalize_username(entry.username or "") == username:
        return True
    raw = entry.raw if isinstance(entry.raw, Mapping) else {}
    raw_usernames = raw.get("usernames", ())
    if not isinstance(raw_usernames, Iterable) or isinstance(raw_usernames, str | bytes):
        return False
    return any(_normalize_username(str(item)) == username for item in raw_usernames)


def _numeric_candidates(value: int) -> tuple[tuple[PeerKind | None, int], ...]:
    if value >= 0:
        return ((None, value),)
    raw = abs(value)
    if raw > 1_000_000_000_000:
        return (("channel", raw - 1_000_000_000_000),)
    return (("chat", raw),)


def _is_self_alias(value: str) -> bool:
    return value.strip().casefold() in {"me", "self", "saved messages", "saved_messages"}


def _maybe_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def _normalize_username(value: str) -> str | None:
    rendered = value.strip()
    for prefix in ("https://t.me/", "http://t.me/", "t.me/"):
        if rendered.casefold().startswith(prefix):
            rendered = rendered[len(prefix) :]
            break
    rendered = rendered.removeprefix("@").split("/", 1)[0].strip().casefold()
    return rendered or None


def _normalize_phone(value: str | None) -> str | None:
    if value is None:
        return None
    digits = "".join(character for character in value if character.isdigit())
    return digits or None


def _iter_attr(raw: object, attr: str) -> tuple[object, ...]:
    value = getattr(raw, attr, ())
    if isinstance(value, tuple):
        return cast("tuple[object, ...]", value)
    if isinstance(value, list):
        return tuple(value)
    return ()


def _compact_raw(**values: object) -> Mapping[str, Any] | None:
    compacted = {key: value for key, value in values.items() if value not in (None, (), [])}
    return compacted or None


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)


__all__ = ["PeerCache", "input_channel_from_peer", "input_peer_from_peer", "input_user_from_peer"]
