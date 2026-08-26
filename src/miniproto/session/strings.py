"""Import and export validated portable bearer session strings without client dependencies.

Only protected native strings use scrypt-derived AES-256-GCM authenticated encryption.
Plain native strings, Telethon strings and Pyrogram strings are bearer encodings:
they are validated for shape and may carry a checksum, but do not authenticate a
holder or protect their contained authorization key.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import ipaddress
import json
import os
import re
import struct
from collections.abc import Mapping
from typing import Any, Literal, cast

from miniproto.crypto.native import aes_256_gcm_decrypt, aes_256_gcm_encrypt, scrypt_derive
from miniproto.errors import SessionEnvelopeError
from miniproto.session.models import AuthKey, DCOption, SessionRecord, UserIdentity, session_record_from_mapping
from miniproto.session.storage import deserialize_session_data, serialize_session_data

SessionStringFormat = Literal["auto", "miniproto", "telethon", "pyrogram"]

NATIVE_SESSION_PREFIX = "mp1:"
MAX_SESSION_PAYLOAD_BYTES = 1024 * 1024
MAX_SESSION_STRING_CHARS = 1_398_256
MAX_DC_OPTIONS = 256
MAX_PEERS = 10_000

_NATIVE_MAGIC = b"MPS1"
_FLAG_PROTECTED = 0x01
_KNOWN_FLAGS = _FLAG_PROTECTED
_KDF_NONE = 0
_KDF_SCRYPT = 1
_CIPHER_NONE = 0
_CIPHER_AES_256_GCM = 1
_SCRYPT_N = 2**14
_SCRYPT_R = 8
_SCRYPT_P = 1
_SALT_SIZE = 16
_NONCE_SIZE = 12
_CHECKSUM_SIZE = 32
_GCM_TAG_SIZE = 16
_HEADER = struct.Struct(">4sBBBBBIBBI")
_CHECKSUM_CONTEXT = b"miniproto-session-string-checksum-v1\0"
_URLSAFE_UNPADDED_RE = re.compile(r"[A-Za-z0-9_-]+\Z")
_URLSAFE_PADDED_RE = re.compile(r"[A-Za-z0-9_-]+={0,2}\Z")
_TELETHON_IPV4 = struct.Struct(">B4sH256s")
_TELETHON_IPV6 = struct.Struct(">B16sH256s")
_PYROGRAM_MODERN = struct.Struct(">BI?256sQ?")
_PYROGRAM_LEGACY_32 = struct.Struct(">B?256sI?")
_PYROGRAM_LEGACY_64 = struct.Struct(">B?256sQ?")
_PYROGRAM_LAYOUTS_BY_TEXT_SIZE = {
    351: ("pyrogram-legacy32", _PYROGRAM_LEGACY_32),
    356: ("pyrogram-legacy64", _PYROGRAM_LEGACY_64),
    362: ("pyrogram-v2", _PYROGRAM_MODERN),
}
_SESSION_RECORD_FIELDS = frozenset(
    {"version", "dc_id", "auth_key", "dc_options", "user", "update_state", "peers", "metadata"}
)


class SessionString(str):
    """A bearer-secret string whose representation is always redacted."""

    __slots__ = ()
    __miniproto_secret__ = True

    def __repr__(self) -> str:
        """Return a redacted representation that never exposes session material."""
        return "SessionString('[redacted]')"


def export_session_string(
    record_or_mapping: SessionRecord | Mapping[str, Any],
    *,
    format: Literal["miniproto", "telethon", "pyrogram"] = "miniproto",
    passphrase: str | bytes | None = None,
    api_id: int | None = None,
    test_mode: bool | None = None,
) -> SessionString:
    """Export a typed or decoded session record in a portable bearer format.

    Args:
        record_or_mapping: A validated record or an already decoded record mapping.
        format: Native ``miniproto`` (default), ``telethon`` or ``pyrogram``.
        passphrase: Optional native-only authenticated encryption using scrypt and AES-256-GCM.
        api_id: Required for Pyrogram when absent from record metadata.
        test_mode: Required for Pyrogram when absent from record metadata.

    Returns:
        A redacted-on-representation bearer session string.

    Raises:
        SessionEnvelopeError: If data, authentication material, limits or format options are invalid.
        TypeError: If the input is neither a record nor mapping.

    Protected native strings authenticate and encrypt their payload. Plain native,
    Telethon and Pyrogram outputs remain validated bearer encodings. Generic
    asynchronous storage is exported through ``Client.export_session_string``; this
    layer deliberately only accepts already loaded state.
    """

    record = _coerce_record(record_or_mapping)
    if format == "miniproto":
        return _export_native(record, passphrase=passphrase)
    if passphrase is not None:
        raise SessionEnvelopeError("passphrase protection is available only for miniproto session strings")
    if format == "telethon":
        return _export_telethon(record)
    if format == "pyrogram":
        return _export_pyrogram(record, api_id=api_id, test_mode=test_mode)
    raise SessionEnvelopeError("unsupported session string export format")


def import_session_string(
    value: str, *, format: SessionStringFormat = "auto", passphrase: str | bytes | None = None
) -> SessionRecord:
    """Import a native, Telethon v1 or Pyrogram string into a validated record.

    Args:
        value: Bearer session string; it is parsed without stripping characters.
        format: Explicit format or ``auto`` detection from strict wire shapes.
        passphrase: Required only for protected native miniproto strings.

    Returns:
        A normalized session record. Foreign formats set bootstrap metadata.

    Raises:
        SessionEnvelopeError: If the string, envelope, protected-native authentication or format is invalid.
        TypeError: If ``value`` is not a string.
    """

    raw = _ordinary_string(value)
    selected = _detect_format(raw) if format == "auto" else format
    if selected == "miniproto":
        return _import_native(raw, passphrase=passphrase)
    if passphrase is not None:
        raise SessionEnvelopeError("passphrase protection is available only for miniproto session strings")
    if selected == "telethon":
        return _import_telethon(raw)
    if selected == "pyrogram":
        return _import_pyrogram(raw)
    raise SessionEnvelopeError("unsupported session string import format")


def _export_native(record: SessionRecord, *, passphrase: str | bytes | None) -> SessionString:
    """Encode native plaintext-checksummed or scrypt/AES-GCM-protected state.

    Plain native strings have an unkeyed checksum and remain bearer encodings;
    passphrase-protected strings use authenticated encryption.

    Args:
        record: Validated session record to encode.
        passphrase: Optional native protection secret; ``None`` emits a plain checksummed string.
    """
    _validate_record_limits(record)
    payload = serialize_session_data(record)
    if len(payload) > MAX_SESSION_PAYLOAD_BYTES:
        raise SessionEnvelopeError("session payload is too large")
    if passphrase is None:
        header = _HEADER.pack(_NATIVE_MAGIC, 0, _KDF_NONE, _CIPHER_NONE, 0, 0, 0, 0, 0, len(payload))
        checksum = hashlib.sha256(_CHECKSUM_CONTEXT + header + payload).digest()
        body = header + payload + checksum
    else:
        secret = _passphrase_bytes(passphrase)
        salt = os.urandom(_SALT_SIZE)
        nonce = os.urandom(_NONCE_SIZE)
        encrypted_size = len(payload) + _GCM_TAG_SIZE
        header = _HEADER.pack(
            _NATIVE_MAGIC,
            _FLAG_PROTECTED,
            _KDF_SCRYPT,
            _CIPHER_AES_256_GCM,
            len(salt),
            len(nonce),
            _SCRYPT_N,
            _SCRYPT_R,
            _SCRYPT_P,
            encrypted_size,
        )
        key = _derive_protected_key(secret, salt)
        encrypted = aes_256_gcm_encrypt(payload, key, nonce, header)
        body = header + salt + nonce + encrypted
    return SessionString(NATIVE_SESSION_PREFIX + _encode_unpadded(body))


def _import_native(value: str, *, passphrase: str | bytes | None) -> SessionRecord:
    """Validate and decode the versioned native envelope before loading its record.

    Args:
        value: Raw native session string with the required ``mp1:`` prefix.
        passphrase: Required secret for authenticated encrypted native strings.
    """
    if not value.startswith(NATIVE_SESSION_PREFIX):
        if value.startswith("mp"):
            raise SessionEnvelopeError("unsupported miniproto session string version")
        raise SessionEnvelopeError("invalid miniproto session string prefix")
    encoded = value[len(NATIVE_SESSION_PREFIX) :]
    if len(encoded) > MAX_SESSION_STRING_CHARS:
        raise SessionEnvelopeError("session string is too large")
    body = _decode_unpadded(encoded, field="miniproto session string")
    if len(body) < _HEADER.size:
        raise SessionEnvelopeError("session string is truncated")
    try:
        magic, flags, kdf, cipher, salt_size, nonce_size, kdf_n, kdf_r, kdf_p, payload_size = _HEADER.unpack_from(body)
    except struct.error as exc:
        raise SessionEnvelopeError("session string is truncated") from exc
    if magic != _NATIVE_MAGIC:
        raise SessionEnvelopeError("unsupported miniproto session string version")
    if flags & ~_KNOWN_FLAGS:
        raise SessionEnvelopeError("session string contains unknown critical flags")
    header = body[: _HEADER.size]
    if flags == 0:
        if any((kdf, cipher, salt_size, nonce_size, kdf_n, kdf_r, kdf_p)):
            raise SessionEnvelopeError("plaintext session string has invalid algorithm fields")
        if payload_size > MAX_SESSION_PAYLOAD_BYTES:
            raise SessionEnvelopeError("session payload is too large")
        expected_size = _HEADER.size + payload_size + _CHECKSUM_SIZE
        if len(body) != expected_size:
            raise SessionEnvelopeError("session string is truncated or has trailing data")
        payload = body[_HEADER.size : _HEADER.size + payload_size]
        checksum = body[-_CHECKSUM_SIZE:]
        expected_checksum = hashlib.sha256(_CHECKSUM_CONTEXT + header + payload).digest()
        if not hmac.compare_digest(checksum, expected_checksum):
            raise SessionEnvelopeError("session string checksum validation failed")
        if passphrase is not None:
            raise SessionEnvelopeError("session string is not passphrase-protected")
    else:
        if (
            flags != _FLAG_PROTECTED
            or kdf != _KDF_SCRYPT
            or cipher != _CIPHER_AES_256_GCM
            or salt_size != _SALT_SIZE
            or nonce_size != _NONCE_SIZE
            or kdf_n != _SCRYPT_N
            or kdf_r != _SCRYPT_R
            or kdf_p != _SCRYPT_P
        ):
            raise SessionEnvelopeError("unsupported protected session string parameters")
        if payload_size > MAX_SESSION_PAYLOAD_BYTES + _GCM_TAG_SIZE:
            raise SessionEnvelopeError("session payload is too large")
        expected_size = _HEADER.size + salt_size + nonce_size + payload_size
        if len(body) != expected_size:
            raise SessionEnvelopeError("session string is truncated or has trailing data")
        if passphrase is None:
            raise SessionEnvelopeError("session string requires a passphrase")
        secret = _passphrase_bytes(passphrase)
        cursor = _HEADER.size
        salt = body[cursor : cursor + salt_size]
        cursor += salt_size
        nonce = body[cursor : cursor + nonce_size]
        cursor += nonce_size
        encrypted = body[cursor:]
        try:
            payload = aes_256_gcm_decrypt(encrypted, _derive_protected_key(secret, salt), nonce, header)
        except ValueError as exc:
            raise SessionEnvelopeError("session string authentication failed") from exc
        if len(payload) > MAX_SESSION_PAYLOAD_BYTES:
            raise SessionEnvelopeError("session payload is too large")
    return _record_from_native_payload(payload)


def _record_from_native_payload(payload: bytes) -> SessionRecord:
    """Reject ambiguous JSON and unknown fields before constructing native state.

    Args:
        payload: Decoded native JSON session payload bytes.
    """
    try:
        document = json.loads(payload.decode("utf-8"), object_pairs_hook=_reject_duplicate_fields)
    except _DuplicateFieldError as exc:
        raise SessionEnvelopeError("session payload contains duplicate fields") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SessionEnvelopeError("session payload is not valid JSON") from exc
    if not isinstance(document, Mapping) or set(document) != {"storage_version", "payload"}:
        raise SessionEnvelopeError("session payload contains unknown critical fields")
    mapping = deserialize_session_data(payload)
    if set(mapping) != _SESSION_RECORD_FIELDS:
        raise SessionEnvelopeError("session record contains unknown or missing critical fields")
    _validate_mapping_limits(mapping)
    try:
        record = session_record_from_mapping(mapping)
    except (KeyError, TypeError, ValueError) as exc:
        raise SessionEnvelopeError("session record is invalid") from exc
    _validate_record_limits(record)
    return record


def _import_telethon(value: str) -> SessionRecord:
    """Decode strict Telethon v1 IPv4 or IPv6 bearer session material.

    Args:
        value: Raw Telethon v1 session string.
    """
    if not value or value[0] != "1":
        raise SessionEnvelopeError("unsupported Telethon session string version")
    if len(value) not in {353, 369}:
        raise SessionEnvelopeError("Telethon session string has an invalid size")
    packed = _decode_padded(value[1:], field="Telethon session string")
    layout = _TELETHON_IPV4 if len(packed) == _TELETHON_IPV4.size else _TELETHON_IPV6
    if len(packed) != layout.size:
        raise SessionEnvelopeError("Telethon session string has an invalid size")
    try:
        dc_id, packed_ip, port, auth_key = layout.unpack(packed)
        address = ipaddress.ip_address(packed_ip)
    except (struct.error, ValueError) as exc:
        raise SessionEnvelopeError("Telethon session string is invalid") from exc
    _validate_foreign_auth(dc_id, auth_key)
    try:
        option = DCOption(id=dc_id, ip_address=address.compressed, port=port, ipv6=address.version == 6, static=True)
    except ValueError as exc:
        raise SessionEnvelopeError("Telethon session endpoint is invalid") from exc
    return SessionRecord(
        dc_id=dc_id,
        auth_key=AuthKey(dc_id=dc_id, key=auth_key),
        dc_options=(option,),
        metadata={"session_import_format": "telethon-v1", "update_state_bootstrap_required": True},
    )


def _export_telethon(record: SessionRecord) -> SessionString:
    """Encode the active non-media endpoint and 256-byte auth key for Telethon v1.

    The result is a validated bearer encoding, not encrypted or authenticated.

    Args:
        record: Session record with active DC, endpoint and 256-byte authorization key.
    """
    dc_id, auth_key = _required_dc_and_auth(record, format_name="Telethon")
    option = next(
        (candidate for candidate in record.dc_options if candidate.id == dc_id and not candidate.media_only), None
    )
    if option is None:
        raise SessionEnvelopeError("Telethon export requires a DC endpoint for the active datacenter")
    try:
        packed_ip = ipaddress.ip_address(option.ip_address).packed
        layout = _TELETHON_IPV4 if len(packed_ip) == 4 else _TELETHON_IPV6
        packed = layout.pack(dc_id, packed_ip, option.port, auth_key)
    except (struct.error, ValueError) as exc:
        raise SessionEnvelopeError("Telethon export endpoint is invalid") from exc
    return SessionString("1" + base64.urlsafe_b64encode(packed).decode("ascii"))


def _import_pyrogram(value: str) -> SessionRecord:
    """Decode supported Pyrogram legacy or v2 bearer layouts and record import metadata.

    Args:
        value: Raw Pyrogram legacy or v2 session string.
    """
    from miniproto.auth.dc import default_dc_options

    selected = _PYROGRAM_LAYOUTS_BY_TEXT_SIZE.get(len(value))
    if selected is None:
        raise SessionEnvelopeError("Pyrogram session string has an invalid size")
    import_format, layout = selected
    packed = _decode_unpadded(value, field="Pyrogram session string")
    if len(packed) != layout.size:
        raise SessionEnvelopeError("Pyrogram session string has an invalid size")
    try:
        values = layout.unpack(packed)
    except struct.error as exc:
        raise SessionEnvelopeError("Pyrogram session string is invalid") from exc
    if layout is _PYROGRAM_MODERN:
        dc_id, api_id, test_mode, auth_key, user_id, is_bot = values
    else:
        dc_id, test_mode, auth_key, user_id, is_bot = values
        api_id = None
    dc_id = int(dc_id)
    _validate_foreign_auth(dc_id, cast(bytes, auth_key))
    if int(user_id) <= 0:
        raise SessionEnvelopeError("Pyrogram session string contains an invalid account identity")
    metadata: dict[str, object] = {
        "session_import_format": import_format,
        "test_mode": bool(test_mode),
        "update_state_bootstrap_required": True,
    }
    if api_id is not None:
        if int(api_id) <= 0:
            raise SessionEnvelopeError("Pyrogram session string contains an invalid API ID")
        metadata["api_id"] = int(api_id)
    return SessionRecord(
        dc_id=dc_id,
        auth_key=AuthKey(dc_id=dc_id, key=cast(bytes, auth_key)),
        dc_options=default_dc_options(test_mode=bool(test_mode)),
        user=UserIdentity(id=int(user_id), is_bot=bool(is_bot)),
        metadata=metadata,
    )


def _export_pyrogram(record: SessionRecord, *, api_id: int | None, test_mode: bool | None) -> SessionString:
    """Encode the modern Pyrogram layout using explicit or stored API settings.

    The result is a validated bearer encoding, not encrypted or authenticated.

    Args:
        record: Session record with active DC, key and account identity.
        api_id: Optional API ID overriding record metadata.
        test_mode: Optional test-mode value overriding record metadata.
    """
    dc_id, auth_key = _required_dc_and_auth(record, format_name="Pyrogram")
    resolved_api_id = api_id if api_id is not None else _metadata_int(record.metadata, "api_id")
    if resolved_api_id is None or resolved_api_id <= 0:
        raise SessionEnvelopeError("Pyrogram export requires a positive API ID")
    if test_mode is None:
        metadata_test_mode = record.metadata.get("test_mode")
        if not isinstance(metadata_test_mode, bool):
            raise SessionEnvelopeError("Pyrogram export requires an explicit test-mode value")
        resolved_test_mode = metadata_test_mode
    else:
        resolved_test_mode = test_mode
    if record.user is None:
        raise SessionEnvelopeError("Pyrogram export requires an account identity")
    try:
        packed = _PYROGRAM_MODERN.pack(
            dc_id, resolved_api_id, resolved_test_mode, auth_key, record.user.id, record.user.is_bot
        )
    except struct.error as exc:
        raise SessionEnvelopeError("Pyrogram export fields are out of range") from exc
    return SessionString(_encode_unpadded(packed))


def _required_dc_and_auth(record: SessionRecord, *, format_name: str) -> tuple[int, bytes]:
    """Require a matching active DC and exact 256-byte foreign-format auth key.

    Args:
        record: Session record to validate for foreign-format export.
        format_name: Human-readable target format included in validation errors.
    """
    if record.dc_id is None or record.auth_key is None:
        raise SessionEnvelopeError(f"{format_name} export requires an active datacenter and auth key")
    if len(record.auth_key.key) != 256:
        raise SessionEnvelopeError(f"{format_name} export requires a 256-byte auth key")
    if record.auth_key.dc_id != record.dc_id:
        raise SessionEnvelopeError(f"{format_name} export auth key does not match the active datacenter")
    return record.dc_id, record.auth_key.key


def _detect_format(value: str) -> Literal["miniproto", "telethon", "pyrogram"]:
    """Detect a format only from unambiguous version prefixes and strict lengths.

    Args:
        value: Raw session string whose wire shape is inspected.
    """
    if value.startswith("mp"):
        return "miniproto"
    if value.startswith("1") and len(value) in {353, 369}:
        return "telethon"
    if len(value) in _PYROGRAM_LAYOUTS_BY_TEXT_SIZE:
        return "pyrogram"
    raise SessionEnvelopeError("session string format could not be detected")


def _coerce_record(value: SessionRecord | Mapping[str, Any]) -> SessionRecord:
    """Accept typed state or validate a decoded record mapping for export.

    Args:
        value: Typed session record or decoded canonical mapping.
    """
    if isinstance(value, SessionRecord):
        return value
    if isinstance(value, Mapping):
        try:
            return session_record_from_mapping(value)
        except (KeyError, TypeError, ValueError) as exc:
            raise SessionEnvelopeError("session record is invalid") from exc
    raise TypeError("session export requires a SessionRecord or loaded session mapping")


def _ordinary_string(value: str) -> str:
    """Recover actual string contents even from a redacting ``SessionString``.

    Args:
        value: Plain or redacting string instance containing session material.
    """
    if not isinstance(value, str):
        raise TypeError("session string must be str")
    return str.__str__(value) if isinstance(value, SessionString) else value


def _passphrase_bytes(passphrase: str | bytes) -> bytes:
    """Encode a non-empty native protection passphrase as secret bytes.

    Args:
        passphrase: Text or binary secret used for native authenticated encryption.
    """
    secret = passphrase.encode("utf-8") if isinstance(passphrase, str) else bytes(passphrase)
    if not secret:
        raise SessionEnvelopeError("session string passphrase must not be empty")
    return secret


def _derive_protected_key(passphrase: bytes, salt: bytes) -> bytes:
    """Derive the fixed-size native encryption key with the supported scrypt cost.

    Args:
        passphrase: Non-empty passphrase bytes.
        salt: Fresh native-envelope scrypt salt.
    """
    try:
        return scrypt_derive(passphrase, salt, _SCRYPT_N, _SCRYPT_R, _SCRYPT_P, 32)
    except (MemoryError, TypeError, ValueError) as exc:
        raise SessionEnvelopeError("session string key derivation failed") from exc


def _encode_unpadded(value: bytes) -> str:
    """Encode canonical unpadded URL-safe base64.

    Args:
        value: Binary session-string payload to encode.
    """
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _decode_unpadded(value: str, *, field: str) -> bytes:
    """Decode only canonical unpadded URL-safe base64 for a named field.

    Args:
        value: Candidate unpadded URL-safe base64 text.
        field: Field name included in validation errors.
    """
    if not value or _URLSAFE_UNPADDED_RE.fullmatch(value) is None:
        raise SessionEnvelopeError(f"{field} is not strict URL-safe base64")
    try:
        decoded = base64.b64decode(value + "=" * (-len(value) % 4), altchars=b"-_", validate=True)
    except (ValueError, binascii.Error) as exc:
        raise SessionEnvelopeError(f"{field} is not strict URL-safe base64") from exc
    if _encode_unpadded(decoded) != value:
        raise SessionEnvelopeError(f"{field} is not canonical URL-safe base64")
    return decoded


def _decode_padded(value: str, *, field: str) -> bytes:
    """Decode only canonical padded URL-safe base64 for a named field.

    Args:
        value: Candidate padded URL-safe base64 text.
        field: Field name included in validation errors.
    """
    if not value or _URLSAFE_PADDED_RE.fullmatch(value) is None or len(value) % 4:
        raise SessionEnvelopeError(f"{field} is not strict URL-safe base64")
    try:
        decoded = base64.b64decode(value, altchars=b"-_", validate=True)
    except (ValueError, binascii.Error) as exc:
        raise SessionEnvelopeError(f"{field} is not strict URL-safe base64") from exc
    if base64.urlsafe_b64encode(decoded).decode("ascii") != value:
        raise SessionEnvelopeError(f"{field} is not canonical URL-safe base64")
    return decoded


def _validate_foreign_auth(dc_id: int, auth_key: bytes) -> None:
    """Require usable foreign session DC and non-zero 256-byte auth material.

    Args:
        dc_id: Decoded foreign-format data-center ID.
        auth_key: Decoded foreign-format 256-byte authorization key.
    """
    if dc_id <= 0:
        raise SessionEnvelopeError("session string contains an invalid datacenter")
    if len(auth_key) != 256 or not any(auth_key):
        raise SessionEnvelopeError("session string does not contain a usable auth key")


def _validate_record_limits(record: SessionRecord) -> None:
    """Enforce bounded DC-option and peer counts before native export.

    Args:
        record: Validated record whose collection limits are checked.
    """
    if len(record.dc_options) > MAX_DC_OPTIONS:
        raise SessionEnvelopeError("session record contains too many DC options")
    if len(record.peers) > MAX_PEERS:
        raise SessionEnvelopeError("session record contains too many peers")


def _validate_mapping_limits(mapping: Mapping[str, Any]) -> None:
    """Enforce bounded decoded collection shapes before record construction.

    Args:
        mapping: Decoded native record mapping whose collection shapes are checked.
    """
    dc_options = mapping.get("dc_options", ())
    peers = mapping.get("peers", ())
    if not isinstance(dc_options, list | tuple) or len(dc_options) > MAX_DC_OPTIONS:
        raise SessionEnvelopeError("session record contains too many or invalid DC options")
    if not isinstance(peers, list | tuple) or len(peers) > MAX_PEERS:
        raise SessionEnvelopeError("session record contains too many or invalid peers")


def _metadata_int(metadata: Mapping[str, Any], key: str) -> int | None:
    """Return a non-boolean integer metadata value when present.

    Args:
        metadata: Session metadata mapping to inspect.
        key: Metadata key expected to hold an integer.
    """
    value = metadata.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else None


class _DuplicateFieldError(ValueError):
    """Internal marker raised when JSON decoding detects duplicate object keys."""

    pass


def _reject_duplicate_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Build a JSON object mapping while rejecting duplicate keys fail-closed.

    Args:
        pairs: Ordered key/value pairs supplied by JSON's object-pairs hook.
    """
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateFieldError
        result[key] = value
    return result


__all__ = [
    "MAX_DC_OPTIONS",
    "MAX_PEERS",
    "MAX_SESSION_PAYLOAD_BYTES",
    "MAX_SESSION_STRING_CHARS",
    "NATIVE_SESSION_PREFIX",
    "SessionString",
    "SessionStringFormat",
    "export_session_string",
    "import_session_string",
]
