"""Audit maintained Python, CLI, and Rust sources for missing or structurally inconsistent documentation."""

from __future__ import annotations

import ast
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from griffe import Docstring, DocstringSectionAttributes, DocstringSectionParameters, Parser


@dataclass(frozen=True, slots=True)
class MissingDocumentation:
    """Describe one source item that lacks documentation.

    Attributes:
        path: Repository-relative source path containing the item.
        line: One-based declaration line.
        kind: Source-language declaration kind.
        qualified_name: Fully qualified declaration name.
    """

    path: str
    line: int
    kind: str
    qualified_name: str


@dataclass(frozen=True, slots=True)
class MissingParameterDocumentation:
    """Describe callable argument documentation that does not match its signature.

    Attributes:
        path: Repository-relative source path containing the callable.
        line: One-based declaration line.
        qualified_name: Fully qualified callable name.
        arguments: Explicit argument names without usable descriptions.
        unexpected_arguments: Documented argument names absent from the callable signature.
    """

    path: str
    line: int
    qualified_name: str
    arguments: tuple[str, ...]
    unexpected_arguments: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class MissingCLIHelp:
    """Describe a command-line option without meaningful ``--help`` prose.

    Attributes:
        path: Repository-relative source path containing the parser action.
        line: One-based ``add_argument`` call line.
        options: Literal option spellings declared by the action.
    """

    path: str
    line: int
    options: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RustDocumentationAudit:
    """Summarize whole-source Rust documentation coverage.

    Attributes:
        documentation_unit_count: Total maintained modules, declarations, tuple fields, and test functions audited.
        named_declaration_count: Source-authored named declarations other than modules and test functions.
        module_count: Maintained crate, file, and nested modules audited.
        test_function_count: Source-authored functions carrying ``#[test]``.
        tuple_field_count: Positional enum or struct fields audited through direct or container prose.
        function_count: Non-test source-authored functions whose parameters were audited.
        value_parameter_count: Named non-receiver value parameters audited.
        generic_parameter_count: Explicit type and const parameters audited; lifetimes are excluded.
        missing_docs: Maintained documentation units without meaningful prose.
        missing_parameter_docs: Maintained functions with undocumented explicit parameters.
    """

    documentation_unit_count: int
    named_declaration_count: int
    module_count: int
    test_function_count: int
    tuple_field_count: int
    function_count: int
    value_parameter_count: int
    generic_parameter_count: int
    missing_docs: tuple[MissingDocumentation, ...]
    missing_parameter_docs: tuple[MissingParameterDocumentation, ...]


class _PythonDocVisitor(ast.NodeVisitor):
    """Collect undocumented Python definitions while retaining lexical names."""

    def __init__(self, *, module: str, path: Path) -> None:
        """Initialize a visitor for one parsed Python module.

        Args:
            module: Import-style name used to qualify declarations.
            path: Source path attached to reported defects.
        """
        self._module = module
        self._path = path
        self._parents: list[str] = []
        self.missing: list[MissingDocumentation] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Record an undocumented class and visit definitions nested inside it.

        Args:
            node: Class definition being traversed.
        """
        self._visit_definition(node, kind="class")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Record an undocumented synchronous function or method.

        Args:
            node: Synchronous definition being traversed.
        """
        self._visit_definition(node, kind="function")

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Record an undocumented asynchronous function or method.

        Args:
            node: Asynchronous definition being traversed.
        """
        self._visit_definition(node, kind="function")

    def _visit_definition(self, node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef, *, kind: str) -> None:
        """Record one definition before recursively visiting its lexical children.

        Args:
            node: Definition to audit and traverse.
            kind: Stable declaration kind stored in a missing-doc record.
        """
        qualified_name = ".".join((self._module, *self._parents, node.name))
        if not _has_substantive_docstring(ast.get_docstring(node, clean=False)):
            self.missing.append(
                MissingDocumentation(
                    path=self._path.as_posix(), line=node.lineno, kind=kind, qualified_name=qualified_name
                )
            )
        self._parents.append(node.name)
        self.generic_visit(node)
        self._parents.pop()


class _PythonParameterVisitor(ast.NodeVisitor):
    """Match callable signatures to Griffe-parsed Google parameter sections."""

    def __init__(self, *, module: str, path: Path, dataclass_fields: Mapping[str, tuple[str, ...]]) -> None:
        """Initialize a parameter visitor for one parsed module.

        Args:
            module: Import-style name used to qualify reported definitions.
            path: Source path attached to reported defects.
            dataclass_fields: Constructor field names keyed by local dataclass name.
        """
        self._module = module
        self._path = path
        self._dataclass_fields = dataclass_fields
        self._parents: list[str] = []
        self.missing: list[MissingParameterDocumentation] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Audit a dataclass constructor and visit definitions nested inside it.

        Args:
            node: Class definition being traversed.
        """
        expected = self._dataclass_fields.get(node.name, ())
        if expected:
            documented = _documented_class_parameter_names(ast.get_docstring(node, clean=False) or "")
            missing = tuple(name for name in expected if name not in documented)
            if missing:
                qualified_name = ".".join((self._module, *self._parents, node.name))
                self.missing.append(
                    MissingParameterDocumentation(
                        path=self._path.as_posix(), line=node.lineno, qualified_name=qualified_name, arguments=missing
                    )
                )
        self._parents.append(node.name)
        self.generic_visit(node)
        self._parents.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Audit a synchronous callable and visit its nested definitions.

        Args:
            node: Synchronous definition being traversed.
        """
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Audit an asynchronous callable and visit its nested definitions.

        Args:
            node: Asynchronous definition being traversed.
        """
        self._visit_function(node)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Compare one callable's declared arguments with documented parameters.

        Args:
            node: Callable definition whose explicit parameters are audited.
        """
        qualified_name = ".".join((self._module, *self._parents, node.name))
        expected = _function_argument_names(node)
        if expected:
            documented = _documented_parameter_names(ast.get_docstring(node, clean=False) or "")
            normalized_expected = {name.lstrip("*") for name in expected}
            normalized_documented = {name.lstrip("*") for name in documented}
            missing = tuple(name for name in expected if name.lstrip("*") not in normalized_documented)
            unexpected = tuple(
                sorted(
                    name
                    for name in documented
                    if name.lstrip("*") not in normalized_expected and name.lstrip("*") not in {"self", "cls"}
                )
            )
            if missing or unexpected:
                self.missing.append(
                    MissingParameterDocumentation(
                        path=self._path.as_posix(),
                        line=node.lineno,
                        qualified_name=qualified_name,
                        arguments=missing,
                        unexpected_arguments=unexpected,
                    )
                )
        self._parents.append(node.name)
        self.generic_visit(node)
        self._parents.pop()


def find_missing_python_docs(
    roots: Iterable[Path], *, excluded_roots: Iterable[Path] = ()
) -> tuple[MissingDocumentation, ...]:
    """Return undocumented modules and definitions below the supplied source roots.

    Args:
        roots: Files or directories containing maintained Python source.
        excluded_roots: Generator-owned files or directories that must not be audited.

    Returns:
        Missing documentation records sorted by source path and line.

    Raises:
        SyntaxError: A selected Python source cannot be parsed.
    """
    excluded = tuple(path.resolve() for path in excluded_roots)
    missing: list[MissingDocumentation] = []
    for root in sorted((Path(path) for path in roots), key=lambda path: path.as_posix()):
        files = (root,) if root.is_file() else root.rglob("*.py")
        for path in sorted(files, key=lambda candidate: candidate.as_posix()):
            resolved = path.resolve()
            if any(resolved == excluded_path or resolved.is_relative_to(excluded_path) for excluded_path in excluded):
                continue
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            relative = path.relative_to(root) if root.is_dir() else Path(path.name)
            module_parts = list(relative.with_suffix("").parts)
            if module_parts[-1] == "__init__":
                module_parts.pop()
            module = ".".join(module_parts) or root.name
            if not _has_substantive_docstring(ast.get_docstring(tree, clean=False)):
                missing.append(MissingDocumentation(path=path.as_posix(), line=1, kind="module", qualified_name=module))
            visitor = _PythonDocVisitor(module=module, path=path)
            visitor.visit(tree)
            missing.extend(visitor.missing)
    return tuple(sorted(missing, key=lambda item: (item.path.casefold(), item.line, item.qualified_name)))


def find_missing_cli_help(roots: Iterable[Path], *, excluded_roots: Iterable[Path] = ()) -> tuple[MissingCLIHelp, ...]:
    """Return literal CLI options whose parser action lacks substantive help text.

    Args:
        roots: Files or directories containing maintained Python CLI definitions.
        excluded_roots: Files or directories omitted from the static scan.

    Returns:
        Deterministically ordered option records. Positional arguments and argparse's automatic help action are excluded.

    Raises:
        SyntaxError: A selected Python source cannot be parsed.
    """
    excluded = tuple(path.resolve() for path in excluded_roots)
    missing: list[MissingCLIHelp] = []
    for root in sorted((Path(path) for path in roots), key=lambda path: path.as_posix()):
        files = (root,) if root.is_file() else root.rglob("*.py")
        for path in sorted(files, key=lambda candidate: candidate.as_posix()):
            resolved = path.resolve()
            if any(resolved == excluded_path or resolved.is_relative_to(excluded_path) for excluded_path in excluded):
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if (
                    not isinstance(node, ast.Call)
                    or not isinstance(node.func, ast.Attribute)
                    or node.func.attr != "add_argument"
                ):
                    continue
                options = tuple(
                    argument.value
                    for argument in node.args
                    if isinstance(argument, ast.Constant)
                    and isinstance(argument.value, str)
                    and argument.value.startswith("-")
                )
                if not options or "--help" in options:
                    continue
                help_node = next((keyword.value for keyword in node.keywords if keyword.arg == "help"), None)
                if _static_help_text(help_node):
                    continue
                missing.append(MissingCLIHelp(path=path.as_posix(), line=node.lineno, options=options))
    return tuple(sorted(missing, key=lambda item: (item.path.casefold(), item.line, item.options)))


def _has_substantive_docstring(docstring: str | None) -> bool:
    """Return whether authored documentation contains more than an empty or known placeholder summary.

    Args:
        docstring: Raw AST documentation text, or ``None`` when absent.

    Returns:
        ``True`` for non-empty prose that is not one of the deliberately rejected generic placeholders.
    """
    if not docstring or not docstring.strip():
        return False
    summary = docstring.strip().splitlines()[0].strip().casefold()
    return summary not in {"value.", "candidate value.", "schema tooling.", "schema tooling for miniproto."}


def _static_help_text(node: ast.expr | None) -> str:
    """Return statically visible parser-help prose for a literal or formatted string.

    Args:
        node: AST expression supplied to an ``add_argument(help=...)`` keyword.

    Returns:
        Concatenated literal text, or an empty string for absent, dynamic, or placeholder help.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        value = node.value
    elif isinstance(node, ast.JoinedStr):
        value = "".join(
            part.value for part in node.values if isinstance(part, ast.Constant) and isinstance(part.value, str)
        )
    else:
        return ""
    normalized = value.strip().casefold()
    return "" if normalized in {"", "value", "value.", "candidate value", "candidate value."} else value


def find_missing_python_parameter_docs(
    roots: Iterable[Path], *, excluded_roots: Iterable[Path] = ()
) -> tuple[MissingParameterDocumentation, ...]:
    """Return callables whose declared arguments lack Griffe-parsed descriptions.

    Args:
        roots: Files or directories containing maintained Python source.
        excluded_roots: Generator-owned files or directories that must not be audited.

    Returns:
        Deterministically ordered parameter-documentation defects. Implicit ``self``
        and ``cls`` receivers are excluded; every other argument kind is required.
    """
    excluded = tuple(path.resolve() for path in excluded_roots)
    missing: list[MissingParameterDocumentation] = []
    for root in sorted((Path(path) for path in roots), key=lambda path: path.as_posix()):
        files = (root,) if root.is_file() else root.rglob("*.py")
        for path in sorted(files, key=lambda candidate: candidate.as_posix()):
            resolved = path.resolve()
            if any(resolved == excluded_path or resolved.is_relative_to(excluded_path) for excluded_path in excluded):
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            relative = path.relative_to(root) if root.is_dir() else Path(path.name)
            module_parts = list(relative.with_suffix("").parts)
            if module_parts[-1] == "__init__":
                module_parts.pop()
            module = ".".join(module_parts) or root.name
            visitor = _PythonParameterVisitor(
                module=module, path=path, dataclass_fields=_dataclass_constructor_fields(tree)
            )
            visitor.visit(tree)
            missing.extend(visitor.missing)
    return tuple(sorted(missing, key=lambda item: (item.path.casefold(), item.line, item.qualified_name)))


def _function_argument_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    """Return every explicit callable argument using Google-docstring spelling.

    Args:
        node: Function definition supplying the signature.

    Returns:
        Argument names in declaration order, excluding an implicit receiver.
    """
    positional = [argument.arg for argument in (*node.args.posonlyargs, *node.args.args)]
    if positional and positional[0] in {"self", "cls"}:
        positional.pop(0)
    names = [*positional]
    if node.args.vararg is not None:
        names.append(f"*{node.args.vararg.arg}")
    names.extend(argument.arg for argument in node.args.kwonlyargs)
    if node.args.kwarg is not None:
        names.append(f"**{node.args.kwarg.arg}")
    return tuple(names)


def _documented_parameter_names(docstring: str) -> set[str]:
    """Return parameter names with non-empty descriptions parsed by Griffe.

    Args:
        docstring: Google-style function documentation to parse statically.

    Returns:
        Parameter spellings associated with meaningful prose.
    """
    documented: set[str] = set()
    for section in Docstring(docstring, parser=Parser.google).parse(warnings=False):
        if not isinstance(section, DocstringSectionParameters):
            continue
        for parameter in section.value:
            if str(parameter.description or "").strip():
                documented.add(parameter.name)
    return documented


def _documented_class_parameter_names(docstring: str) -> set[str]:
    """Return described constructor fields from a dataclass docstring.

    Args:
        docstring: Google-style class documentation to parse statically.

    Returns:
        Field names described by either Args or Attributes sections.
    """
    documented = _documented_parameter_names(docstring)
    for section in Docstring(docstring, parser=Parser.google).parse(warnings=False):
        if not isinstance(section, DocstringSectionAttributes):
            continue
        for attribute in section.value:
            if str(attribute.description or "").strip():
                documented.add(attribute.name)
    return documented


def _dataclass_constructor_fields(tree: ast.Module) -> Mapping[str, tuple[str, ...]]:
    """Resolve local dataclass constructor fields, including inherited fields.

    Args:
        tree: Parsed Python module containing candidate dataclass definitions.

    Returns:
        Constructor field names keyed by local dataclass name.
    """
    candidates = {
        node.name: node for node in tree.body if isinstance(node, ast.ClassDef) and _dataclass_init_enabled(node)
    }
    resolved: dict[str, tuple[str, ...]] = {}

    def resolve(name: str, visiting: frozenset[str] = frozenset()) -> tuple[str, ...]:
        """Resolve one local dataclass without recursing through inheritance cycles.

        Args:
            name: Local dataclass name to resolve.
            visiting: Class names already visited on the active inheritance path.

        Returns:
            Inherited and locally declared constructor fields in declaration order.
        """
        if name in resolved:
            return resolved[name]
        if name in visiting:
            return ()
        node = candidates[name]
        fields: list[str] = []
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id in candidates:
                fields.extend(resolve(base.id, visiting | {name}))
        fields.extend(_own_dataclass_constructor_fields(node))
        resolved[name] = tuple(dict.fromkeys(fields))
        return resolved[name]

    for name in candidates:
        resolve(name)
    return resolved


def _dataclass_init_enabled(node: ast.ClassDef) -> bool:
    """Return whether a class uses a synthesized dataclass initializer.

    Args:
        node: Class definition whose decorators are inspected.

    Returns:
        ``True`` for ``@dataclass`` declarations unless ``init=False`` is explicit.
    """
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        name = target.id if isinstance(target, ast.Name) else target.attr if isinstance(target, ast.Attribute) else ""
        if name != "dataclass":
            continue
        if isinstance(decorator, ast.Call):
            for keyword in decorator.keywords:
                if keyword.arg == "init" and isinstance(keyword.value, ast.Constant) and keyword.value.value is False:
                    return False
        return True
    return False


def _own_dataclass_constructor_fields(node: ast.ClassDef) -> tuple[str, ...]:
    """Return initializer fields declared directly by one dataclass.

    Args:
        node: Dataclass definition whose annotated assignments are inspected.

    Returns:
        Direct constructor field names after ClassVar, KW_ONLY, and init-false filtering.
    """
    fields: list[str] = []
    for statement in node.body:
        if not isinstance(statement, ast.AnnAssign) or not isinstance(statement.target, ast.Name):
            continue
        name = statement.target.id
        annotation = ast.unparse(statement.annotation)
        if name == "_" or annotation.endswith("KW_ONLY") or "ClassVar" in annotation:
            continue
        if isinstance(statement.value, ast.Call):
            call_name = (
                statement.value.func.id
                if isinstance(statement.value.func, ast.Name)
                else statement.value.func.attr
                if isinstance(statement.value.func, ast.Attribute)
                else ""
            )
            if call_name == "field" and any(
                keyword.arg == "init" and isinstance(keyword.value, ast.Constant) and keyword.value.value is False
                for keyword in statement.value.keywords
            ):
                continue
        fields.append(name)
    return tuple(fields)


def audit_maintained_rust_docs(
    rustdoc_json: Path, *, source_root: Path, maintained_paths: Sequence[str], excluded_paths: Sequence[str] = ()
) -> RustDocumentationAudit:
    """Audit every source-authored documentation unit in maintained Rust files.

    Args:
        rustdoc_json: Format-versioned JSON emitted by the pinned nightly with private items enabled.
        source_root: Repository root used to resolve rustdoc source spans.
        maintained_paths: Repository-relative Rust files whose authored declarations are in scope.
        excluded_paths: Generator-owned Rust files that must remain outside coverage.

    Returns:
        Coverage counts and deterministic missing-documentation records, independently of reference-page selection.

    Raises:
        KeyError: The rustdoc artifact lacks its root or item index.
        OSError: A maintained source file cannot be read.
        ValueError: A maintained source path escapes ``source_root``.
    """
    payload = json.loads(rustdoc_json.read_text(encoding="utf-8"))
    index: Mapping[str, Mapping[str, Any]] = payload["index"]
    root_id = str(payload["root"])
    root_item = index[root_id]
    root_crate_id = root_item["crate_id"]
    paths: Mapping[str, Mapping[str, Any]] = payload.get("paths", {})
    resolved_root = source_root.resolve()
    maintained = {_validated_relative_rust_path(path) for path in maintained_paths}
    excluded = {_validated_relative_rust_path(path) for path in excluded_paths}
    maintained.difference_update(excluded)
    source_lines = {
        path: (resolved_root / Path(path)).read_text(encoding="utf-8").splitlines() for path in sorted(maintained)
    }

    parents = _rustdoc_parent_ids(index)
    module_ranges: list[tuple[str, int, int, tuple[str, ...]]] = []
    candidates: dict[tuple[str, int, int, str, str], tuple[str, Mapping[str, Any]]] = {}
    tuple_fields: list[tuple[str, Mapping[str, Any], str]] = []

    for item_id, item in index.items():
        if item.get("crate_id") != root_crate_id:
            continue
        span = item.get("span")
        if not isinstance(span, Mapping):
            continue
        source_path = _normalized_rustdoc_path(str(span.get("filename", "")), resolved_root)
        if source_path not in maintained:
            continue
        name = item.get("name")
        if name is None:
            continue
        inner = item.get("inner")
        if not isinstance(inner, Mapping) or not inner:
            continue
        kind = str(next(iter(inner)))
        begin = span.get("begin", (1, 0))
        end = span.get("end", begin)
        begin_line = int(begin[0])
        end_line = int(end[0])
        qualified_parts = _rustdoc_qualified_parts(item_id, index=index, paths=paths, parents=parents)

        if kind == "module":
            spans_file = begin_line <= 1 and end_line >= len(source_lines[source_path])
            if (
                item_id != root_id
                and not spans_file
                and not _span_contains_identifier(source_lines[source_path], begin_line, end_line, str(name))
            ):
                continue
            module_ranges.append((source_path, begin_line, end_line, qualified_parts))
            key = (source_path, begin_line, end_line, str(name), kind)
            candidates[key] = (item_id, item)
            continue

        parent_id = parents.get(item_id)
        parent_item = index.get(parent_id, {}) if parent_id is not None else {}
        parent_variant_kind = parent_item.get("inner", {}).get("variant", {}).get("kind", {})
        parent_struct_kind = parent_item.get("inner", {}).get("struct", {}).get("kind", {})
        is_tuple_field = kind == "struct_field" and (
            (isinstance(parent_variant_kind, Mapping) and "tuple" in parent_variant_kind)
            or (isinstance(parent_struct_kind, Mapping) and "tuple" in parent_struct_kind)
        )
        if is_tuple_field:
            parent_span = parent_item.get("span")
            parent_name = parent_item.get("name")
            if not isinstance(parent_span, Mapping) or parent_name is None:
                continue
            parent_path = _normalized_rustdoc_path(str(parent_span.get("filename", "")), resolved_root)
            parent_begin = parent_span.get("begin", (1, 0))
            parent_end = parent_span.get("end", parent_begin)
            if parent_path != source_path or not _span_contains_identifier(
                source_lines[source_path], int(parent_begin[0]), int(parent_end[0]), str(parent_name)
            ):
                continue
            tuple_fields.append((item_id, item, source_path))
            continue

        if not _span_contains_identifier(source_lines[source_path], begin_line, end_line, str(name)):
            continue
        key = (source_path, begin_line, end_line, str(name), kind)
        previous = candidates.get(key)
        if previous is None or _rustdoc_candidate_rank(item_id, item, paths) > _rustdoc_candidate_rank(
            previous[0], previous[1], paths
        ):
            candidates[key] = (item_id, item)

    tests = _source_test_functions(source_lines, module_ranges, str(root_item.get("name") or "crate"))
    test_locations = {(test.path, test.line, test.name) for test in tests}
    missing_docs: list[MissingDocumentation] = []
    missing_parameters: list[MissingParameterDocumentation] = []
    named_declaration_count = 0
    module_count = 0
    function_count = 0
    value_parameter_count = 0
    generic_parameter_count = 0

    for item_id, item in candidates.values():
        span = item["span"]
        source_path = _normalized_rustdoc_path(str(span["filename"]), resolved_root)
        line = int(span.get("begin", (1, 0))[0])
        name = str(item["name"])
        inner = item["inner"]
        kind = str(next(iter(inner)))
        qualified_name = "::".join(_rustdoc_qualified_parts(item_id, index=index, paths=paths, parents=parents))
        if kind == "module":
            module_count += 1
        elif (source_path, line, name) in test_locations:
            continue
        else:
            named_declaration_count += 1
        if not str(item.get("docs") or "").strip():
            missing_docs.append(
                MissingDocumentation(path=source_path, line=line, kind=kind, qualified_name=qualified_name)
            )

        function = inner.get("function")
        if not isinstance(function, Mapping) or (source_path, line, name) in test_locations:
            continue
        function_count += 1
        value_names = _rust_function_argument_names(function)
        generic_names = _explicit_rust_generic_parameter_names(
            function, source_lines[source_path], line, int(span.get("end", (line, 0))[0])
        )
        value_parameter_count += len(value_names)
        generic_parameter_count += len(generic_names)
        documented = _documented_rust_parameter_names(str(item.get("docs") or ""))
        undocumented = tuple(name for name in (*generic_names, *value_names) if name not in documented)
        if undocumented:
            missing_parameters.append(
                MissingParameterDocumentation(
                    path=source_path, line=line, qualified_name=qualified_name, arguments=undocumented
                )
            )

    for item_id, item, source_path in tuple_fields:
        parent_id = parents[item_id]
        parent_item = index[parent_id]
        qualified_name = "::".join(_rustdoc_qualified_parts(item_id, index=index, paths=paths, parents=parents))
        if not _tuple_field_is_documented(item, parent_item):
            line = int(item["span"].get("begin", (1, 0))[0])
            missing_docs.append(
                MissingDocumentation(path=source_path, line=line, kind="tuple_field", qualified_name=qualified_name)
            )

    for test in tests:
        if not test.documented:
            missing_docs.append(
                MissingDocumentation(
                    path=test.path, line=test.line, kind="test_function", qualified_name="::".join(test.qualified_parts)
                )
            )

    missing_docs.sort(key=lambda item: (item.path.casefold(), item.line, item.qualified_name))
    missing_parameters.sort(key=lambda item: (item.path.casefold(), item.line, item.qualified_name))
    test_function_count = len(tests)
    tuple_field_count = len(tuple_fields)
    return RustDocumentationAudit(
        documentation_unit_count=named_declaration_count + module_count + test_function_count + tuple_field_count,
        named_declaration_count=named_declaration_count,
        module_count=module_count,
        test_function_count=test_function_count,
        tuple_field_count=tuple_field_count,
        function_count=function_count,
        value_parameter_count=value_parameter_count,
        generic_parameter_count=generic_parameter_count,
        missing_docs=tuple(missing_docs),
        missing_parameter_docs=tuple(missing_parameters),
    )


@dataclass(frozen=True, slots=True)
class _RustTestFunction:
    """Retain one source-scanned Rust test function.

    Attributes:
        path: Repository-relative source path.
        line: One-based function declaration line.
        name: Source-level function name.
        qualified_parts: Crate and module path followed by the function name.
        documented: Whether adjacent rustdoc comments contain meaningful prose.
    """

    path: str
    line: int
    name: str
    qualified_parts: tuple[str, ...]
    documented: bool


def _validated_relative_rust_path(path: str) -> str:
    """Normalize one configured repository-relative Rust path.

    Args:
        path: Configured source path using either slash convention.

    Returns:
        Normalized POSIX-style relative path.

    Raises:
        ValueError: The path is absolute or traverses above the source root.
    """
    candidate = Path(path.replace("\\", "/"))
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"maintained Rust path must be repository-relative: {path}")
    return candidate.as_posix()


def _normalized_rustdoc_path(path: str, source_root: Path) -> str:
    """Normalize a rustdoc span filename against the repository root.

    Args:
        path: Filename stored in a rustdoc JSON span.
        source_root: Resolved repository root.

    Returns:
        POSIX-style repository-relative path when possible, otherwise the normalized filename.
    """
    candidate = Path(path)
    if candidate.is_absolute():
        try:
            return candidate.resolve().relative_to(source_root).as_posix()
        except ValueError:
            return candidate.as_posix()
    return Path(path.replace("\\", "/")).as_posix()


def _rustdoc_parent_ids(index: Mapping[str, Mapping[str, Any]]) -> dict[str, str]:
    """Build structural parents from format-61 rustdoc container records.

    Args:
        index: Complete rustdoc item index.

    Returns:
        Child item ids mapped to source-level parents, with inherent impl methods attached to their target type.
    """
    parents: dict[str, str] = {}
    impl_targets: dict[str, str] = {}
    impl_children: dict[str, tuple[str, ...]] = {}
    for item_id, item in index.items():
        inner = item.get("inner", {})
        if not isinstance(inner, Mapping):
            continue
        implementation = inner.get("impl")
        if isinstance(implementation, Mapping):
            target = implementation.get("for", {})
            target_id = target.get("resolved_path", {}).get("id") if isinstance(target, Mapping) else None
            if target_id is not None:
                impl_targets[item_id] = str(target_id)
            impl_children[item_id] = tuple(str(child) for child in implementation.get("items", ()))
            continue
        for child in _rustdoc_direct_children(inner):
            parents.setdefault(child, item_id)
    for impl_id, children in impl_children.items():
        target_id = impl_targets.get(impl_id)
        if target_id is None:
            continue
        for child in children:
            parents.setdefault(child, target_id)
    return parents


def _rustdoc_direct_children(inner: Mapping[str, Any]) -> tuple[str, ...]:
    """Return structurally nested item ids from one rustdoc ``inner`` mapping.

    Args:
        inner: One rustdoc item's tagged inner representation.

    Returns:
        Direct module, type, variant, field, or trait children.
    """
    children: list[str] = []
    module = inner.get("module")
    if isinstance(module, Mapping):
        children.extend(str(item) for item in module.get("items", ()))
    enumeration = inner.get("enum")
    if isinstance(enumeration, Mapping):
        children.extend(str(item) for item in enumeration.get("variants", ()))
    structure = inner.get("struct")
    if isinstance(structure, Mapping):
        children.extend(_rustdoc_kind_fields(structure.get("kind")))
    variant = inner.get("variant")
    if isinstance(variant, Mapping):
        children.extend(_rustdoc_kind_fields(variant.get("kind")))
    union = inner.get("union")
    if isinstance(union, Mapping):
        children.extend(str(item) for item in union.get("fields", ()))
    trait = inner.get("trait")
    if isinstance(trait, Mapping):
        children.extend(str(item) for item in trait.get("items", ()))
    return tuple(children)


def _rustdoc_kind_fields(kind: Any) -> tuple[str, ...]:
    """Extract positional or named field ids from a rustdoc struct-like kind.

    Args:
        kind: Tagged ``struct.kind`` or ``variant.kind`` value.

    Returns:
        Field item ids in declaration order.
    """
    if not isinstance(kind, Mapping):
        return ()
    for label in ("tuple", "plain", "struct"):
        value = kind.get(label)
        if isinstance(value, Mapping):
            value = value.get("fields", ())
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            return tuple(str(item) for item in value)
    return ()


def _rustdoc_qualified_parts(
    item_id: str,
    *,
    index: Mapping[str, Mapping[str, Any]],
    paths: Mapping[str, Mapping[str, Any]],
    parents: Mapping[str, str],
) -> tuple[str, ...]:
    """Resolve one item path using rustdoc paths and structural parents.

    Args:
        item_id: Rustdoc item id to qualify.
        index: Complete rustdoc item index.
        paths: Canonical rustdoc path table.
        parents: Structural parent ids derived from the index.

    Returns:
        Crate-qualified source-level path components.
    """
    path_entry = paths.get(item_id, {})
    canonical = path_entry.get("path") if isinstance(path_entry, Mapping) else None
    if isinstance(canonical, Sequence) and not isinstance(canonical, (str, bytes)) and canonical:
        return tuple(str(part) for part in canonical)
    name = index[item_id].get("name")
    parent_id = parents.get(item_id)
    if parent_id is None:
        return (str(name or item_id),)
    return (*_rustdoc_qualified_parts(parent_id, index=index, paths=paths, parents=parents), str(name or item_id))


def _span_contains_identifier(lines: Sequence[str], begin_line: int, end_line: int, name: str) -> bool:
    """Return whether an item span contains its declared source identifier.

    Args:
        lines: Source file split into physical lines.
        begin_line: One-based first span line.
        end_line: One-based final span line.
        name: Rustdoc item name whose source provenance is tested.

    Returns:
        ``True`` only when the exact identifier occurs inside the source span.
    """
    snippet = "\n".join(lines[max(begin_line - 1, 0) : min(end_line, len(lines))])
    source_name = name.removeprefix("r#")
    return re.search(rf"(?<![A-Za-z0-9_])(?:r#)?{re.escape(source_name)}(?![A-Za-z0-9_])", snippet) is not None


def _rustdoc_candidate_rank(
    item_id: str, item: Mapping[str, Any], paths: Mapping[str, Mapping[str, Any]]
) -> tuple[bool, bool]:
    """Rank duplicate rustdoc records in favor of canonical documented items.

    Args:
        item_id: Candidate rustdoc item id.
        item: Rustdoc record ranked by canonical-path membership and non-empty authored documentation.
        paths: Canonical rustdoc path table.

    Returns:
        Canonical-path and non-empty-doc flags used for deterministic duplicate selection.
    """
    return item_id in paths, bool(str(item.get("docs") or "").strip())


def _explicit_rust_generic_parameter_names(
    function: Mapping[str, Any], lines: Sequence[str], begin_line: int, end_line: int
) -> tuple[str, ...]:
    """Return explicit type and const generic names present in a source function span.

    Args:
        function: The ``inner.function`` mapping from rustdoc JSON.
        lines: Source file split into physical lines.
        begin_line: One-based first function span line.
        end_line: One-based final function span line.

    Returns:
        Declared type and const parameter names in rustdoc order, excluding lifetimes and synthetic ``impl Trait`` params.
    """
    generics = function.get("generics", {})
    params = generics.get("params", ()) if isinstance(generics, Mapping) else ()
    names: list[str] = []
    for param in params:
        if not isinstance(param, Mapping):
            continue
        name = str(param.get("name") or "").removeprefix("r#")
        kind = param.get("kind", {})
        if not name or not isinstance(kind, Mapping) or ("type" not in kind and "const" not in kind):
            continue
        type_kind = kind.get("type")
        if isinstance(type_kind, Mapping) and type_kind.get("is_synthetic") is True:
            continue
        if _span_contains_identifier(lines, begin_line, end_line, name):
            names.append(name)
    return tuple(names)


def _tuple_field_is_documented(field: Mapping[str, Any], parent_variant: Mapping[str, Any]) -> bool:
    """Return whether a positional field has direct or explicit container prose.

    Args:
        field: Positional ``struct_field`` rustdoc item.
        parent_variant: Variant containing the positional field.

    Returns:
        ``True`` when field docs are non-empty or the variant prose names the backticked field type and explains containment.
    """
    if str(field.get("docs") or "").strip():
        return True
    field_type = field.get("inner", {}).get("struct_field")
    type_name = _rust_type_name(field_type)
    docs = str(parent_variant.get("docs") or "")
    if not type_name or f"`{type_name}`" not in docs:
        return False
    return (
        re.search(
            r"\b(?:contain(?:s|ed|ing)?|carr(?:y|ies)|hold(?:s|ing)?|stor(?:e|es|ing)|wrap(?:s|ping)?|payload|field|value)\b",
            docs,
            re.IGNORECASE,
        )
        is not None
    )


def _rust_type_name(value: Any) -> str:
    """Render the stable name of a rustdoc type for tuple-field prose matching.

    Args:
        value: Tagged rustdoc type representation.

    Returns:
        Concise source-facing type name, or an empty string when unavailable.
    """
    if not isinstance(value, Mapping):
        return ""
    for key in ("primitive", "generic"):
        if key in value:
            return str(value[key])
    resolved = value.get("resolved_path")
    if isinstance(resolved, Mapping):
        return str(resolved.get("name") or "")
    borrowed = value.get("borrowed_ref")
    if isinstance(borrowed, Mapping):
        inner = _rust_type_name(borrowed.get("type"))
        return f"&{inner}" if inner else ""
    sequence = value.get("slice")
    if sequence is not None:
        inner = _rust_type_name(sequence)
        return f"[{inner}]" if inner else ""
    array = value.get("array")
    if isinstance(array, Mapping):
        inner = _rust_type_name(array.get("type"))
        length = array.get("len")
        return f"[{inner}; {length}]" if inner and length is not None else ""
    return ""


_RUST_TEST_ATTRIBUTE = re.compile(r"^\s*#\[test\]\s*$")
_RUST_FUNCTION_DECLARATION = re.compile(
    r"^\s*(?:(?:pub(?:\([^)]*\))?|const|async|unsafe|extern(?:\s+\"[^\"]+\")?)\s+)*fn\s+(?P<name>(?:r#)?[A-Za-z_][A-Za-z0-9_]*)\b"
)


def _source_test_functions(
    source_lines: Mapping[str, Sequence[str]],
    module_ranges: Sequence[tuple[str, int, int, tuple[str, ...]]],
    crate_name: str,
) -> tuple[_RustTestFunction, ...]:
    """Find ``#[test]`` functions omitted from rustdoc JSON.

    Args:
        source_lines: Maintained source files split into lines.
        module_ranges: Rustdoc module spans and qualified paths used for lexical qualification.
        crate_name: Root crate name used when no module range encloses a test.

    Returns:
        Source-authored tests in deterministic path and line order.
    """
    tests: list[_RustTestFunction] = []
    for path, lines in sorted(source_lines.items()):
        for attribute_index, line in enumerate(lines):
            if _RUST_TEST_ATTRIBUTE.match(line) is None:
                continue
            function_index = attribute_index + 1
            while function_index < len(lines) and (
                not lines[function_index].strip()
                or lines[function_index].lstrip().startswith("///")
                or lines[function_index].lstrip().startswith("#[")
            ):
                function_index += 1
            if function_index >= len(lines):
                continue
            declaration = _RUST_FUNCTION_DECLARATION.match(lines[function_index])
            if declaration is None:
                continue
            function_line = function_index + 1
            name = declaration.group("name").removeprefix("r#")
            doc_lines = _adjacent_test_doc_lines(lines, attribute_index, function_index)
            enclosing = [
                (end - begin, qualified)
                for module_path, begin, end, qualified in module_ranges
                if module_path == path and begin <= function_line <= end
            ]
            qualified_module = (
                min(enclosing, key=lambda entry: (entry[0], -len(entry[1])))[1] if enclosing else (crate_name,)
            )
            tests.append(
                _RustTestFunction(
                    path=path,
                    line=function_line,
                    name=name,
                    qualified_parts=(*qualified_module, name),
                    documented=any(text.strip() for text in doc_lines),
                )
            )
    return tuple(tests)


def _adjacent_test_doc_lines(lines: Sequence[str], attribute_index: int, function_index: int) -> tuple[str, ...]:
    """Collect rustdoc prose immediately surrounding a test attribute.

    Args:
        lines: Source file split into physical lines.
        attribute_index: Zero-based line carrying ``#[test]``.
        function_index: Zero-based function declaration line.

    Returns:
        Rustdoc comment bodies before the attribute or between it and the function.
    """
    docs = [line.split("///", 1)[1] for line in lines[attribute_index + 1 : function_index] if "///" in line]
    cursor = attribute_index - 1
    while cursor >= 0:
        stripped = lines[cursor].strip()
        if stripped.startswith("///"):
            docs.append(stripped.removeprefix("///"))
        elif not stripped or stripped.startswith("#["):
            pass
        else:
            break
        cursor -= 1
    return tuple(docs)


def find_missing_rustdoc_docs(
    rustdoc_json: Path, *, excluded_paths: Sequence[str] = ()
) -> tuple[MissingDocumentation, ...]:
    """Return undocumented local declarations from one rustdoc JSON artifact.

    Args:
        rustdoc_json: JSON emitted by the pinned nightly with private items enabled.
        excluded_paths: Generator-owned source paths to omit from coverage.

    Returns:
        Missing documentation records for items belonging to the root crate.
    """
    payload = json.loads(rustdoc_json.read_text(encoding="utf-8"))
    index: Mapping[str, Mapping[str, Any]] = payload["index"]
    root_item = index[str(payload["root"])]
    root_crate_id = root_item["crate_id"]
    paths: Mapping[str, Mapping[str, Any]] = payload.get("paths", {})
    excluded = {path.replace("\\", "/") for path in excluded_paths}
    missing: list[MissingDocumentation] = []
    for item_id, item in index.items():
        if item.get("crate_id") != root_crate_id or item.get("name") is None:
            continue
        span = item.get("span")
        if span is None:
            continue
        source_path = str(span["filename"]).replace("\\", "/")
        if source_path in excluded:
            continue
        if str(item.get("docs") or "").strip():
            continue
        inner = item.get("inner", {})
        kind = next(iter(inner), "item")
        path_entry = paths.get(item_id, {})
        qualified_parts = path_entry.get("path") or (item["name"],)
        begin = span.get("begin", (1, 0))
        missing.append(
            MissingDocumentation(
                path=source_path,
                line=int(begin[0]),
                kind=str(path_entry.get("kind") or kind),
                qualified_name="::".join(str(part) for part in qualified_parts),
            )
        )
    return tuple(sorted(missing, key=lambda item: (item.path.casefold(), item.line, item.qualified_name)))


def find_missing_rustdoc_parameter_docs(
    rustdoc_json: Path, *, excluded_paths: Sequence[str] = ()
) -> tuple[MissingParameterDocumentation, ...]:
    """Return Rust functions whose non-receiver arguments lack descriptions.

    Args:
        rustdoc_json: JSON emitted by the pinned nightly with private items enabled.
        excluded_paths: Generator-owned source paths to omit from coverage.

    Returns:
        Deterministically ordered argument-documentation defects for local functions.
    """
    payload = json.loads(rustdoc_json.read_text(encoding="utf-8"))
    index: Mapping[str, Mapping[str, Any]] = payload["index"]
    root_item = index[str(payload["root"])]
    root_crate_id = root_item["crate_id"]
    paths: Mapping[str, Mapping[str, Any]] = payload.get("paths", {})
    excluded = {path.replace("\\", "/") for path in excluded_paths}
    missing: list[MissingParameterDocumentation] = []
    for item_id, item in index.items():
        if item.get("crate_id") != root_crate_id or item.get("name") is None:
            continue
        span = item.get("span")
        if span is None:
            continue
        source_path = str(span["filename"]).replace("\\", "/")
        if source_path in excluded:
            continue
        function = item.get("inner", {}).get("function")
        if not isinstance(function, Mapping):
            continue
        expected = _rust_function_argument_names(function)
        if not expected:
            continue
        documented = _documented_rust_parameter_names(str(item.get("docs") or ""))
        undocumented = tuple(name for name in expected if name not in documented)
        if not undocumented:
            continue
        path_entry = paths.get(item_id, {})
        qualified_parts = path_entry.get("path") or (item["name"],)
        begin = span.get("begin", (1, 0))
        missing.append(
            MissingParameterDocumentation(
                path=source_path,
                line=int(begin[0]),
                qualified_name="::".join(str(part) for part in qualified_parts),
                arguments=undocumented,
            )
        )
    return tuple(sorted(missing, key=lambda item: (item.path.casefold(), item.line, item.qualified_name)))


def _rust_function_argument_names(function: Mapping[str, Any]) -> tuple[str, ...]:
    """Return named non-receiver arguments from a rustdoc function record.

    Args:
        function: The ``inner.function`` mapping from one rustdoc JSON item.

    Returns:
        Argument names in declaration order, excluding Rust receiver spellings.
    """
    signature = function.get("sig", {})
    inputs = signature.get("inputs", ()) if isinstance(signature, Mapping) else ()
    names: list[str] = []
    for item in inputs:
        if not isinstance(item, Sequence) or isinstance(item, (str, bytes)) or not item:
            continue
        name = str(item[0]).strip()
        if not name or name in {"self", "slf", "_"} or "self" in name.split():
            continue
        names.append(name.removeprefix("r#"))
    return tuple(names)


_RUSTDOC_SECTION = re.compile(r"^\s{0,3}#{1,6}\s+(?:arguments|parameters)\s*$", re.IGNORECASE)
_RUSTDOC_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+")
_RUSTDOC_PARAMETER = re.compile(
    r"^\s*[-*+]\s+(?:`(?P<code>[^`]+)`|\*\*(?P<bold>[^*]+)\*\*|(?P<plain>[A-Za-z_][A-Za-z0-9_]*))\s*(?::|-|–|—)\s*(?P<description>.*)$"  # noqa: RUF001 - intentionally accepts Markdown en/em dash separators.
)


def _documented_rust_parameter_names(documentation: str) -> set[str]:
    """Return Rust argument names backed by non-empty parameter prose.

    Args:
        documentation: Markdown documentation copied from one rustdoc JSON item.

    Returns:
        Parameter names documented below an Arguments or Parameters heading.
    """
    documented: set[str] = set()
    in_parameters = False
    current_name: str | None = None
    current_description: list[str] = []

    def flush() -> None:
        """Record the current parameter when its accumulated prose is meaningful."""
        nonlocal current_name, current_description
        if current_name is not None and any(part.strip() for part in current_description):
            documented.add(current_name.removeprefix("r#"))
        current_name = None
        current_description = []

    for line in documentation.splitlines():
        if _RUSTDOC_SECTION.match(line):
            flush()
            in_parameters = True
            continue
        if _RUSTDOC_HEADING.match(line):
            flush()
            in_parameters = False
            continue
        if not in_parameters:
            continue
        parameter = _RUSTDOC_PARAMETER.match(line)
        if parameter is not None:
            flush()
            current_name = next(value for value in parameter.group("code", "bold", "plain") if value is not None)
            current_description.append(parameter.group("description"))
        elif current_name is not None:
            current_description.append(line)
    flush()
    return documented


__all__ = [
    "MissingCLIHelp",
    "MissingDocumentation",
    "MissingParameterDocumentation",
    "RustDocumentationAudit",
    "audit_maintained_rust_docs",
    "find_missing_cli_help",
    "find_missing_python_docs",
    "find_missing_python_parameter_docs",
    "find_missing_rustdoc_docs",
    "find_missing_rustdoc_parameter_docs",
]
