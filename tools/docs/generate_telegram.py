"""Statically extract deterministic Telegram reference pages from pinned JSON.

The extractor reads the normalized canonical TDLib structure, schema metadata,
and independently pinned RPC-error database without importing generated raw
bindings, importing ``miniproto`` or accessing the network.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.docs.model import ReferencePage

_MISSING_SCHEMA_DESCRIPTION = "No description provided by the pinned schema."
_MISSING_ERROR_DESCRIPTION = "No description provided by the pinned RPC error database."
_FLAG_TYPE = re.compile(r"^(?P<word>[A-Za-z_][A-Za-z0-9_]*)\.(?P<bit>\d+)\?(?P<value>.+)$")
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*")
_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_PARAMETERIZED_ERROR = re.compile(r"%[A-Za-z]")
_PRIMITIVE_TYPES = frozenset({"bytes", "double", "false", "int", "int128", "int256", "long", "string", "true"})


@dataclass(frozen=True, slots=True)
class TelegramParameter:
    """Represent one schema-authoritative Telegram declaration parameter.

    Attributes:
        name: Exact parameter spelling from the normalized canonical schema.
        type_name: Exact raw TL type expression, including optional flag syntax.
        description: Merged upstream prose when the normalized schema provides it.
        default: Explicit normalized default when the schema provides one.
    """

    name: str
    type_name: str
    description: str | None
    default: str | None


@dataclass(frozen=True, slots=True)
class TelegramDeclaration:
    """Represent one normalized canonical constructor or RPC method.

    Attributes:
        kind: ``function`` for a schema ``methods`` entry, otherwise ``type``.
        name: Exact qualified method or constructor predicate name.
        constructor_id: Normalized unsigned hexadecimal constructor identifier.
        result_type: Exact raw TL result expression from canonical TDLib structure.
        parameters: Ordered parameter specifications from the canonical entry.
        description: Merged upstream declaration prose, if the normalized input has it.
    """

    kind: str
    name: str
    constructor_id: str
    result_type: str
    parameters: tuple[TelegramParameter, ...]
    description: str | None


@dataclass(frozen=True, slots=True)
class TelegramRPCError:
    """Represent one independently pinned RPC error name/code/method mapping.

    Attributes:
        name: Symbolic error name, preserving any printf-style parameter marker.
        code: Numeric RPC error code.
        methods: Sorted canonical method names mapped to the error.
        description: Independently pinned error prose, if available.
    """

    name: str
    code: int
    methods: tuple[str, ...]
    description: str | None


@dataclass(frozen=True, slots=True)
class TelegramPythonBinding:
    """Describe one exact generated public Python binding for a TL declaration.

    Attributes:
        kind: Telegram declaration category, ``"function"`` or ``"type"``.
        qualified_name: Exact raw TL constructor or method name.
        constructor_id: Unsigned eight-hex-digit constructor identifier.
        python_module: Public module exporting the generated Python class.
        python_name: Public generated Python class name.
        python_import: Exact import statement for the public binding.
        public_access: Fully qualified public Python access path.
    """

    kind: str
    qualified_name: str
    constructor_id: str
    python_module: str
    python_name: str
    python_import: str
    public_access: str


@dataclass(frozen=True, slots=True)
class TelegramPythonErrorBinding:
    """Describe one exact public Python exception class for a pinned RPC error.

    Attributes:
        code: Numeric Telegram RPC error code.
        name: Exact pinned symbolic error template.
        python_module: Public module exporting the generated exception class.
        python_name: Public generated exception class name.
        python_import: Exact import statement for the public exception class.
        public_access: Fully qualified public Python exception access path.
    """

    code: int
    name: str
    python_module: str
    python_name: str
    python_import: str
    public_access: str


@dataclass(frozen=True, slots=True)
class TelegramBindingManifest:
    """Represent validated static Python bindings generated from the pinned schema surface.

    Attributes:
        layer: Telegram layer covered by every declaration binding.
        declarations: Bindings keyed by declaration kind, TL qualified name and constructor ID.
        errors: Bindings keyed by numeric error code and symbolic error template.
    """

    layer: int
    declarations: Mapping[tuple[str, str, str], TelegramPythonBinding]
    errors: Mapping[tuple[int, str], TelegramPythonErrorBinding]


@dataclass(frozen=True, slots=True)
class TelegramReferenceSurface:
    """Return rendered Telegram pages together with a deterministic relationship artifact.

    Attributes:
        pages: Detailed and index Markdown pages sorted by stable relative path.
        relationship_manifest_path: Relative JSON path the outer writer should materialize.
        relationship_manifest: Deterministic JSON relationship graph for the generated pages.
    """

    pages: tuple[ReferencePage, ...]
    relationship_manifest_path: str
    relationship_manifest: str


def generate_telegram_pages(
    *,
    schema_path: Path,
    metadata_path: Path,
    rpc_errors_path: Path,
    binding_manifest: TelegramBindingManifest,
    repository_url: str,
) -> tuple[ReferencePage, ...]:
    """Generate deterministic Telegram Markdown pages from exact static bindings.

    Args:
        schema_path: Normalized canonical schema JSON with ``constructors`` and
            ``methods`` declaration arrays.
        metadata_path: Pinned metadata JSON providing canonical source, layer,
            documentation-precedence, source note, URLs and diff summary.
        rpc_errors_path: Pinned core RPC error JSON with code/name/method maps
            and optional descriptions.
        binding_manifest: Static schema-generator-owned Python binding manifest
            reconciled to the selected declarations and errors.
        repository_url: Repository browser base URL used for local pinned-input
            source links in page frontmatter.

    Returns:
        Detailed and index pages sorted by stable relative Markdown path.

    Raises:
        ValueError: If static inputs, manifest records or generated routes do
            not reconcile.

    Notes:
        The generator performs file reads only. It never imports generated raw
        bindings, imports the miniproto package, scrapes web content or makes
        network requests.
    """
    return generate_telegram_reference_surface(
        schema_path=schema_path,
        metadata_path=metadata_path,
        rpc_errors_path=rpc_errors_path,
        binding_manifest=binding_manifest,
        repository_url=repository_url,
    ).pages


def generate_telegram_reference_surface(
    *,
    schema_path: Path,
    metadata_path: Path,
    rpc_errors_path: Path,
    binding_manifest: TelegramBindingManifest,
    repository_url: str,
) -> TelegramReferenceSurface:
    """Generate Telegram pages and the relationship artifact for an outer writer.

    Args:
        schema_path: Normalized canonical schema JSON with constructors and methods.
        metadata_path: Pinned source/layer/provenance metadata for the selected schema.
        rpc_errors_path: Pinned core RPC error code/name/method database.
        binding_manifest: Exact public Python bindings generated from the same schema surface.
        repository_url: Repository browser base URL used for source-link frontmatter.

    Returns:
        Immutable pages plus a deterministic relationship JSON artifact. The
        caller owns writing these generated artifacts into a documentation tree.

    Raises:
        ValueError: If static inputs, bindings, relationship targets or routes
            do not reconcile.

    Notes:
        The extractor performs file reads only. It never imports generated raw
        bindings, imports the miniproto package, scrapes web content or makes
        network requests.
    """
    schema = _load_json_object(schema_path, label="schema")
    metadata = _load_json_object(metadata_path, label="schema metadata")
    rpc_errors = _load_json_object(rpc_errors_path, label="RPC errors")
    declarations = _normalize_declarations(schema)
    errors = _normalize_rpc_errors(rpc_errors)
    layer = _positive_integer(metadata.get("layer"), field="metadata.layer")
    canonical_source = _required_string(metadata.get("canonical_source"), field="metadata.canonical_source")
    _validate_metadata_reconciliation(metadata, declarations=declarations, errors=errors, layer=layer)
    _validate_binding_reconciliation(binding_manifest, declarations=declarations, errors=errors, layer=layer)
    repository_base = _repository_url(repository_url)
    structural_url = _metadata_url(metadata, "structural_source_url", "schema_source_url", "source_url")
    error_url = _metadata_url_or_repository_fallback(
        metadata,
        fallback=f"{repository_base}/blob/master/tools/schema/rpc-errors.json",
        fields=("rpc_error_source_url", "rpc_error_download_url"),
    )
    types = tuple(item for item in declarations if item.kind == "type")
    result_family_paths = _result_family_paths(types)
    reserved_routes = _reserved_index_routes(declarations, errors, result_family_paths=result_family_paths)
    function_paths = _declaration_paths(
        (item for item in declarations if item.kind == "function"),
        category="functions",
        reserved_routes=reserved_routes,
    )
    type_paths = _declaration_paths(
        types, category="types", reserved_routes=reserved_routes | _routes_for_paths(function_paths.values())
    )
    error_paths = _error_paths(
        errors,
        reserved_routes=reserved_routes
        | _routes_for_paths(function_paths.values())
        | _routes_for_paths(type_paths.values()),
    )
    relationship_index = _relationship_index(declarations, errors, rpc_errors)
    declaration_paths = function_paths | type_paths
    pages: list[ReferencePage] = []
    for declaration in declarations:
        path = function_paths[declaration] if declaration.kind == "function" else type_paths[declaration]
        pages.append(
            _declaration_page(
                declaration,
                path=path,
                binding=binding_manifest.declarations[(declaration.kind, declaration.name, declaration.constructor_id)],
                relationship_index=relationship_index,
                declaration_paths=declaration_paths,
                error_paths=error_paths,
                result_family_paths=result_family_paths,
                canonical_source=canonical_source,
                structural_url=structural_url,
                repository_base=repository_base,
                metadata=metadata,
            )
        )
    for error in errors:
        pages.append(
            _error_page(
                error,
                path=error_paths[error],
                binding=binding_manifest.errors[(error.code, error.name)],
                relationship_index=relationship_index,
                function_paths=function_paths,
                layer=layer,
                canonical_source=canonical_source,
                error_url=error_url,
                repository_base=repository_base,
                metadata=metadata,
            )
        )
    pages.extend(
        _index_pages(
            declarations=declarations,
            errors=errors,
            declaration_paths=declaration_paths,
            error_paths=error_paths,
            function_paths=function_paths,
            result_family_paths=result_family_paths,
            relationship_index=relationship_index,
            layer=layer,
            canonical_source=canonical_source,
            structural_url=structural_url,
            error_url=error_url,
            repository_base=repository_base,
        )
    )
    ordered_pages = tuple(sorted(pages, key=lambda page: page.path))
    _validate_page_routes(ordered_pages)
    return TelegramReferenceSurface(
        pages=ordered_pages,
        relationship_manifest_path="telegram/relationships.json",
        relationship_manifest=_relationship_manifest(
            layer=layer,
            relationship_index=relationship_index,
            declaration_paths=declaration_paths,
            error_paths=error_paths,
            result_family_paths=result_family_paths,
        ),
    )


def load_telegram_binding_manifest(path: Path) -> TelegramBindingManifest:
    """Load a schema-generator-owned static Telegram-to-Python binding manifest.

    Args:
        path: Local deterministic ``telegram-bindings.json`` artifact to validate.

    Returns:
        Exact declaration and error bindings keyed by their source identities.

    Raises:
        ValueError: If a record is malformed, duplicated or violates the public
            generated Python import contract.
    """
    payload = _load_json_object(path, label="Telegram binding manifest")
    if _integer(payload.get("schema_version"), field="binding_manifest.schema_version") != 1:
        raise ValueError("binding_manifest.schema_version must be 1")
    layer = _positive_integer(payload.get("layer"), field="binding_manifest.layer")
    declarations: dict[tuple[str, str, str], TelegramPythonBinding] = {}
    for index, raw in enumerate(_object_sequence(payload.get("declarations"), field="binding_manifest.declarations")):
        binding = _declaration_binding(raw, index=index)
        key = (binding.kind, binding.qualified_name, binding.constructor_id)
        if key in declarations:
            raise ValueError(f"duplicate declaration binding: {key!r}")
        declarations[key] = binding
    errors: dict[tuple[int, str], TelegramPythonErrorBinding] = {}
    for index, raw in enumerate(_object_sequence(payload.get("errors"), field="binding_manifest.errors")):
        binding = _error_binding(raw, index=index)
        key = (binding.code, binding.name)
        if key in errors:
            raise ValueError(f"duplicate RPC error binding: {key!r}")
        errors[key] = binding
    return TelegramBindingManifest(layer=layer, declarations=declarations, errors=errors)


def _declaration_binding(raw: Mapping[str, Any], *, index: int) -> TelegramPythonBinding:
    """Validate one public raw declaration binding record from the generated manifest.

    Args:
        raw: JSON object containing one generated declaration binding.
        index: Source-array position included in validation failures.

    Returns:
        Exact normalized public binding record.

    Raises:
        ValueError: If the record is malformed or names a non-public raw facade.
    """
    field = f"binding_manifest.declarations[{index}]"
    kind = _required_string(raw.get("kind"), field=f"{field}.kind")
    if kind not in {"function", "type"}:
        raise ValueError(f"{field}.kind must be function or type")
    qualified_name = _required_string(raw.get("qualified_name"), field=f"{field}.qualified_name")
    constructor_id = _constructor_id(raw.get("constructor_id"), field=f"{field}.constructor_id")
    python_module = _required_string(raw.get("python_module"), field=f"{field}.python_module")
    python_name = _required_string(raw.get("python_name"), field=f"{field}.python_name")
    python_import = _required_string(raw.get("python_import"), field=f"{field}.python_import")
    public_access = _required_string(raw.get("public_access"), field=f"{field}.public_access")
    expected_module = f"miniproto.raw.{'functions' if kind == 'function' else 'types'}"
    _validate_public_binding(
        module=python_module,
        name=python_name,
        rendered_import=python_import,
        public_access=public_access,
        expected_module=expected_module,
        field=field,
    )
    return TelegramPythonBinding(
        kind=kind,
        qualified_name=qualified_name,
        constructor_id=constructor_id,
        python_module=python_module,
        python_name=python_name,
        python_import=python_import,
        public_access=public_access,
    )


def _error_binding(raw: Mapping[str, Any], *, index: int) -> TelegramPythonErrorBinding:
    """Validate one public generated RPC error binding record from the manifest.

    Args:
        raw: JSON object containing one generated RPC error binding.
        index: Source-array position included in validation failures.

    Returns:
        Exact normalized public error binding record.

    Raises:
        ValueError: If the record is malformed or does not name the public error module.
    """
    field = f"binding_manifest.errors[{index}]"
    code = _integer(raw.get("code"), field=f"{field}.code")
    name = _required_string(raw.get("name"), field=f"{field}.name")
    python_module = _required_string(raw.get("python_module"), field=f"{field}.python_module")
    python_name = _required_string(raw.get("python_name"), field=f"{field}.python_name")
    python_import = _required_string(raw.get("python_import"), field=f"{field}.python_import")
    public_access = _required_string(raw.get("public_access"), field=f"{field}.public_access")
    _validate_public_binding(
        module=python_module,
        name=python_name,
        rendered_import=python_import,
        public_access=public_access,
        expected_module="miniproto.errors",
        field=field,
    )
    return TelegramPythonErrorBinding(
        code=code,
        name=name,
        python_module=python_module,
        python_name=python_name,
        python_import=python_import,
        public_access=public_access,
    )


def _validate_public_binding(
    *, module: str, name: str, rendered_import: str, public_access: str, expected_module: str, field: str
) -> None:
    """Ensure a manifest record names the exact stable public import contract.

    Args:
        module: Declared Python module path.
        name: Declared public class name.
        rendered_import: Declared import statement.
        public_access: Declared fully qualified access path.
        expected_module: Only public module allowed for this binding category.
        field: Manifest-record prefix included in validation failures.

    Raises:
        ValueError: If a field points to an internal module or inconsistent name.
    """
    if module != expected_module:
        raise ValueError(f"{field}.python_module must be {expected_module!r}")
    expected_import = f"from {module} import {name}"
    if rendered_import != expected_import:
        raise ValueError(f"{field}.python_import must be {expected_import!r}")
    expected_access = f"{module}.{name}"
    if public_access != expected_access:
        raise ValueError(f"{field}.public_access must be {expected_access!r}")


def _validate_binding_reconciliation(
    manifest: TelegramBindingManifest,
    *,
    declarations: Sequence[TelegramDeclaration],
    errors: Sequence[TelegramRPCError],
    layer: int,
) -> None:
    """Require every canonical declaration/error to have exactly one source-owned binding.

    Args:
        manifest: Validated static Python binding manifest.
        declarations: Complete normalized canonical constructor and method set.
        errors: Complete flattened pinned RPC error set.
        layer: Selected Telegram layer from schema metadata.

    Raises:
        ValueError: If the manifest layer, identities or record count differs from pinned inputs.
    """
    if manifest.layer != layer:
        raise ValueError(f"binding manifest layer {manifest.layer} does not match metadata.layer={layer}")
    declaration_keys = {(item.kind, item.name, item.constructor_id) for item in declarations}
    binding_keys = set(manifest.declarations)
    if declaration_keys != binding_keys:
        missing = sorted(declaration_keys - binding_keys)
        extra = sorted(binding_keys - declaration_keys)
        raise ValueError(
            f"binding manifest declaration identities differ; missing={missing[:3]!r}, extra={extra[:3]!r}"
        )
    error_keys = {(item.code, item.name) for item in errors}
    binding_error_keys = set(manifest.errors)
    if error_keys != binding_error_keys:
        missing = sorted(error_keys - binding_error_keys)
        extra = sorted(binding_error_keys - error_keys)
        raise ValueError(f"binding manifest error identities differ; missing={missing[:3]!r}, extra={extra[:3]!r}")


def _load_json_object(path: Path, *, label: str) -> Mapping[str, Any]:
    """Load one UTF-8 JSON object without importing code or contacting a service.

    Args:
        path: Local JSON file to read.
        label: Human-readable input name included in validation failures.

    Returns:
        Parsed top-level object mapping.

    Raises:
        ValueError: If the file is not a valid JSON object.
    """
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} must be readable UTF-8 JSON: {path}") from exc
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _normalize_declarations(schema: Mapping[str, Any]) -> tuple[TelegramDeclaration, ...]:
    """Validate and normalize canonical constructor and method arrays.

    Args:
        schema: Top-level normalized schema object with ``constructors`` and
            ``methods`` arrays.

    Returns:
        Canonical declarations sorted by kind, qualified name and identifier.

    Raises:
        ValueError: If either supported declaration collection has an invalid shape.
    """
    constructors = _object_sequence(schema.get("constructors"), field="schema.constructors")
    methods = _object_sequence(schema.get("methods"), field="schema.methods")
    declarations = [
        *(_declaration_from_raw(item, kind="type", name_key="predicate") for item in constructors),
        *(_declaration_from_raw(item, kind="function", name_key="method") for item in methods),
    ]
    return tuple(sorted(declarations, key=lambda item: (item.kind, item.name, item.constructor_id)))


def _object_sequence(value: object, *, field: str) -> tuple[Mapping[str, Any], ...]:
    """Validate a JSON array whose elements must all be objects.

    Args:
        value: Value read from a selected schema, RPC-error or binding-manifest
            array field.
        field: Dotted JSON location reported when the selected array is absent,
            scalar or contains a non-object member.

    Returns:
        Object entries in their original source order.

    Raises:
        ValueError: If the candidate is not an array of objects.
    """
    if not isinstance(value, Sequence) or isinstance(value, str | bytes | bytearray):
        raise ValueError(f"{field} must be an array")
    if not all(isinstance(item, Mapping) for item in value):
        raise ValueError(f"{field} must contain only objects")
    return tuple(value)


def _declaration_from_raw(raw: Mapping[str, Any], *, kind: str, name_key: str) -> TelegramDeclaration:
    """Convert one normalized schema declaration into immutable extraction data.

    Args:
        raw: Canonical declaration object from a supported schema array.
        kind: Output category, either ``function`` or ``type``.
        name_key: Raw field containing ``method`` or ``predicate`` identity.

    Returns:
        Validated declaration preserving canonical order and exact TL expressions.

    Raises:
        ValueError: If identity, ID, result type or parameters are malformed.
    """
    name = _required_string(raw.get(name_key), field=f"declaration.{name_key}")
    result_type = _required_string(raw.get("type"), field=f"declaration {name}.type")
    constructor_id = _constructor_id(raw.get("id"), field=f"declaration {name}.id")
    parameters = _parameters(raw.get("params", ()), declaration=name)
    return TelegramDeclaration(
        kind=kind,
        name=name,
        constructor_id=constructor_id,
        result_type=result_type,
        parameters=parameters,
        description=_optional_description(raw.get("description")),
    )


def _parameters(value: object, *, declaration: str) -> tuple[TelegramParameter, ...]:
    """Validate and normalize ordered parameter objects for one declaration.

    Args:
        value: ``params`` array from one selected canonical schema declaration.
        declaration: Exact qualified declaration identity used to locate an
            invalid parameter in the pinned schema.

    Returns:
        Exact ordered parameter specifications, including optional prose/defaults.

    Raises:
        ValueError: If a parameter lacks a non-empty name or type expression.
    """
    parameters: list[TelegramParameter] = []
    for index, raw in enumerate(_object_sequence(value, field=f"declaration {declaration}.params")):
        name = _required_string(raw.get("name"), field=f"declaration {declaration}.params[{index}].name")
        type_name = _required_string(raw.get("type"), field=f"declaration {declaration}.params[{index}].type")
        default = raw.get("default")
        if default is not None and not isinstance(default, str | int | float | bool):
            raise ValueError(f"declaration {declaration}.params[{index}].default must be scalar")
        parameters.append(
            TelegramParameter(
                name=name,
                type_name=type_name,
                description=_optional_description(raw.get("description")),
                default=None if default is None else str(default),
            )
        )
    return tuple(parameters)


def _normalize_rpc_errors(payload: Mapping[str, Any]) -> tuple[TelegramRPCError, ...]:
    """Validate the pinned error database and flatten code/name method mappings.

    Args:
        payload: RPC-error JSON object with ``errors`` and optional ``descriptions``.

    Returns:
        Errors sorted by numeric code then symbolic name.

    Raises:
        ValueError: If the supported error mapping shape is invalid.
    """
    raw_errors = payload.get("errors")
    if not isinstance(raw_errors, Mapping):
        raise ValueError("RPC errors.errors must be an object mapping codes to error mappings")
    descriptions = payload.get("descriptions", {})
    if not isinstance(descriptions, Mapping):
        raise ValueError("RPC errors.descriptions must be an object when present")
    errors: list[TelegramRPCError] = []
    for raw_code, names in raw_errors.items():
        code = _integer(raw_code, field="RPC error code")
        if not isinstance(names, Mapping):
            raise ValueError(f"RPC errors[{raw_code!r}] must map names to method arrays")
        for raw_name, raw_methods in names.items():
            name = _required_string(raw_name, field=f"RPC errors[{raw_code!r}] name")
            methods = _string_sequence(raw_methods, field=f"RPC errors[{raw_code!r}][{name!r}]")
            description = _optional_description(descriptions.get(name))
            errors.append(
                TelegramRPCError(name=name, code=code, methods=tuple(sorted(set(methods))), description=description)
            )
    return tuple(sorted(errors, key=lambda item: (item.code, item.name, item.methods)))


def _string_sequence(value: object, *, field: str) -> tuple[str, ...]:
    """Validate a JSON array of non-empty strings.

    Args:
        value: Selected RPC-error method list or metadata precedence list.
        field: Dotted JSON location reported when a member is missing, blank,
            or not a string.

    Returns:
        Source-order non-empty strings.

    Raises:
        ValueError: If the value is not an array of non-empty strings.
    """
    if not isinstance(value, Sequence) or isinstance(value, str | bytes | bytearray):
        raise ValueError(f"{field} must be an array of strings")
    values = tuple(_required_string(item, field=field) for item in value)
    return values


def _required_string(value: object, *, field: str) -> str:
    """Return one non-empty string or raise a source-shape validation error.

    Args:
        value: Selected declaration identity, binding field, metadata field, or
            error-database value that the pinned input requires to be text.
        field: Dotted pinned-input location reported when the selected value is
            absent, non-textual or blank after trimming.

    Returns:
        Stripped non-empty text.

    Raises:
        ValueError: If the candidate is not a non-empty string.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_description(value: object) -> str | None:
    """Return non-empty normalized prose without fabricating an unavailable description.

    Args:
        value: Candidate declaration, parameter or error description value.

    Returns:
        Stripped prose when supplied as a non-empty string, otherwise ``None``.
    """
    return value.strip() if isinstance(value, str) and value.strip() else None


def _integer(value: object, *, field: str) -> int:
    """Parse an integer-like JSON key or scalar for a protocol identifier/code.

    Args:
        value: Selected schema identifier, RPC error code or metadata count in
            integer/base-ten/``0x`` string form.
        field: Dotted JSON location reported when the selected protocol value
            cannot be represented as an integer.

    Returns:
        Parsed integer.

    Raises:
        ValueError: If the candidate cannot be parsed as an integer.
    """
    if isinstance(value, bool):
        raise ValueError(f"{field} must be an integer")
    try:
        if isinstance(value, str):
            return int(value, 0)
        if isinstance(value, int | float):
            return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an integer") from exc
    raise ValueError(f"{field} must be an integer")


def _positive_integer(value: object, *, field: str) -> int:
    """Parse a strictly positive schema metadata integer.

    Args:
        value: Selected metadata layer or count value that must be an integer
            greater than zero.
        field: Dotted metadata location reported when the selected layer/count
            is absent, non-numeric, zero or negative.

    Returns:
        Positive parsed integer.

    Raises:
        ValueError: If the value is zero, negative or not an integer.
    """
    result = _integer(value, field=field)
    if result <= 0:
        raise ValueError(f"{field} must be positive")
    return result


def _constructor_id(value: object, *, field: str) -> str:
    """Normalize a signed or unsigned schema constructor ID to eight hex digits.

    Args:
        value: JSON numeric ID in signed decimal, unsigned decimal or ``0x`` form.
        field: Input field name included in validation failures.

    Returns:
        Unsigned ``0x``-prefixed 32-bit hexadecimal constructor identifier.
    """
    return f"0x{_integer(value, field=field) & 0xFFFFFFFF:08x}"


def _validate_metadata_reconciliation(
    metadata: Mapping[str, Any],
    *,
    declarations: Sequence[TelegramDeclaration],
    errors: Sequence[TelegramRPCError],
    layer: int,
) -> None:
    """Validate optional pinned counts and schema layer against extracted inputs.

    Args:
        metadata: Parsed schema metadata, which may record expected counts.
        declarations: Complete normalized canonical constructor and method set.
        errors: Complete flattened pinned RPC error set.
        layer: Validated structural layer used in generated frontmatter.

    Raises:
        ValueError: If a present count/layer is malformed, negative or does not
            reconcile with the static inputs.
    """
    expected_counts = {
        "constructor_count": sum(item.kind == "type" for item in declarations),
        "function_count": sum(item.kind == "function" for item in declarations),
        "rpc_error_count": len(errors),
    }
    for field, actual in expected_counts.items():
        if field not in metadata:
            continue
        expected = _integer(metadata[field], field=f"metadata.{field}")
        if expected < 0:
            raise ValueError(f"metadata.{field} must not be negative")
        if expected != actual:
            raise ValueError(f"metadata.{field}={expected} does not match extracted value {actual}")
    if "schema_layer" in metadata:
        schema_layer = _positive_integer(metadata["schema_layer"], field="metadata.schema_layer")
        if schema_layer != layer:
            raise ValueError(f"metadata.schema_layer={schema_layer} does not match metadata.layer={layer}")


def _metadata_url(metadata: Mapping[str, Any], *fields: str) -> str:
    """Return the first non-empty metadata URL among supported fallback field names.

    Args:
        metadata: Parsed schema metadata object.
        *fields: Ordered candidate URL field names.

    Returns:
        First configured URL.

    Raises:
        ValueError: If none of the supported metadata fields contains a URL.
    """
    for field in fields:
        value = _optional_description(metadata.get(field))
        if value is not None:
            return value
    rendered = ", ".join(fields)
    raise ValueError(f"metadata requires one of: {rendered}")


def _metadata_url_or_repository_fallback(metadata: Mapping[str, Any], *, fallback: str, fields: Sequence[str]) -> str:
    """Return a pinned metadata URL or the checked-in repository source fallback.

    Args:
        metadata: Parsed selected-layer schema metadata object.
        fallback: Non-empty repository URL for the checked-in pinned input when
            no upstream URL is present in the metadata.
        fields: Ordered metadata URL field names to prefer over the fallback.

    Returns:
        First configured non-empty URL, otherwise the validated checked-in
        repository source URL.
    """
    for field in fields:
        value = _optional_description(metadata.get(field))
        if value is not None:
            return value
    return _required_string(fallback, field="repository fallback URL")


def _repository_url(repository_url: str) -> str:
    """Normalize a repository browser base URL for local pinned-input links.

    Args:
        repository_url: Configured repository URL without a required trailing slash.

    Returns:
        Non-empty URL with trailing slash removed.

    Raises:
        ValueError: If the URL is empty after trimming.
    """
    return _required_string(repository_url, field="repository_url").rstrip("/")


def _declaration_paths(
    declarations: Iterable[TelegramDeclaration], *, category: str, reserved_routes: Iterable[str] = ()
) -> dict[TelegramDeclaration, str]:
    """Assign deterministic declaration paths while reserving every generated index route.

    Args:
        declarations: Function or type declarations to route.
        category: Top-level route category, ``functions`` or ``types``.
        reserved_routes: Routes already allocated to global, namespace, result or error indexes.

    Returns:
        Mapping from each declaration to its unique relative Markdown path.
    """
    used_paths: set[str] = set()
    used_routes = set(reserved_routes)
    paths: dict[TelegramDeclaration, str] = {}
    for declaration in sorted(declarations, key=lambda item: (item.name, item.constructor_id)):
        namespace = _namespace(declaration.name)
        leaf = _slug(_leaf_name(declaration.name))
        if leaf == "index":
            leaf = f"{leaf}-{declaration.constructor_id[2:]}"
        candidate = f"telegram/{category}/{namespace}/{leaf}.md"
        paths[declaration] = _unique_path(
            candidate, identifier=declaration.constructor_id[2:], used_paths=used_paths, used_routes=used_routes
        )
    return paths


def _error_paths(
    errors: Sequence[TelegramRPCError], *, reserved_routes: Iterable[str] = ()
) -> dict[TelegramRPCError, str]:
    """Assign deterministic error paths while reserving every existing generated route.

    Args:
        errors: Flattened error specifications to route.
        reserved_routes: Routes already allocated to declaration or index pages.

    Returns:
        Mapping from every error code/name pair to a unique path.
    """
    used_paths: set[str] = set()
    used_routes = set(reserved_routes)
    paths: dict[TelegramRPCError, str] = {}
    for error in sorted(errors, key=lambda item: (item.name, item.code)):
        leaf = _slug(_PARAMETERIZED_ERROR.sub("", error.name))
        if leaf == "index":
            leaf = f"{leaf}-{error.code}"
        candidate = f"telegram/errors/{leaf}.md"
        paths[error] = _unique_path(
            candidate, identifier=str(error.code), used_paths=used_paths, used_routes=used_routes
        )
    return paths


def _unique_path(candidate: str, *, identifier: str, used_paths: set[str], used_routes: set[str]) -> str:
    """Reserve a candidate path and route or suffix it with a stable identity.

    Args:
        candidate: Preferred relative Markdown path.
        identifier: Stable constructor-ID or error-code suffix for collisions.
        used_paths: Mutable paths allocated in the current category.
        used_routes: Mutable global routes already allocated or reserved by indexes.

    Returns:
        A path and Starlight route not already present in the supplied sets.
    """
    if candidate not in used_paths and _route_for_path(candidate) not in used_routes:
        used_paths.add(candidate)
        used_routes.add(_route_for_path(candidate))
        return candidate
    stem = candidate.removesuffix(".md")
    numbered = f"{stem}-{identifier}.md"
    index = 2
    while numbered in used_paths or _route_for_path(numbered) in used_routes:
        numbered = f"{stem}-{identifier}-{index}.md"
        index += 1
    used_paths.add(numbered)
    used_routes.add(_route_for_path(numbered))
    return numbered


def _route_for_path(path: str) -> str:
    """Return the Starlight reference route represented by one generated Markdown path.

    Args:
        path: Relative Markdown path below the generated reference root.

    Returns:
        Absolute trailing-slash reference route.
    """
    route_path = path.removesuffix("index.md").removesuffix(".md").rstrip("/")
    return f"/reference/{route_path}/"


def _routes_for_paths(paths: Iterable[str]) -> frozenset[str]:
    """Convert generated Markdown paths to their corresponding stable reference routes.

    Args:
        paths: Relative generated Markdown paths.

    Returns:
        Immutable set of derived Starlight routes.
    """
    return frozenset(_route_for_path(path) for path in paths)


def _result_family_paths(declarations: Sequence[TelegramDeclaration]) -> Mapping[str, str]:
    """Assign collision-safe stable index paths for all constructor result families.

    Args:
        declarations: Canonical type constructors grouped by their raw result families.

    Returns:
        Result-family to generated index-path mapping.
    """
    families = sorted({_result_family(item.result_type) for item in declarations})
    used_paths: set[str] = set()
    used_routes: set[str] = set()
    return {
        family: _unique_path(
            f"telegram/types/results/{_slug(family)}/index.md",
            identifier=_stable_identifier(family),
            used_paths=used_paths,
            used_routes=used_routes,
        )
        for family in families
    }


def _stable_identifier(value: str) -> str:
    """Return a short deterministic suffix for non-ID index-route collisions.

    Args:
        value: Exact family or other textual identity requiring a route suffix.

    Returns:
        First eight hexadecimal characters of the identity's SHA-256 digest.
    """
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]


def _reserved_index_routes(
    declarations: Sequence[TelegramDeclaration],
    errors: Sequence[TelegramRPCError],
    *,
    result_family_paths: Mapping[str, str],
) -> frozenset[str]:
    """Reserve every index route before assigning declaration and error detail pages.

    Args:
        declarations: Complete normalized canonical function and type declarations.
        errors: Flattened pinned RPC errors represented by the error indexes.
        result_family_paths: Preallocated collision-safe result-family index paths.

    Returns:
        Immutable route set that cannot be claimed by a detail page.
    """
    function_namespaces = {_namespace(item.name) for item in declarations if item.kind == "function"}
    type_namespaces = {_namespace(item.name) for item in declarations if item.kind == "type"}
    paths = {
        "telegram/index.md",
        "telegram/functions/index.md",
        "telegram/types/index.md",
        "telegram/errors/index.md",
        "telegram/errors/by-code/index.md",
        "telegram/errors/by-name/index.md",
        "telegram/errors/by-method/index.md",
        *(f"telegram/functions/{namespace}/index.md" for namespace in function_namespaces),
        *(f"telegram/types/{namespace}/index.md" for namespace in type_namespaces),
        *result_family_paths.values(),
    }
    if not errors:
        paths.add("telegram/errors/index.md")
    return _routes_for_paths(paths)


def _namespace(name: str) -> str:
    """Return the first raw namespace segment or ``base`` for unqualified names.

    Args:
        name: Exact method or predicate name from the canonical schema.

    Returns:
        Collision-safe namespace route segment.
    """
    return _slug(name.split(".", 1)[0]) if "." in name else "base"


def _leaf_name(name: str) -> str:
    """Return the final raw namespace segment used as a declaration page name.

    Args:
        name: Exact qualified or unqualified declaration name.

    Returns:
        Text after the final dot or the original unqualified name.
    """
    return name.rsplit(".", 1)[-1]


def _slug(value: str) -> str:
    """Convert a raw Telegram identity segment to a stable kebab-case path segment.

    Args:
        value: Raw method, predicate, result-family or error-name segment.

    Returns:
        Non-empty collision-readable lowercase route segment.
    """
    normalized = _CAMEL_BOUNDARY.sub("-", value)
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.casefold()).strip("-")
    return slug or "symbol"


def _errors_by_method(errors: Sequence[TelegramRPCError]) -> Mapping[str, tuple[TelegramRPCError, ...]]:
    """Index pinned errors by every mapped canonical method name.

    Args:
        errors: Flattened error specifications from the pinned error database.

    Returns:
        Method-to-error tuples sorted by code and symbolic name.
    """
    indexed: defaultdict[str, list[TelegramRPCError]] = defaultdict(list)
    for error in errors:
        for method in error.methods:
            indexed[method].append(error)
    return {method: tuple(sorted(items, key=lambda item: (item.code, item.name))) for method, items in indexed.items()}


def _availability_by_method(payload: Mapping[str, Any]) -> Mapping[str, tuple[str, ...]]:
    """Index only explicit user/bot/business/unauthenticated availability evidence.

    Args:
        payload: Pinned RPC-error database which may contain availability arrays.

    Returns:
        Method-to-evidence labels. Methods absent from these arrays receive no
        availability statement rather than an inferred one.
    """
    labels = {
        "user_only": "user only",
        "bot_only": "bot only",
        "business_supported": "business supported",
        "unauthed_allowed": "unauthenticated allowed",
    }
    indexed: defaultdict[str, list[str]] = defaultdict(list)
    for field, label in labels.items():
        values = payload.get(field, ())
        if not isinstance(values, Sequence) or isinstance(values, str | bytes | bytearray):
            continue
        for value in values:
            if isinstance(value, str) and value.strip():
                indexed[value].append(label)
    return {method: tuple(sorted(set(items))) for method, items in indexed.items()}


@dataclass(frozen=True, slots=True)
class _TelegramRelationshipIndex:
    """Cache all structural relationships required by detailed Telegram pages.

    Attributes:
        functions_by_name: Canonical function declarations keyed by exact TL name.
        errors_by_method: Pinned errors keyed by their mapped method name.
        availability_by_method: Explicit source-backed availability labels by method.
        accepted_types: Non-primitive parameter-type families by function.
        returned_types: Non-primitive return-type families by function.
        related_methods: Functions sharing at least one accepted or returned family.
        related_constructors: Constructors sharing the same result family.
        constructors_by_family: Constructors grouped by their exact raw result family.
        accepted_by: Declarations accepting each result family in a parameter.
        returned_by: Functions returning each result family.
    """

    functions_by_name: Mapping[str, TelegramDeclaration]
    errors_by_method: Mapping[str, tuple[TelegramRPCError, ...]]
    availability_by_method: Mapping[str, tuple[str, ...]]
    accepted_types: Mapping[TelegramDeclaration, tuple[str, ...]]
    returned_types: Mapping[TelegramDeclaration, tuple[str, ...]]
    related_methods: Mapping[TelegramDeclaration, tuple[TelegramDeclaration, ...]]
    related_constructors: Mapping[TelegramDeclaration, tuple[TelegramDeclaration, ...]]
    constructors_by_family: Mapping[str, tuple[TelegramDeclaration, ...]]
    accepted_by: Mapping[TelegramDeclaration, tuple[TelegramDeclaration, ...]]
    returned_by: Mapping[TelegramDeclaration, tuple[TelegramDeclaration, ...]]


def _relationship_index(
    declarations: Sequence[TelegramDeclaration], errors: Sequence[TelegramRPCError], rpc_errors: Mapping[str, Any]
) -> _TelegramRelationshipIndex:
    """Precompute complete declaration/error relationships without per-page full scans.

    Args:
        declarations: Complete normalized canonical function and type declaration set.
        errors: Complete flattened pinned RPC error records.
        rpc_errors: Original pinned error database containing explicit availability arrays.

    Returns:
        Cached linkable relationships reused by every detailed page and manifest edge.
    """
    functions = tuple(item for item in declarations if item.kind == "function")
    types = tuple(item for item in declarations if item.kind == "type")
    accepted_types: dict[TelegramDeclaration, tuple[str, ...]] = {}
    returned_types: dict[TelegramDeclaration, tuple[str, ...]] = {}
    functions_by_reference: defaultdict[str, set[TelegramDeclaration]] = defaultdict(set)
    accepted_by_family: defaultdict[str, set[TelegramDeclaration]] = defaultdict(set)
    returned_by_family: defaultdict[str, set[TelegramDeclaration]] = defaultdict(set)
    for declaration in declarations:
        accepted = tuple(sorted(_parameter_type_references(declaration.parameters)))
        for family in accepted:
            accepted_by_family[family].add(declaration)
        if declaration.kind != "function":
            continue
        returned = tuple(sorted(_type_references(declaration.result_type)))
        accepted_types[declaration] = accepted
        returned_types[declaration] = returned
        for family in set(accepted) | set(returned):
            functions_by_reference[family].add(declaration)
        for family in returned:
            returned_by_family[family].add(declaration)
    families: defaultdict[str, list[TelegramDeclaration]] = defaultdict(list)
    for declaration in types:
        families[_result_family(declaration.result_type)].append(declaration)
    related_methods = {
        declaration: tuple(
            sorted(
                {
                    other
                    for family in set(accepted_types[declaration]) | set(returned_types[declaration])
                    for other in functions_by_reference[family]
                    if other != declaration
                },
                key=lambda item: (item.name, item.constructor_id),
            )
        )
        for declaration in functions
    }
    related_constructors = {
        declaration: tuple(
            item
            for item in sorted(
                families[_result_family(declaration.result_type)], key=lambda item: (item.name, item.constructor_id)
            )
            if item != declaration
        )
        for declaration in types
    }
    accepted_by = {
        declaration: tuple(
            sorted(
                accepted_by_family[_result_family(declaration.result_type)],
                key=lambda item: (item.kind, item.name, item.constructor_id),
            )
        )
        for declaration in types
    }
    returned_by = {
        declaration: tuple(
            sorted(
                returned_by_family[_result_family(declaration.result_type)],
                key=lambda item: (item.name, item.constructor_id),
            )
        )
        for declaration in types
    }
    return _TelegramRelationshipIndex(
        functions_by_name={item.name: item for item in functions},
        errors_by_method=_errors_by_method(errors),
        availability_by_method=_availability_by_method(rpc_errors),
        accepted_types=accepted_types,
        returned_types=returned_types,
        related_methods=related_methods,
        related_constructors=related_constructors,
        constructors_by_family={
            family: tuple(sorted(items, key=lambda item: (item.name, item.constructor_id)))
            for family, items in families.items()
        },
        accepted_by=accepted_by,
        returned_by=returned_by,
    )


def _declaration_page(
    declaration: TelegramDeclaration,
    *,
    path: str,
    binding: TelegramPythonBinding,
    relationship_index: _TelegramRelationshipIndex,
    declaration_paths: Mapping[TelegramDeclaration, str],
    error_paths: Mapping[TelegramRPCError, str],
    result_family_paths: Mapping[str, str],
    canonical_source: str,
    structural_url: str,
    repository_base: str,
    metadata: Mapping[str, Any],
) -> ReferencePage:
    """Render one function or constructor page from canonical static data.

    Args:
        declaration: Canonical declaration to render.
        path: Precomputed collision-safe relative Markdown page path.
        binding: Exact static public Python import binding for this declaration.
        relationship_index: Precomputed errors, availability and structural relationship cache.
        declaration_paths: All generated function/type paths keyed by canonical declaration.
        error_paths: All generated error paths keyed by pinned error identity.
        result_family_paths: Generated result-family index paths keyed by raw family name.
        canonical_source: Canonical structural source identifier, normally TDLib.
        structural_url: Canonical external schema source URL for provenance text.
        repository_base: Repository browser URL for pinned local JSON source links.
        metadata: Full metadata object providing merge precedence, notes and diffs.

    Returns:
        A frontmatter-ready Telegram reference page.
    """
    body = _declaration_body(
        declaration,
        binding=binding,
        relationship_index=relationship_index,
        declaration_paths=declaration_paths,
        error_paths=error_paths,
        result_family_paths=result_family_paths,
        canonical_source=canonical_source,
        structural_url=structural_url,
        metadata=metadata,
    )
    return ReferencePage(
        path=path,
        title=declaration.name,
        description=_schema_description(declaration.description),
        language="telegram",
        kind=declaration.kind,
        qualified_name=declaration.name,
        source_path="tools/schema/schema.json",
        source_url=f"{repository_base}/blob/master/tools/schema/schema.json",
        body=body,
        namespace=_namespace(declaration.name),
        schema_source=canonical_source,
        constructor_id=declaration.constructor_id,
    )


def _declaration_body(
    declaration: TelegramDeclaration,
    *,
    binding: TelegramPythonBinding,
    relationship_index: _TelegramRelationshipIndex,
    declaration_paths: Mapping[TelegramDeclaration, str],
    error_paths: Mapping[TelegramRPCError, str],
    result_family_paths: Mapping[str, str],
    canonical_source: str,
    structural_url: str,
    metadata: Mapping[str, Any],
) -> str:
    """Render detailed Markdown sections for one canonical declaration.

    Args:
        declaration: Function or type declaration whose exact TL structure is rendered.
        binding: Exact static public Python binding for the declaration.
        relationship_index: Precomputed errors, availability and structural relationships.
        declaration_paths: All generated detail paths keyed by declaration.
        error_paths: All generated RPC error paths keyed by error identity.
        result_family_paths: All generated result-family index paths keyed by family.
        canonical_source: Identifier for the structure-authoritative source.
        structural_url: External canonical schema URL for provenance.
        metadata: Source metadata supplying prose precedence, notes and diffs.

    Returns:
        Deterministic Markdown body without frontmatter.
    """
    lines = [
        f"# `{declaration.name}`",
        "",
        _schema_description(declaration.description),
        "",
        "## Signature",
        "",
        "```tl",
        _signature(declaration),
        "```",
        "",
        "## Result type",
        "",
        f"`{declaration.result_type}`",
        "",
        "## Parameters",
        "",
        "| Name | Type | Flag | Default | Description |",
        "| --- | --- | --- | --- | --- |",
    ]
    if declaration.parameters:
        lines.extend(_parameter_row(parameter) for parameter in declaration.parameters)
    else:
        lines.append("| — | — | — | — | This declaration has no parameters. |")
    flag_rows = _flag_rows(declaration.parameters)
    if flag_rows:
        lines.extend(["", "## Flags", "", "| Parameter | Bit | Meaning |", "| --- | ---: | --- |"])
        lines.extend(flag_rows)
    lines.extend(_python_binding_sections(declaration, binding=binding))
    lines.extend(_safe_usage_sections(declaration, binding=binding))
    family = _result_family(declaration.result_type)
    lines.extend(["", "## Result family", "", _family_link(family, result_family_paths=result_family_paths)])
    if declaration.kind == "function":
        lines.extend(
            _function_sections(
                declaration,
                relationship_index=relationship_index,
                declaration_paths=declaration_paths,
                error_paths=error_paths,
                result_family_paths=result_family_paths,
            )
        )
    else:
        lines.extend(
            _type_relationship_sections(
                declaration,
                relationship_index=relationship_index,
                declaration_paths=declaration_paths,
                result_family_paths=result_family_paths,
            )
        )
    lines.extend(
        _provenance_sections(metadata, canonical_source=canonical_source, structural_url=structural_url, error_url=None)
    )
    return "\n".join(lines)


def _python_binding_sections(declaration: TelegramDeclaration, *, binding: TelegramPythonBinding) -> tuple[str, ...]:
    """Render the exact generated public Python import without loading its module.

    Args:
        declaration: Canonical declaration receiving the binding section.
        binding: Source-owned manifest binding reconciled to the declaration identity.

    Returns:
        Markdown lines containing the stable public import and access path.
    """
    return (
        "",
        "## Python binding",
        "",
        "```python",
        binding.python_import,
        "```",
        "",
        f"Public access: `{binding.public_access}`.",
    )


def _safe_usage_sections(declaration: TelegramDeclaration, *, binding: TelegramPythonBinding) -> tuple[str, ...]:
    """Render a minimal local-only binding shape without implying a network operation.

    Args:
        declaration: Canonical function or type declaration being documented.
        binding: Exact public Python binding for the declaration.

    Returns:
        Markdown lines that name the binding without constructing, sending or authenticating.
    """
    variable = "request_type" if declaration.kind == "function" else "constructor_type"
    noun = "request" if declaration.kind == "function" else "constructor"
    return (
        "",
        "## Safe usage shape",
        "",
        "```python",
        binding.python_import,
        "",
        f"# Naming the raw {noun} class is local only; it performs no I/O or network request.",
        f"{variable} = {binding.python_name}",
        "```",
    )


def _signature(declaration: TelegramDeclaration) -> str:
    """Render the exact normalized declaration as a compact raw TL signature.

    Args:
        declaration: Canonical constructor or method declaration to serialize.

    Returns:
        ``name#id parameters = result;`` using the normalized canonical fields.
    """
    parameters = " ".join(f"{parameter.name}:{parameter.type_name}" for parameter in declaration.parameters)
    separator = " " if parameters else ""
    return f"{declaration.name}#{declaration.constructor_id[2:]}{separator}{parameters} = {declaration.result_type};"


def _parameter_row(parameter: TelegramParameter) -> str:
    """Render one parameter table row with flags/defaults and honest missing prose.

    Args:
        parameter: Normalized declaration parameter to present.

    Returns:
        Escaped Markdown table row.
    """
    flag = _flag_label(parameter.type_name)
    default = parameter.default if parameter.default is not None else "—"
    return f"| {_markdown_cell(parameter.name)} | {_markdown_cell(parameter.type_name)} | {_markdown_cell(flag)} | {_markdown_cell(default)} | {_markdown_cell(_schema_description(parameter.description))} |"


def _flag_label(type_name: str) -> str:
    """Return a parameter's raw flag location or non-conditional marker.

    Args:
        type_name: Exact normalized raw TL type expression.

    Returns:
        ``flag word`` for ``#``, ``word.bit`` for conditional fields or an em dash.
    """
    if type_name == "#":
        return "flag word"
    match = _FLAG_TYPE.fullmatch(type_name)
    return f"{match['word']}.{match['bit']}" if match is not None else "—"


def _flag_rows(parameters: Sequence[TelegramParameter]) -> tuple[str, ...]:
    """Render explicit flag-bit rows derived solely from conditional TL parameter types.

    Args:
        parameters: Ordered canonical parameters to inspect.

    Returns:
        Markdown rows for every ``word.bit?type`` parameter in source order.
    """
    rows: list[str] = []
    for parameter in parameters:
        match = _FLAG_TYPE.fullmatch(parameter.type_name)
        if match is None:
            continue
        rows.append(
            "| {name} | {bit} | Controlled by `{word}`; present when this bit is set. |".format(
                name=_markdown_cell(parameter.name), bit=match["bit"], word=match["word"]
            )
        )
    return tuple(rows)


def _function_sections(
    declaration: TelegramDeclaration,
    *,
    relationship_index: _TelegramRelationshipIndex,
    declaration_paths: Mapping[TelegramDeclaration, str],
    error_paths: Mapping[TelegramRPCError, str],
    result_family_paths: Mapping[str, str],
) -> tuple[str, ...]:
    """Render method-specific errors, availability and structural relationships.

    Args:
        declaration: Function declaration for which relationships are rendered.
        relationship_index: Precomputed errors, availability and structural relationships.
        declaration_paths: All generated declaration detail paths.
        error_paths: All generated pinned RPC error paths.
        result_family_paths: All generated result-family index paths.

    Returns:
        Markdown lines appended after the result family section.
    """
    lines = ["", "## RPC errors", ""]
    errors = relationship_index.errors_by_method.get(declaration.name, ())
    if errors:
        lines.extend(["| Code | Error | Description |", "| ---: | --- | --- |"])
        lines.extend(
            f"| {error.code} | {_page_link(error.name, error_paths[error])} | {_markdown_cell(_error_description(error.description))} |"
            for error in errors
        )
    else:
        lines.append("No RPC errors are mapped to this method by the pinned error database.")
    accepted_types = relationship_index.accepted_types[declaration]
    returned_types = relationship_index.returned_types[declaration]
    lines.extend(
        [
            "",
            "## Accepted types",
            "",
            _family_links(accepted_types, result_family_paths=result_family_paths),
            _family_constructor_links(
                accepted_types,
                constructors_by_family=relationship_index.constructors_by_family,
                declaration_paths=declaration_paths,
            ),
        ]
    )
    lines.extend(
        [
            "",
            "## Returned types",
            "",
            _family_links(returned_types, result_family_paths=result_family_paths),
            _family_constructor_links(
                returned_types,
                constructors_by_family=relationship_index.constructors_by_family,
                declaration_paths=declaration_paths,
            ),
        ]
    )
    related_methods = relationship_index.related_methods[declaration]
    if related_methods:
        lines.extend(
            [
                "",
                "## Related methods",
                "",
                ", ".join(_declaration_link(item, declaration_paths=declaration_paths) for item in related_methods),
            ]
        )
    availability = relationship_index.availability_by_method.get(declaration.name, ())
    if availability:
        lines.extend(["", "## Availability evidence", ""])
        lines.extend(f"- {item}" for item in availability)
    return tuple(lines)


def _type_relationship_sections(
    declaration: TelegramDeclaration,
    *,
    relationship_index: _TelegramRelationshipIndex,
    declaration_paths: Mapping[TelegramDeclaration, str],
    result_family_paths: Mapping[str, str],
) -> tuple[str, ...]:
    """Render constructor relationships derived from canonical structural references.

    Args:
        declaration: Type constructor whose result family is related.
        relationship_index: Precomputed structural relationship cache.
        declaration_paths: All generated declaration detail paths.
        result_family_paths: Generated result-family index paths.

    Returns:
        Markdown lines naming related constructors and accepted/returned use sites.
    """
    family = _result_family(declaration.result_type)
    related = relationship_index.related_constructors[declaration]
    accepted_by = relationship_index.accepted_by[declaration]
    returned_by = relationship_index.returned_by[declaration]
    lines = [
        "",
        "## Relationships",
        "",
        f"- Result family: {_family_link(family, result_family_paths=result_family_paths)}",
    ]
    if related:
        lines.append(
            f"- Related constructors: {', '.join(_declaration_link(item, declaration_paths=declaration_paths) for item in related)}"
        )
    if accepted_by:
        lines.append(
            f"- Accepted by: {', '.join(_declaration_link(item, declaration_paths=declaration_paths) for item in accepted_by)}"
        )
    if returned_by:
        lines.append(
            f"- Returned by: {', '.join(_declaration_link(item, declaration_paths=declaration_paths) for item in returned_by)}"
        )
    if len(lines) == 4:
        lines.append("- No additional canonical relationships were found.")
    return tuple(lines)


def _declaration_link(declaration: TelegramDeclaration, *, declaration_paths: Mapping[TelegramDeclaration, str]) -> str:
    """Render one exact canonical declaration link using its preallocated detail path.

    Args:
        declaration: Canonical declaration to link.
        declaration_paths: Generated paths keyed by canonical declaration identity.

    Returns:
        Stable Markdown link preserving the exact raw qualified name.
    """
    return _page_link(declaration.name, declaration_paths[declaration])


def _family_link(family: str, *, result_family_paths: Mapping[str, str]) -> str:
    """Render one linked result-family identity or label a structural family with no page.

    Args:
        family: Raw non-primitive TL result family.
        result_family_paths: Generated result-family indexes keyed by exact family.

    Returns:
        Markdown link for a known family or an explicit non-page label.
    """
    path = result_family_paths.get(family)
    return _page_link(family, path) if path is not None else f"`{family}` (no selected constructor result-family page)"


def _family_links(families: Sequence[str], *, result_family_paths: Mapping[str, str]) -> str:
    """Render linked type-family relationships or an explicit empty relationship result.

    Args:
        families: Ordered non-primitive raw TL families.
        result_family_paths: Generated result-family indexes keyed by exact family.

    Returns:
        Comma-separated links or a stable explanation when no relationship exists.
    """
    if not families:
        return "No non-primitive type relationships were found."
    return ", ".join(_family_link(family, result_family_paths=result_family_paths) for family in families)


def _family_constructor_links(
    families: Sequence[str],
    *,
    constructors_by_family: Mapping[str, Sequence[TelegramDeclaration]],
    declaration_paths: Mapping[TelegramDeclaration, str],
) -> str:
    """Render selected constructor links for otherwise family-level type references.

    Args:
        families: Ordered raw type families referenced by a function signature.
        constructors_by_family: Precomputed selected constructors keyed by result family.
        declaration_paths: Generated detail paths keyed by canonical constructor.

    Returns:
        Constructor links when the selected layer exposes matching constructors,
        otherwise an empty string so the caller makes no unsupported claim.
    """
    constructors = tuple(declaration for family in families for declaration in constructors_by_family.get(family, ()))
    if not constructors:
        return ""
    return "Known selected constructors: " + ", ".join(
        _declaration_link(declaration, declaration_paths=declaration_paths) for declaration in constructors
    )


def _result_family(type_name: str) -> str:
    """Return a readable primary raw TL result family from a type expression.

    Args:
        type_name: Exact normalized raw TL result type expression.

    Returns:
        Outer result family or the first referenced type when generic syntax is used.
    """
    references = _type_references(type_name)
    return sorted(references)[0] if references else type_name


def _parameter_type_references(parameters: Sequence[TelegramParameter]) -> set[str]:
    """Collect referenced raw TL type names from ordered declaration parameters.

    Args:
        parameters: Canonical parameter specifications to inspect.

    Returns:
        Distinct non-primitive type names.
    """
    references: set[str] = set()
    for parameter in parameters:
        references.update(_type_references(parameter.type_name))
    return references


def _type_references(type_name: str) -> set[str]:
    """Extract non-primitive type identifiers from a raw TL expression.

    Args:
        type_name: Raw type expression that may include vectors, flags or generics.

    Returns:
        Identifier set excluding scalar primitives and conditional flag words.
    """
    match = _FLAG_TYPE.fullmatch(type_name)
    if match is not None:
        type_name = match["value"]
    references = {item for item in _IDENTIFIER.findall(type_name) if item.casefold() not in _PRIMITIVE_TYPES}
    return {item for item in references if item != "Vector"}


def _error_page(
    error: TelegramRPCError,
    *,
    path: str,
    binding: TelegramPythonErrorBinding,
    relationship_index: _TelegramRelationshipIndex,
    function_paths: Mapping[TelegramDeclaration, str],
    layer: int,
    canonical_source: str,
    error_url: str,
    repository_base: str,
    metadata: Mapping[str, Any],
) -> ReferencePage:
    """Render one independently pinned RPC error reference page.

    Args:
        error: Pinned error code/name/method mapping to document.
        path: Precomputed collision-safe relative Markdown page path.
        binding: Exact public generated Python error-class binding.
        relationship_index: Precomputed canonical function lookup by exact TL name.
        function_paths: Generated canonical function paths keyed by declaration.
        layer: Validated selected Telegram schema layer for common frontmatter.
        canonical_source: Canonical structural source identifier for common provenance.
        error_url: Pinned upstream RPC-error URL or checked-in repository fallback.
        repository_base: Repository browser base for local error JSON source links.
        metadata: Full schema metadata supplying source note and diff context.

    Returns:
        A Telegram reference page containing code, parameterization, methods, and
        independent error provenance.
    """
    methods = _error_method_links(
        error.methods, relationship_index=relationship_index, function_paths=function_paths, layer=layer
    )
    body_lines = [
        f"# `{error.name}`",
        "",
        _error_description(error.description),
        "",
        "## Error details",
        "",
        f"- code: {error.code}",
        f"- parameterized: {'yes' if _PARAMETERIZED_ERROR.search(error.name) else 'no'}",
        f"- mapped methods: {methods}",
        "",
        "## Python error class",
        "",
        "```python",
        binding.python_import,
        "```",
        "",
        f"Public access: `{binding.public_access}`.",
    ]
    body_lines.extend(
        _provenance_sections(metadata, canonical_source=canonical_source, structural_url=None, error_url=error_url)
    )
    return ReferencePage(
        path=path,
        title=error.name,
        description=_error_description(error.description),
        language="telegram",
        kind="error",
        qualified_name=f"{error.code}:{error.name}",
        source_path="tools/schema/rpc-errors.json",
        source_url=f"{repository_base}/blob/master/tools/schema/rpc-errors.json",
        body="\n".join(body_lines),
        namespace="errors",
        schema_source=canonical_source,
    )


def _error_method_links(
    methods: Sequence[str],
    *,
    relationship_index: _TelegramRelationshipIndex,
    function_paths: Mapping[TelegramDeclaration, str],
    layer: int,
) -> str:
    """Render pinned error methods as links or explicit external-to-layer mappings.

    Args:
        methods: Exact method names recorded by the pinned RPC-error database.
        relationship_index: Precomputed selected-layer function declarations by name.
        function_paths: Generated function paths keyed by canonical declaration.
        layer: Selected canonical Telegram layer used to qualify unmatched mappings.

    Returns:
        Linked methods or a non-deceptive label for mappings absent from the selected layer.
    """
    if not methods:
        return "No methods are mapped."
    rendered = []
    for method in methods:
        declaration = relationship_index.functions_by_name.get(method)
        if declaration is None:
            rendered.append(f"`{method}` (not in selected Layer {layer} schema)")
        else:
            rendered.append(_declaration_link(declaration, declaration_paths=function_paths))
    return ", ".join(rendered)


def _validate_page_routes(pages: Sequence[ReferencePage]) -> None:
    """Reject duplicate Markdown paths or route-equivalent generated pages.

    Args:
        pages: Fully rendered detail and index pages to validate.

    Raises:
        ValueError: If two pages use the same path or resolve to the same
            Starlight reference route.
    """
    paths: set[str] = set()
    routes: dict[str, str] = {}
    for page in pages:
        if page.path in paths:
            raise ValueError(f"duplicate Telegram reference path: {page.path}")
        paths.add(page.path)
        route = _route_for_path(page.path)
        existing = routes.setdefault(route, page.path)
        if existing != page.path:
            raise ValueError(f"Telegram reference route collision: {existing} and {page.path} both map to {route}")


def _relationship_manifest(
    *,
    layer: int,
    relationship_index: _TelegramRelationshipIndex,
    declaration_paths: Mapping[TelegramDeclaration, str],
    error_paths: Mapping[TelegramRPCError, str],
    result_family_paths: Mapping[str, str],
) -> str:
    """Serialize a deterministic machine-readable relationship graph for outer writers.

    Args:
        layer: Validated selected Telegram schema layer.
        relationship_index: Precomputed source-backed declaration/error relationships.
        declaration_paths: Generated declaration detail paths keyed by declaration.
        error_paths: Generated RPC error detail paths keyed by pinned error.
        result_family_paths: Generated result-family index paths keyed by raw family.

    Returns:
        Pretty, key-sorted JSON with a schema version and stable relationship records.
    """
    relationships: list[dict[str, object]] = []
    functions = tuple(
        sorted(relationship_index.functions_by_name.values(), key=lambda item: (item.name, item.constructor_id))
    )
    for function in functions:
        source = _declaration_relationship_node(function, declaration_paths=declaration_paths)
        for error in relationship_index.errors_by_method.get(function.name, ()):
            relationships.append(
                {
                    "relation": "rpc_error",
                    "source": source,
                    "target": _error_relationship_node(error, error_paths=error_paths, selected_layer=True),
                }
            )
        for family in relationship_index.accepted_types[function]:
            relationships.append(
                {
                    "relation": "accepts_type_family",
                    "source": source,
                    "target": _result_family_relationship_node(family, result_family_paths=result_family_paths),
                }
            )
        for family in relationship_index.returned_types[function]:
            relationships.append(
                {
                    "relation": "returns_type_family",
                    "source": source,
                    "target": _result_family_relationship_node(family, result_family_paths=result_family_paths),
                }
            )
    types = tuple(
        sorted(
            (declaration for declaration in declaration_paths if declaration.kind == "type"),
            key=lambda item: (item.name, item.constructor_id),
        )
    )
    for declaration in types:
        relationships.append(
            {
                "relation": "constructor_result_family",
                "source": _declaration_relationship_node(declaration, declaration_paths=declaration_paths),
                "target": _result_family_relationship_node(
                    _result_family(declaration.result_type), result_family_paths=result_family_paths
                ),
            }
        )
    ordered = sorted(relationships, key=_relationship_sort_key)
    return json.dumps({"schema_version": 1, "layer": layer, "relationships": ordered}, indent=2, sort_keys=True) + "\n"


def _declaration_relationship_node(
    declaration: TelegramDeclaration, *, declaration_paths: Mapping[TelegramDeclaration, str]
) -> dict[str, object]:
    """Return one stable machine-readable declaration relationship endpoint.

    Args:
        declaration: Canonical function or constructor endpoint.
        declaration_paths: Generated detail paths keyed by canonical declaration.

    Returns:
        Object with exact kind, qualified name, constructor ID and generated path.
    """
    return {
        "kind": declaration.kind,
        "qualified_name": declaration.name,
        "constructor_id": declaration.constructor_id,
        "path": declaration_paths[declaration],
    }


def _error_relationship_node(
    error: TelegramRPCError, *, error_paths: Mapping[TelegramRPCError, str], selected_layer: bool
) -> dict[str, object]:
    """Return one stable machine-readable RPC-error relationship endpoint.

    Args:
        error: Pinned error code/name mapping.
        error_paths: Generated detail paths keyed by error identity.
        selected_layer: Whether the associated mapping exists in the selected schema layer.

    Returns:
        Object with code-qualified identity, null constructor ID, path and layer status.
    """
    return {
        "kind": "error",
        "qualified_name": f"{error.code}:{error.name}",
        "constructor_id": None,
        "path": error_paths[error],
        "selected_layer": selected_layer,
    }


def _result_family_relationship_node(family: str, *, result_family_paths: Mapping[str, str]) -> dict[str, object]:
    """Return one machine-readable raw result-family relationship endpoint.

    Args:
        family: Exact non-primitive TL family identity.
        result_family_paths: Generated result-family index paths keyed by raw family.

    Returns:
        Object naming the family and its page path when selected constructors provide one.
    """
    return {
        "kind": "result_family",
        "qualified_name": family,
        "constructor_id": None,
        "path": result_family_paths.get(family),
        "selected_layer": family in result_family_paths,
    }


def _relationship_sort_key(relationship: Mapping[str, object]) -> tuple[str, str, str, str, str]:
    """Build a total deterministic sort key for one relationship artifact record.

    Args:
        relationship: Relationship object produced by the static extractor.

    Returns:
        Relation/source/target identity tuple independent of incidental mapping order.
    """
    source = relationship["source"]
    target = relationship["target"]
    if not isinstance(source, Mapping) or not isinstance(target, Mapping):
        raise ValueError("invalid generated Telegram relationship endpoint")
    return (
        str(relationship["relation"]),
        str(source.get("kind")),
        str(source.get("qualified_name")),
        str(target.get("kind")),
        str(target.get("qualified_name")),
    )


def _schema_description(description: str | None) -> str:
    """Return available normalized schema prose or the required honest missing label.

    Args:
        description: Merged declaration or parameter prose from normalized schema JSON.

    Returns:
        Available prose, otherwise a stable non-fabricated missing-description label.
    """
    return description if description is not None else _MISSING_SCHEMA_DESCRIPTION


def _error_description(description: str | None) -> str:
    """Return available pinned error prose or the required honest missing label.

    Args:
        description: Pinned RPC error prose from the error database.

    Returns:
        Available prose, otherwise a stable non-fabricated missing-description label.
    """
    return description if description is not None else _MISSING_ERROR_DESCRIPTION


def _markdown_cell(value: str) -> str:
    """Escape text for one deterministic single-line Markdown table cell.

    Args:
        value: Arbitrary display text from static schema/error JSON.

    Returns:
        Table-safe text with pipes escaped and line breaks normalized to spaces.
    """
    return value.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _provenance_sections(
    metadata: Mapping[str, Any], *, canonical_source: str, structural_url: str | None, error_url: str | None
) -> tuple[str, ...]:
    """Render canonical structure/prose/error provenance and deterministic diff notes.

    Args:
        metadata: Parsed schema metadata object.
        canonical_source: Structure-authoritative source identifier.
        structural_url: Canonical schema URL for declaration pages, if applicable.
        error_url: Independent RPC-error source URL for error pages, if applicable.

    Returns:
        Markdown lines preserving available source-note, precedence and diff data.
    """
    precedence = _string_sequence(
        metadata.get("documentation_merge_precedence", ()), field="metadata.documentation_merge_precedence"
    )
    rendered_precedence = " → ".join(_source_label(item) for item in precedence)
    note = _optional_description(metadata.get("source_note"))
    lines = ["", "## Provenance", "", f"- structural source: `{canonical_source}`"]
    if structural_url is not None:
        lines.append(f"- canonical schema: {structural_url}")
    if error_url is not None:
        lines.append(f"- RPC error source: {error_url}")
    lines.append(f"- prose merge precedence: {rendered_precedence}")
    if note is not None:
        lines.append(f"- source note: {note}")
    lines.extend(_diff_note_lines(metadata.get("source_comparison_summary")))
    return tuple(lines)


def _source_label(source: str) -> str:
    """Render one normalized source identifier for human-facing provenance prose.

    Args:
        source: Metadata precedence identifier such as ``tdlib`` or ``core_json``.

    Returns:
        Display label preserving recognized source identities.
    """
    labels = {"tdlib": "TDLib", "tdesktop": "Telegram Desktop", "core_json": "Core JSON"}
    return labels.get(source, source)


def _diff_note_lines(value: object) -> tuple[str, ...]:
    """Render scalar source-comparison summary values without interpreting structure.

    Args:
        value: Metadata ``source_comparison_summary`` object, if present.

    Returns:
        Empty lines when no supported summary exists, otherwise sorted Markdown
        diff-note bullets preserving provided scalar/list values.
    """
    if not isinstance(value, Mapping):
        return ()
    lines = ["", "## Source-diff notes", ""]
    for comparison, details in sorted(value.items(), key=lambda item: str(item[0])):
        if not isinstance(details, Mapping):
            continue
        scalar_items = [
            f"{key}={_render_metadata_value(item)}"
            for key, item in sorted(details.items(), key=lambda item: str(item[0]))
            if isinstance(item, str | int | float | bool) or _string_list(item) is not None
        ]
        if scalar_items:
            lines.append(f"- {comparison}: {'; '.join(scalar_items)}")
    return tuple(lines) if len(lines) > 3 else ()


def _render_metadata_value(value: object) -> str:
    """Render a supported scalar/list metadata value deterministically.

    Args:
        value: Scalar or string-list metadata value accepted by diff-note output.

    Returns:
        Stable human-readable representation without JSON object formatting.
    """
    strings = _string_list(value)
    if strings is not None:
        return ", ".join(strings)
    return str(value).casefold() if isinstance(value, bool) else str(value)


def _string_list(value: object) -> tuple[str, ...] | None:
    """Return a tuple for a string list/tuple, otherwise signal unsupported metadata.

    Args:
        value: ``source_comparison_summary`` scalar detail accepted only when it
            is a list or tuple whose every member is a string.

    Returns:
        String tuple when the value is a list/tuple of strings; ``None`` for
        scalars, mappings, other sequences or non-string members.
    """
    if not isinstance(value, list | tuple):
        return None
    if not all(isinstance(item, str) for item in value):
        return None
    return tuple(value)


def _index_pages(
    *,
    declarations: Sequence[TelegramDeclaration],
    errors: Sequence[TelegramRPCError],
    declaration_paths: Mapping[TelegramDeclaration, str],
    error_paths: Mapping[TelegramRPCError, str],
    function_paths: Mapping[TelegramDeclaration, str],
    result_family_paths: Mapping[str, str],
    relationship_index: _TelegramRelationshipIndex,
    layer: int,
    canonical_source: str,
    structural_url: str,
    error_url: str,
    repository_base: str,
) -> tuple[ReferencePage, ...]:
    """Build deterministic global, namespace, result-family and error index pages.

    Args:
        declarations: Every normalized function and constructor from the selected
            canonical schema layer.
        errors: Every code/name mapping flattened from the checked-in RPC-error
            database.
        declaration_paths: Collision-checked detail routes keyed by selected
            schema declaration identity.
        error_paths: Collision-checked detail routes keyed by pinned error
            code/name identity.
        function_paths: Selected-layer function routes used to link mapped RPC
            error method names.
        result_family_paths: Collision-checked result-family index routes keyed
            by exact raw TL result family.
        relationship_index: Precomputed selected-layer/error database joins used
            by the method index without repeated full scans.
        layer: Validated selected Telegram schema layer rendered in each index.
        canonical_source: Metadata source identifier for selected-layer
            canonical structure.
        structural_url: Pinned canonical schema URL rendered by function/type
            category indexes.
        error_url: Pinned upstream RPC-error URL or checked-in repository fallback
            for error-index provenance.
        repository_base: Repository browser base used for checked-in JSON source
            frontmatter links and error-source fallback.

    Returns:
        Deterministically sorted index pages without duplicate routes.
    """
    functions = tuple(item for item in declarations if item.kind == "function")
    types = tuple(item for item in declarations if item.kind == "type")
    pages = [
        _index_page(
            path="telegram/index.md",
            title="Telegram raw API",
            qualified_name="telegram",
            description=(
                f"Layer {layer} Telegram raw API: {len(functions)} functions, {len(types)} type constructors, "
                f"and {len(errors)} pinned RPC errors from {canonical_source}."
            ),
            body=(
                f"## Layer {layer} selected surface\n\n"
                f"- [Functions](/reference/telegram/functions/): {len(functions)} canonical methods\n"
                f"- [Types](/reference/telegram/types/): {len(types)} canonical constructors\n"
                f"- [RPC errors](/reference/telegram/errors/): {len(errors)} pinned error records\n\n"
                f"Canonical structure source: `{canonical_source}`."
            ),
            namespace="telegram",
            layer=layer,
            canonical_source=canonical_source,
            source_path="tools/schema/schema.json",
            source_url=f"{repository_base}/blob/master/tools/schema/schema.json",
        ),
        _category_index_page(
            category="functions",
            title="Telegram functions",
            declarations=functions,
            paths=declaration_paths,
            layer=layer,
            canonical_source=canonical_source,
            source_url=structural_url,
            repository_base=repository_base,
        ),
        _category_index_page(
            category="types",
            title="Telegram types",
            declarations=types,
            paths=declaration_paths,
            layer=layer,
            canonical_source=canonical_source,
            source_url=structural_url,
            repository_base=repository_base,
        ),
        _error_index_page(
            errors=errors,
            paths=error_paths,
            relationship_index=relationship_index,
            function_paths=function_paths,
            layer=layer,
            canonical_source=canonical_source,
            source_url=error_url,
            repository_base=repository_base,
        ),
    ]
    pages.extend(
        _namespace_index_pages(
            declarations=functions,
            category="functions",
            paths=declaration_paths,
            layer=layer,
            canonical_source=canonical_source,
            repository_base=repository_base,
        )
    )
    pages.extend(
        _namespace_index_pages(
            declarations=types,
            category="types",
            paths=declaration_paths,
            layer=layer,
            canonical_source=canonical_source,
            repository_base=repository_base,
        )
    )
    pages.extend(
        _result_family_index_pages(
            declarations=types,
            paths=declaration_paths,
            result_family_paths=result_family_paths,
            layer=layer,
            canonical_source=canonical_source,
            repository_base=repository_base,
        )
    )
    pages.extend(
        _error_sort_index_pages(
            errors=errors,
            paths=error_paths,
            relationship_index=relationship_index,
            function_paths=function_paths,
            layer=layer,
            canonical_source=canonical_source,
            source_url=error_url,
            repository_base=repository_base,
        )
    )
    return tuple(sorted(pages, key=lambda page: page.path))


def _index_page(
    *,
    path: str,
    title: str,
    qualified_name: str,
    description: str,
    body: str,
    namespace: str,
    layer: int,
    canonical_source: str,
    source_path: str,
    source_url: str,
) -> ReferencePage:
    """Create one common frontmatter-valid Telegram index page.

    Args:
        path: Previously reserved relative Markdown route for this generated
            index, including any collision-safe suffix.
        title: Human-readable title derived from the selected category, namespace,
            or result family.
        qualified_name: Stable generated index identity separate from any TL
            declaration identity.
        description: Layer/count/kind summary derived from selected static inputs.
        body: Deterministic Markdown navigation content derived from selected
            declaration/error records.
        namespace: Telegram category or namespace attached to page frontmatter.
        layer: Validated selected Telegram schema layer for page frontmatter.
        canonical_source: Metadata source identifier for selected-layer canonical
            structure.
        source_path: Repository-relative checked-in JSON input from which this
            index is derived.
        source_url: Non-empty upstream or repository link to the pinned JSON source.

    Returns:
        Validated Telegram ``ReferencePage`` index instance.
    """
    return ReferencePage(
        path=path,
        title=title,
        description=description,
        language="telegram",
        kind="index",
        qualified_name=qualified_name,
        source_path=source_path,
        source_url=source_url,
        body=body,
        namespace=namespace,
        schema_source=canonical_source,
    )


def _category_index_page(
    *,
    category: str,
    title: str,
    declarations: Sequence[TelegramDeclaration],
    paths: Mapping[TelegramDeclaration, str],
    layer: int,
    canonical_source: str,
    source_url: str,
    repository_base: str,
) -> ReferencePage:
    """Create a global function/type category index with all split declaration links.

    Args:
        category: ``functions`` or ``types`` route category.
        title: Human-readable category title.
        declarations: Category declarations to list in deterministic order.
        paths: Precomputed declaration paths keyed by declaration.
        layer: Validated Telegram schema layer.
        canonical_source: Structure-authoritative source identifier.
        source_url: External canonical schema URL, mentioned in index content.
        repository_base: Repository browser base for pinned JSON frontmatter links.

    Returns:
        One global category index page.
    """
    links = _declaration_links(declarations, paths=paths)
    body = (
        f"## Layer {layer} {category}\n\n"
        f"Selected canonical {category}: {len(declarations)}.\n\n"
        f"## Canonical source\n\n{source_url}\n\n## Declarations\n\n" + "\n".join(links)
    )
    return _index_page(
        path=f"telegram/{category}/index.md",
        title=title,
        qualified_name=f"telegram.{category}",
        description=f"Layer {layer} index of {len(declarations)} canonical Telegram {category} from {canonical_source}.",
        body=body,
        namespace=category,
        layer=layer,
        canonical_source=canonical_source,
        source_path="tools/schema/schema.json",
        source_url=f"{repository_base}/blob/master/tools/schema/schema.json",
    )


def _namespace_index_pages(
    *,
    declarations: Sequence[TelegramDeclaration],
    category: str,
    paths: Mapping[TelegramDeclaration, str],
    layer: int,
    canonical_source: str,
    repository_base: str,
) -> tuple[ReferencePage, ...]:
    """Create one deterministic split-page index for every declaration namespace.

    Args:
        declarations: Function or type declarations to group by namespace.
        category: Route category matching the declarations.
        paths: Precomputed paths for linked declarations.
        layer: Validated Telegram schema layer.
        canonical_source: Structure-authoritative source identifier.
        repository_base: Repository browser base for pinned JSON provenance links.

    Returns:
        Namespace index pages sorted by their stable paths.
    """
    grouped: defaultdict[str, list[TelegramDeclaration]] = defaultdict(list)
    for declaration in declarations:
        grouped[_namespace(declaration.name)].append(declaration)
    pages = [
        _index_page(
            path=f"telegram/{category}/{namespace}/index.md",
            title=f"Telegram {category}: {namespace}",
            qualified_name=f"telegram.{category}.{namespace}",
            description=(
                f"Layer {layer} index of {len(items)} canonical Telegram {category} in the {namespace} namespace "
                f"from {canonical_source}."
            ),
            body=(
                f"## Layer {layer} {namespace} {category}\n\n"
                f"Selected canonical {category} in this namespace: {len(items)}.\n\n## Declarations\n\n"
                + "\n".join(_declaration_links(items, paths=paths))
            ),
            namespace=namespace,
            layer=layer,
            canonical_source=canonical_source,
            source_path="tools/schema/schema.json",
            source_url=f"{repository_base}/blob/master/tools/schema/schema.json",
        )
        for namespace, items in sorted(grouped.items())
    ]
    return tuple(sorted(pages, key=lambda page: page.path))


def _result_family_index_pages(
    *,
    declarations: Sequence[TelegramDeclaration],
    paths: Mapping[TelegramDeclaration, str],
    result_family_paths: Mapping[str, str],
    layer: int,
    canonical_source: str,
    repository_base: str,
) -> tuple[ReferencePage, ...]:
    """Create deterministic type-constructor indexes grouped by result family.

    Args:
        declarations: Type constructors to group by raw TL result family.
        paths: Precomputed constructor paths keyed by declaration.
        result_family_paths: Preallocated result-family index paths keyed by family.
        layer: Validated Telegram schema layer.
        canonical_source: Structure-authoritative source identifier.
        repository_base: Repository browser base for pinned JSON provenance links.

    Returns:
        Result-family index pages sorted by stable path.
    """
    grouped: defaultdict[str, list[TelegramDeclaration]] = defaultdict(list)
    for declaration in declarations:
        grouped[_result_family(declaration.result_type)].append(declaration)
    pages = [
        _index_page(
            path=result_family_paths[family],
            title=f"Telegram result family: {family}",
            qualified_name=f"telegram.types.result.{family}",
            description=(
                f"Layer {layer} result-family index for {len(items)} canonical constructors returning {family} "
                f"from {canonical_source}."
            ),
            body=(
                f"## Layer {layer} result family `{family}`\n\n"
                f"Selected canonical constructors in this family: {len(items)}.\n\n## Constructors\n\n"
                + "\n".join(_declaration_links(items, paths=paths))
            ),
            namespace="results",
            layer=layer,
            canonical_source=canonical_source,
            source_path="tools/schema/schema.json",
            source_url=f"{repository_base}/blob/master/tools/schema/schema.json",
        )
        for family, items in sorted(grouped.items())
    ]
    return tuple(sorted(pages, key=lambda page: page.path))


def _error_index_page(
    *,
    errors: Sequence[TelegramRPCError],
    paths: Mapping[TelegramRPCError, str],
    relationship_index: _TelegramRelationshipIndex,
    function_paths: Mapping[TelegramDeclaration, str],
    layer: int,
    canonical_source: str,
    source_url: str,
    repository_base: str,
) -> ReferencePage:
    """Create an RPC-error index sortable by code, name and mapped methods.

    Args:
        errors: Flattened pinned RPC errors to list.
        paths: Precomputed error paths keyed by code/name mapping.
        relationship_index: Precomputed selected-layer method lookup for links.
        function_paths: Generated function paths keyed by selected-layer declaration.
        layer: Validated Telegram schema layer.
        canonical_source: Structure-authoritative source identifier.
        source_url: Independent error-database URL rendered in the index body,
            or ``None`` when the metadata does not record an upstream URL.
        repository_base: Repository browser base for local error JSON frontmatter.

    Returns:
        Global error index with code/name/method relationship table.
    """
    lines = [
        "## Independent error source",
        "",
        source_url,
        "",
        "## Indexes",
        "",
        "- [By code](/reference/telegram/errors/by-code/)",
        "- [By name](/reference/telegram/errors/by-name/)",
        "- [By method](/reference/telegram/errors/by-method/)",
        "",
        "## Errors",
        "",
        "| Code | Error | Methods |",
        "| ---: | --- | --- |",
    ]
    for error in sorted(errors, key=lambda item: (item.code, item.name)):
        link = _page_link(error.name, paths[error])
        methods = _error_method_links(
            error.methods, relationship_index=relationship_index, function_paths=function_paths, layer=layer
        )
        lines.append(f"| {error.code} | {link} | {methods} |")
    return _index_page(
        path="telegram/errors/index.md",
        title="Telegram RPC errors",
        qualified_name="telegram.errors",
        description=(
            f"Layer {layer} index of {len(errors)} pinned Telegram RPC errors and their recorded method mappings."
        ),
        body="\n".join(lines),
        namespace="errors",
        layer=layer,
        canonical_source=canonical_source,
        source_path="tools/schema/rpc-errors.json",
        source_url=f"{repository_base}/blob/master/tools/schema/rpc-errors.json",
    )


def _error_sort_index_pages(
    *,
    errors: Sequence[TelegramRPCError],
    paths: Mapping[TelegramRPCError, str],
    relationship_index: _TelegramRelationshipIndex,
    function_paths: Mapping[TelegramDeclaration, str],
    layer: int,
    canonical_source: str,
    source_url: str,
    repository_base: str,
) -> tuple[ReferencePage, ...]:
    """Create separately navigable RPC-error indexes by code, name and method.

    Args:
        errors: Flattened pinned RPC error records to organize.
        paths: Generated detail-page paths keyed by error identity.
        relationship_index: Precomputed selected-layer function lookup for method links.
        function_paths: Generated selected-layer function paths keyed by declaration.
        layer: Validated selected Telegram schema layer.
        canonical_source: Structure-authoritative source identifier in page frontmatter.
        source_url: Pinned upstream RPC-error URL or checked-in repository fallback.
        repository_base: Repository browser base for pinned JSON provenance links.

    Returns:
        Code-, name- and method-sorted error index pages in stable path order.
    """
    common = {
        "layer": layer,
        "canonical_source": canonical_source,
        "source_path": "tools/schema/rpc-errors.json",
        "source_url": f"{repository_base}/blob/master/tools/schema/rpc-errors.json",
    }
    by_code = _error_list_index_page(
        path="telegram/errors/by-code/index.md",
        title="Telegram RPC errors by code",
        qualified_name="telegram.errors.by_code",
        description=f"Layer {layer} index of {len(errors)} pinned Telegram RPC errors sorted by numeric code.",
        heading="Errors by code",
        errors=tuple(sorted(errors, key=lambda item: (item.code, item.name))),
        paths=paths,
        **common,
    )
    by_name = _error_list_index_page(
        path="telegram/errors/by-name/index.md",
        title="Telegram RPC errors by name",
        qualified_name="telegram.errors.by_name",
        description=f"Layer {layer} index of {len(errors)} pinned Telegram RPC errors sorted by symbolic name.",
        heading="Errors by name",
        errors=tuple(sorted(errors, key=lambda item: (item.name, item.code))),
        paths=paths,
        **common,
    )
    by_method = _error_method_index_page(
        errors=errors,
        paths=paths,
        relationship_index=relationship_index,
        function_paths=function_paths,
        layer=layer,
        canonical_source=canonical_source,
        source_url=source_url,
        repository_base=repository_base,
    )
    return (by_code, by_method, by_name)


def _error_list_index_page(
    *,
    path: str,
    title: str,
    qualified_name: str,
    description: str,
    heading: str,
    errors: Sequence[TelegramRPCError],
    paths: Mapping[TelegramRPCError, str],
    layer: int,
    canonical_source: str,
    source_path: str,
    source_url: str,
) -> ReferencePage:
    """Render one simple ordered RPC-error list index.

    Args:
        path: Collision-reserved generated index path.
        title: Human-readable page title.
        qualified_name: Stable generated index identity.
        description: Search/index summary for the page frontmatter.
        heading: Visible ordering heading.
        errors: Errors already sorted according to the requested index ordering.
        paths: Generated error detail paths keyed by error identity.
        layer: Validated selected Telegram schema layer.
        canonical_source: Structure-authoritative source identifier in frontmatter.
        source_path: Repository-relative pinned error database path.
        source_url: Repository browser URL for the pinned error database.

    Returns:
        A deterministic error index with code/name rows.
    """
    lines = [f"## {heading}", "", "| Code | Error |", "| ---: | --- |"]
    lines.extend(f"| {error.code} | {_page_link(error.name, paths[error])} |" for error in errors)
    return _index_page(
        path=path,
        title=title,
        qualified_name=qualified_name,
        description=description,
        body="\n".join(lines),
        namespace="errors",
        layer=layer,
        canonical_source=canonical_source,
        source_path=source_path,
        source_url=source_url,
    )


def _error_method_index_page(
    *,
    errors: Sequence[TelegramRPCError],
    paths: Mapping[TelegramRPCError, str],
    relationship_index: _TelegramRelationshipIndex,
    function_paths: Mapping[TelegramDeclaration, str],
    layer: int,
    canonical_source: str,
    source_url: str,
    repository_base: str,
) -> ReferencePage:
    """Render a method-to-error index that labels mappings absent from the selected layer.

    Args:
        errors: Flattened pinned RPC error records to map by method.
        paths: Generated error detail paths keyed by error identity.
        relationship_index: Precomputed selected-layer function lookup for method links.
        function_paths: Generated selected-layer function paths keyed by declaration.
        layer: Validated selected Telegram schema layer.
        canonical_source: Structure-authoritative source identifier in frontmatter.
        source_url: Pinned upstream RPC-error URL or checked-in repository fallback.
        repository_base: Repository browser base for pinned JSON provenance links.

    Returns:
        A deterministic method/error table with explicit external mappings.
    """
    rows: list[tuple[str, TelegramRPCError]] = []
    for error in errors:
        rows.extend((method, error) for method in error.methods)
    lines = ["## Errors by method", "", source_url, "", "| Method | Code | Error |", "| --- | ---: | --- |"]
    for method, error in sorted(rows, key=lambda item: (item[0], item[1].code, item[1].name)):
        declaration = relationship_index.functions_by_name.get(method)
        rendered_method = (
            _declaration_link(declaration, declaration_paths=function_paths)
            if declaration is not None
            else f"`{method}` (not in selected Layer {layer} schema)"
        )
        lines.append(f"| {rendered_method} | {error.code} | {_page_link(error.name, paths[error])} |")
    if not rows:
        lines.append("| — | — | No method mappings are present in the pinned error database. |")
    return _index_page(
        path="telegram/errors/by-method/index.md",
        title="Telegram RPC errors by method",
        qualified_name="telegram.errors.by_method",
        description=f"Layer {layer} index of {len(errors)} pinned Telegram RPC errors grouped by recorded method names.",
        body="\n".join(lines),
        namespace="errors",
        layer=layer,
        canonical_source=canonical_source,
        source_path="tools/schema/rpc-errors.json",
        source_url=f"{repository_base}/blob/master/tools/schema/rpc-errors.json",
    )


def _declaration_links(
    declarations: Sequence[TelegramDeclaration], *, paths: Mapping[TelegramDeclaration, str]
) -> tuple[str, ...]:
    """Render sorted split-page links for a declaration collection.

    Args:
        declarations: Function/type declarations to list.
        paths: Stable page paths keyed by declaration.

    Returns:
        Markdown bullet links sorted by qualified name and constructor identifier.
    """
    return tuple(
        f"- {_page_link(declaration.name, paths[declaration])}: `{declaration.result_type}`"
        for declaration in sorted(declarations, key=lambda item: (item.name, item.constructor_id))
    )


def _page_link(title: str, path: str) -> str:
    """Render an absolute stable reference route link for one generated Markdown path.

    Args:
        title: Link text preserving the exact Telegram qualified identity.
        path: Relative generated Markdown path below the reference root.

    Returns:
        Markdown link targeting the corresponding Starlight reference route.
    """
    route_path = path.removesuffix("index.md").removesuffix(".md").rstrip("/")
    return f"[`{title}`](/reference/{route_path}/)"


__all__ = [
    "TelegramBindingManifest",
    "TelegramPythonBinding",
    "TelegramPythonErrorBinding",
    "TelegramReferenceSurface",
    "generate_telegram_pages",
    "generate_telegram_reference_surface",
    "load_telegram_binding_manifest",
]
