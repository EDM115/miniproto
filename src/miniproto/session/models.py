from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, cast

from miniproto.types import PeerKind

SESSION_RECORD_VERSION = 1


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _coerce_datetime(value: datetime | str | None, *, default: datetime | None = None) -> datetime | None:
    if value is None:
        return default
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


@dataclass(slots=True, frozen=True)
class AuthKey:
    dc_id: int
    key: bytes = field(repr=False)
    key_id: int | None = None
    created_at: datetime = field(default_factory=_utc_now)
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.dc_id <= 0:
            raise ValueError("auth key dc_id must be positive")
        if not self.key:
            raise ValueError("auth key bytes must not be empty")
        object.__setattr__(self, "key", bytes(self.key))
        object.__setattr__(self, "created_at", _coerce_datetime(self.created_at, default=_utc_now()))
        object.__setattr__(self, "expires_at", _coerce_datetime(self.expires_at))


@dataclass(slots=True, frozen=True)
class DCOption:
    id: int
    ip_address: str
    port: int
    ipv6: bool = False
    media_only: bool = False
    tcpo_only: bool = False
    static: bool = False
    secret: bytes | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("dc option id must be positive")
        if not self.ip_address:
            raise ValueError("dc option ip_address must not be empty")
        if not 0 < self.port < 65536:
            raise ValueError("dc option port must be between 1 and 65535")
        if self.secret is not None:
            object.__setattr__(self, "secret", bytes(self.secret))


@dataclass(slots=True, frozen=True)
class UserIdentity:
    id: int
    access_hash: int | None = None
    is_bot: bool = False
    username: str | None = None
    phone: str | None = field(default=None, repr=False)
    first_name: str | None = None
    last_name: str | None = None

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("user identity id must be positive")


@dataclass(slots=True, frozen=True)
class UpdateState:
    pts: int = 0
    qts: int = 0
    seq: int = 0
    date: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if self.pts < 0 or self.qts < 0 or self.seq < 0:
            raise ValueError("update state counters must not be negative")
        object.__setattr__(self, "date", _coerce_datetime(self.date, default=_utc_now()))


@dataclass(slots=True, frozen=True)
class PeerCacheEntry:
    id: int
    kind: PeerKind
    access_hash: int | None = None
    username: str | None = None
    phone: str | None = field(default=None, repr=False)
    updated_at: datetime = field(default_factory=_utc_now)
    raw: Mapping[str, Any] | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("peer cache entry id must be positive")
        object.__setattr__(self, "updated_at", _coerce_datetime(self.updated_at, default=_utc_now()))
        if self.raw is not None:
            object.__setattr__(self, "raw", dict(self.raw))


@dataclass(slots=True, frozen=True)
class SessionRecord:
    version: int = SESSION_RECORD_VERSION
    dc_id: int | None = None
    auth_key: AuthKey | None = None
    dc_options: tuple[DCOption, ...] = ()
    user: UserIdentity | None = None
    update_state: UpdateState = field(default_factory=UpdateState)
    peers: tuple[PeerCacheEntry, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        if self.version != SESSION_RECORD_VERSION:
            raise ValueError(f"unsupported session record version: {self.version}")
        if self.dc_id is not None and self.dc_id <= 0:
            raise ValueError("session dc_id must be positive when set")
        object.__setattr__(self, "dc_options", tuple(self.dc_options))
        object.__setattr__(self, "peers", tuple(self.peers))
        object.__setattr__(self, "metadata", dict(self.metadata))


def session_record_to_mapping(record: SessionRecord) -> dict[str, Any]:
    return {
        "version": record.version,
        "dc_id": record.dc_id,
        "auth_key": _auth_key_to_mapping(record.auth_key) if record.auth_key is not None else None,
        "dc_options": [_dc_option_to_mapping(option) for option in record.dc_options],
        "user": _user_identity_to_mapping(record.user) if record.user is not None else None,
        "update_state": _update_state_to_mapping(record.update_state),
        "peers": [_peer_cache_entry_to_mapping(peer) for peer in record.peers],
        "metadata": dict(record.metadata),
    }


def session_record_from_mapping(data: Mapping[str, Any]) -> SessionRecord:
    return SessionRecord(
        version=int(data.get("version", SESSION_RECORD_VERSION)),
        dc_id=_optional_int(data.get("dc_id")),
        auth_key=_auth_key_from_mapping(data.get("auth_key")),
        dc_options=tuple(_dc_option_from_mapping(option) for option in data.get("dc_options", ())),
        user=_user_identity_from_mapping(data.get("user")),
        update_state=_update_state_from_mapping(data.get("update_state")),
        peers=tuple(_peer_cache_entry_from_mapping(peer) for peer in data.get("peers", ())),
        metadata=_mapping_or_empty(data.get("metadata")),
    )


def _auth_key_to_mapping(auth_key: AuthKey) -> dict[str, Any]:
    return {
        "dc_id": auth_key.dc_id,
        "key": auth_key.key,
        "key_id": auth_key.key_id,
        "created_at": auth_key.created_at,
        "expires_at": auth_key.expires_at,
    }


def _dc_option_to_mapping(option: DCOption) -> dict[str, Any]:
    return {
        "id": option.id,
        "ip_address": option.ip_address,
        "port": option.port,
        "ipv6": option.ipv6,
        "media_only": option.media_only,
        "tcpo_only": option.tcpo_only,
        "static": option.static,
        "secret": option.secret,
    }


def _user_identity_to_mapping(user: UserIdentity) -> dict[str, Any]:
    return {
        "id": user.id,
        "access_hash": user.access_hash,
        "is_bot": user.is_bot,
        "username": user.username,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


def _update_state_to_mapping(state: UpdateState) -> dict[str, Any]:
    return {"pts": state.pts, "qts": state.qts, "seq": state.seq, "date": state.date}


def _peer_cache_entry_to_mapping(peer: PeerCacheEntry) -> dict[str, Any]:
    return {
        "id": peer.id,
        "kind": peer.kind,
        "access_hash": peer.access_hash,
        "username": peer.username,
        "phone": peer.phone,
        "updated_at": peer.updated_at,
        "raw": dict(peer.raw) if peer.raw is not None else None,
    }


def _auth_key_from_mapping(data: object) -> AuthKey | None:
    if data is None:
        return None
    mapping = _require_mapping(data, "auth_key")
    return AuthKey(
        dc_id=int(mapping["dc_id"]),
        key=_require_bytes(mapping["key"], "auth_key.key"),
        key_id=_optional_int(mapping.get("key_id")),
        created_at=_coerce_datetime(mapping.get("created_at"), default=_utc_now()) or _utc_now(),
        expires_at=_coerce_datetime(mapping.get("expires_at")),
    )


def _dc_option_from_mapping(data: object) -> DCOption:
    mapping = _require_mapping(data, "dc_option")
    return DCOption(
        id=int(mapping["id"]),
        ip_address=str(mapping["ip_address"]),
        port=int(mapping["port"]),
        ipv6=bool(mapping.get("ipv6", False)),
        media_only=bool(mapping.get("media_only", False)),
        tcpo_only=bool(mapping.get("tcpo_only", False)),
        static=bool(mapping.get("static", False)),
        secret=None if mapping.get("secret") is None else _require_bytes(mapping["secret"], "dc_option.secret"),
    )


def _user_identity_from_mapping(data: object) -> UserIdentity | None:
    if data is None:
        return None
    mapping = _require_mapping(data, "user")
    return UserIdentity(
        id=int(mapping["id"]),
        access_hash=_optional_int(mapping.get("access_hash")),
        is_bot=bool(mapping.get("is_bot", False)),
        username=_optional_str(mapping.get("username")),
        phone=_optional_str(mapping.get("phone")),
        first_name=_optional_str(mapping.get("first_name")),
        last_name=_optional_str(mapping.get("last_name")),
    )


def _update_state_from_mapping(data: object) -> UpdateState:
    if data is None:
        return UpdateState()
    mapping = _require_mapping(data, "update_state")
    return UpdateState(
        pts=int(mapping.get("pts", 0)),
        qts=int(mapping.get("qts", 0)),
        seq=int(mapping.get("seq", 0)),
        date=_coerce_datetime(mapping.get("date"), default=_utc_now()) or _utc_now(),
    )


def _peer_kind(value: object) -> PeerKind:
    match str(value):
        case "user":
            return "user"
        case "chat":
            return "chat"
        case "channel":
            return "channel"
        case "self":
            return "self"
        case other:
            raise ValueError(f"unsupported peer kind: {other}")


def _peer_cache_entry_from_mapping(data: object) -> PeerCacheEntry:
    mapping = _require_mapping(data, "peer")
    return PeerCacheEntry(
        id=int(mapping["id"]),
        kind=_peer_kind(mapping["kind"]),
        access_hash=_optional_int(mapping.get("access_hash")),
        username=_optional_str(mapping.get("username")),
        phone=_optional_str(mapping.get("phone")),
        updated_at=_coerce_datetime(mapping.get("updated_at"), default=_utc_now()) or _utc_now(),
        raw=None if mapping.get("raw") is None else _require_mapping(mapping["raw"], "peer.raw"),
    )


def _mapping_or_empty(value: object) -> dict[str, Any]:
    if value is None:
        return {}
    return dict(_require_mapping(value, "metadata"))


def _require_mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return cast("Mapping[str, Any]", value)


def _require_bytes(value: object, name: str) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray | memoryview):
        return bytes(value)
    raise TypeError(f"{name} must be bytes")


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str | bytes | bytearray):
        return int(value)
    return int(str(value))


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)
