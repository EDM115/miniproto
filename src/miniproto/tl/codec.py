from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any, cast

from miniproto.crypto import native as _native

VECTOR_CONSTRUCTOR_ID = 0x1CB5C415
BOOL_FALSE_ID = 0xBC799737
BOOL_TRUE_ID = 0x997275B5
_PRIMITIVES = {
    "int",
    "#",
    "long",
    "int128",
    "int256",
    "double",
    "bytes",
    "string",
    "Bool",
    "bool",
    "true",
}
_VECTOR_RE = re.compile(r"^[Vv]ector[< ](?P<inner>.+?)[>)]?$")


class TLCodecError(ValueError):
    pass


def encode_int(value: int) -> bytes:
    return _native.tl_encode_int(value)


def decode_int(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]:
    return _native.tl_decode_int(bytes(data), offset)


def encode_uint(value: int) -> bytes:
    return _native.tl_encode_uint(value)


def decode_uint(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]:
    return _native.tl_decode_uint(bytes(data), offset)


def encode_constructor_id(value: int) -> bytes:
    return encode_uint(value & 0xFFFFFFFF)


def decode_constructor_id(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]:
    return decode_uint(data, offset)


def encode_long(value: int) -> bytes:
    return _native.tl_encode_long(value)


def decode_long(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]:
    return _native.tl_decode_long(bytes(data), offset)


def encode_int128(value: int) -> bytes:
    return _native.tl_encode_int128(value)


def decode_int128(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]:
    return _native.tl_decode_int128(bytes(data), offset)


def encode_int256(value: int) -> bytes:
    return _native.tl_encode_int256(value)


def decode_int256(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]:
    return _native.tl_decode_int256(bytes(data), offset)


def encode_double(value: float) -> bytes:
    return _native.tl_encode_double(value)


def decode_double(data: bytes | memoryview, offset: int = 0) -> tuple[float, int]:
    return _native.tl_decode_double(bytes(data), offset)


def encode_bytes(value: bytes) -> bytes:
    return _native.tl_encode_bytes(value)


def decode_bytes(data: bytes | memoryview, offset: int = 0) -> tuple[bytes, int]:
    return _native.tl_decode_bytes(bytes(data), offset)


def encode_string(value: str) -> bytes:
    return _native.tl_encode_string(value)


def decode_string(data: bytes | memoryview, offset: int = 0) -> tuple[str, int]:
    return _native.tl_decode_string(bytes(data), offset)


def encode_bool(value: bool) -> bytes:
    return encode_constructor_id(BOOL_TRUE_ID if value else BOOL_FALSE_ID)


def decode_bool(data: bytes | memoryview, offset: int = 0) -> tuple[bool, int]:
    constructor_id, offset = decode_constructor_id(data, offset)
    if constructor_id == BOOL_TRUE_ID:
        return True, offset
    if constructor_id == BOOL_FALSE_ID:
        return False, offset
    raise TLCodecError(f"expected Bool constructor, got 0x{constructor_id:08x}")


def encode_vector(values: Iterable[Any], item_type: str) -> bytes:
    items = tuple(values)
    clean_item_type = _clean_type(item_type)
    if clean_item_type in {"int", "#"}:
        return _native.tl_encode_int_vector(int(item) for item in items)
    if clean_item_type == "long":
        return _native.tl_encode_long_vector(int(item) for item in items)
    output = bytearray(encode_constructor_id(VECTOR_CONSTRUCTOR_ID))
    output.extend(encode_int(len(items)))
    for item in items:
        output.extend(encode_value(item_type, item))
    return bytes(output)


def decode_vector(
    data: bytes | memoryview, offset: int, item_type: str
) -> tuple[tuple[Any, ...], int]:
    clean_item_type = _clean_type(item_type)
    if clean_item_type in {"int", "#"}:
        return _native.tl_decode_int_vector(bytes(data), offset)
    if clean_item_type == "long":
        return _native.tl_decode_long_vector(bytes(data), offset)
    constructor_id, offset = decode_constructor_id(data, offset)
    if constructor_id != VECTOR_CONSTRUCTOR_ID:
        raise TLCodecError(f"expected Vector constructor, got 0x{constructor_id:08x}")
    count, offset = decode_int(data, offset)
    if count < 0:
        raise TLCodecError("TL vector count cannot be negative")
    values: list[Any] = []
    for _ in range(count):
        value, offset = decode_value(item_type, data, offset)
        values.append(value)
    return tuple(values), offset


def serialize_object(obj: Any, *, boxed: bool = True) -> bytes:
    cls = type(obj)
    if not _looks_like_tl_class(cls):
        raise TLCodecError(f"expected TL object, got {type(obj).__name__}")
    output = bytearray()
    if boxed:
        output.extend(encode_constructor_id(int(cls.CONSTRUCTOR_ID)))
    output.extend(_serialize_fields(obj, cls))
    return bytes(output)


def deserialize_object[TLObjectT](
    cls: type[TLObjectT], data: bytes | memoryview, offset: int = 0, *, boxed: bool = True
) -> tuple[TLObjectT, int]:
    if not _looks_like_tl_class(cls):
        raise TLCodecError(f"expected TL object class, got {cls!r}")
    if boxed:
        constructor_id, offset = decode_constructor_id(data, offset)
        expected = int(cast(Any, cls).CONSTRUCTOR_ID)
        if constructor_id != expected:
            raise TLCodecError(f"expected constructor 0x{expected:08x}, got 0x{constructor_id:08x}")
    values, offset = _deserialize_fields(cls, data, offset)
    return cls(**values), offset


def decode_object(
    data: bytes | memoryview, offset: int = 0, expected_type: str | None = None
) -> tuple[Any, int]:
    if expected_type is not None and _clean_type(expected_type) in _PRIMITIVES:
        return decode_value(expected_type, data, offset)
    constructor_id, value_offset = decode_constructor_id(data, offset)
    if constructor_id == BOOL_TRUE_ID:
        return True, value_offset
    if constructor_id == BOOL_FALSE_ID:
        return False, value_offset
    cls = _constructor_maps().get(constructor_id)
    if cls is None:
        raise TLCodecError(f"unknown TL constructor 0x{constructor_id:08x}")
    values, new_offset = _deserialize_fields(cls, data, value_offset)
    return cls(**values), new_offset


def encode_value(type_name: str, value: Any) -> bytes:
    clean = _clean_type(type_name)
    vector_item_type = _vector_item_type(clean)
    if vector_item_type is not None:
        return encode_vector(cast(Iterable[Any], value), vector_item_type)
    match clean:
        case "int" | "#":
            return encode_int(cast(int, value))
        case "long":
            return encode_long(cast(int, value))
        case "int128":
            return encode_int128(cast(int, value))
        case "int256":
            return encode_int256(cast(int, value))
        case "double":
            return encode_double(cast(float, value))
        case "bytes":
            return encode_bytes(cast(bytes, value))
        case "string":
            return encode_string(cast(str, value))
        case "Bool" | "bool":
            return encode_bool(cast(bool, value))
        case "true":
            return b""
        case _:
            if _looks_like_tl_object(value):
                return serialize_object(value, boxed=not _is_bare_type(type_name))
            raise TLCodecError(f"cannot serialize TL value of type {type_name!r}")


def decode_value(type_name: str, data: bytes | memoryview, offset: int) -> tuple[Any, int]:
    clean = _clean_type(type_name)
    vector_item_type = _vector_item_type(clean)
    if vector_item_type is not None:
        return decode_vector(data, offset, vector_item_type)
    match clean:
        case "int" | "#":
            return decode_int(data, offset)
        case "long":
            return decode_long(data, offset)
        case "int128":
            return decode_int128(data, offset)
        case "int256":
            return decode_int256(data, offset)
        case "double":
            return decode_double(data, offset)
        case "bytes":
            return decode_bytes(data, offset)
        case "string":
            return decode_string(data, offset)
        case "Bool" | "bool":
            return decode_bool(data, offset)
        case "true":
            return True, offset
        case _:
            if _is_bare_type(type_name):
                raise TLCodecError(
                    f"cannot deserialize bare TL value {type_name!r} without a concrete class"
                )
            return decode_object(data, offset, clean)


def _serialize_fields(obj: Any, cls: type[Any]) -> bytes:
    fields = tuple(getattr(cls, "TL_FIELDS", ()))
    flag_groups = tuple(getattr(cls, "TL_FLAG_GROUPS", ()))
    flag_values = _flag_values(obj, fields)
    output = bytearray()
    groups_by_index = _flag_groups_by_index(flag_groups)
    for index, field in enumerate(fields):
        for group in groups_by_index.get(index, ()):
            output.extend(encode_int(flag_values.get(group.name, 0)))
        if field.is_optional:
            value = getattr(obj, field.python_name)
            if field.is_true_flag or value is None:
                continue
        else:
            value = getattr(obj, field.python_name)
        output.extend(encode_value(field.type, value))
    for group in groups_by_index.get(len(fields), ()):
        output.extend(encode_int(flag_values.get(group.name, 0)))
    return bytes(output)


def _deserialize_fields(
    cls: type[Any], data: bytes | memoryview, offset: int
) -> tuple[dict[str, Any], int]:
    fields = tuple(getattr(cls, "TL_FIELDS", ()))
    flag_groups = tuple(getattr(cls, "TL_FLAG_GROUPS", ()))
    flag_values: dict[str, int] = {}
    values: dict[str, Any] = {}
    groups_by_index = _flag_groups_by_index(flag_groups)
    for index, field in enumerate(fields):
        for group in groups_by_index.get(index, ()):
            flag_values[group.name], offset = decode_int(data, offset)
        if field.is_optional:
            present = bool(flag_values.get(field.flag or "", 0) & (1 << int(field.flag_index or 0)))
            if field.is_true_flag:
                values[field.python_name] = present
                continue
            if not present:
                values[field.python_name] = None
                continue
        values[field.python_name], offset = decode_value(field.type, data, offset)
    for group in groups_by_index.get(len(fields), ()):
        flag_values[group.name], offset = decode_int(data, offset)
    return values, offset


def _flag_values(obj: Any, fields: tuple[Any, ...]) -> dict[str, int]:
    values: dict[str, int] = {}
    for field in fields:
        if not field.is_optional or field.flag is None or field.flag_index is None:
            continue
        value = getattr(obj, field.python_name)
        present = bool(value) if field.is_true_flag else value is not None
        if present:
            values[field.flag] = values.get(field.flag, 0) | (1 << field.flag_index)
    return values


def _flag_groups_by_index(flag_groups: tuple[Any, ...]) -> dict[int, tuple[Any, ...]]:
    grouped: dict[int, list[Any]] = {}
    for group in flag_groups:
        grouped.setdefault(int(group.before_field_index), []).append(group)
    return {index: tuple(groups) for index, groups in grouped.items()}


def _constructor_maps() -> dict[int, type[Any]]:
    from miniproto.raw import functions, types

    mapping: dict[int, type[Any]] = {}
    mapping.update(types.CONSTRUCTOR_ID_MAP)
    mapping.update(functions.CONSTRUCTOR_ID_MAP)
    return mapping


def _looks_like_tl_object(value: Any) -> bool:
    return _looks_like_tl_class(type(value))


def _looks_like_tl_class(cls: type[Any]) -> bool:
    return all(hasattr(cls, name) for name in ("CONSTRUCTOR_ID", "TL_FIELDS", "QUALNAME"))


def _clean_type(type_name: str) -> str:
    clean = type_name.removeprefix("!").strip()
    while clean.startswith("(") and clean.endswith(")"):
        clean = clean[1:-1].strip()
    return clean


def _is_bare_type(type_name: str) -> bool:
    clean = type_name.removeprefix("!").strip()
    if clean.startswith("%"):
        return True
    name = clean.rsplit(".", 1)[-1]
    return name[:1].islower() and clean not in _PRIMITIVES and _vector_item_type(clean) is None


def _vector_item_type(type_name: str) -> str | None:
    match = _VECTOR_RE.match(type_name)
    if match is None:
        return None
    return match.group("inner").strip()
