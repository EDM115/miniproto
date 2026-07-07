from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, cast

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

    @property
    def rpc_error_name(self) -> str:
        return str(getattr(type(self), "RPC_ERROR_NAME", self.message))

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


class InvokeError(RpcError):
    """Base exception for raw invocation failures before Telegram returns a typed RPC error."""


class ClientDisconnected(InvokeError):
    def __init__(
        self,
        message: str = "client disconnected",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, request=request, context=context)


class RequestTimeout(InvokeError):
    def __init__(
        self,
        message: str = "request timed out",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, request=request, context=context)


class ResultTypeMismatch(InvokeError):
    def __init__(self, expected: str, actual: object, *, request: object | None = None) -> None:
        self.expected = expected
        self.actual = actual
        super().__init__(
            message=f"RPC result type mismatch: expected {expected}, got {_result_type_name(actual)}",
            request=request,
            context={"expected": expected, "actual": _result_type_name(actual)},
        )


class BadRequest(RpcError):
    def __init__(
        self,
        message: str = "bad request",
        *,
        code: int = 400,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, request=request, context=context)


class Unauthorized(RpcError):
    def __init__(
        self,
        message: str = "unauthorized",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=401, request=request, context=context)


class Forbidden(RpcError):
    def __init__(
        self,
        message: str = "forbidden",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=403, request=request, context=context)


class NotFound(RpcError):
    def __init__(
        self,
        message: str = "not found",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=404, request=request, context=context)


class RpcTimeout(RpcError):
    def __init__(
        self,
        message: str = "RPC timeout",
        *,
        code: int | None = -503,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, request=request, context=context)


class InternalServerError(RpcError):
    def __init__(
        self,
        message: str = "internal server error",
        *,
        code: int | None = 500,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, request=request, context=context)


class FloodWait(RpcError):
    def __init__(
        self,
        seconds: int,
        message: str | None = None,
        *,
        code: int = 420,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        self.seconds = seconds
        super().__init__(
            message=message or f"flood wait for {seconds} seconds",
            code=code,
            request=request,
            context=context,
        )


class AuthError(RpcError):
    """Base exception for authentication and authorization flow failures."""


class InvalidCode(AuthError):
    def __init__(
        self,
        message: str = "invalid phone code",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=400, request=request, context=context)


class PasswordRequired(AuthError):
    def __init__(
        self,
        message: str = "2FA password required",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=401, request=request, context=context)


class PasswordInvalid(AuthError):
    def __init__(
        self,
        message: str = "invalid 2FA password",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=400, request=request, context=context)


class SignUpRequired(AuthError):
    def __init__(
        self,
        message: str = "sign-up required",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=401, request=request, context=context)


class AuthKeyNotFound(AuthError):
    def __init__(
        self,
        message: str = "auth key not registered",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=401, request=request, context=context)


class AuthKeyRegenerationRequired(AuthError):
    def __init__(
        self,
        message: str = "auth key must be regenerated",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=406, request=request, context=context)


class InvalidDatacenter(AuthError):
    def __init__(
        self,
        message: str = "invalid datacenter",
        *,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=303, request=request, context=context)


class DatacenterMigration(InvalidDatacenter):
    def __init__(
        self,
        dc_id: int,
        *,
        kind: str = "MIGRATE",
        message: str | None = None,
        request: object | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> None:
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


_MIGRATION_RE = re.compile(
    r"^(?P<kind>NETWORK|PHONE|STATS|USER|FILE)_MIGRATE_(?P<dc_id>\d+)$", re.IGNORECASE
)
_FLOOD_RE = re.compile(r"^(?P<kind>[A-Z0-9_]*WAIT)_(?P<seconds>\d+)$", re.IGNORECASE)
_TRAILING_INT_RE = re.compile(r"^(?P<prefix>.+)_(?P<value>\d+)$")
_TEMPLATE_INT_RE = re.compile(r"%d", re.IGNORECASE)
_AUTH_KEY_NOT_FOUND = {"AUTH_KEY_INVALID", "AUTH_KEY_PERM_EMPTY", "AUTH_KEY_UNREGISTERED"}
_AUTH_KEY_REGENERATE = {"AUTH_KEY_DUPLICATED", "AUTH_KEY_UNSYNCHRONIZED"}
_INVALID_CODE = {
    "PHONE_CODE_EMPTY",
    "PHONE_CODE_EXPIRED",
    "PHONE_CODE_HASH_EMPTY",
    "PHONE_CODE_INVALID",
}
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
    raw_message = str(error.message).strip()
    upper_message = raw_message.upper()
    if migration_match := _MIGRATION_RE.match(upper_message):
        cls = _ERROR_CLASS_BY_TEMPLATE.get(
            f"{migration_match.group('kind')}_MIGRATE_%d", DatacenterMigration
        )
        return _instantiate_migration_error(cls, migration_match, error)
    if flood_match := _FLOOD_RE.match(upper_message):
        template = f"{flood_match.group('kind')}_%d"
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
        return RpcTimeout(
            error.message, code=error.code, request=error.request, context=error.context
        )
    if error.code is not None and error.code >= 500:
        return InternalServerError(
            error.message, code=error.code, request=error.request, context=error.context
        )
    return error


def _instantiate_migration_error(
    cls: type[RpcError], match: re.Match[str], error: RpcError
) -> RpcError:
    dc_id = int(match.group("dc_id"))
    kind = match.group("kind").upper()
    if issubclass(cls, DatacenterMigration):
        return cast(
            RpcError,
            cls(
                dc_id,
                kind=kind,
                message=error.message,
                request=error.request,
                context=error.context,
            ),
        )
    return DatacenterMigration(
        dc_id, kind=kind, message=error.message, request=error.request, context=error.context
    )


def _instantiate_flood_error(
    cls: type[RpcError], match: re.Match[str], error: RpcError
) -> RpcError:
    seconds = int(match.group("seconds"))
    if issubclass(cls, FloodWait):
        return cast(
            RpcError,
            cls(
                seconds,
                message=error.message,
                code=error.code or 420,
                request=error.request,
                context=error.context,
            ),
        )
    return FloodWait(seconds, message=error.message, request=error.request, context=error.context)


def _instantiate_error_class(cls: type[RpcError], error: RpcError) -> RpcError:
    if issubclass(cls, FloodWait):
        _template, values = _template_from_message(error.message)
        seconds = values[0] if values else 0
        return cast(
            RpcError,
            cls(
                seconds,
                message=error.message,
                code=error.code or 420,
                request=error.request,
                context=error.context,
            ),
        )
    if issubclass(cls, DatacenterMigration):
        match = _MIGRATION_RE.match(error.message.upper())
        if match is not None:
            return _instantiate_migration_error(cls, match, error)
    if issubclass(cls, BadRequest):
        return cast(
            RpcError,
            cls(
                error.message, code=error.code or 400, request=error.request, context=error.context
            ),
        )
    if issubclass(cls, RpcTimeout):
        return cast(
            RpcError,
            cls(error.message, code=error.code, request=error.request, context=error.context),
        )
    if issubclass(cls, InternalServerError):
        return cast(
            RpcError,
            cls(error.message, code=error.code, request=error.request, context=error.context),
        )
    return cls(error.message, request=error.request, context=error.context)


def _register_generated_rpc_error_classes() -> None:
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


def _make_rpc_error_class(
    class_name: str, name: str, code: int, description: str
) -> type[RpcError]:
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
    upper_name = _canonical_error_template(name)
    if _TEMPLATE_INT_RE.search(upper_name) and "_MIGRATE_" in upper_name:
        return DatacenterMigration
    if _TEMPLATE_INT_RE.search(upper_name) and upper_name.endswith("WAIT_%d"):
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
    raw = message.strip().upper()
    values: list[int] = []
    if match := _TRAILING_INT_RE.match(raw):
        values.append(int(match.group("value")))
        raw = f"{match.group('prefix')}_%d"
    return raw, tuple(values)


def _canonical_error_template(name: str) -> str:
    return name.upper().replace("%D", "%d")


def _error_class_name(name: str) -> str:
    cleaned = _TEMPLATE_INT_RE.sub("", name).strip("_")
    parts = [part for part in re.split(r"[^0-9A-Za-z]+", cleaned) if part]
    if not parts:
        return "UnknownRpcError"
    rendered = "".join(_class_name_part(part) for part in parts)
    if rendered[0].isdigit():
        rendered = f"Rpc{rendered}"
    return rendered


def _class_name_part(part: str) -> str:
    upper = part.upper()
    if upper == "2FA":
        return "TwoFa"
    if part.isdigit():
        return part
    return part[:1].upper() + part[1:].lower()


def _result_type_name(value: object) -> str:
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
