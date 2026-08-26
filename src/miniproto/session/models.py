"""Validated frozen session records and their durable mapping conversion.

The dataclasses prevent attribute reassignment and copy collection containers, but
their mappings are shallow copies: nested values such as ``metadata`` or peer
``raw`` dictionaries can still be mutable.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, cast

from miniproto.types import PeerKind

SESSION_RECORD_VERSION = 1


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp for model defaults."""
    return datetime.now(UTC)


def _coerce_datetime(value: datetime | str | None, *, default: datetime | None = None) -> datetime | None:
    """Preserve aware timestamps and assume UTC only for naive values.

    Args:
        value: Datetime or ISO-8601 string to coerce or ``None``.
        default: Value returned unchanged when ``value`` is ``None``.
    """
    if value is None:
        return default
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


@dataclass(slots=True, frozen=True)
class AuthKey:
    """Validated non-empty MTProto authorization key bound to a positive DC.

    Attributes:
        dc_id: Positive data-centre identifier that owns the key.
        key: Secret authorization-key bytes, hidden from ``repr``.
        key_id: Optional server-derived authorization-key fingerprint.
        created_at: Creation timestamp; aware input retains its original timezone and naive input assumes UTC.
        expires_at: Optional expiry timestamp with the same aware/naive handling.

    Raises:
        ValueError: If ``dc_id`` is not positive or ``key`` is empty.
    """

    dc_id: int
    key: bytes = field(repr=False)
    key_id: int | None = None
    created_at: datetime = field(default_factory=_utc_now)
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate identifiers and defensively copy secret bytes and timestamps."""
        if self.dc_id <= 0:
            raise ValueError("auth key dc_id must be positive")
        if not self.key:
            raise ValueError("auth key bytes must not be empty")
        object.__setattr__(self, "key", bytes(self.key))
        object.__setattr__(self, "created_at", _coerce_datetime(self.created_at, default=_utc_now()))
        object.__setattr__(self, "expires_at", _coerce_datetime(self.expires_at))


@dataclass(slots=True, frozen=True)
class DCOption:
    """One validated Telegram data-centre endpoint and optional transport secret.

    Attributes:
        id: Positive data-centre identifier.
        ip_address: Non-empty endpoint address.
        port: Endpoint TCP port from 1 through 65535.
        ipv6: Whether the address is IPv6.
        media_only: Whether this endpoint serves only media requests.
        cdn: Whether this endpoint belongs to Telegram's CDN trust domain.
        tcpo_only: Whether this endpoint is TCP-obfuscated-only.
        static: Whether Telegram marks this option static.
        secret: Optional copied transport secret, hidden from ``repr``.

    Raises:
        ValueError: If the ID, address or port is invalid.
    """

    id: int
    ip_address: str
    port: int
    ipv6: bool = False
    media_only: bool = False
    cdn: bool = False
    tcpo_only: bool = False
    static: bool = False
    secret: bytes | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Validate endpoint ranges and defensively copy an optional secret."""
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
    """Durable Telegram user identity with optional private contact metadata.

    ``phone`` is intentionally hidden from ``repr``. ``access_hash`` is absent
    when Telegram did not provide one.

    Attributes:
        id: Positive Telegram user identifier.
        access_hash: Optional access hash needed to address the user.
        is_bot: Whether Telegram identifies this user as a bot.
        username: Optional public username.
        phone: Optional private phone number, hidden from ``repr``.
        first_name: Optional profile first name.
        last_name: Optional profile last name.

    Raises:
        ValueError: If the user ID is not positive.
    """

    id: int
    access_hash: int | None = None
    is_bot: bool = False
    username: str | None = None
    phone: str | None = field(default=None, repr=False)
    first_name: str | None = None
    last_name: str | None = None

    def __post_init__(self) -> None:
        """Require a positive Telegram user identifier."""
        if self.id <= 0:
            raise ValueError("user identity id must be positive")


@dataclass(slots=True, frozen=True)
class UpdateState:
    """Monotonic Telegram update cursors and their latest server timestamp.

    All counters default to zero and ``date`` defaults to current UTC time.

    Attributes:
        pts: Global persistent timestamp cursor.
        qts: Secret-chat timestamp cursor.
        seq: Global update sequence cursor.
        date: Latest server timestamp; aware input retains its timezone and naive input assumes UTC.

    Raises:
        ValueError: If any counter is negative.
    """

    pts: int = 0
    qts: int = 0
    seq: int = 0
    date: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Reject negative counters and preserve aware timestamps while assuming UTC for naive input."""
        if self.pts < 0 or self.qts < 0 or self.seq < 0:
            raise ValueError("update state counters must not be negative")
        object.__setattr__(self, "date", _coerce_datetime(self.date, default=_utc_now()))


@dataclass(slots=True, frozen=True)
class PeerCacheEntry:
    """Durable peer lookup metadata with a shallow-copied optional raw-field mapping.

    ``raw`` is copied at its outer mapping level, so nested raw values remain
    mutable. ``phone`` is hidden from ``repr`` and optional access hashes remain
    absent for minimal Telegram peers.

    Attributes:
        id: Positive Telegram peer identifier.
        kind: Peer category used to construct input peers.
        access_hash: Optional access hash required for some peer operations.
        username: Optional public username.
        phone: Optional private phone number, hidden from ``repr``.
        updated_at: Last-known peer metadata timestamp; aware input retains its timezone.
        raw: Optional shallow-copied extra raw fields; nested values remain mutable.

    Raises:
        ValueError: If the peer ID is not positive.
    """

    id: int
    kind: PeerKind
    access_hash: int | None = None
    username: str | None = None
    phone: str | None = field(default=None, repr=False)
    updated_at: datetime = field(default_factory=_utc_now)
    raw: Mapping[str, Any] | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Require a positive ID and shallow-copy raw data from callers."""
        if self.id <= 0:
            raise ValueError("peer cache entry id must be positive")
        object.__setattr__(self, "updated_at", _coerce_datetime(self.updated_at, default=_utc_now()))
        if self.raw is not None:
            object.__setattr__(self, "raw", dict(self.raw))


@dataclass(slots=True, frozen=True)
class SessionRecord:
    """Complete versioned session state with frozen, shallow collection snapshots.

    Attributes:
        version: Storage schema version; only the current version is accepted.
        dc_id: Optional active data-centre identifier.
        auth_key: Optional active authorization key.
        dc_options: Immutable configured endpoint sequence.
        user: Optional authenticated account identity.
        update_state: Update cursors, defaulting to an empty state.
        peers: Immutable cached peer sequence.
        metadata: Shallow-copied extension mapping, hidden from ``repr``; nested values remain mutable.

    Default update state is empty, while every other optional domain remains
    absent or empty until the client obtains it.

    Raises:
        ValueError: If the version is unsupported or configured DC is invalid.
    """

    version: int = SESSION_RECORD_VERSION
    dc_id: int | None = None
    auth_key: AuthKey | None = None
    dc_options: tuple[DCOption, ...] = ()
    user: UserIdentity | None = None
    update_state: UpdateState = field(default_factory=UpdateState)
    peers: tuple[PeerCacheEntry, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        """Enforce the record version and shallow-copy collection-backed session domains."""
        if self.version != SESSION_RECORD_VERSION:
            raise ValueError(f"unsupported session record version: {self.version}")
        if self.dc_id is not None and self.dc_id <= 0:
            raise ValueError("session dc_id must be positive when set")
        object.__setattr__(self, "dc_options", tuple(self.dc_options))
        object.__setattr__(self, "peers", tuple(self.peers))
        object.__setattr__(self, "metadata", dict(self.metadata))


def session_record_to_mapping(record: SessionRecord) -> dict[str, Any]:
    """Serialize a typed record to the canonical storage-compatible mapping.

    Args:
        record: Validated immutable session state.

    Returns:
        A new mapping retaining bytes and datetimes for storage encoding.
    """
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
    """Construct a validated record from a decoded canonical mapping.

    Args:
        data: Canonical session mapping decoded from storage.

    Raises:
        KeyError: If required nested fields are missing.
        TypeError: If nested mappings or byte fields have invalid shapes.
        ValueError: If model validation or peer-kind conversion fails.
    """
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
    """Project an auth key into its storage mapping.

    Args:
        auth_key: Validated authorization key to serialize.
    """
    return {
        "dc_id": auth_key.dc_id,
        "key": auth_key.key,
        "key_id": auth_key.key_id,
        "created_at": auth_key.created_at,
        "expires_at": auth_key.expires_at,
    }


def _dc_option_to_mapping(option: DCOption) -> dict[str, Any]:
    """Project a DC endpoint into its storage mapping.

    Args:
        option: Validated Telegram data-center endpoint to serialize.
    """
    payload = {
        "id": option.id,
        "ip_address": option.ip_address,
        "port": option.port,
        "ipv6": option.ipv6,
        "media_only": option.media_only,
        "tcpo_only": option.tcpo_only,
        "static": option.static,
        "secret": option.secret,
    }
    if option.cdn:
        payload["cdn"] = True
    return payload


def _user_identity_to_mapping(user: UserIdentity) -> dict[str, Any]:
    """Project durable user identity fields into storage form.

    Args:
        user: User identity to serialize.
    """
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
    """Project update cursors and date into storage form.

    Args:
        state: Update cursor state to serialize.
    """
    return {"pts": state.pts, "qts": state.qts, "seq": state.seq, "date": state.date}


def _peer_cache_entry_to_mapping(peer: PeerCacheEntry) -> dict[str, Any]:
    """Project one peer entry while copying its optional raw mapping.

    Args:
        peer: Cached peer entry to serialize.
    """
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
    """Build an optional validated authorization key from decoded storage data.

    Args:
        data: Decoded authorization-key mapping or ``None``.
    """
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
    """Build one validated DC endpoint from decoded storage data.

    Args:
        data: Decoded data-center option mapping.
    """
    mapping = _require_mapping(data, "dc_option")
    return DCOption(
        id=int(mapping["id"]),
        ip_address=str(mapping["ip_address"]),
        port=int(mapping["port"]),
        ipv6=bool(mapping.get("ipv6", False)),
        media_only=bool(mapping.get("media_only", False)),
        cdn=bool(mapping.get("cdn", False)),
        tcpo_only=bool(mapping.get("tcpo_only", False)),
        static=bool(mapping.get("static", False)),
        secret=None if mapping.get("secret") is None else _require_bytes(mapping["secret"], "dc_option.secret"),
    )


def _user_identity_from_mapping(data: object) -> UserIdentity | None:
    """Build optional user identity from decoded storage data.

    Args:
        data: Decoded user mapping or ``None``.
    """
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
    """Build update state or its empty default from decoded storage data.

    Args:
        data: Decoded update-state mapping or ``None`` for a default state.
    """
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
    """Validate a serialized peer-kind spelling against public peer kinds.

    Args:
        value: Decoded peer-kind value to validate and normalize.
    """
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
    """Build one validated cached peer from decoded storage data.

    Args:
        data: Decoded cached-peer mapping.
    """
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
    """Copy optional metadata mappings, using an empty mapping for ``None``.

    Args:
        value: Optional decoded metadata mapping.
    """
    if value is None:
        return {}
    return dict(_require_mapping(value, "metadata"))


def _require_mapping(value: object, name: str) -> Mapping[str, Any]:
    """Require a mapping at a named serialized field.

    Args:
        value: Decoded field value to validate.
        name: Field path included in a type-validation error.
    """
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return cast("Mapping[str, Any]", value)


def _require_bytes(value: object, name: str) -> bytes:
    """Accept and copy supported mutable or immutable byte-like values.

    Args:
        value: Decoded byte-like field value.
        name: Field path included in a type-validation error.
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray | memoryview):
        return bytes(value)
    raise TypeError(f"{name} must be bytes")


def _optional_int(value: object) -> int | None:
    """Convert an optional serialized integer using Python's integer coercion.

    Args:
        value: Optional decoded scalar to convert.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str | bytes | bytearray):
        return int(value)
    return int(str(value))


def _optional_str(value: object) -> str | None:
    """Convert a present optional serialized value to string.

    Args:
        value: Optional decoded value to convert.
    """
    return None if value is None else str(value)
