from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol, cast, runtime_checkable

from miniproto.errors import SessionEnvelopeError, SessionStorageError
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


@runtime_checkable
class SessionStorage(Protocol):
    async def load(self) -> Mapping[str, Any] | None: ...

    async def save(self, data: SessionPayload) -> None: ...

    async def clear(self) -> None: ...

    async def close(self) -> None: ...


class InMemorySessionStorage:
    def __init__(self, initial: SessionPayload | None = None) -> None:
        self._data: dict[str, Any] | None = (
            _copy_session_data(initial) if initial is not None else None
        )

    async def load(self) -> Mapping[str, Any] | None:
        return _copy_session_data(self._data) if self._data is not None else None

    async def save(self, data: SessionPayload) -> None:
        self._data = _copy_session_data(data)

    async def clear(self) -> None:
        self._data = None

    async def close(self) -> None:
        return None


class EncryptedSQLiteSessionStorage:
    """Encrypted SQLite session persistence with fail-closed key handling."""

    def __init__(self, path: str | os.PathLike[str], key: bytes | str | None = None) -> None:
        resolved_key = key if key is not None else os.environ.get("MINIPROTO_SESSION_KEY")
        if not resolved_key:
            raise ValueError(
                "EncryptedSQLiteSessionStorage requires a key or MINIPROTO_SESSION_KEY"
            )
        key_material = (
            resolved_key.encode() if isinstance(resolved_key, str) else bytes(resolved_key)
        )
        if len(key_material) < 16:
            raise ValueError("EncryptedSQLiteSessionStorage key must be at least 16 bytes")
        self.path = Path(path)
        self._encryption_key, self._mac_key = _derive_keys(key_material)

    async def load(self) -> Mapping[str, Any] | None:
        return await asyncio.to_thread(self._load_sync)

    async def save(self, data: SessionPayload) -> None:
        envelope = self._encrypt(serialize_session_data(data))
        await asyncio.to_thread(self._save_sync, envelope)

    async def clear(self) -> None:
        await asyncio.to_thread(self._clear_sync)

    async def close(self) -> None:
        return None

    def _load_sync(self) -> Mapping[str, Any] | None:
        if not self.path.exists():
            return None
        try:
            with self._connect() as connection:
                _ensure_schema(connection)
                row = connection.execute(
                    "SELECT envelope FROM session_records WHERE name = ?", (_DEFAULT_RECORD_NAME,)
                ).fetchone()
        except sqlite3.Error as exc:
            raise SessionStorageError("failed to load session database") from exc
        if row is None:
            return None
        return self._decrypt(bytes(row[0]))

    def _save_sync(self, envelope: bytes) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = self._connect()
        try:
            _ensure_schema(connection)
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """
                INSERT INTO session_records (name, envelope, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET envelope = excluded.envelope, updated_at = excluded.updated_at
                """,
                (_DEFAULT_RECORD_NAME, envelope, datetime.now(UTC).isoformat()),
            )
            connection.commit()
        except sqlite3.Error as exc:
            connection.rollback()
            raise SessionStorageError("failed to save session database") from exc
        finally:
            connection.close()

    def _clear_sync(self) -> None:
        if not self.path.exists():
            return
        connection = self._connect()
        try:
            _ensure_schema(connection)
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "DELETE FROM session_records WHERE name = ?", (_DEFAULT_RECORD_NAME,)
            )
            connection.commit()
        except sqlite3.Error as exc:
            connection.rollback()
            raise SessionStorageError("failed to clear session database") from exc
        finally:
            connection.close()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _encrypt(self, plaintext: bytes) -> bytes:
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
        envelope = _decode_envelope(envelope_bytes)
        nonce = _b64decode(str(envelope["nonce"]), "nonce")
        ciphertext = _b64decode(str(envelope["payload"]), "payload")
        tag = _b64decode(str(envelope["tag"]), "tag")
        expected_tag = hmac.new(
            self._mac_key, _mac_input(nonce, ciphertext), hashlib.sha256
        ).digest()
        if not hmac.compare_digest(tag, expected_tag):
            raise SessionEnvelopeError("session envelope authentication failed")
        plaintext = _xor_bytes(ciphertext, _keystream(self._encryption_key, nonce, len(ciphertext)))
        return deserialize_session_data(plaintext)


def serialize_session_data(data: SessionPayload) -> bytes:
    document = {
        "storage_version": _SERIALIZATION_VERSION,
        "payload": _encode_json_value(_normalize_session_payload(data)),
    }
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode()


def deserialize_session_data(payload: bytes) -> dict[str, Any]:
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
    return deserialize_session_data(serialize_session_data(data))


def _normalize_session_payload(data: SessionPayload) -> Mapping[str, Any]:
    if isinstance(data, SessionRecord):
        return session_record_to_mapping(data)
    if isinstance(data, Mapping):
        return cast("Mapping[str, Any]", data)
    raise TypeError("session data must be a mapping or SessionRecord")


def _encode_json_value(value: object) -> object:
    if isinstance(value, bytes | bytearray | memoryview):
        return {_JSON_TYPE_KEY: "bytes", "value": _b64encode(bytes(value))}
    if isinstance(value, datetime):
        normalized = value if value.tzinfo is not None else value.replace(tzinfo=UTC)
        return {_JSON_TYPE_KEY: "datetime", "value": normalized.isoformat()}
    if isinstance(value, SessionRecord):
        return _encode_json_value(session_record_to_mapping(value))
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: _encode_json_value(getattr(value, field.name)) for field in fields(value)
        }
    if isinstance(value, Mapping):
        return {str(key): _encode_json_value(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_encode_json_value(item) for item in value]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    raise TypeError(f"session value of type {type(value).__name__} is not serializable")


def _decode_json_value(value: object) -> object:
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
    connection.execute(_TABLE_SCHEMA)


def _derive_keys(key_material: bytes) -> tuple[bytes, bytes]:
    derived = hashlib.pbkdf2_hmac("sha256", key_material, _KDF_SALT, _KDF_ITERATIONS, dklen=64)
    return derived[:32], derived[32:]


def _mac_input(nonce: bytes, ciphertext: bytes) -> bytes:
    return _MAC_CONTEXT + _ENVELOPE_VERSION.to_bytes(2, "big") + nonce + ciphertext


def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    output = bytearray()
    counter = 0
    while len(output) < length:
        output.extend(hmac.new(key, nonce + counter.to_bytes(8, "big"), hashlib.sha256).digest())
        counter += 1
    return bytes(output[:length])


def _xor_bytes(left: bytes, right: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(left, right, strict=True))


def _b64encode(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def _b64decode(value: str, field_name: str) -> bytes:
    try:
        return base64.b64decode(value.encode("ascii"), validate=True)
    except (ValueError, UnicodeEncodeError) as exc:
        raise SessionEnvelopeError(
            f"session envelope field {field_name} is not valid base64"
        ) from exc


def _parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)
