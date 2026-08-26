"""Redaction-safe public exceptions and Telegram RPC error classification."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, cast

from miniproto.security.redaction import redact_text, safe_repr


class MiniprotoError(Exception):
    """Base exception for all library-defined failures."""


class ProtocolValidationError(MiniprotoError, ValueError):
    """An authenticated MTProto message violated the inbound protocol contract."""

    def __init__(self, reason: str, *, context: Mapping[str, Any] | None = None) -> None:
        """Capture a validation reason and optional diagnostic context safely.

        Args:
            reason: Protocol rule that the inbound authenticated message violated.
            context: Optional diagnostic fields rendered through secret-safe formatting.
        """
        self.reason = reason
        self.context = dict(context or {})
        Exception.__init__(self, f"inbound MTProto validation failed: {reason}")

    def __str__(self) -> str:
        """Render the reason and safely represented context."""
        rendered = f"inbound MTProto validation failed: {self.reason}"
        if self.context:
            rendered = f"{rendered} context={safe_repr(self.context)}"
        return rendered

    def __repr__(self) -> str:
        """Return a redacted diagnostic representation."""
        return f"{type(self).__name__}(reason={redact_text(self.reason)!r}, context={safe_repr(self.context)})"


class AmbiguousRpcResult(MiniprotoError):
    """The transport failed after an RPC may already have reached Telegram."""

    def __init__(
        self,
        message: str = "RPC result is ambiguous; the request may have executed",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Capture a possibly executed request without exposing secret text.

        Args:
            message: Human-readable ambiguity explanation, redacted for exception output.
            request: Optional raw request that may have reached Telegram.
            context: Optional diagnostic fields rendered with secret redaction.
        """
        self.message = message
        self.request = request
        self.context = context
        Exception.__init__(self, redact_text(message))

    def __str__(self) -> str:
        """Render redacted message, request and optional context."""
        rendered = redact_text(self.message)
        if self.request is not None:
            rendered = f"{rendered} request={safe_repr(self.request)}"
        if self.context:
            rendered = f"{rendered} context={safe_repr(self.context)}"
        return rendered

    def __repr__(self) -> str:
        """Return a redacted diagnostic representation."""
        return f"{type(self).__name__}(message={redact_text(self.message)!r}, request={safe_repr(self.request)}, context={safe_repr(self.context)})"


@dataclass(slots=True, repr=False)
class RpcError(MiniprotoError):
    """Raw or classified Telegram RPC failure with redaction-safe diagnostics.

    Attributes:
        message: Telegram's symbolic or descriptive error text.
        code: Optional numeric RPC status code.
        request: Optional request object associated with the failure.
        context: Optional diagnostic metadata rendered with secret redaction.
    """

    message: str
    code: int | None = None
    request: object | None = None
    context: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        """Initialize the exception base with a redacted message."""
        Exception.__init__(self, redact_text(self.message))

    @property
    def rpc_error_name(self) -> str:
        """Return generated canonical name when available, otherwise raw message."""
        return str(getattr(type(self), "RPC_ERROR_NAME", self.message))

    def __str__(self) -> str:
        """Render code and safe request/context diagnostics without leaking secrets."""
        message = redact_text(self.message)
        rendered = message if self.code is None else f"[{self.code}] {message}"
        if self.request is not None:
            rendered = f"{rendered} request={safe_repr(self.request)}"
        if self.context:
            rendered = f"{rendered} context={safe_repr(self.context)}"
        return rendered

    def __repr__(self) -> str:
        """Return a redacted constructor-style diagnostic representation."""
        return f"{type(self).__name__}(message={redact_text(self.message)!r}, code={self.code!r}, request={safe_repr(self.request)}, context={safe_repr(self.context)})"


class InvokeError(RpcError):
    """Base exception for raw invocation failures before Telegram returns a typed RPC error."""


class ClientDisconnected(InvokeError):
    """Raised when invocation cannot continue because the client disconnected."""

    def __init__(
        self,
        message: str = "client disconnected",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a disconnect failure with optional request diagnostics.

        Args:
            message: Disconnect explanation, redacted by the base exception.
            request: Optional request interrupted by the client lifecycle change.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, request=request, context=context)


class RequestTimeout(InvokeError):
    """Raised when the client-side request deadline expires."""

    def __init__(
        self,
        message: str = "request timed out",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a request-timeout failure with optional request diagnostics.

        Args:
            message: Timeout explanation, redacted by the base exception.
            request: Optional request that exceeded its local deadline.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, request=request, context=context)


class ResultTypeMismatch(InvokeError):
    """Raised when an RPC result does not match the requested result contract."""

    def __init__(self, expected: str, actual: object, *, request: object | None = None) -> None:
        """Record expected and actual result type names for a failed invocation.

        Args:
            expected: Declared TL result type expected by the request.
            actual: Decoded result object that failed the type contract.
            request: Optional original request retained for diagnostics.
        """
        self.expected = expected
        self.actual = actual
        super().__init__(
            message=f"RPC result type mismatch: expected {expected}, got {_result_type_name(actual)}",
            request=request,
            context={"expected": expected, "actual": _result_type_name(actual)},
        )


class BadRequest(RpcError):
    """Classified client-side Telegram RPC error, normally status code 400."""

    def __init__(
        self,
        message: str = "bad request",
        *,
        code: int = 400,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a bad-request error, defaulting its code to 400.

        Args:
            message: Telegram error text, redacted by the base exception.
            code: RPC status code, defaulting to Telegram's bad-request code.
            request: Optional request associated with the error.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=code, request=request, context=context)


class Unauthorized(RpcError):
    """Classified Telegram authorization failure with status code 401."""

    def __init__(
        self, message: str = "unauthorized", *, request: object | None = None, context: Mapping[str, Any] | None = None
    ) -> None:
        """Create an unauthorized error with optional request context.

        Args:
            message: Telegram authorization-failure text.
            request: Optional request associated with the failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=401, request=request, context=context)


class Forbidden(RpcError):
    """Classified Telegram permission failure with status code 403."""

    def __init__(
        self, message: str = "forbidden", *, request: object | None = None, context: Mapping[str, Any] | None = None
    ) -> None:
        """Create a forbidden error with optional request context.

        Args:
            message: Telegram permission-failure text.
            request: Optional request associated with the failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=403, request=request, context=context)


class NotFound(RpcError):
    """Classified Telegram missing-resource failure with status code 404."""

    def __init__(
        self, message: str = "not found", *, request: object | None = None, context: Mapping[str, Any] | None = None
    ) -> None:
        """Create a not-found error with optional request context.

        Args:
            message: Telegram missing-resource text.
            request: Optional request associated with the failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=404, request=request, context=context)


class RpcTimeout(RpcError):
    """Classified Telegram-side or transport RPC timeout, commonly code -503."""

    def __init__(
        self,
        message: str = "RPC timeout",
        *,
        code: int | None = -503,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create an RPC timeout while preserving an explicit server code.

        Args:
            message: Telegram or transport timeout explanation.
            code: Optional RPC code, defaulting to the common ``-503`` timeout code.
            request: Optional request associated with the timeout.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=code, request=request, context=context)


class InternalServerError(RpcError):
    """Classified retryable server failure, normally a 5xx RPC code."""

    def __init__(
        self,
        message: str = "internal server error",
        *,
        code: int | None = 500,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a server error while preserving an explicit server code.

        Args:
            message: Telegram server-failure text.
            code: Optional RPC code, defaulting to 500.
            request: Optional request associated with the server failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=code, request=request, context=context)


class FloodWait(RpcError):
    """Telegram pacing failure that exposes the required wait duration in seconds."""

    def __init__(
        self,
        seconds: int,
        message: str | None = None,
        *,
        code: int = 420,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a flood wait with its server-provided delay and optional diagnostics.

        Args:
            seconds: Server-required wait duration in seconds.
            message: Optional Telegram error text; a descriptive default is generated when absent.
            code: RPC code, defaulting to Telegram's flood-wait code 420.
            request: Optional request that triggered pacing.
            context: Optional secret-safe diagnostic metadata.
        """
        self.seconds = seconds
        super().__init__(
            message=message or f"flood wait for {seconds} seconds", code=code, request=request, context=context
        )


class AuthError(RpcError):
    """Base exception for authentication and authorization flow failures."""


class InvalidCode(AuthError):
    """Authentication flow failure for a missing, expired or invalid phone code."""

    def __init__(
        self,
        message: str = "invalid phone code",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create an invalid-code failure with status code 400.

        Args:
            message: Phone-code failure text.
            request: Optional sign-in request associated with the failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=400, request=request, context=context)


class PasswordRequired(AuthError):
    """Authentication flow requires a configured two-factor password."""

    def __init__(
        self,
        message: str = "2FA password required",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a password-required failure with status code 401.

        Args:
            message: Two-factor-password requirement text.
            request: Optional authentication request associated with the failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=401, request=request, context=context)


class PasswordInvalid(AuthError):
    """Authentication flow received an invalid two-factor password."""

    def __init__(
        self,
        message: str = "invalid 2FA password",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a password-invalid failure with status code 400.

        Args:
            message: Two-factor-password failure text.
            request: Optional password-check request associated with the failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=400, request=request, context=context)


class SignUpRequired(AuthError):
    """Authentication flow requires creating a Telegram account first."""

    def __init__(
        self,
        message: str = "sign-up required",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a sign-up-required failure with status code 401.

        Args:
            message: Telegram sign-up requirement text.
            request: Optional sign-in request associated with the failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=401, request=request, context=context)


class AuthKeyNotFound(AuthError):
    """Authentication key is invalid, unregistered or no longer available."""

    def __init__(
        self,
        message: str = "auth key not registered",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create an auth-key-not-found failure with status code 401.

        Args:
            message: Telegram auth-key failure text.
            request: Optional request attempted with the unavailable key.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=401, request=request, context=context)


class AuthKeyRegenerationRequired(AuthError):
    """Authentication key is duplicated or unsynchronized and must be replaced."""

    def __init__(
        self,
        message: str = "auth key must be regenerated",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create an auth-key-regeneration failure with status code 406.

        Args:
            message: Telegram key-regeneration requirement text.
            request: Optional request attempted with the unsynchronized key.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=406, request=request, context=context)


class InvalidDatacenter(AuthError):
    """Telegram rejects the current data centre, commonly before a migration hint."""

    def __init__(
        self,
        message: str = "invalid datacenter",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create an invalid-datacenter failure with status code 303.

        Args:
            message: Telegram data-center failure text.
            request: Optional request associated with the data-center failure.
            context: Optional secret-safe diagnostic metadata.
        """
        super().__init__(message=message, code=303, request=request, context=context)


class DatacenterMigration(InvalidDatacenter):
    """Telegram directs the request to ``dc_id`` for a named migration kind."""

    def __init__(
        self,
        dc_id: int,
        *,
        kind: str = "MIGRATE",
        message: str | None = None,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Create a migration error from the target DC and migration kind.

        Args:
            dc_id: Target Telegram data-center ID.
            kind: Migration family extracted from Telegram's symbolic error name.
            message: Optional raw error text; a migration name is generated when absent.
            request: Optional request that Telegram directed to another DC.
            context: Optional secret-safe diagnostic metadata.
        """
        self.dc_id = dc_id
        self.kind = kind
        super().__init__(message or f"{kind}_MIGRATE_{dc_id}", request=request, context=context)


class TransportFlood(FloodWait):
    """Raised for transport-level 429 responses, not ordinary RPC flood waits."""


class PendingRpcLimitExceeded(MiniprotoError):
    """Raised when a sender has too many in-flight RPCs and cannot accept more."""


class SessionStorageError(MiniprotoError):
    """Raised when session persistence cannot safely continue."""


class SessionEnvelopeError(SessionStorageError):
    """Raised when an encrypted session envelope fails validation or authentication."""


_MIGRATION_RE = re.compile(r"^(?P<kind>NETWORK|PHONE|STATS|USER|FILE)_MIGRATE_(?P<dc_id>\d+)$", re.IGNORECASE)
_FLOOD_RE = re.compile(r"^(?P<kind>[A-Z0-9_]*WAIT)_(?P<seconds>\d+)$", re.IGNORECASE)
_PACING_WAIT_TEMPLATES = frozenset(
    {"FLOOD_WAIT_%d", "FLOOD_PREMIUM_WAIT_%d", "SLOWMODE_WAIT_%d", "TAKEOUT_INIT_DELAY_%d"}
)
_TRAILING_INT_RE = re.compile(r"^(?P<prefix>.+)_(?P<value>\d+)$")
_TEMPLATE_INT_RE = re.compile(r"%d", re.IGNORECASE)
_AUTH_KEY_NOT_FOUND = {"AUTH_KEY_INVALID", "AUTH_KEY_PERM_EMPTY", "AUTH_KEY_UNREGISTERED"}
_AUTH_KEY_REGENERATE = {"AUTH_KEY_DUPLICATED", "AUTH_KEY_UNSYNCHRONIZED"}
_INVALID_CODE = {"PHONE_CODE_EMPTY", "PHONE_CODE_EXPIRED", "PHONE_CODE_HASH_EMPTY", "PHONE_CODE_INVALID"}
_COMMON_EXACT_BASES: dict[str, type[RpcError]] = {
    "SESSION_PASSWORD_NEEDED": PasswordRequired,
    "PASSWORD_HASH_INVALID": PasswordInvalid,
    **dict.fromkeys(_INVALID_CODE, InvalidCode),
    **dict.fromkeys(_AUTH_KEY_NOT_FOUND, AuthKeyNotFound),
    **dict.fromkeys(_AUTH_KEY_REGENERATE, AuthKeyRegenerationRequired),
}
_ERROR_CLASS_BY_TEMPLATE: dict[str, type[RpcError]] = {}
_GENERATED_ERROR_CLASS_NAMES: set[str] = set()


def classify_rpc_error(error: RpcError) -> RpcError:
    """Return the most specific public error matching a raw Telegram RPC error.

    Migration and flood suffixes preserve their extracted DC or wait duration;
    generated schema classes take precedence, followed by known exact errors and
    numeric status classes. Unknown errors are returned unchanged.

    Args:
        error: Raw or already classified RPC error to inspect.

    Returns:
        The same instance when no classification applies, otherwise a specific
        error that preserves message, code, request and context.
    """
    raw_message = str(error.message).strip()
    upper_message = raw_message.upper()
    if migration_match := _MIGRATION_RE.match(upper_message):
        cls = _ERROR_CLASS_BY_TEMPLATE.get(f"{migration_match.group('kind')}_MIGRATE_%d", DatacenterMigration)
        return _instantiate_migration_error(cls, migration_match, error)
    if flood_match := _FLOOD_RE.match(upper_message):
        template = f"{flood_match.group('kind')}_%d"
        if template in _PACING_WAIT_TEMPLATES:
            cls = _ERROR_CLASS_BY_TEMPLATE.get(template, FloodWait)
            return _instantiate_flood_error(cls, flood_match, error)
    template, _values = _template_from_message(raw_message)
    cls = _ERROR_CLASS_BY_TEMPLATE.get(template) or _ERROR_CLASS_BY_TEMPLATE.get(upper_message)
    if cls is not None:
        return _instantiate_error_class(cls, error)
    if exact_base := _COMMON_EXACT_BASES.get(upper_message):
        return _instantiate_error_class(exact_base, error)
    if error.code == 400:
        return BadRequest(error.message, request=error.request, context=error.context)
    if error.code == 401:
        return Unauthorized(error.message, request=error.request, context=error.context)
    if error.code == 403:
        return Forbidden(error.message, request=error.request, context=error.context)
    if error.code == 404:
        return NotFound(error.message, request=error.request, context=error.context)
    if error.code == -503:
        return RpcTimeout(error.message, code=error.code, request=error.request, context=error.context)
    if error.code is not None and error.code >= 500:
        return InternalServerError(error.message, code=error.code, request=error.request, context=error.context)
    return error


def _instantiate_migration_error(cls: type[RpcError], match: re.Match[str], error: RpcError) -> RpcError:
    """Instantiate generated or fallback migration errors with the parsed target DC.

    Args:
        cls: Generated or base error class selected for the migration template.
        match: Regex match containing Telegram's migration kind and target DC.
        error: Original raw RPC error whose diagnostics are retained.
    """
    dc_id = int(match.group("dc_id"))
    kind = match.group("kind").upper()
    if issubclass(cls, DatacenterMigration):
        return cast(
            RpcError, cls(dc_id, kind=kind, message=error.message, request=error.request, context=error.context)
        )
    return DatacenterMigration(dc_id, kind=kind, message=error.message, request=error.request, context=error.context)


def _instantiate_flood_error(cls: type[RpcError], match: re.Match[str], error: RpcError) -> RpcError:
    """Instantiate generated or fallback flood errors with parsed wait seconds.

    Args:
        cls: Generated or base error class selected for the flood template.
        match: Regex match containing Telegram's wait duration.
        error: Original raw RPC error whose diagnostics are retained.
    """
    seconds = int(match.group("seconds"))
    if issubclass(cls, FloodWait):
        return cast(
            RpcError,
            cls(seconds, message=error.message, code=error.code or 420, request=error.request, context=error.context),
        )
    return FloodWait(seconds, message=error.message, request=error.request, context=error.context)


def _instantiate_error_class(cls: type[RpcError], error: RpcError) -> RpcError:
    """Reconstruct a specific error while retaining raw diagnostic fields.

    Args:
        cls: More specific classified RPC error class to instantiate.
        error: Raw RPC error supplying message, code, request and context.
    """
    if issubclass(cls, FloodWait):
        _template, values = _template_from_message(error.message)
        seconds = values[0] if values else 0
        return cast(
            RpcError,
            cls(seconds, message=error.message, code=error.code or 420, request=error.request, context=error.context),
        )
    if issubclass(cls, DatacenterMigration):
        match = _MIGRATION_RE.match(error.message.upper())
        if match is not None:
            return _instantiate_migration_error(cls, match, error)
    if issubclass(cls, BadRequest):
        return cast(RpcError, cls(error.message, code=error.code or 400, request=error.request, context=error.context))
    if issubclass(cls, RpcTimeout):
        return cast(RpcError, cls(error.message, code=error.code, request=error.request, context=error.context))
    if issubclass(cls, InternalServerError):
        return cast(RpcError, cls(error.message, code=error.code, request=error.request, context=error.context))
    if cls.__bases__ == (RpcError,):
        return cls(error.message, code=error.code, request=error.request, context=error.context)
    return cls(error.message, request=error.request, context=error.context)


def _register_generated_rpc_error_classes() -> None:
    """Create and register schema-derived RPC error classes at module import time."""
    from miniproto.raw.errors import RPC_ERROR_MAP

    for (name, code), spec in RPC_ERROR_MAP.items():
        template = _canonical_error_template(name)
        class_name = _error_class_name(name)
        if class_name in globals():
            cls = cast(type[RpcError], globals()[class_name])
        else:
            cls = _make_rpc_error_class(class_name, name, code, spec.description)
            globals()[class_name] = cls
            _GENERATED_ERROR_CLASS_NAMES.add(class_name)
        _ERROR_CLASS_BY_TEMPLATE[template] = cls


def _make_rpc_error_class(class_name: str, name: str, code: int, description: str) -> type[RpcError]:
    """Build one public schema-derived error subclass with stable metadata.

    Args:
        class_name: Python class name generated from Telegram's symbolic error name.
        name: Canonical Telegram RPC error template.
        code: Numeric Telegram RPC error code.
        description: Schema-provided class documentation, when available.
    """
    base = _base_for_error(name, code)
    namespace: dict[str, object] = {
        "RPC_ERROR_NAME": name,
        "RPC_ERROR_CODE": code,
        "__doc__": description or f"Telegram RPC error {name}.",
    }
    if issubclass(base, DatacenterMigration):
        namespace["MIGRATION_KIND"] = name.split("_MIGRATE", 1)[0]
    return type(class_name, (base,), namespace)


def _base_for_error(name: str, code: int) -> type[RpcError]:
    """Select the semantic base class from a schema name template and code.

    Args:
        name: Telegram symbolic error name or template.
        code: Telegram numeric RPC error code.
    """
    upper_name = _canonical_error_template(name)
    if _TEMPLATE_INT_RE.search(upper_name) and "_MIGRATE_" in upper_name:
        return DatacenterMigration
    if upper_name in _PACING_WAIT_TEMPLATES:
        return FloodWait
    if upper_name in _COMMON_EXACT_BASES:
        return _COMMON_EXACT_BASES[upper_name]
    if code == 400:
        return BadRequest
    if code == 401:
        return Unauthorized
    if code == 403:
        return Forbidden
    if code == 404:
        return NotFound
    if code == -503:
        return RpcTimeout
    if code >= 500:
        return InternalServerError
    return RpcError


def _template_from_message(message: str) -> tuple[str, tuple[int, ...]]:
    """Canonicalize one trailing numeric error argument as a ``%d`` template.

    Args:
        message: Raw Telegram error text to normalize.
    """
    raw = message.strip().upper()
    values: list[int] = []
    if match := _TRAILING_INT_RE.match(raw):
        values.append(int(match.group("value")))
        raw = f"{match.group('prefix')}_%d"
    return raw, tuple(values)


def _canonical_error_template(name: str) -> str:
    """Normalize schema template case and integer placeholder spelling.

    Args:
        name: Schema error name/template to normalize.
    """
    return name.upper().replace("%D", "%d")


def _error_class_name(name: str) -> str:
    """Convert an RPC symbolic name into a deterministic Python class name.

    Args:
        name: Telegram symbolic error name or template.
    """
    cleaned = _TEMPLATE_INT_RE.sub("", name).strip("_")
    parts = [part for part in re.split(r"[^0-9A-Za-z]+", cleaned) if part]
    if not parts:
        return "UnknownRpcError"
    rendered = "".join(_class_name_part(part) for part in parts)
    if rendered[0].isdigit():
        rendered = f"Rpc{rendered}"
    return rendered


def _class_name_part(part: str) -> str:
    """Render one symbolic-name component as a Python class-name component.

    Args:
        part: One alphanumeric segment of a symbolic Telegram error name.
    """
    upper = part.upper()
    if upper == "2FA":
        return "TwoFa"
    if part.isdigit():
        return part
    return part[:1].upper() + part[1:].lower()


def _result_type_name(value: object) -> str:
    """Return a protocol-aware diagnostic name for an unexpected result value.

    Args:
        value: Decoded RPC result whose type needs a protocol-aware name.
    """
    if isinstance(value, bool):
        return "Bool"
    if isinstance(value, tuple):
        return "Vector"
    return str(getattr(type(value), "RESULT_TYPE", type(value).__name__))


_register_generated_rpc_error_classes()
FloodPremiumWait = cast(type[FloodWait], globals()["FloodPremiumWait"])
PhoneCodeInvalid = cast(type[InvalidCode], globals()["PhoneCodeInvalid"])

__all__ = tuple(
    sorted(
        {
            "AuthError",
            "AuthKeyNotFound",
            "AuthKeyRegenerationRequired",
            "AmbiguousRpcResult",
            "BadRequest",
            "ClientDisconnected",
            "DatacenterMigration",
            "FloodWait",
            "Forbidden",
            "InternalServerError",
            "InvalidCode",
            "InvalidDatacenter",
            "InvokeError",
            "MiniprotoError",
            "NotFound",
            "PasswordInvalid",
            "PasswordRequired",
            "PendingRpcLimitExceeded",
            "ProtocolValidationError",
            "RequestTimeout",
            "ResultTypeMismatch",
            "RpcError",
            "RpcTimeout",
            "SessionEnvelopeError",
            "SessionStorageError",
            "SignUpRequired",
            "TransportFlood",
            "Unauthorized",
            "classify_rpc_error",
            *_GENERATED_ERROR_CLASS_NAMES,
        }
    )
)
