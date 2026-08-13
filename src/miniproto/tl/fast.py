from __future__ import annotations

from importlib import import_module
from typing import Any

_native_encode: Any | None = None
_native_decode: Any | None = None
try:
    _native = import_module("miniproto._native")
except Exception:
    _native = None
else:
    _native_encode = getattr(_native, "tl_fast_encode", None)
    _native_decode = getattr(_native, "tl_fast_decode", None)


def encode_fast(constructor_id: int, values: tuple[object, ...], *, boxed: bool = True) -> bytes | None:
    if _native_encode is None:
        return None
    result = _native_encode(constructor_id & 0xFFFFFFFF, values, boxed)
    return None if result is None else bytes(result)


def decode_fast(
    constructor_id: int, data: bytes | memoryview, offset: int = 0, *, boxed: bool = True
) -> tuple[tuple[object, ...], int] | None:
    if _native_decode is None or isinstance(data, memoryview):
        return None
    result = _native_decode(constructor_id & 0xFFFFFFFF, data, offset, boxed)
    if result is None:
        return None
    values, cursor = result
    return tuple(values), int(cursor)


def materialize_empty_object(constructor_id: object) -> object:
    from miniproto.raw import types

    if not isinstance(constructor_id, int):
        raise TypeError("native TL empty-object token must be an integer constructor ID")
    cls = types.CONSTRUCTOR_ID_MAP[constructor_id & 0xFFFFFFFF]
    if cls.TL_FIELDS:
        raise TypeError(f"native TL empty-object token resolved to non-empty {cls.QUALNAME}")
    return cls()


def native_fast_paths_available() -> bool:
    return _native_encode is not None and _native_decode is not None


__all__ = ["decode_fast", "encode_fast", "materialize_empty_object", "native_fast_paths_available"]
