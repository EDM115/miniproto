"""Copy-isolated in-memory and authenticated encrypted SQLite session storage."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import inspect
import json
import logging
import os
import re
import secrets
import sqlite3
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import fields, is_dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol, cast, runtime_checkable

from miniproto.errors import SessionEnvelopeError, SessionStorageError
from miniproto.observability import emit_event, get_logger, record_metric
from miniproto.session.models import SessionRecord, session_record_to_mapping

type SessionPayload = Mapping[str, Any] | SessionRecord

_SERIALIZATION_VERSION = 1
_ENVELOPE_VERSION = 1
_DEFAULT_RECORD_NAME = "default"
_JSON_TYPE_KEY = "__miniproto_type__"
_KDF_SALT = b"miniproto-session-storage-v1"
_KDF_ITERATIONS = 200_000
_NONCE_SIZE = 32
_MAC_CONTEXT = b"miniproto-session-envelope-v1\0"
_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS session_records (
    name TEXT PRIMARY KEY,
    envelope BLOB NOT NULL,
    updated_at TEXT NOT NULL
)
"""
_DOMAIN_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS session_domains (
    domain TEXT PRIMARY KEY,
    envelope BLOB NOT NULL,
    updated_at TEXT NOT NULL
)
"""
_KNOWN_SESSION_DOMAINS = ("auth", "peers", "update_state", "metadata", "payload")
_SESSION_RECORD_KEYS = frozenset(
    {"version", "dc_id", "auth_key", "dc_options", "user", "update_state", "peers", "metadata"}
)
_LOGGER = get_logger("session.storage")
_SIBLING_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


@runtime_checkable
class SessionStorage(Protocol):
    """Async session persistence contract with atomic synchronous transforms."""

    async def load(self) -> Mapping[str, Any] | None:
        """Load a detached snapshot, or ``None`` when no session is stored."""
        ...

    async def save(self, data: SessionPayload) -> None:
        """Replace stored state using a detached copy of ``data``.

        Args:
            data: Session mapping or typed record to persist.
        """
        ...

    async def mutate(
        self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]
    ) -> Mapping[str, Any] | None:
        """Atomically apply a synchronous transform to an isolated current snapshot.

        Args:
            transform: Synchronous callback receiving detached stored data and returning replacement data or ``None``.
        """
        ...

    def domain_revisions(self) -> Mapping[str, int]:
        """Return copy-safe monotonically increasing revisions per logical domain."""
        ...

    async def clear(self) -> None:
        """Delete the stored session and advance revisions for removed domains."""
        ...

    async def close(self) -> None:
        """Close this storage instance to later load, save, mutate, and clear operations.

        ``sibling`` and ``domain_revisions`` remain available after closure.
        """
        ...


class InMemorySessionStorage:
    """Thread-safe in-process storage that snapshots all values by serialization."""

    def __init__(self, initial: SessionPayload | None = None) -> None:
        """Initialize optional state and independent per-domain revision counters.

        Args:
            initial: Optional mapping or typed record copied into initial storage state.
        """
        self._lock = threading.RLock()
        self._closed = False
        self._revisions = _new_domain_revisions()
        self._data: dict[str, Any] | None = _copy_session_data(initial) if initial is not None else None
        self._domains = _canonical_session_domains(initial)
        self._siblings: dict[str, InMemorySessionStorage] = {}

    def sibling(self, name: str) -> InMemorySessionStorage:
        """Return a stable independent named in-memory sibling storage.

        Raises:
            ValueError: If the portable sibling name contains unsafe characters.

        Args:
            name: Portable sibling identifier used as the stable lookup key.
        """
        _validate_sibling_name(name)
        with self._lock:
            storage = self._siblings.get(name)
            if storage is None:
                storage = InMemorySessionStorage()
                self._siblings[name] = storage
            return storage

    async def load(self) -> Mapping[str, Any] | None:
        """Return a detached current snapshot while holding the storage lock."""
        started = time.perf_counter()
        with self._lock:
            self._ensure_open()
            result = _copy_session_data(self._data) if self._data is not None else None
        _emit_storage_event("session.load", started, outcome="success", backend="memory", found=result is not None)
        return result

    async def save(self, data: SessionPayload) -> None:
        """Atomically replace state and advance only changed domain revisions.

        Args:
            data: Session mapping or typed record to deep-copy and persist.
        """
        started = time.perf_counter()
        with self._lock:
            self._ensure_open()
            new_data = _copy_session_data(data)
            new_domains = _canonical_session_domains(data)
            changed = _changed_domain_plaintexts(self._domains, new_domains)
            self._data = new_data
            self._domains = new_domains
            _advance_domain_revisions(self._revisions, changed)
        _emit_storage_event("session.save", started, outcome="success", backend="memory")

    async def mutate(
        self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]
    ) -> Mapping[str, Any] | None:
        """Run a synchronous transform atomically against an isolated snapshot.

        Awaitable transforms are rejected so locks are never held across an await.

        Args:
            transform: Synchronous callback receiving a detached current snapshot.
        """
        started = time.perf_counter()
        with self._lock:
            self._ensure_open()
            current = _copy_session_data(self._data) if self._data is not None else None
            transformed = _apply_sync_transform(transform, current)
            new_data = None if transformed is None else _copy_session_data(transformed)
            new_domains = _canonical_session_domains(transformed)
            changed = _changed_domain_plaintexts(self._domains, new_domains)
            self._data = new_data
            self._domains = new_domains
            _advance_domain_revisions(self._revisions, changed)
            result = _copy_session_data(new_data) if new_data is not None else None
        _emit_storage_event("session.mutate", started, outcome="success", backend="memory")
        return result

    def domain_revisions(self) -> Mapping[str, int]:
        """Return a detached revision mapping safe to inspect without locking callers."""
        with self._lock:
            return dict(self._revisions)

    async def clear(self) -> None:
        """Discard all state and advance revisions for every previously stored domain."""
        started = time.perf_counter()
        with self._lock:
            self._ensure_open()
            changed = set(self._domains)
            self._data = None
            self._domains = {}
            _advance_domain_revisions(self._revisions, changed)
        _emit_storage_event("session.clear", started, outcome="success", backend="memory")

    async def close(self) -> None:
        """Close load, save, mutate, and clear; sibling lookup and revisions remain available."""
        with self._lock:
            self._closed = True

    def _ensure_open(self) -> None:
        """Raise when a lifecycle operation targets already closed storage."""
        if self._closed:
            raise SessionStorageError("session storage is closed")


class EncryptedSQLiteSessionStorage:
    """Thread-safe SQLite persistence with per-domain authenticated encryption.

    Encryption and MAC keys derive from supplied key material. Reads and writes
    run off the event loop, while SQLite ``BEGIN IMMEDIATE`` serializes mutations.
    Legacy single-record payloads migrate to independently encrypted domains on
    the next replacement or mutation.
    """

    def __init__(self, path: str | os.PathLike[str], key: bytes | str | None = None) -> None:
        """Open a lazy encrypted database using explicit or environment key material.

        Args:
            path: SQLite database path created lazily on first write.
            key: Secret bytes/text, or ``None`` to read ``MINIPROTO_SESSION_KEY``.

        Raises:
            ValueError: If no key is supplied or its material is under 16 bytes.
        """
        resolved_key = key if key is not None else os.environ.get("MINIPROTO_SESSION_KEY")
        if not resolved_key:
            raise ValueError("EncryptedSQLiteSessionStorage requires a key or MINIPROTO_SESSION_KEY")
        key_material = resolved_key.encode() if isinstance(resolved_key, str) else bytes(resolved_key)
        if len(key_material) < 16:
            raise ValueError("EncryptedSQLiteSessionStorage key must be at least 16 bytes")
        self.path = Path(path)
        self._encryption_key, self._mac_key = _derive_keys(key_material)
        self._lock = threading.RLock()
        self._closed = False
        self._revisions = _new_domain_revisions()

    def sibling(self, name: str) -> EncryptedSQLiteSessionStorage:
        """Create an independent sibling database that reuses derived secret keys.

        Raises:
            ValueError: If ``name`` contains unsafe path characters.

        Args:
            name: Portable suffix used to construct the sibling database filename.
        """
        _validate_sibling_name(name)
        suffix = self.path.suffix
        path = self.path.with_name(f"{self.path.stem}-{name}{suffix}")
        return self._from_derived_keys(path, self._encryption_key, self._mac_key)

    @classmethod
    def _from_derived_keys(cls, path: Path, encryption_key: bytes, mac_key: bytes) -> EncryptedSQLiteSessionStorage:
        """Construct a sibling directly from already-derived secret subkeys.

        Args:
            path: Sibling SQLite database path.
            encryption_key: Derived stream-encryption key reused by the sibling.
            mac_key: Derived message-authentication key reused by the sibling.
        """
        storage = cls.__new__(cls)
        storage.path = path
        storage._encryption_key = encryption_key
        storage._mac_key = mac_key
        storage._lock = threading.RLock()
        storage._closed = False
        storage._revisions = _new_domain_revisions()
        return storage

    async def load(self) -> Mapping[str, Any] | None:
        """Load and authenticate a detached session snapshot on a worker thread.

        Raises:
            SessionEnvelopeError: If encrypted content cannot be authenticated or decoded.
            SessionStorageError: If SQLite loading fails or storage is closed.
        """
        started = time.perf_counter()
        try:
            result = await asyncio.to_thread(self._load_sync)
        except BaseException as exc:
            _emit_storage_event(
                "session.load", started, outcome="error", backend="sqlite", error_type=type(exc).__name__
            )
            raise
        _emit_storage_event("session.load", started, outcome="success", backend="sqlite", found=result is not None)
        return result

    async def save(self, data: SessionPayload) -> None:
        """Atomically replace changed encrypted domains on a worker thread.

        Args:
            data: Session mapping or typed record to serialize and protect.
        """
        started = time.perf_counter()
        try:
            await asyncio.to_thread(self._save_sync, data)
        except BaseException as exc:
            _emit_storage_event(
                "session.save", started, outcome="error", backend="sqlite", error_type=type(exc).__name__
            )
            raise
        _emit_storage_event("session.save", started, outcome="success", backend="sqlite")

    async def mutate(
        self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]
    ) -> Mapping[str, Any] | None:
        """Atomically transform detached state under SQLite's write transaction.

        The transform must be synchronous; it executes while the backend lock and
        ``BEGIN IMMEDIATE`` transaction ensure no lost update.

        Args:
            transform: Synchronous callback receiving a detached current snapshot.
        """
        started = time.perf_counter()
        try:
            result = await asyncio.to_thread(self._mutate_sync, transform)
        except BaseException as exc:
            _emit_storage_event(
                "session.mutate", started, outcome="error", backend="sqlite", error_type=type(exc).__name__
            )
            raise
        _emit_storage_event("session.mutate", started, outcome="success", backend="sqlite")
        return result

    def domain_revisions(self) -> Mapping[str, int]:
        """Return local copy-safe revisions advanced after successful writes."""
        with self._lock:
            return dict(self._revisions)

    async def clear(self) -> None:
        """Delete both legacy and domain rows transactionally on a worker thread."""
        started = time.perf_counter()
        try:
            await asyncio.to_thread(self._clear_sync)
        except BaseException as exc:
            _emit_storage_event(
                "session.clear", started, outcome="error", backend="sqlite", error_type=type(exc).__name__
            )
            raise
        _emit_storage_event("session.clear", started, outcome="success", backend="sqlite")

    async def close(self) -> None:
        """Close load, save, mutate, and clear after queued worker work reaches the lock.

        ``sibling`` and ``domain_revisions`` remain usable after closure.
        """
        await asyncio.to_thread(self._close_sync)

    def _load_sync(self) -> Mapping[str, Any] | None:
        """Load and decrypt state while holding the backend lock."""
        with self._lock:
            self._ensure_open()
            if not self.path.exists():
                return None
            try:
                with self._connect() as connection:
                    _ensure_schema(connection)
                    data, _domains, _legacy_present = self._load_current(connection)
            except sqlite3.Error as exc:
                raise SessionStorageError("failed to load session database") from exc
            return _copy_session_data(data) if data is not None else None

    def _save_sync(self, data: SessionPayload) -> None:
        """Copy supplied data and write only its changed canonical domains.

        Args:
            data: Session mapping or typed record to serialize and replace.
        """
        with self._lock:
            self._ensure_open()
            new_data = _copy_session_data(data)
            new_domains = _canonical_session_domains(data)
            self._write_replacement(new_data, new_domains, operation="save")

    def _mutate_sync(
        self, transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]
    ) -> Mapping[str, Any] | None:
        """Execute a synchronous transform inside one immediate SQLite transaction.

        Args:
            transform: Synchronous callback receiving detached current session data.
        """
        with self._lock:
            self._ensure_open()
            self.path.parent.mkdir(parents=True, exist_ok=True)
            connection = self._connect()
            try:
                _ensure_schema(connection)
                connection.execute("BEGIN IMMEDIATE")
                current, old_domains, legacy_present = self._load_current(connection)
                isolated = _copy_session_data(current) if current is not None else None
                transformed = _apply_sync_transform(transform, isolated)
                new_data = _copy_session_data(transformed) if transformed is not None else None
                new_domains = _canonical_session_domains(transformed)
                changed = _changed_domain_plaintexts(old_domains, new_domains)
                writes = set(new_domains) if legacy_present else changed
                self._apply_domain_changes(connection, new_domains, writes)
                connection.commit()
            except sqlite3.Error as exc:
                connection.rollback()
                raise SessionStorageError("failed to mutate session database") from exc
            except BaseException:
                connection.rollback()
                raise
            finally:
                connection.close()
            _advance_domain_revisions(self._revisions, changed)
            return _copy_session_data(new_data) if new_data is not None else None

    def _write_replacement(
        self, new_data: Mapping[str, Any] | None, new_domains: Mapping[str, bytes], *, operation: str
    ) -> None:
        """Replace domain rows transactionally and advance changed-domain revisions.

        Args:
            new_data: Replacement session data retained only for call-shape symmetry.
            new_domains: Serialized canonical plaintexts keyed by logical domain.
            operation: Operation name included in storage failure messages.
        """
        del new_data
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = self._connect()
        try:
            _ensure_schema(connection)
            connection.execute("BEGIN IMMEDIATE")
            _current, old_domains, legacy_present = self._load_current(connection)
            changed = _changed_domain_plaintexts(old_domains, new_domains)
            writes = set(new_domains) if legacy_present else changed
            self._apply_domain_changes(connection, new_domains, writes)
            connection.commit()
        except sqlite3.Error as exc:
            connection.rollback()
            raise SessionStorageError(f"failed to {operation} session database") from exc
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()
        _advance_domain_revisions(self._revisions, changed)

    def _load_current(self, connection: sqlite3.Connection) -> tuple[dict[str, Any] | None, dict[str, bytes], bool]:
        """Load domain rows or legacy record and identify whether migration is needed.

        Args:
            connection: Open SQLite connection used for the read.
        """
        domain_rows = connection.execute("SELECT domain, envelope FROM session_domains ORDER BY domain").fetchall()
        if domain_rows:
            merged: dict[str, Any] = {}
            domains: dict[str, bytes] = {}
            for domain, envelope in domain_rows:
                payload = self._decrypt(bytes(envelope))
                merged.update(payload)
                domains[str(domain)] = serialize_session_data(payload)
            return merged, domains, False
        row = connection.execute(
            "SELECT envelope FROM session_records WHERE name = ?", (_DEFAULT_RECORD_NAME,)
        ).fetchone()
        if row is None:
            return None, {}, False
        payload = dict(self._decrypt(bytes(row[0])))
        return payload, _canonical_loaded_domains(payload), True

    def _apply_domain_changes(
        self, connection: sqlite3.Connection, new_domains: Mapping[str, bytes], changed: set[str]
    ) -> None:
        """Apply ordered encrypted domain upserts/deletes and remove legacy storage.

        Args:
            connection: Open SQLite transaction connection.
            new_domains: Serialized plaintext payloads keyed by logical domain.
            changed: Domains to upsert or delete in deterministic order.
        """
        connection.execute("DELETE FROM session_records WHERE name = ?", (_DEFAULT_RECORD_NAME,))
        now = datetime.now(UTC).isoformat()
        for domain in _ordered_session_domains(changed):
            plaintext = new_domains.get(domain)
            if plaintext is None:
                connection.execute("DELETE FROM session_domains WHERE domain = ?", (domain,))
                continue
            envelope = self._encrypt(plaintext)
            connection.execute(
                """
                INSERT INTO session_domains (domain, envelope, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(domain) DO UPDATE SET envelope = excluded.envelope, updated_at = excluded.updated_at
                """,
                (domain, envelope, now),
            )

    def _clear_sync(self) -> None:
        """Delete all stored rows under an immediate transaction."""
        with self._lock:
            self._ensure_open()
            if not self.path.exists():
                return
            connection = self._connect()
            try:
                _ensure_schema(connection)
                connection.execute("BEGIN IMMEDIATE")
                _current, old_domains, _legacy_present = self._load_current(connection)
                connection.execute("DELETE FROM session_records WHERE name = ?", (_DEFAULT_RECORD_NAME,))
                connection.execute("DELETE FROM session_domains")
                connection.commit()
            except sqlite3.Error as exc:
                connection.rollback()
                raise SessionStorageError("failed to clear session database") from exc
            finally:
                connection.close()
            _advance_domain_revisions(self._revisions, set(old_domains))

    def _close_sync(self) -> None:
        """Mark this backend closed while holding its lifecycle lock."""
        with self._lock:
            self._closed = True

    def _ensure_open(self) -> None:
        """Raise when a caller uses encrypted storage after closure."""
        if self._closed:
            raise SessionStorageError("session storage is closed")

    def _connect(self) -> sqlite3.Connection:
        """Open a SQLite connection with foreign-key enforcement enabled."""
        connection = sqlite3.connect(self.path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _encrypt(self, plaintext: bytes) -> bytes:
        """Encrypt and authenticate one domain plaintext in a versioned JSON envelope.

        Args:
            plaintext: Serialized domain bytes to protect with fresh nonce and MAC.
        """
        nonce = secrets.token_bytes(_NONCE_SIZE)
        ciphertext = _xor_bytes(plaintext, _keystream(self._encryption_key, nonce, len(plaintext)))
        tag = hmac.new(self._mac_key, _mac_input(nonce, ciphertext), hashlib.sha256).digest()
        envelope = {
            "version": _ENVELOPE_VERSION,
            "cipher": "hmac-sha256-ctr",
            "mac": "hmac-sha256",
            "kdf": "pbkdf2-hmac-sha256",
            "nonce": _b64encode(nonce),
            "payload": _b64encode(ciphertext),
            "tag": _b64encode(tag),
        }
        return json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode()

    def _decrypt(self, envelope_bytes: bytes) -> Mapping[str, Any]:
        """Authenticate, decrypt, and deserialize one versioned domain envelope.

        Args:
            envelope_bytes: Versioned JSON envelope bytes read from SQLite.
        """
        envelope = _decode_envelope(envelope_bytes)
        nonce = _b64decode(str(envelope["nonce"]), "nonce")
        ciphertext = _b64decode(str(envelope["payload"]), "payload")
        tag = _b64decode(str(envelope["tag"]), "tag")
        expected_tag = hmac.new(self._mac_key, _mac_input(nonce, ciphertext), hashlib.sha256).digest()
        if not hmac.compare_digest(tag, expected_tag):
            raise SessionEnvelopeError("session envelope authentication failed")
        plaintext = _xor_bytes(ciphertext, _keystream(self._encryption_key, nonce, len(ciphertext)))
        return deserialize_session_data(plaintext)


def _validate_sibling_name(name: str) -> None:
    """Allow portable sibling names only, preventing path traversal or separators.

    Args:
        name: Candidate sibling identifier to validate.
    """
    if _SIBLING_NAME_RE.fullmatch(name) is None:
        raise ValueError("session sibling name must contain only letters, numbers, '.', '_', or '-'")


def serialize_session_data(data: SessionPayload) -> bytes:
    """Encode a mapping or record into versioned canonical JSON bytes.

    Args:
        data: Mapping or typed session record to encode.

    Raises:
        TypeError: If the payload or any nested value is not serializable.
    """
    document = {
        "storage_version": _SERIALIZATION_VERSION,
        "payload": _encode_json_value(_normalize_session_payload(data)),
    }
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode()


def deserialize_session_data(payload: bytes) -> dict[str, Any]:
    """Decode versioned canonical session JSON into a new plain mapping.

    Args:
        payload: Versioned canonical JSON bytes.

    Raises:
        SessionEnvelopeError: If encoding, version, or top-level shape is invalid.
    """
    try:
        document = json.loads(payload.decode())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SessionEnvelopeError("session payload is not valid JSON") from exc
    if document.get("storage_version") != _SERIALIZATION_VERSION:
        raise SessionEnvelopeError("unsupported session payload version")
    decoded = _decode_json_value(document.get("payload"))
    if not isinstance(decoded, Mapping):
        raise SessionEnvelopeError("session payload must decode to a mapping")
    return dict(cast("Mapping[str, Any]", decoded))


def _copy_session_data(data: SessionPayload) -> dict[str, Any]:
    """Create a deep serialization boundary copy of session payload data.

    Args:
        data: Mapping or typed record to copy through canonical serialization.
    """
    return deserialize_session_data(serialize_session_data(data))


def _normalize_session_payload(data: SessionPayload) -> Mapping[str, Any]:
    """Accept only typed records or mappings as session payloads.

    Args:
        data: Candidate session payload to normalize.
    """
    if isinstance(data, SessionRecord):
        return session_record_to_mapping(data)
    if isinstance(data, Mapping):
        return cast("Mapping[str, Any]", data)
    raise TypeError("session data must be a mapping or SessionRecord")


def _split_session_domains(data: SessionPayload) -> dict[str, Mapping[str, Any]]:
    """Separate typed records into independently encrypted logical domains.

    Args:
        data: Typed record or opaque session mapping to partition.
    """
    if not isinstance(data, SessionRecord):
        return {"payload": _normalize_session_payload(data)}
    payload = dict(session_record_to_mapping(data))
    return _split_session_record_mapping_domains(payload)


def _split_session_record_mapping_domains(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """Split canonical record fields into auth, peers, update, and metadata domains.

    Args:
        payload: Canonical session-record mapping to partition.
    """
    return {
        "auth": {
            "version": payload.get("version"),
            "dc_id": payload.get("dc_id"),
            "auth_key": payload.get("auth_key"),
            "dc_options": payload.get("dc_options", ()),
            "user": payload.get("user"),
        },
        "peers": {"peers": payload.get("peers", ())},
        "update_state": {"update_state": payload.get("update_state")},
        "metadata": {"metadata": payload.get("metadata", {})},
    }


def _canonical_loaded_domains(data: Mapping[str, Any]) -> dict[str, bytes]:
    """Derive canonical domain plaintexts from legacy or record-shaped loaded data.

    Args:
        data: Decoded session mapping from legacy or domain storage.
    """
    if set(data) == _SESSION_RECORD_KEYS:
        return {
            domain: serialize_session_data(payload)
            for domain, payload in _split_session_record_mapping_domains(data).items()
        }
    return {"payload": serialize_session_data(data)}


def _new_domain_revisions() -> dict[str, int]:
    """Initialize every known domain revision at zero."""
    return dict.fromkeys(_KNOWN_SESSION_DOMAINS, 0)


def _canonical_session_domains(data: SessionPayload | None) -> dict[str, bytes]:
    """Serialize every logical domain, treating ``None`` as no stored domains.

    Args:
        data: Optional session mapping or typed record to serialize by domain.
    """
    if data is None:
        return {}
    return {domain: serialize_session_data(payload) for domain, payload in _split_session_domains(data).items()}


def _changed_domain_plaintexts(old_domains: Mapping[str, bytes], new_domains: Mapping[str, bytes]) -> set[str]:
    """Return domains whose serialized plaintext changed, appeared, or disappeared.

    Args:
        old_domains: Previous domain plaintexts keyed by domain.
        new_domains: Replacement domain plaintexts keyed by domain.
    """
    return {
        domain
        for domain in old_domains.keys() | new_domains.keys()
        if old_domains.get(domain) != new_domains.get(domain)
    }


def _advance_domain_revisions(revisions: dict[str, int], changed: set[str]) -> None:
    """Increment local revisions only for changed logical domains.

    Args:
        revisions: Mutable local revision counters to advance.
        changed: Logical domains whose serialized plaintext changed.
    """
    for domain in changed:
        revisions[domain] += 1


def _ordered_session_domains(domains: set[str]) -> tuple[str, ...]:
    """Order known domains deterministically before unknown extension domains.

    Args:
        domains: Domain names to order for transactional persistence.
    """
    known = tuple(domain for domain in _KNOWN_SESSION_DOMAINS if domain in domains)
    return (*known, *sorted(domains - set(_KNOWN_SESSION_DOMAINS)))


def _apply_sync_transform(
    transform: Callable[[Mapping[str, Any] | None], SessionPayload | None], payload: Mapping[str, Any] | None
) -> SessionPayload | None:
    """Run a transform and reject awaitables before storage locks span an await.

    Args:
        transform: Candidate synchronous mutation callback.
        payload: Detached current snapshot supplied to the callback.
    """
    transformed = transform(payload)
    if inspect.isawaitable(transformed):
        close = getattr(transformed, "close", None)
        if callable(close):
            close()
        raise TypeError("session mutation transform must be synchronous")
    return transformed


def _encode_json_value(value: object) -> object:
    """Recursively encode supported session values with bytes/date type markers.

    Args:
        value: Supported scalar, collection, datetime, dataclass, or session model value.
    """
    if isinstance(value, bytes | bytearray | memoryview):
        return {_JSON_TYPE_KEY: "bytes", "value": _b64encode(bytes(value))}
    if isinstance(value, datetime):
        normalized = value if value.tzinfo is not None else value.replace(tzinfo=UTC)
        return {_JSON_TYPE_KEY: "datetime", "value": normalized.isoformat()}
    if isinstance(value, SessionRecord):
        return _encode_json_value(session_record_to_mapping(value))
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: _encode_json_value(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): _encode_json_value(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_encode_json_value(item) for item in value]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    raise TypeError(f"session value of type {type(value).__name__} is not serializable")


def _decode_json_value(value: object) -> object:
    """Recursively restore JSON values and registered bytes/date type markers.

    Args:
        value: Decoded JSON scalar, list, or mapping to restore recursively.
    """
    if isinstance(value, list):
        return [_decode_json_value(item) for item in value]
    if isinstance(value, Mapping):
        marker = value.get(_JSON_TYPE_KEY)
        if marker == "bytes":
            return _b64decode(str(value.get("value")), "bytes")
        if marker == "datetime":
            return _parse_datetime(str(value.get("value")))
        return {str(key): _decode_json_value(item) for key, item in value.items()}
    return value


def _decode_envelope(envelope_bytes: bytes) -> Mapping[str, Any]:
    """Validate versioned envelope structure and supported crypto algorithm labels.

    Args:
        envelope_bytes: Raw JSON envelope bytes read from SQLite.
    """
    try:
        envelope = json.loads(envelope_bytes.decode())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SessionEnvelopeError("session envelope is not valid JSON") from exc
    if not isinstance(envelope, Mapping):
        raise SessionEnvelopeError("session envelope must be a mapping")
    if envelope.get("version") != _ENVELOPE_VERSION:
        raise SessionEnvelopeError("unsupported session envelope version")
    if envelope.get("cipher") != "hmac-sha256-ctr" or envelope.get("mac") != "hmac-sha256":
        raise SessionEnvelopeError("unsupported session envelope algorithms")
    for field_name in ("nonce", "payload", "tag"):
        if field_name not in envelope:
            raise SessionEnvelopeError(f"session envelope missing {field_name}")
    return envelope


def _ensure_schema(connection: sqlite3.Connection) -> None:
    """Create legacy and domain session tables if absent.

    Args:
        connection: Open SQLite connection whose schema is initialized.
    """
    connection.execute(_TABLE_SCHEMA)
    connection.execute(_DOMAIN_TABLE_SCHEMA)


def _derive_keys(key_material: bytes) -> tuple[bytes, bytes]:
    """Derive separate fixed-size encryption and MAC keys with PBKDF2-HMAC-SHA256.

    Args:
        key_material: Validated secret session key bytes.
    """
    derived = hashlib.pbkdf2_hmac("sha256", key_material, _KDF_SALT, _KDF_ITERATIONS, dklen=64)
    return derived[:32], derived[32:]


def _mac_input(nonce: bytes, ciphertext: bytes) -> bytes:
    """Bind envelope version, nonce, and ciphertext into the authenticated input.

    Args:
        nonce: Fresh envelope nonce.
        ciphertext: Encrypted domain bytes authenticated by the MAC.
    """
    return _MAC_CONTEXT + _ENVELOPE_VERSION.to_bytes(2, "big") + nonce + ciphertext


def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    """Expand HMAC-SHA256 blocks into exactly ``length`` stream bytes.

    Args:
        key: Derived stream-encryption key.
        nonce: Per-envelope nonce incorporated in every HMAC block.
        length: Required output stream length in bytes.
    """
    output = bytearray()
    counter = 0
    while len(output) < length:
        output.extend(hmac.new(key, nonce + counter.to_bytes(8, "big"), hashlib.sha256).digest())
        counter += 1
    return bytes(output[:length])


def _xor_bytes(left: bytes, right: bytes) -> bytes:
    """XOR equally sized byte strings, relying on strict zip length validation.

    Args:
        left: First byte string.
        right: Equal-length second byte string.
    """
    return bytes(a ^ b for a, b in zip(left, right, strict=True))


def _b64encode(value: bytes) -> str:
    """Encode envelope binary fields as standard ASCII base64.

    Args:
        value: Binary envelope field to encode.
    """
    return base64.b64encode(value).decode("ascii")


def _b64decode(value: str, field_name: str) -> bytes:
    """Strictly decode a named envelope base64 field.

    Args:
        value: ASCII base64 field value.
        field_name: Envelope field name included in validation errors.
    """
    try:
        return base64.b64decode(value.encode("ascii"), validate=True)
    except (ValueError, UnicodeEncodeError) as exc:
        raise SessionEnvelopeError(f"session envelope field {field_name} is not valid base64") from exc


def _parse_datetime(value: str) -> datetime:
    """Parse an ISO timestamp, preserving aware timezones and assuming UTC for naive values.

    Args:
        value: ISO-8601 datetime text from canonical session JSON.
    """
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


def _emit_storage_event(event: str, started: float, *, outcome: str, **fields: object) -> None:
    """Record duration metrics and structured success or failure telemetry.

    Args:
        event: Stable storage event name used for telemetry.
        started: Monotonic start timestamp used to calculate milliseconds elapsed.
        outcome: Operation outcome used for log severity and metric attributes.
        **fields: Additional non-secret structured telemetry fields.
    """
    duration_ms = (time.perf_counter() - started) * 1000
    record_metric(f"{event}.duration", duration_ms, unit="ms", attributes={"outcome": outcome})
    emit_event(
        _LOGGER,
        logging.ERROR if outcome == "error" else logging.DEBUG,
        event,
        outcome=outcome,
        duration_ms=duration_ms,
        **fields,
    )
