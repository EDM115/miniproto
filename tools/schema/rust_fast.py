"""Validate reviewed TL fast paths and render their deterministic Rust and Python metadata."""

from __future__ import annotations

import hashlib
import json
import pprint
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from tools.schema.parser import TLEntry, TLParameter, TLSchema, iter_public_params

Direction = Literal["encode", "decode"]


@dataclass(frozen=True, slots=True)
class FastField:
    """One reviewed native-codec field, including wire and optional-flag metadata.

    Attributes:
        name: Original API parameter or static MTProto manifest field name.
        python_name: Python attribute name used when binding the field to generated metadata or a raw object.
        schema_type: Declared TL or reviewed static-manifest type before native wire-type classification.
        wire_type: Supported native codec representation selected for Rust fast-path rendering.
        value_index: Zero-based native value-slot index, or ``None`` for a flags-word field.
        flag_group: Zero-based flags-word group for a marker or optional field, or ``None`` when no flags word applies.
        flag_index: Bit index in ``flag_group`` that enables an optional field, or ``None`` for unconditional or marker fields.
    """

    name: str
    python_name: str
    schema_type: str
    wire_type: str
    value_index: int | None
    flag_group: int | None = None
    flag_index: int | None = None


@dataclass(frozen=True, slots=True)
class FastEntry:
    """One reviewed API or MTProto service constructor selected for native fast paths.

    Attributes:
        source: Provenance selector, ``"api"`` for parsed API schema entries or ``"mtproto"`` for reviewed service metadata.
        kind: API declaration kind or ``"service"`` for static MTProto entries.
        name: Qualified API declaration name or reviewed MTProto service name.
        python_type: Python class name used to identify the corresponding runtime constructor.
        constructor_id: Unsigned 32-bit wire constructor identifier selected for the native lookup table.
        directions: Immutable reviewed subset of allowed native ``"encode"`` and ``"decode"`` operations.
        fields: Ordered normalized field metadata, including flags words that do not consume value slots.
    """

    source: Literal["api", "mtproto"]
    kind: str
    name: str
    python_type: str
    constructor_id: int
    directions: frozenset[Direction]
    fields: tuple[FastField, ...]

    @property
    def value_fields(self) -> tuple[FastField, ...]:
        """Return fields that consume a native value-slot, excluding flag words."""
        return tuple(field for field in self.fields if field.value_index is not None)


def load_fast_entries(
    manifest_path: Path, schema_path: Path, schema_layer: int, schema: TLSchema
) -> tuple[FastEntry, ...]:
    """Load and validate the reviewed fixed-size Rust TL fast-path manifest.

    Args:
        manifest_path: Reviewed fast-path manifest JSON.
        schema_path: Pinned normalized schema JSON used for hash validation.
        schema_layer: Expected Telegram schema layer.
        schema: Parsed schema used to resolve API entries.

    Returns:
        Exactly 30 unique, validated reviewed fast-path entries.

    Raises:
        ValueError: Manifest version, provenance, selection, fields, or uniqueness validation fails.
    """
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != 1:
        raise ValueError("Rust TL fast-path manifest version must be 1")
    if manifest.get("schema_layer") != schema_layer:
        raise ValueError("Rust TL fast-path manifest layer does not match pinned schema metadata")
    actual_sha256 = hashlib.sha256(schema_path.read_bytes()).hexdigest()
    if manifest.get("schema_json_sha256") != actual_sha256:
        raise ValueError("Rust TL fast-path manifest schema hash is stale")
    by_key = {(entry.kind, entry.name): entry for entry in schema.entries}
    entries: list[FastEntry] = []
    for item in manifest.get("api", ()):
        kind = "function" if item.get("kind") == "function" else "type"
        name = str(item.get("name", ""))
        schema_entry = by_key.get((kind, name))
        if schema_entry is None:
            raise ValueError(f"Rust TL fast-path manifest references missing {kind} {name!r}")
        directions = _directions(item)
        fields = _api_fields(schema_entry)
        _validate_decode_fields(name, directions, fields)
        entries.append(
            FastEntry(
                source="api",
                kind=str(item["kind"]),
                name=name,
                python_type=schema_entry.python_class_name,
                constructor_id=schema_entry.constructor_id,
                directions=directions,
                fields=fields,
            )
        )
    for item in manifest.get("mtproto", ()):
        fields = tuple(
            FastField(
                name=str(field["name"]),
                python_name=str(field["name"]),
                schema_type=str(field["type"]),
                wire_type=_static_wire_type(str(field["type"])),
                value_index=index,
            )
            for index, field in enumerate(item.get("fields", ()))
        )
        directions = _directions(item)
        _validate_decode_fields(str(item["name"]), directions, fields)
        entries.append(
            FastEntry(
                source="mtproto",
                kind="service",
                name=str(item["name"]),
                python_type=str(item["python_type"]),
                constructor_id=int(str(item["constructor_id"]), 16),
                directions=directions,
                fields=fields,
            )
        )
    if len(entries) != 30:
        raise ValueError(f"Rust TL fast-path manifest must select exactly 30 reviewed constructors, got {len(entries)}")
    ids: set[int] = set()
    names: set[tuple[str, str]] = set()
    for entry in entries:
        if entry.constructor_id in ids:
            raise ValueError(f"duplicate Rust TL fast-path constructor ID 0x{entry.constructor_id:08x}")
        key = (entry.source, entry.name)
        if key in names:
            raise ValueError(f"duplicate Rust TL fast-path name {entry.source}:{entry.name}")
        ids.add(entry.constructor_id)
        names.add(key)
    return tuple(entries)


def render_rust(entries: tuple[FastEntry, ...], schema_layer: int, schema_sha256: str) -> str:
    """Render deterministic Rust specifications for reviewed fast-path constructors.

    Args:
        entries: Validated fast-path entries in manifest order.
        schema_layer: Pinned schema layer embedded in the generated header.
        schema_sha256: Pinned normalized schema digest embedded in the header.

    Returns:
        Generated Rust source defining field tables and constructor lookup.
    """
    lines = [
        "// Generated by tools/schema/generate.py; do not edit by hand.",
        f"// Layer {schema_layer}; normalized schema SHA-256 {schema_sha256}.",
        "",
        "use super::tl::{FastConstructorSpec, FastFieldSpec, FastWireType};",
        "",
    ]
    for index, entry in enumerate(entries):
        lines.append(f"const FIELDS_{index}: &[FastFieldSpec] = &[")
        for field in entry.fields:
            lines.append(f"    {_rust_field(field)},")
        lines.extend(["];"])
    lines.extend(["", "pub(crate) const FAST_CONSTRUCTORS: &[FastConstructorSpec] = &["])
    for index, entry in enumerate(entries):
        lines.extend(
            [
                "    FastConstructorSpec {",
                f"        constructor_id: 0x{entry.constructor_id:08x},",
                f"        name: {entry.name!r},".replace("'", '"'),
                f"        encode: {str('encode' in entry.directions).lower()},",
                f"        decode: {str('decode' in entry.directions).lower()},",
                f"        value_count: {len(entry.value_fields)},",
                f"        fields: FIELDS_{index},",
                "    },",
            ]
        )
    lines.extend(
        [
            "];",
            "",
            "pub(crate) fn fast_constructor(constructor_id: u32) -> Option<&'static FastConstructorSpec> {",
            "    match constructor_id {",
        ]
    )
    for index, entry in enumerate(entries):
        lines.append(f"        0x{entry.constructor_id:08x} => Some(&FAST_CONSTRUCTORS[{index}]),")
    lines.extend(["        _ => None,", "    }", "}", ""])
    return "\n".join(lines)


def render_python_metadata(entries: tuple[FastEntry, ...], schema_layer: int, schema_sha256: str) -> str:
    """Render generated Python metadata for the reviewed native TL fast paths.

    Args:
        entries: Validated fast-path entries in manifest order.
        schema_layer: Pinned schema layer embedded in the output.
        schema_sha256: Pinned normalized schema digest embedded in the output.

    Returns:
        Python module source beginning with its generated-metadata module docstring.
    """
    payload = []
    for entry in entries:
        payload.append(
            {
                "source": entry.source,
                "kind": entry.kind,
                "name": entry.name,
                "python_type": entry.python_type,
                "constructor_id": entry.constructor_id,
                "directions": sorted(entry.directions),
                "fields": [
                    {
                        "name": field.name,
                        "python_name": field.python_name,
                        "schema_type": field.schema_type,
                        "wire_type": field.wire_type,
                        "value_index": field.value_index,
                    }
                    for field in entry.fields
                ],
            }
        )
    rendered = pprint.pformat(payload, sort_dicts=True, width=120)
    return (
        '"""Generated metadata describing the TL constructors with native fast paths."""\n\n'
        "# Generated by tools/schema/generate.py; do not edit by hand.\n"
        "from __future__ import annotations\n\n"
        f"SCHEMA_LAYER = {schema_layer}\n"
        f"SCHEMA_JSON_SHA256 = {schema_sha256!r}\n"
        f"FAST_PATHS = {rendered}\n"
        "FAST_PATHS_BY_ID = {entry['constructor_id']: entry for entry in FAST_PATHS}\n"
        "__all__ = ['FAST_PATHS', 'FAST_PATHS_BY_ID', 'SCHEMA_JSON_SHA256', 'SCHEMA_LAYER']\n"
    )


def fast_api_directions(entries: tuple[FastEntry, ...]) -> dict[int, frozenset[Direction]]:
    """Index reviewed API entries by constructor ID and native directions.

    Args:
        entries: Validated API and MTProto fast-path entries.

    Returns:
        Directions for API entries only; MTProto service entries are excluded.
    """
    return {entry.constructor_id: entry.directions for entry in entries if entry.source == "api"}


def _api_fields(entry: TLEntry) -> tuple[FastField, ...]:
    """Translate one parsed API entry's parameters into reviewed native field metadata.

    Args:
        entry: Parsed API constructor or method selected by the manifest.

    Raises:
        ValueError: Public-field normalization diverges from the parsed declaration or a selected field layout is unsupported.
    """
    group_indexes: dict[str, int] = {}
    value_index = 0
    fields: list[FastField] = []
    for param in entry.params:
        if param.is_flags_marker:
            group_index = len(group_indexes)
            group_indexes[param.name] = group_index
            fields.append(
                FastField(
                    name=param.name,
                    python_name=param.python_name,
                    schema_type=param.type,
                    wire_type="flags",
                    value_index=None,
                    flag_group=group_index,
                )
            )
            continue
        if param.is_template or param.is_bare:
            continue
        wire_type = _api_wire_type(param)
        flag_group = group_indexes.get(param.flag) if param.flag is not None else None
        fields.append(
            FastField(
                name=param.name,
                python_name=param.python_name,
                schema_type=param.type,
                wire_type=wire_type,
                value_index=value_index,
                flag_group=flag_group,
                flag_index=param.flag_index,
            )
        )
        value_index += 1
    public = iter_public_params(entry.params)
    if len(public) != value_index:
        raise ValueError(f"Rust TL fast-path field normalization mismatch for {entry.name}")
    return tuple(fields)


def _api_wire_type(param: TLParameter) -> str:
    """Classify a parsed API parameter into its supported native wire representation.

    Args:
        param: Parsed public TL parameter.

    Raises:
        ValueError: The selected parameter uses an optional value or vector item type unsupported by the native fast path.
    """
    if param.is_optional and not param.is_true_flag:
        raise ValueError(f"Rust TL fast path does not support optional value field {param.name!r}")
    if param.is_true_flag:
        return "true"
    if param.is_vector:
        item = (param.vector_item_type or "").removeprefix("!")
        if item == "long":
            return "vector_long"
        raise ValueError(f"Rust TL fast path does not support vector field {param.name!r} of {item!r}")
    clean = param.type.removeprefix("!")
    if clean in {"int", "long", "bytes", "string"}:
        return clean
    if clean == "storage.FileType":
        return "empty_object"
    return "object"


def _static_wire_type(type_name: str) -> str:
    """Map a reviewed static MTProto field type to its native wire representation.

    Args:
        type_name: Manifest-declared static field type.

    Raises:
        ValueError: The manifest type has no reviewed native wire representation.
    """
    mapping = {
        "int": "int",
        "long": "long",
        "uint64": "uint64",
        "bytes": "bytes",
        "string": "string",
        "Vector<long>": "vector_long",
        "raw": "raw",
        "message_container": "message_container",
    }
    try:
        return mapping[type_name]
    except KeyError as exc:
        raise ValueError(f"unsupported static Rust TL fast-path type {type_name!r}") from exc


def _directions(item: dict[str, Any]) -> frozenset[Direction]:
    """Validate and freeze a manifest entry's allowed encode/decode directions.

    Args:
        item: Raw manifest entry mapping.

    Raises:
        ValueError: The entry has no directions or includes a value other than ``encode`` or ``decode``.
    """
    raw = frozenset(item.get("directions", ()))
    if not raw or not raw <= {"encode", "decode"}:
        raise ValueError(f"invalid Rust TL fast-path directions for {item.get('name')!r}")
    return raw  # type: ignore[return-value]


def _validate_decode_fields(name: str, directions: frozenset[Direction], fields: tuple[FastField, ...]) -> None:
    """Reject decode selections with unsupported native object field types.

    Args:
        name: Reviewed constructor or service name for diagnostics.
        directions: Manifest-selected native directions.
        fields: Normalized native field metadata.

    Raises:
        ValueError: Decode was selected for a field whose object representation is not supported natively.
    """
    if "decode" not in directions:
        return
    unsupported = [field.schema_type for field in fields if field.wire_type == "object"]
    if unsupported:
        raise ValueError(f"Rust TL fast-path decode for {name!r} has unsupported object fields: {unsupported}")


def _rust_field(field: FastField) -> str:
    """Render one Rust ``FastFieldSpec`` expression.

    Args:
        field: Reviewed normalized field metadata.
    """
    if field.wire_type == "flags":
        return f"FastFieldSpec::Flags {{ group: {field.flag_group or 0} }}"
    if field.wire_type == "true":
        return (
            "FastFieldSpec::True { "
            f"value: {field.value_index}, group: {field.flag_group or 0}, bit: {field.flag_index or 0}"
            " }"
        )
    variant = {
        "int": "Int",
        "long": "Long",
        "uint64": "UInt64",
        "bytes": "Bytes",
        "string": "String",
        "vector_long": "VectorLong",
        "object": "Object",
        "empty_object": "EmptyObject",
        "raw": "Raw",
        "message_container": "MessageContainer",
    }[field.wire_type]
    return f"FastFieldSpec::Value {{ value: {field.value_index}, wire_type: FastWireType::{variant} }}"
