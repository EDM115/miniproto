from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import fields, is_dataclass
from typing import Any

REDACTED = "[redacted]"

_SENSITIVE_KEY_TOKENS = frozenset(
    {
        "api_hash",
        "apihash",
        "phone",
        "phone_number",
        "phonenumber",
        "auth_key",
        "authkey",
        "session_key",
        "sessionkey",
        "session_blob",
        "sessionblob",
        "raw_session",
        "rawsession",
        "bot_token",
        "bottoken",
        "password",
        "passcode",
        "proxy",
        "proxy_url",
        "proxyurl",
        "proxy_password",
        "proxypassword",
        "token",
        "secret",
    }
)
_SENSITIVE_TEXT_RE = re.compile(
    r"(?P<prefix>\b(?:api[_-]?hash|phone(?:[_-]?number)?|auth[_-]?key|session[_-]?(?:key|blob)|raw[_-]?session|bot[_-]?token|password|passcode|proxy(?:[_-]?(?:url|password))?|token|secret)\b\s*[:=]\s*)(?P<quote>['\"]?)(?P<value>[^'\"\s,;)}\]]+)",
    re.IGNORECASE,
)


def is_sensitive_key(key: object) -> bool:
    normalized = _normalize_key(str(key))
    if normalized in _SENSITIVE_KEY_TOKENS:
        return True
    return any(
        token in normalized for token in _SENSITIVE_KEY_TOKENS if token not in {"token", "secret"}
    )


def redact_value(value: object) -> str:
    return REDACTED


def redact_mapping(data: Mapping[Any, Any]) -> dict[str, Any]:
    return {
        str(key): redact_value(value) if is_sensitive_key(key) else _redact_nested(value)
        for key, value in data.items()
    }


def redact_text(text: str) -> str:
    return _SENSITIVE_TEXT_RE.sub(
        lambda match: f"{match.group('prefix')}{match.group('quote')}{REDACTED}", text
    )


def safe_repr(value: object) -> str:
    return repr(_redact_nested(value))


def _redact_nested(value: object) -> object:
    if isinstance(value, bytes | bytearray | memoryview):
        return _binary_summary(value)
    if isinstance(value, Mapping):
        return redact_mapping(value)
    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: redact_value(getattr(value, field.name))
            if is_sensitive_key(field.name)
            else _redact_nested(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, tuple):
        return tuple(_redact_nested(item) for item in value)
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray | memoryview):
        return [_redact_nested(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def _binary_summary(value: bytes | bytearray | memoryview) -> str:
    view = memoryview(value)
    return f"<{type(value).__name__} len={view.nbytes}>"


def _normalize_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.casefold()).strip("_")
