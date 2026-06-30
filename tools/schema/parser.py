from __future__ import annotations

import keyword
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

SchemaKind = Literal["type", "function"]

_LINE_RE = re.compile(
    r"^(?P<name>[A-Za-z0-9_.]+)#(?P<constructor_id>[0-9A-Fa-f]+)(?P<body>.*?)= (?P<result>.+);$"
)
_FLAG_RE = re.compile(r"^(?P<flag>[A-Za-z_][A-Za-z0-9_]*)\.(?P<index>\d+)\?(?P<inner>.+)$")
_VECTOR_RE = re.compile(r"^[Vv]ector[< ](?P<inner>.+?)[>]?$")
_RESERVED_NAMES = frozenset({"self"})


@dataclass(frozen=True, slots=True)
class TLParameter:
    name: str
    python_name: str
    type: str
    flag: str | None = None
    flag_index: int | None = None
    is_optional: bool = False
    is_true_flag: bool = False
    is_vector: bool = False
    vector_item_type: str | None = None
    is_generic: bool = False
    is_bare: bool = False
    is_template: bool = False
    is_flags_marker: bool = False


@dataclass(frozen=True, slots=True)
class TLEntry:
    kind: SchemaKind
    name: str
    namespace: str | None
    short_name: str
    python_class_name: str
    constructor_id: int
    constructor_id_hex: str
    result_type: str
    params: tuple[TLParameter, ...]
    source_line: str
    line_number: int
    comments: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RPCErrorSpec:
    name: str
    code: int
    description: str = ""


@dataclass(frozen=True, slots=True)
class TLSchema:
    entries: tuple[TLEntry, ...]
    rpc_errors: tuple[RPCErrorSpec, ...] = ()

    @property
    def constructors(self) -> tuple[TLEntry, ...]:
        return tuple(entry for entry in self.entries if entry.kind == "type")

    @property
    def functions(self) -> tuple[TLEntry, ...]:
        return tuple(entry for entry in self.entries if entry.kind == "function")


class TLSchemaParseError(ValueError):
    pass


def parse_schema_file(path: str | Path) -> TLSchema:
    return parse_schema(Path(path).read_text(encoding="utf-8"))


def parse_schema(text: str) -> TLSchema:
    kind: SchemaKind = "type"
    entries: list[TLEntry] = []
    errors: list[RPCErrorSpec] = []
    comments: list[str] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("//"):
            comment = line[2:].strip()
            error = _parse_rpc_error_comment(comment)
            if error is not None:
                errors.append(error)
            else:
                comments.append(comment)
            continue
        if line == "---types---":
            kind = "type"
            comments.clear()
            continue
        if line == "---functions---":
            kind = "function"
            comments.clear()
            continue
        entries.append(
            _parse_entry(line, kind=kind, line_number=line_number, comments=tuple(comments))
        )
        comments.clear()
    _validate_unique_entries(entries)
    return TLSchema(entries=tuple(entries), rpc_errors=tuple(errors))


def _parse_entry(
    line: str, *, kind: SchemaKind, line_number: int, comments: tuple[str, ...]
) -> TLEntry:
    match = _LINE_RE.match(line)
    if match is None:
        raise TLSchemaParseError(f"line {line_number}: expected TL declaration, got {line!r}")
    raw_name = match.group("name")
    namespace, short_name = _split_qualified_name(raw_name)
    body = match.group("body").strip()
    params = tuple(_parse_param(part) for part in _tokenize_body(body))
    constructor_id_hex = match.group("constructor_id").lower()
    return TLEntry(
        kind=kind,
        name=raw_name,
        namespace=namespace,
        short_name=short_name,
        python_class_name=_python_class_name(raw_name),
        constructor_id=int(constructor_id_hex, 16),
        constructor_id_hex=constructor_id_hex,
        result_type=match.group("result").strip(),
        params=params,
        source_line=line,
        line_number=line_number,
        comments=comments,
    )


def _parse_param(part: str) -> TLParameter:
    if part.startswith("{") and part.endswith("}"):
        inner = part[1:-1]
        name, _, type_name = inner.partition(":")
        return TLParameter(
            name=name,
            python_name=_python_field_name(name),
            type=type_name or "Type",
            is_template=True,
            is_generic=True,
        )
    if part == "#":
        return TLParameter(name="#", python_name="_bare", type="#", is_bare=True)
    if ":" not in part:
        return TLParameter(
            name=part,
            python_name=_python_field_name(part),
            type=part,
            is_bare=True,
            is_generic=part[:1].isupper(),
        )
    name, type_name = part.split(":", 1)
    if type_name == "#":
        return TLParameter(
            name=name, python_name=_python_field_name(name), type=type_name, is_flags_marker=True
        )
    flag: str | None = None
    flag_index: int | None = None
    is_optional = False
    flag_match = _FLAG_RE.match(type_name)
    if flag_match is not None:
        flag = flag_match.group("flag")
        flag_index = int(flag_match.group("index"))
        type_name = flag_match.group("inner")
        is_optional = True
    vector_item = _vector_item_type(type_name)
    is_generic = type_name.startswith("!") or (
        type_name[:1].isupper() and type_name.endswith("Type")
    )
    return TLParameter(
        name=name,
        python_name=_python_field_name(name),
        type=type_name,
        flag=flag,
        flag_index=flag_index,
        is_optional=is_optional,
        is_true_flag=is_optional and type_name == "true",
        is_vector=vector_item is not None,
        vector_item_type=vector_item,
        is_generic=is_generic,
    )


def _tokenize_body(body: str) -> tuple[str, ...]:
    if not body:
        return ()
    return tuple(part for part in body.split() if part)


def _vector_item_type(type_name: str) -> str | None:
    match = _VECTOR_RE.match(type_name)
    if match is None:
        return None
    return match.group("inner").strip()


def _split_qualified_name(name: str) -> tuple[str | None, str]:
    if "." not in name:
        return None, name
    namespace, short_name = name.rsplit(".", 1)
    return namespace, short_name


def _python_class_name(name: str) -> str:
    parts = re.split(r"[._]", name)
    class_name = "".join(_pascal_case(part) for part in parts if part) or "Anonymous"
    return f"{class_name}Value" if keyword.iskeyword(class_name) else class_name


def _pascal_case(value: str) -> str:
    split = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value).replace("_", " ").split()
    return "".join(part[:1].upper() + part[1:] for part in split) or "Anonymous"


def _python_field_name(name: str) -> str:
    cleaned = re.sub(r"\W", "_", name)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"field_{cleaned}"
    if keyword.iskeyword(cleaned) or cleaned in _RESERVED_NAMES:
        cleaned = f"{cleaned}_"
    return cleaned


def _parse_rpc_error_comment(comment: str) -> RPCErrorSpec | None:
    if not comment.startswith("@rpc_error "):
        return None
    _, name, code, *description = comment.split()
    return RPCErrorSpec(name=name, code=int(code), description=" ".join(description))


def _validate_unique_entries(entries: Sequence[TLEntry]) -> None:
    seen: dict[tuple[SchemaKind, str], int] = {}
    class_names: dict[tuple[SchemaKind, str], int] = {}
    for entry in entries:
        key = (entry.kind, entry.name)
        if key in seen:
            raise TLSchemaParseError(
                f"duplicate {entry.kind} {entry.name!r} at lines {seen[key]} and {entry.line_number}"
            )
        seen[key] = entry.line_number
        class_key = (entry.kind, entry.python_class_name)
        if class_key in class_names:
            raise TLSchemaParseError(
                f"duplicate generated class {entry.python_class_name!r} at lines {class_names[class_key]} and {entry.line_number}"
            )
        class_names[class_key] = entry.line_number


def iter_public_params(params: Iterable[TLParameter]) -> tuple[TLParameter, ...]:
    return tuple(
        param
        for param in params
        if not param.is_template and not param.is_flags_marker and not param.is_bare
    )
