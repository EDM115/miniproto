"""Optional native fast paths for selected generated TL constructors."""

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
    """Attempt native serialization for a generated TL constructor.

    Args:
        constructor_id: Unsigned 32-bit TL constructor identifier.
        values: Constructor field values in generated-field order.
        boxed: Whether the wire value includes its constructor identifier.

    Returns:
        Encoded bytes when the native fast path accepts the constructor, otherwise ``None``.
    """
    if _native_encode is None:
        return None
    result = _native_encode(constructor_id & 0xFFFFFFFF, values, boxed)
    return None if result is None else bytes(result)


def decode_fast(
    constructor_id: int, data: bytes | memoryview, offset: int = 0, *, boxed: bool = True
) -> tuple[tuple[object, ...], int] | None:
    """Attempt native deserialization for a generated TL constructor.

    Args:
        constructor_id: Unsigned 32-bit TL constructor identifier.
        data: Wire bytes; memoryviews deliberately use the Python path.
        offset: Initial byte offset, defaulting to ``0``.
        boxed: Whether the input includes a constructor identifier.

    Returns:
        Decoded field values and next offset, or ``None`` when no fast path applies.
    """
    if _native_decode is None or isinstance(data, memoryview):
        return None
    result = _native_decode(constructor_id & 0xFFFFFFFF, data, offset, boxed)
    if result is None:
        return None
    values, cursor = result
    return tuple(values), int(cursor)


def materialize_empty_object(constructor_id: object) -> object:
    """Resolve a native empty-object token to its generated TL instance.

    Args:
        constructor_id: Integer TL constructor identifier returned by native code.

    Returns:
        A newly constructed generated object with no TL fields.

    Raises:
        TypeError: If the token is not an integer or resolves to a non-empty constructor.
        KeyError: If no generated constructor has the identifier.
    """
    from miniproto.raw import types

    if not isinstance(constructor_id, int):
        raise TypeError("native TL empty-object token must be an integer constructor ID")
    cls = types.CONSTRUCTOR_ID_MAP[constructor_id & 0xFFFFFFFF]
    if cls.TL_FIELDS:
        raise TypeError(f"native TL empty-object token resolved to non-empty {cls.QUALNAME}")
    return cls()


def native_fast_paths_available() -> bool:
    """Report whether both native TL encode and decode fast paths were imported."""
    return _native_encode is not None and _native_decode is not None


__all__ = ["decode_fast", "encode_fast", "materialize_empty_object", "native_fast_paths_available"]
