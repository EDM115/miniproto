from __future__ import annotations

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


class SessionStorageError(MiniprotoError):
    """Raised when session persistence cannot safely continue."""


class SessionEnvelopeError(SessionStorageError):
    """Raised when an encrypted session envelope fails validation or authentication."""
