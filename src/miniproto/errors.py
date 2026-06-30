from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from miniproto.security.redaction import redact_text, safe_repr


class MiniprotoError(Exception):
    """Base exception for miniproto."""


@dataclass(slots=True, repr=False)
class RpcError(MiniprotoError):
    message: str
    code: int | None = None
    request: object | None = None
    context: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        Exception.__init__(self, redact_text(self.message))

    def __str__(self) -> str:
        message = redact_text(self.message)
        rendered = message if self.code is None else f"[{self.code}] {message}"
        if self.request is not None:
            rendered = f"{rendered} request={safe_repr(self.request)}"
        if self.context:
            rendered = f"{rendered} context={safe_repr(self.context)}"
        return rendered

    def __repr__(self) -> str:
        return f"{type(self).__name__}(message={redact_text(self.message)!r}, code={self.code!r}, request={safe_repr(self.request)}, context={safe_repr(self.context)})"


class Unauthorized(RpcError):
    def __init__(self, message: str = "unauthorized") -> None:
        super().__init__(message=message, code=401)


class FloodWait(RpcError):
    def __init__(self, seconds: int, message: str | None = None) -> None:
        self.seconds = seconds
        super().__init__(message=message or f"flood wait for {seconds} seconds", code=420)


class AuthError(RpcError):
    """Base exception for authentication and authorization flow failures."""


class InvalidCode(AuthError):
    def __init__(self, message: str = "invalid phone code") -> None:
        super().__init__(message=message, code=400)


class PasswordRequired(AuthError):
    def __init__(self, message: str = "2FA password required") -> None:
        super().__init__(message=message, code=401)


class PasswordInvalid(AuthError):
    def __init__(self, message: str = "invalid 2FA password") -> None:
        super().__init__(message=message, code=400)


class SignUpRequired(AuthError):
    def __init__(self, message: str = "sign-up required") -> None:
        super().__init__(message=message, code=401)


class AuthKeyNotFound(AuthError):
    def __init__(self, message: str = "auth key not registered") -> None:
        super().__init__(message=message, code=401)


class AuthKeyRegenerationRequired(AuthError):
    def __init__(self, message: str = "auth key must be regenerated") -> None:
        super().__init__(message=message, code=406)


class InvalidDatacenter(AuthError):
    def __init__(self, message: str = "invalid datacenter") -> None:
        super().__init__(message=message, code=303)


class DatacenterMigration(InvalidDatacenter):
    def __init__(self, dc_id: int, *, kind: str = "MIGRATE", message: str | None = None) -> None:
        self.dc_id = dc_id
        self.kind = kind
        super().__init__(message or f"{kind}_{dc_id}")


class TransportFlood(FloodWait):
    """Raised when Telegram asks the client to stop retrying for a bounded interval."""


class SessionStorageError(MiniprotoError):
    """Raised when session persistence cannot safely continue."""


class SessionEnvelopeError(SessionStorageError):
    """Raised when an encrypted session envelope fails validation or authentication."""


_MIGRATION_RE = re.compile(r"^(?P<kind>NETWORK|PHONE|STATS|USER|FILE)_MIGRATE_(?P<dc_id>\d+)$")
_FLOOD_RE = re.compile(r"^FLOOD_WAIT_(?P<seconds>\d+)$")
_AUTH_KEY_NOT_FOUND = {"AUTH_KEY_INVALID", "AUTH_KEY_PERM_EMPTY", "AUTH_KEY_UNREGISTERED"}
_AUTH_KEY_REGENERATE = {"AUTH_KEY_DUPLICATED", "AUTH_KEY_UNSYNCHRONIZED"}
_INVALID_CODE = {
    "PHONE_CODE_EMPTY",
    "PHONE_CODE_EXPIRED",
    "PHONE_CODE_HASH_EMPTY",
    "PHONE_CODE_INVALID",
}


def classify_rpc_error(error: RpcError) -> RpcError:
    raw_message = str(error.message).upper()
    if flood_match := _FLOOD_RE.match(raw_message):
        return TransportFlood(int(flood_match.group("seconds")), message=error.message)
    if migration_match := _MIGRATION_RE.match(raw_message):
        return DatacenterMigration(
            int(migration_match.group("dc_id")),
            kind=migration_match.group("kind"),
            message=error.message,
        )
    if raw_message in _INVALID_CODE:
        return InvalidCode(error.message)
    if raw_message == "SESSION_PASSWORD_NEEDED":
        return PasswordRequired(error.message)
    if raw_message == "PASSWORD_HASH_INVALID":
        return PasswordInvalid(error.message)
    if raw_message in _AUTH_KEY_NOT_FOUND:
        return AuthKeyNotFound(error.message)
    if raw_message in _AUTH_KEY_REGENERATE:
        return AuthKeyRegenerationRequired(error.message)
    if error.code == 401:
        return Unauthorized(error.message)
    return error
