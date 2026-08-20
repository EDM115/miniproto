"""Conservative redaction helpers for logs, metrics, and diagnostic representations."""

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
    r"(?P<prefix>\b(?:api[_-]?hash|phone(?:[_-]?number)?|auth[_-]?key|session[_-]?(?:key|blob)|raw[_-]?session|bot[_-]?token|password|passcode|proxy(?:[_-]?(?:url|password))?|token|secret)\b\s*[:=]\s*)"
    r'(?:"(?P<double>(?:\\.|[^"\\])*)(?:"|$)|\'(?P<single>(?:\\.|[^\'\\])*)(?:\'|$)|(?P<bare>[^\'"\s,;)}\]]+))',
    re.IGNORECASE,
)


def is_sensitive_key(key: object) -> bool:
    """Return whether a mapping key is recognized as sensitive.

    Args:
        key: Arbitrary mapping key converted to text for normalization.

    Returns:
        ``True`` for known secret-bearing key names or compound variants.
    """
    normalized = _normalize_key(str(key))
    if normalized in _SENSITIVE_KEY_TOKENS:
        return True
    if normalized.endswith("_token") or normalized.endswith("_secret"):
        return True
    return any(token in normalized for token in _SENSITIVE_KEY_TOKENS if token not in {"token", "secret"})


def redact_value(value: object) -> str:
    """Replace a value with the fixed redaction marker.

    Args:
        value: Value deliberately ignored so secrets never reach output.

    Returns:
        The constant ``"[redacted]"`` marker.
    """
    return REDACTED


def redact_mapping(data: Mapping[Any, Any]) -> dict[str, Any]:
    """Return a recursively sanitized copy of a mapping.

    Args:
        data: Mapping whose keys and nested values may contain credentials.

    Returns:
        A string-keyed mapping with recognized sensitive values replaced.
    """
    return {
        str(key): redact_value(value) if is_sensitive_key(key) else _redact_nested(value) for key, value in data.items()
    }


def redact_text(text: str) -> str:
    """Mask recognized ``key=value`` and ``key: value`` secrets in text.

    Args:
        text: Text that may contain supported sensitive assignments.

    Returns:
        Text with matched values replaced by the redaction marker.
    """
    return _SENSITIVE_TEXT_RE.sub(_replace_sensitive_text, text)


def _replace_sensitive_text(match: re.Match[str]) -> str:
    """Replace one complete sensitive assignment while preserving its quote style.

    Args:
        match: Assignment match produced by ``_SENSITIVE_TEXT_RE``.

    Returns:
        Original assignment prefix followed by one quoted or bare redaction marker.
    """
    if match.group("double") is not None:
        replacement = f'"{REDACTED}"'
    elif match.group("single") is not None:
        replacement = f"'{REDACTED}'"
    else:
        replacement = REDACTED
    return f"{match.group('prefix')}{replacement}"


def safe_repr(value: object) -> str:
    """Return a representation after recursively redacting supported secret shapes.

    Args:
        value: Arbitrary value intended for diagnostic output.

    Returns:
        The safe representation of the redacted value.
    """
    return repr(_redact_nested(value))


def _redact_nested(value: object) -> object:
    """Recursively sanitize mappings, dataclasses, sequences, binary values, and text.

    Args:
        value: Arbitrary nested value whose supported secret assignments must be redacted.
    """
    if getattr(value, "__miniproto_secret__", False) is True:
        return REDACTED
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
    """Describe binary data by type and byte length without exposing its contents.

    Args:
        value: Binary value whose contents must remain undisclosed.
    """
    view = memoryview(value)
    return f"<{type(value).__name__} len={view.nbytes}>"


def _normalize_key(key: str) -> str:
    """Canonicalize a key before matching it against sensitive-key tokens.

    Args:
        key: Mapping key text to normalize for secret-name matching.
    """
    return re.sub(r"[^a-z0-9]+", "_", key.casefold()).strip("_")
