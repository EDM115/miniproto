from __future__ import annotations

from dataclasses import dataclass


class MiniprotoError(Exception):
    """Base exception for miniproto."""


@dataclass(slots=True)
class RpcError(MiniprotoError):
    message: str
    code: int | None = None
    request: object | None = None

    def __str__(self) -> str:
        if self.code is None:
            return self.message
        return f"[{self.code}] {self.message}"


class Unauthorized(RpcError):
    def __init__(self, message: str = "unauthorized") -> None:
        super().__init__(message=message, code=401)


class FloodWait(RpcError):
    def __init__(self, seconds: int, message: str | None = None) -> None:
        self.seconds = seconds
        super().__init__(message=message or f"flood wait for {seconds} seconds", code=420)
