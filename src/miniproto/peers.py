from __future__ import annotations

import inspect
from collections.abc import Awaitable, Iterable, Mapping
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol, cast

from miniproto.config import ClientConfig
from miniproto.errors import NotFound, RpcError, Unauthorized, classify_rpc_error
from miniproto.invoke import load_session_record
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, SessionRecord, UserIdentity
from miniproto.session.storage import SessionStorage
from miniproto.types import Peer, PeerKind, User

USERNAME_CACHE_TTL = timedelta(hours=24)


class PeerInvoker(Protocol):
    def __call__(self, raw_request: object) -> Awaitable[object] | object: ...


class PeerCache:
    def __init__(self, config: ClientConfig, storage: SessionStorage, invoker: PeerInvoker) -> None:
        self._config = config
        self._storage = storage
        self._invoke = invoker

    async def get_me(self, *, refresh: bool = False) -> User:
        record = await self._load_record()
        if record.user is not None and not refresh:
            return _user_from_identity(record.user)
        result = await self._invoke_raw(functions.UsersGetUsers(id=(types.InputUserSelf(),)))
        users = result if isinstance(result, tuple) else ()
        raw_user = next((item for item in users if isinstance(item, types.User)), None)
        if raw_user is None:
            if record.user is not None:
                return _user_from_identity(record.user)
            raise Unauthorized("users.getUsers(inputUserSelf) returned no self user")
        user = _user_from_raw_user(raw_user, force_self=True)
        await self._save_entries(
            (_entry_from_user(raw_user, force_self=True),), user=_identity_from_user(user)
        )
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
        record = await self._load_record()
        entry = _find_entry(record.peers, kind=peer.kind, id=peer.id)
        if entry is None or entry.access_hash is None:
            raise NotFound(f"{peer.kind} access hash is not cached")
        return _peer_from_entry(entry)

    async def _resolve_numeric_peer(self, value: int) -> Peer:
        record = await self._load_record()
        resolved = _resolve_numeric_peer_from_record(record, value)
        if resolved is not None:
            return resolved
        await self._seed_dialog_peers()
        record = await self._load_record()
        resolved = _resolve_numeric_peer_from_record(record, value)
        if resolved is not None:
            return resolved
        raise NotFound("numeric peer id is not cached")

    async def _resolve_phone(self, phone: str) -> Peer:
        normalized = _normalize_phone(phone)
        record = await self._load_record()
        for entry in record.peers:
            if _normalize_phone(entry.phone) == normalized:
                return _peer_from_entry(entry)
        if record.user is not None and _normalize_phone(record.user.phone) == normalized:
            return _user_from_identity(record.user).peer
        raise NotFound("phone peer is not cached")

    async def _resolve_username(self, username: str) -> Peer:
        record = await self._load_record()
        cached = _find_username_entry(record.peers, username)
        if cached is not None:
            return _peer_from_entry(cached)
        result = await self._invoke_raw(functions.ContactsResolveUsername(username=username))
        if not isinstance(result, types.ContactsResolvedPeer):
            raise RpcError(
                "contacts.resolveUsername returned an unexpected result",
                request="contacts.resolveUsername",
            )
        entries = tuple(_entries_from_raw(result))
        await self._save_entries(entries)
        resolved = _peer_from_raw_peer(result.peer, entries)
        if resolved is None:
            raise NotFound("resolved username did not include a usable peer")
        return resolved

    async def _seed_dialog_peers(self, *, limit: int = 100) -> None:
        result = await self._invoke_raw(
            functions.MessagesGetDialogs(
                exclude_pinned=True,
                offset_date=0,
                offset_id=0,
                offset_peer=types.InputPeerEmpty(),
                limit=limit,
                hash=0,
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

    async def _load_record(self) -> SessionRecord:
        return load_session_record(await self._storage.load(), self._config.dc_id)

    async def _save_entries(
        self, entries: Iterable[PeerCacheEntry], *, user: UserIdentity | None = None
    ) -> None:
        incoming = tuple(entries)
        record = await self._load_record()
        peers = _merge_entries(record.peers, incoming)
        identity = user or _identity_updated_from_entries(record.user, incoming)
        await self._storage.save(replace(record, peers=peers, user=identity))


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
        raw=_compact_raw(
            is_bot=user.bot,
            first_name=user.first_name,
            last_name=user.last_name,
            usernames=usernames,
        ),
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
    merged: dict[tuple[PeerKind, int], PeerCacheEntry] = {
        (entry.kind, entry.id): entry for entry in existing
    }
    for entry in incoming:
        if entry.kind == "self":
            merged.pop(("user", entry.id), None)
        current = merged.get((entry.kind, entry.id))
        merged[(entry.kind, entry.id)] = entry if current is None else _merge_entry(current, entry)
    return tuple(merged.values())


def _merge_entry(current: PeerCacheEntry, incoming: PeerCacheEntry) -> PeerCacheEntry:
    raw = dict(current.raw or {})
    raw.update(dict(incoming.raw or {}))
    return PeerCacheEntry(
        id=incoming.id,
        kind=incoming.kind,
        access_hash=incoming.access_hash
        if incoming.access_hash is not None
        else current.access_hash,
        username=incoming.username or current.username,
        phone=incoming.phone or current.phone,
        updated_at=incoming.updated_at,
        raw=raw or None,
    )


def _identity_updated_from_entries(
    current: UserIdentity | None, entries: Iterable[PeerCacheEntry]
) -> UserIdentity | None:
    if current is None:
        return None
    self_entry = next(
        (entry for entry in entries if entry.kind == "self" and entry.id == current.id), None
    )
    if self_entry is None:
        return current
    raw = dict(self_entry.raw or {})
    return UserIdentity(
        id=current.id,
        access_hash=self_entry.access_hash
        if self_entry.access_hash is not None
        else current.access_hash,
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
        entry = (
            _find_entry(record.peers, kind=preferred_kind, id=peer_id) if preferred_kind else None
        )
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
        return Peer(
            id=raw_peer.channel_id,
            kind="channel",
            access_hash=None if entry is None else entry.access_hash,
        )
    return None


def _find_entry(
    entries: Iterable[PeerCacheEntry], *, kind: PeerKind | None, id: int
) -> PeerCacheEntry | None:
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
