"""Parse pinned Telegram TL declarations into deterministic generation metadata."""

from __future__ import annotations

import json
import keyword
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

SchemaKind = Literal["type", "function"]
IgnoredDeclarationKind = Literal["primitive", "alias", "test_combinator"]

_LINE_RE = re.compile(r"^(?P<name>[A-Za-z0-9_.]+)#(?P<constructor_id>[0-9A-Fa-f]+)(?P<body>.*?)= (?P<result>.+);$")
_FLAG_RE = re.compile(r"^(?P<flag>[A-Za-z_][A-Za-z0-9_]*)\.(?P<index>\d+)\?(?P<inner>.+)$")
_VECTOR_RE = re.compile(r"^[Vv]ector[< ](?P<inner>.+?)[>]?$")
_PARAM_COMMENT_RE = re.compile(r"^@param\s+(?P<name>\S+)(?:\s+.+)?$")
_LAYER_COMMENT_RE = re.compile(r"^LAYER\s+[1-9]\d*$")
_RESERVED_NAMES = frozenset({"self"})
_KNOWN_NON_ID_DECLARATIONS: dict[str, IgnoredDeclarationKind] = {
    "int ? = Int;": "primitive",
    "long ? = Long;": "primitive",
    "double ? = Double;": "primitive",
    "string ? = String;": "primitive",
    "bytes = Bytes;": "alias",
    "int256 = Int256;": "alias",
    "test.useConfigSimple = help.ConfigSimple;": "test_combinator",
    "test.parseInputAppEvent = InputAppEvent;": "test_combinator",
}
_KNOWN_CONSTRUCTOR_ID_ALIAS_PAIRS = frozenset(
    {
        frozenset({"invokeWithBusinessConnectionPrefix", "invokeWithBusinessConnection"}),
        frozenset({"invokeWithGooglePlayIntegrityPrefix", "invokeWithGooglePlayIntegrity"}),
        frozenset({"invokeWithApnsSecretPrefix", "invokeWithApnsSecret"}),
        frozenset({"invokeWithReCaptchaPrefix", "invokeWithReCaptcha"}),
    }
)


@dataclass(frozen=True, slots=True)
class TLParameter:
    """Parsed TL parameter, including flag, vector, bare, and template metadata.

    Attributes:
        name: Original parameter token name from the TL declaration, including special marker spellings where applicable.
        python_name: Generated Python attribute spelling used by the public raw class surface.
        type: TL type spelling after any optional ``flag.bit?`` prefix is separated into flag metadata.
        flag: Name of the flags-marker parameter controlling this field's presence, or ``None`` when unconditional.
        flag_index: Zero-based bit index in ``flag`` that controls this optional field, or ``None`` when not flag-gated.
        is_optional: Whether the source type uses a ``flag.bit?`` conditional prefix.
        is_true_flag: Whether the optional field has TL type ``true`` and is represented by its presence bit alone.
        is_vector: Whether ``type`` is a supported TL vector spelling.
        vector_item_type: Parsed element type for a vector field, or ``None`` for non-vectors.
        is_generic: Whether the parameter carries a TL generic/type-variable spelling.
        is_bare: Whether the token is a constructor-ID-free bare parameter rather than a regular named field.
        is_template: Whether the parameter was declared in braces as a TL template parameter.
        is_flags_marker: Whether this parameter declares a ``#`` flags word rather than a caller-visible value.
    """

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
    """One parsed constructor or method declaration with its exact source representation.

    Attributes:
        kind: Schema section, ``"type"`` for constructors or ``"function"`` for methods.
        name: Fully qualified TL declaration name as it appears before the constructor ID.
        namespace: Dotted-name prefix, or ``None`` when the declaration has no namespace.
        short_name: Final component of ``name`` after removing any namespace.
        python_class_name: Deterministic public Python class name derived from the TL declaration name.
        constructor_id: Unsigned 32-bit TL constructor identifier used on the wire.
        constructor_id_hex: Lowercase hexadecimal constructor-ID token retained for deterministic source rendering.
        result_type: TL result type written to the right of the declaration's equals sign.
        params: Parsed declaration-body parameters in source order, including non-public markers and templates.
        source_line: Complete original TL line or deterministic equivalent reconstructed from normalized JSON.
        line_number: One-based source line, or the deterministic normalized-JSON position used for diagnostics.
        comments: Contiguous declaration comments with their TL comment prefixes removed.
    """

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
    """RPC error annotation parsed from a supported schema comment.

    Attributes:
        name: Symbolic RPC error name from the ``@rpc_error`` comment.
        code: Integer Telegram RPC error code associated with ``name``.
        description: Optional trailing human-readable comment text; defaults to an empty string.
    """

    name: str
    code: int
    description: str = ""


@dataclass(frozen=True, slots=True)
class TLIgnoredDeclaration:
    """Known non-constructor declaration deliberately excluded from generated surfaces.

    Attributes:
        kind: Schema section containing the declaration, ``"type"`` or ``"function"``.
        name: Leading declaration token retained for diagnostics and provenance.
        source_line: Complete trimmed source declaration that the parser intentionally did not turn into a constructor.
        line_number: One-based source line of the ignored declaration.
        classification: Parser-approved exclusion reason: ``"primitive"``, ``"alias"``, or ``"test_combinator"``.
    """

    kind: SchemaKind
    name: str
    source_line: str
    line_number: int
    classification: IgnoredDeclarationKind


@dataclass(frozen=True, slots=True)
class TLSchema:
    """Parsed schema entries plus supported RPC-error and ignored-declaration metadata.

    Attributes:
        entries: Parsed constructor-ID-bearing declarations in the schema's source order.
        rpc_errors: Supported ``@rpc_error`` comment annotations encountered while parsing; defaults to an empty tuple.
        ignored_declarations: Recognized constructor-ID-free declarations deliberately excluded from generated surfaces; defaults to an empty tuple.
    """

    entries: tuple[TLEntry, ...]
    rpc_errors: tuple[RPCErrorSpec, ...] = ()
    ignored_declarations: tuple[TLIgnoredDeclaration, ...] = ()

    @property
    def constructors(self) -> tuple[TLEntry, ...]:
        """Return declarations belonging to the TL type/constructor section."""
        return tuple(entry for entry in self.entries if entry.kind == "type")

    @property
    def functions(self) -> tuple[TLEntry, ...]:
        """Return declarations belonging to the TL function/method section."""
        return tuple(entry for entry in self.entries if entry.kind == "function")


class TLSchemaParseError(ValueError):
    """Raised when a TL or normalized JSON schema violates supported parser rules."""

    pass


def parse_schema_file(path: str | Path) -> TLSchema:
    """Parse a TL text file or normalized JSON schema based on filename suffix.

    Args:
        path: Schema file path; ``.json`` selects normalized JSON parsing.

    Returns:
        Parsed schema model.
    """
    schema_path = Path(path)
    text = schema_path.read_text(encoding="utf-8")
    if schema_path.suffix == ".json":
        return parse_schema_json(json.loads(text))
    return parse_schema(text)


def parse_schema(text: str) -> TLSchema:
    """Parse canonical TL text with type/function sections and supported comments.

    Args:
        text: Complete TL declaration text.

    Returns:
        Parsed schema with entries, RPC errors, and known ignored declarations.

    Raises:
        TLSchemaParseError: A declaration, comment, or collision is unsupported or invalid.
    """
    kind: SchemaKind = "type"
    entries: list[TLEntry] = []
    errors: list[RPCErrorSpec] = []
    ignored_declarations: list[TLIgnoredDeclaration] = []
    comments: list[str] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("//"):
            comment = line[2:].strip()
            if _LAYER_COMMENT_RE.fullmatch(comment):
                continue
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
        ignored = _parse_known_non_id_declaration(line, kind=kind, line_number=line_number)
        if ignored is not None:
            ignored_declarations.append(ignored)
            comments.clear()
            continue
        entry = _parse_entry(line, kind=kind, line_number=line_number, comments=tuple(comments))
        _validate_entry_comments(entry)
        entries.append(entry)
        comments.clear()
    _validate_unique_entries(entries)
    return TLSchema(entries=tuple(entries), rpc_errors=tuple(errors), ignored_declarations=tuple(ignored_declarations))


def parse_schema_json_file(path: str | Path) -> TLSchema:
    """Load and parse a normalized JSON schema file.

    Args:
        path: JSON schema file path.

    Returns:
        Parsed schema model.
    """
    return parse_schema_json(json.loads(Path(path).read_text(encoding="utf-8")))


def parse_schema_json(data: Mapping[str, Any]) -> TLSchema:
    """Parse normalized constructor and method JSON arrays into schema entries.

    Args:
        data: Mapping containing ``constructors`` and ``methods`` arrays.

    Returns:
        Parsed schema model.

    Raises:
        TLSchemaParseError: Required arrays or entry fields are invalid.
    """
    constructors = data.get("constructors", ())
    methods = data.get("methods", ())
    if not isinstance(constructors, Sequence) or isinstance(constructors, str):
        raise TLSchemaParseError("JSON schema constructors must be an array")
    if not isinstance(methods, Sequence) or isinstance(methods, str):
        raise TLSchemaParseError("JSON schema methods must be an array")
    entries: list[TLEntry] = []
    for index, item in enumerate(constructors, start=1):
        entries.append(_parse_json_entry(item, kind="type", line_number=index))
    function_offset = len(entries) + 2
    for index, item in enumerate(methods, start=function_offset):
        entries.append(_parse_json_entry(item, kind="function", line_number=index))
    _validate_unique_entries(entries)
    return TLSchema(entries=tuple(entries))


def schema_to_tl(schema: TLSchema) -> str:
    """Render parsed declarations as deterministic TL text.

    Args:
        schema: Parsed schema whose entries retain their source declarations.

    Returns:
        Constructor declarations, a function delimiter, and function declarations.
    """
    lines: list[str] = [entry.source_line for entry in schema.constructors]
    lines.append("---functions---")
    lines.extend(entry.source_line for entry in schema.functions)
    return "\n".join(lines) + "\n"


def _parse_entry(line: str, *, kind: SchemaKind, line_number: int, comments: tuple[str, ...]) -> TLEntry:
    """Parse one constructor-ID-bearing TL declaration.

    Args:
        line: Trimmed declaration text.
        kind: Current schema section kind.
        line_number: One-based source line for diagnostics.
        comments: Supported preceding comments attached to the entry.

    Raises:
        TLSchemaParseError: The line is not a constructor-ID-bearing TL declaration or contains malformed parameters.
    """
    match = _LINE_RE.match(line)
    if match is None:
        if " = " in line and line.endswith(";") and "#" not in line:
            raise TLSchemaParseError(f"line {line_number}: unknown constructor-id-free TL declaration {line!r}")
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


def _parse_json_entry(item: object, *, kind: SchemaKind, line_number: int) -> TLEntry:
    """Convert one normalized JSON declaration to a schema entry.

    Args:
        item: JSON declaration object containing the kind-specific name, constructor ID, result type, and parameter array.
        kind: Constructor or function category selecting JSON field names.
        line_number: Synthetic source position for diagnostics.

    Raises:
        TLSchemaParseError: The declaration is not an object or lacks a valid name, constructor ID, result type, or parameter array.
    """
    if not isinstance(item, Mapping):
        raise TLSchemaParseError(f"JSON schema entry {line_number}: expected object")
    name_key = "predicate" if kind == "type" else "method"
    raw_name = item.get(name_key)
    result_type = item.get("type")
    raw_id = item.get("id")
    raw_params = item.get("params", ())
    if not isinstance(raw_name, str) or not raw_name:
        raise TLSchemaParseError(f"JSON schema entry {line_number}: missing {name_key}")
    if not isinstance(result_type, str) or not result_type:
        raise TLSchemaParseError(f"JSON schema entry {line_number}: missing result type")
    if not isinstance(raw_params, Sequence) or isinstance(raw_params, str):
        raise TLSchemaParseError(f"JSON schema entry {line_number}: params must be an array")
    try:
        constructor_id = int(str(raw_id)) & 0xFFFFFFFF
    except (TypeError, ValueError) as exc:
        raise TLSchemaParseError(f"JSON schema entry {line_number}: invalid id {raw_id!r}") from exc
    namespace, short_name = _split_qualified_name(raw_name)
    params = tuple(_parse_json_param(param, line_number=line_number) for param in raw_params)
    constructor_id_hex = f"{constructor_id:08x}"
    source_line = _json_entry_source_line(raw_name, constructor_id_hex, params, result_type)
    return TLEntry(
        kind=kind,
        name=raw_name,
        namespace=namespace,
        short_name=short_name,
        python_class_name=_python_class_name(raw_name),
        constructor_id=constructor_id,
        constructor_id_hex=constructor_id_hex,
        result_type=result_type,
        params=params,
        source_line=source_line,
        line_number=line_number,
    )


def _parse_json_param(item: object, *, line_number: int) -> TLParameter:
    """Convert one normalized JSON parameter mapping to a TL parameter.

    Args:
        item: JSON parameter object containing non-empty ``name`` and ``type`` fields; optional documentation/default metadata is ignored structurally.
        line_number: Parent entry position for diagnostics.

    Raises:
        TLSchemaParseError: The parameter is not an object or lacks a non-empty name or TL type.
    """
    if not isinstance(item, Mapping):
        raise TLSchemaParseError(f"JSON schema entry {line_number}: parameter must be an object")
    name = item.get("name")
    type_name = item.get("type")
    if not isinstance(name, str) or not name:
        raise TLSchemaParseError(f"JSON schema entry {line_number}: parameter missing name")
    if not isinstance(type_name, str) or not type_name:
        raise TLSchemaParseError(f"JSON schema entry {line_number}: parameter {name!r} missing type")
    return _parse_param(f"{name}:{type_name}")


def _json_entry_source_line(name: str, constructor_id_hex: str, params: Sequence[TLParameter], result_type: str) -> str:
    """Reconstruct the canonical TL source line for a normalized JSON entry.

    Args:
        name: Qualified schema declaration name.
        constructor_id_hex: Eight-digit hexadecimal constructor ID.
        params: Parsed parameters in declaration order.
        result_type: Declared TL result type.
    """
    body = " ".join(f"{param.name}:{param.type}" for param in params)
    if body:
        return f"{name}#{constructor_id_hex} {body} = {result_type};"
    return f"{name}#{constructor_id_hex} = {result_type};"


def _parse_param(part: str) -> TLParameter:
    """Parse one whitespace-tokenized TL parameter expression.

    Args:
        part: Raw parameter token from a declaration body.
    """
    if part.startswith("{") and part.endswith("}"):
        inner = part[1:-1]
        name, _, type_name = inner.partition(":")
        return TLParameter(
            name=name, python_name=_python_field_name(name), type=type_name or "Type", is_template=True, is_generic=True
        )
    if part == "#":
        return TLParameter(name="#", python_name="_bare", type="#", is_bare=True)
    if ":" not in part:
        return TLParameter(
            name=part, python_name=_python_field_name(part), type=part, is_bare=True, is_generic=part[:1].isupper()
        )
    name, type_name = part.split(":", 1)
    if type_name == "#":
        return TLParameter(name=name, python_name=_python_field_name(name), type=type_name, is_flags_marker=True)
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
    is_generic = type_name.startswith("!") or (type_name[:1].isupper() and type_name.endswith("Type"))
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
    """Split a declaration parameter body into non-empty whitespace tokens.

    Args:
        body: Unparsed declaration body between identifier and result type.
    """
    if not body:
        return ()
    return tuple(part for part in body.split() if part)


def _vector_item_type(type_name: str) -> str | None:
    """Return a supported vector item type, if the expression is a vector.

    Args:
        type_name: TL type expression.
    """
    match = _VECTOR_RE.match(type_name)
    if match is None:
        return None
    return match.group("inner").strip()


def _split_qualified_name(name: str) -> tuple[str | None, str]:
    """Split a qualified schema name into optional namespace and short name.

    Args:
        name: Schema declaration name.
    """
    if "." not in name:
        return None, name
    namespace, short_name = name.rsplit(".", 1)
    return namespace, short_name


def _python_class_name(name: str) -> str:
    """Convert a schema declaration name into a collision-safe Python class name.

    Args:
        name: Qualified schema declaration name.
    """
    parts = re.split(r"[._]", name)
    class_name = "".join(_pascal_case(part) for part in parts if part) or "Anonymous"
    return f"{class_name}Value" if keyword.iskeyword(class_name) else class_name


def _pascal_case(value: str) -> str:
    """Normalize one schema name fragment to PascalCase.

    Args:
        value: Schema name fragment.
    """
    split = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value).replace("_", " ").split()
    return "".join(part[:1].upper() + part[1:] for part in split) or "Anonymous"


def _python_field_name(name: str) -> str:
    """Convert a schema parameter name into a valid non-reserved Python field name.

    Args:
        name: Raw schema parameter name.
    """
    cleaned = re.sub(r"\W", "_", name)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"field_{cleaned}"
    if keyword.iskeyword(cleaned) or cleaned in _RESERVED_NAMES:
        cleaned = f"{cleaned}_"
    return cleaned


def _parse_rpc_error_comment(comment: str) -> RPCErrorSpec | None:
    """Parse a supported ``@rpc_error`` comment or return ``None``.

    Args:
        comment: Comment text without the TL ``//`` prefix.
    """
    if not comment.startswith("@rpc_error "):
        return None
    _, name, code, *description = comment.split()
    return RPCErrorSpec(name=name, code=int(code), description=" ".join(description))


def _parse_known_non_id_declaration(line: str, *, kind: SchemaKind, line_number: int) -> TLIgnoredDeclaration | None:
    """Classify a known constructor-ID-free declaration or leave it unrecognized.

    Args:
        line: Trimmed source declaration.
        kind: Current schema section kind.
        line_number: One-based source line for the ignored record.
    """
    classification = _KNOWN_NON_ID_DECLARATIONS.get(line)
    if classification is None:
        return None
    name = line.split(maxsplit=1)[0]
    return TLIgnoredDeclaration(
        kind=kind, name=name, source_line=line, line_number=line_number, classification=classification
    )


def _validate_entry_comments(entry: TLEntry) -> None:
    """Validate supported parameter comments against an entry's declared fields.

    Args:
        entry: Parsed entry carrying source comments.

    Raises:
        TLSchemaParseError: A ``@param`` comment is malformed or names a field absent from the declaration.
    """
    parameter_names = {parameter.name for parameter in entry.params}
    for comment in entry.comments:
        if not comment.startswith("@param"):
            continue
        match = _PARAM_COMMENT_RE.fullmatch(comment)
        if match is None:
            raise TLSchemaParseError(f"line {entry.line_number}: malformed @param comment {comment!r}")
        parameter_name = match.group("name")
        if parameter_name not in parameter_names:
            raise TLSchemaParseError(
                f"line {entry.line_number}: @param documents unknown parameter {parameter_name!r} on {entry.name!r}"
            )


def _validate_unique_entries(entries: Sequence[TLEntry]) -> None:
    """Reject duplicate names, generated class names, and unapproved constructor-ID collisions.

    Args:
        entries: Parsed entries to validate in source order.

    Raises:
        TLSchemaParseError: Names, generated class names, or constructor IDs collide outside the explicit alias allowlist.
    """
    seen: dict[tuple[SchemaKind, str], int] = {}
    class_names: dict[tuple[SchemaKind, str], int] = {}
    constructor_ids: dict[int, tuple[str, int]] = {}
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
        duplicate_id = constructor_ids.get(entry.constructor_id)
        if duplicate_id is not None:
            previous_name, previous_line = duplicate_id
            if frozenset({previous_name, entry.name}) not in _KNOWN_CONSTRUCTOR_ID_ALIAS_PAIRS:
                raise TLSchemaParseError(
                    f"duplicate constructor id {entry.constructor_id_hex} for {previous_name!r} at line {previous_line} "
                    f"and {entry.name!r} at line {entry.line_number}"
                )
        constructor_ids[entry.constructor_id] = (entry.name, entry.line_number)


def iter_public_params(params: Iterable[TLParameter]) -> tuple[TLParameter, ...]:
    """Return parameters emitted as public generated Python fields.

    Args:
        params: Parsed declaration parameters, including hidden schema markers.
    """
    return tuple(param for param in params if not param.is_template and not param.is_flags_marker and not param.is_bare)
