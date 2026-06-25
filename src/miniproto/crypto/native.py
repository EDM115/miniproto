from __future__ import annotations

from importlib import import_module
from typing import Protocol, cast


class _NativeModule(Protocol):
    def native_available(self) -> bool: ...

    def xor_bytes(self, left: bytes, right: bytes) -> bytes: ...


try:
    _native_impl = cast(_NativeModule, import_module("miniproto._native"))
except ImportError:
    _native_impl = cast(_NativeModule, import_module("miniproto._native_fallback"))


def native_available() -> bool:
    return bool(_native_impl.native_available())


def xor_bytes(left: bytes, right: bytes) -> bytes:
    return bytes(_native_impl.xor_bytes(left, right))
