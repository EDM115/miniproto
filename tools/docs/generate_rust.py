"""Normalize pinned rustdoc JSON and cargo-docs-md output into Rust reference pages.

The module only reads JSON, rendered Markdown, and Rust source files.  It never imports
``miniproto`` or loads the native extension, so reference generation cannot run package code.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tomllib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.docs.manifest import write_reference_tree
from tools.docs.model import ReferencePage, normalize_generated_markdown_paths

DEFAULT_EXCLUDED_SOURCE_PATHS = ("rust/miniproto/src/generated_tl.rs",)
"""Generator-owned Rust files deliberately excluded from committed reference pages."""

DEFAULT_TOOLCHAIN_FILE = Path(__file__).resolve().parents[2] / "rust/miniproto/rust-toolchain-docs.toml"
"""Repository-local exact nightly and cargo-docs-md pin for Rust documentation only."""

_DOCUMENTABLE_KINDS = frozenset({"struct", "enum", "trait", "function", "constant", "type_alias", "macro"})
_PYFUNCTION_ATTRIBUTE = re.compile(r"#\[pyfunction(?:\((?P<options>.*?)\))?\]", re.DOTALL)
_PYCLASS_ATTRIBUTE = re.compile(r"#\[pyclass(?:\((?P<options>.*?)\))?\]", re.DOTALL)
_PYMETHOD_ATTRIBUTE = re.compile(r"#\[pyo3\((?P<options>.*?)\)\]", re.DOTALL)
_PYMETHOD_NEW_ATTRIBUTE = re.compile(r"#\[new\]")
_PYTHON_NAME_OPTION = re.compile(r'\bname\s*=\s*"(?P<name>[^"]+)"')
_PYTHON_MODULE_OPTION = re.compile(r'\bmodule\s*=\s*"(?P<module>[^"]+)"')
_ARGUMENTS_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(?:arguments|parameters)\s*$", re.IGNORECASE)
_CARGO_DOCS_MODULE_LINK = re.compile(r"\[(?P<label>[^\]\n]+)\]\((?P<slug>[A-Za-z0-9_.-]+)/index\.md\)")
_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+")
_ARGUMENT = re.compile(
    r"^\s*[-*+]\s+(?:`(?P<code>[^`]+)`|\*\*(?P<bold>[^*]+)\*\*|(?P<plain>[A-Za-z_][A-Za-z0-9_]*))\s*(?::|-|–|—)\s*(?P<description>.*)$"  # noqa: RUF001 - accepts Rustdoc's ordinary dash separators.
)


class RustDocumentationError(ValueError):
    """Report an incomplete, incompatible, or non-deterministic Rust documentation input."""


class RustDocumentationPending(RuntimeError):
    """Report that an exact live Rust documentation prerequisite is not installed."""


@dataclass(frozen=True, slots=True)
class RustDocumentationToolchain:
    """Describe the exact tool versions accepted for documentation generation.

    Attributes:
        nightly: Exact Rust nightly used to emit the rustdoc JSON artifact.
        cargo_docs_md: Exact cargo-docs-md renderer version accepted by the normalizer.
    """

    nightly: str
    cargo_docs_md: str


def load_documentation_toolchain(path: Path = DEFAULT_TOOLCHAIN_FILE) -> RustDocumentationToolchain:
    """Load and validate the repository's documentation-only Rust toolchain pin.

    Args:
        path: TOML file that records the nightly date and cargo-docs-md version.

    Returns:
        Validated immutable exact-version toolchain description.

    Raises:
        RustDocumentationError: The pin is missing either required exact version or is malformed.
    """
    with path.open("rb") as stream:
        payload = tomllib.load(stream)
    documentation = payload.get("documentation")
    if not isinstance(documentation, Mapping):
        raise RustDocumentationError(f"Rust documentation toolchain lacks [documentation]: {path}")
    nightly = str(documentation.get("nightly") or "")
    cargo_docs_md = str(documentation.get("cargo-docs-md") or "")
    if re.fullmatch(r"nightly-\d{4}-\d{2}-\d{2}", nightly) is None:
        raise RustDocumentationError(f"Rust documentation nightly must be date-pinned: {nightly!r}")
    if cargo_docs_md != "0.2.4":
        raise RustDocumentationError(f"cargo-docs-md must be pinned to 0.2.4, not {cargo_docs_md!r}")
    return RustDocumentationToolchain(nightly=nightly, cargo_docs_md=cargo_docs_md)


def pinned_rustdoc_command(
    *, toolchain: RustDocumentationToolchain, manifest_path: Path, target_dir: Path
) -> tuple[str, ...]:
    """Build the exact nightly command that emits private-item rustdoc JSON.

    Args:
        toolchain: Validated documentation-only nightly/version pin.
        manifest_path: Cargo manifest for the native miniproto crate.
        target_dir: Isolated artifact directory for transient rustdoc JSON output.

    Returns:
        Command argv for Cargo's nightly-only JSON documentation mode.

    Notes:
        The command deliberately uses Cargo's supported unstable flag and never sets
        ``RUSTC_BOOTSTRAP``.  Stable Rust remains responsible for builds and tests.
    """
    return (
        "cargo",
        f"+{toolchain.nightly}",
        "rustdoc",
        "--manifest-path",
        str(manifest_path),
        "--lib",
        "--target-dir",
        str(target_dir),
        "--",
        "-Z",
        "unstable-options",
        "--output-format",
        "json",
        "--document-private-items",
    )


def cargo_docs_md_install_command(toolchain: RustDocumentationToolchain) -> tuple[str, ...]:
    """Build the non-executing installation command for the selected Markdown renderer.

    Args:
        toolchain: Validated documentation-only renderer-version pin.

    Returns:
        Cargo argv that installs exactly the declared cargo-docs-md version.
    """
    return ("cargo", "install", "--locked", "cargo-docs-md", "--version", toolchain.cargo_docs_md)


def cargo_docs_md_command(*, json_directory: Path, output_directory: Path, crate: str) -> tuple[str, ...]:
    """Build the renderer command with full detail but no converter-owned site artifacts.

    Args:
        json_directory: Directory containing JSON files emitted by the pinned rustdoc command.
        output_directory: Isolated staging tree for cargo-docs-md Markdown files.
        crate: Primary crate name used to resolve otherwise ambiguous links.

    Returns:
        Cargo-subcommand argv retaining source locations and complete method documentation.
    """
    return (
        "cargo",
        "docs-md",
        "--dir",
        str(json_directory),
        "-o",
        str(output_directory),
        "--primary-crate",
        crate,
        "--source-locations",
        "--full-method-docs",
        "--no-mdbook",
        "--no-search-index",
    )


def ensure_pinned_nightly_available(
    toolchain: RustDocumentationToolchain, *, runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run
) -> None:
    """Require the exact nightly before any live rustdoc generation is attempted.

    Args:
        toolchain: Validated documentation-only nightly/version pin.
        runner: Process runner injected by tests or callers that control subprocess execution.

    Raises:
        RustDocumentationPending: The exact dated nightly is absent from rustup.
        RustDocumentationError: Rustup could not report the installed toolchains.
    """
    result = runner(("rustup", "toolchain", "list"), capture_output=True, check=False, text=True)
    if result.returncode:
        raise RustDocumentationError("could not enumerate installed Rust toolchains")
    installed = {line.partition(" ")[0].strip() for line in result.stdout.splitlines() if line.strip()}
    if not any(
        candidate == toolchain.nightly or candidate.startswith(f"{toolchain.nightly}-") for candidate in installed
    ):
        raise RustDocumentationPending(
            f"live Rust reference generation is pending: install exact {toolchain.nightly}; do not substitute stable Rust"
        )


def verify_cargo_docs_md_version(
    toolchain: RustDocumentationToolchain, *, runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run
) -> None:
    """Require cargo-docs-md to report the exact renderer version before conversion.

    Args:
        toolchain: Validated documentation-only renderer-version pin.
        runner: Process runner injected by tests or callers that control subprocess execution.

    Raises:
        RustDocumentationPending: The converter is missing or reports an unpinned version.
    """
    result = runner(("cargo", "docs-md", "--version"), capture_output=True, check=False, text=True)
    version_output = f"{result.stdout}\n{result.stderr}"
    if result.returncode or toolchain.cargo_docs_md not in version_output:
        raise RustDocumentationPending(
            f"live Rust reference generation is pending: install cargo-docs-md {toolchain.cargo_docs_md} exactly"
        )


def generate_pinned_rustdoc_json(
    *,
    toolchain: RustDocumentationToolchain,
    manifest_path: Path,
    target_dir: Path,
    artifact_stem: str,
    runner: Callable[..., subprocess.CompletedProcess[Any]] = subprocess.run,
) -> Path:
    """Emit one rustdoc JSON artifact with the exact nightly and private-item visibility.

    Args:
        toolchain: Validated documentation-only nightly/version pin.
        manifest_path: Cargo manifest for the native miniproto crate.
        target_dir: Isolated Cargo target directory for transient documentation artifacts.
        artifact_stem: Rustdoc JSON file stem, normally the Rust crate name with underscores.
        runner: Process runner injected by tests or callers that control subprocess execution.

    Returns:
        Existing path to the exact-nightly rustdoc JSON artifact.

    Raises:
        RustDocumentationPending: The exact nightly is absent and stable substitution is forbidden.
        RustDocumentationError: Cargo fails or does not emit the expected JSON artifact.
    """
    manifest_path = manifest_path.resolve()
    target_dir = target_dir.resolve()
    ensure_pinned_nightly_available(toolchain, runner=runner)
    result = runner(
        pinned_rustdoc_command(toolchain=toolchain, manifest_path=manifest_path, target_dir=target_dir),
        check=False,
        cwd=manifest_path.parent,
    )
    if result.returncode:
        raise RustDocumentationError(f"pinned rustdoc JSON generation failed for {manifest_path}")
    artifact = target_dir / "doc" / f"{artifact_stem}.json"
    if not artifact.is_file():
        raise RustDocumentationError(f"pinned rustdoc did not emit expected JSON artifact: {artifact}")
    return artifact


def render_rustdoc_with_cargo_docs_md(
    *,
    toolchain: RustDocumentationToolchain,
    json_directory: Path,
    output_directory: Path,
    crate: str,
    runner: Callable[..., subprocess.CompletedProcess[Any]] = subprocess.run,
) -> Path:
    """Render pinned rustdoc JSON through the exact converter without converter-owned site assets.

    Args:
        toolchain: Validated documentation-only renderer-version pin.
        json_directory: Directory containing the exact rustdoc JSON artifact.
        output_directory: Isolated cargo-docs-md staging tree for Markdown files.
        crate: Primary Rust crate used by the converter's cross-reference resolver.
        runner: Process runner injected by tests or callers that control subprocess execution.

    Returns:
        The converter staging directory after successful full-method/source-location rendering.

    Raises:
        RustDocumentationPending: The converter is absent or no longer exactly pinned.
        RustDocumentationError: cargo-docs-md fails to render the supplied JSON directory.
    """
    verify_cargo_docs_md_version(toolchain, runner=runner)
    result = runner(
        cargo_docs_md_command(json_directory=json_directory, output_directory=output_directory, crate=crate),
        check=False,
    )
    if result.returncode:
        raise RustDocumentationError(f"cargo-docs-md failed for rustdoc JSON directory: {json_directory}")
    if not output_directory.is_dir():
        raise RustDocumentationError(f"cargo-docs-md did not create its staging directory: {output_directory}")
    return output_directory


def load_cargo_docs_md_fragments(*, rustdoc_json: Path, output_directory: Path, crate: str) -> dict[str, str]:
    """Index canonical item fragments from cargo-docs-md's per-module Markdown.

    Args:
        rustdoc_json: Exact-nightly rustdoc JSON consumed by cargo-docs-md.
        output_directory: Converter staging root containing the crate/module indexes.
        crate: Rust crate directory name emitted by cargo-docs-md.

    Returns:
        Rustdoc identifier to converter-owned Markdown fragment mapping. Module identifiers retain their complete converter files; top-level items and associated methods retain their exact sections from those files. Renderer-owned source paths use POSIX separators on every host.

    Raises:
        RustDocumentationError: Rustdoc structure or a required module Markdown
        file is absent. Individual item fragments may remain absent so the
        normalizer can report their qualified names through its ordinary gate.
    """
    payload = json.loads(rustdoc_json.read_text(encoding="utf-8"))
    index = _index(payload)
    paths = _paths(payload)
    root_id = str(payload.get("root"))
    if root_id not in index:
        raise RustDocumentationError("rustdoc JSON root does not resolve to an index item")
    root_crate_id = index[root_id].get("crate_id")
    parent_ids = _parent_ids(index)
    qualified_names = {
        item_id: _qualified_name(item_id, index, paths, parent_ids)
        for item_id, item in index.items()
        if item.get("crate_id") == root_crate_id
    }
    module_markdown: dict[str, str] = {}
    fragments: dict[str, str] = {}
    for item_id, _unused_qualified_name in sorted(qualified_names.items(), key=lambda item: (item[1], item[0])):
        module_id = _owning_module_id(item_id, index=index, parent_ids=parent_ids)
        if module_id is None:
            continue
        if module_id not in module_markdown:
            module_name = qualified_names.get(module_id)
            if module_name is None:
                raise RustDocumentationError(f"cargo-docs-md module identity is missing for rustdoc item {module_id}")
            relative_parts = module_name.split("::")[1:]
            markdown_path = output_directory / crate / Path(*relative_parts) / "index.md"
            if not markdown_path.is_file():
                raise RustDocumentationError(f"cargo-docs-md module output is missing: {markdown_path}")
            module_markdown[module_id] = normalize_generated_markdown_paths(markdown_path.read_text(encoding="utf-8"))
        markdown = module_markdown[module_id]
        if item_id == module_id:
            fragments[item_id] = markdown.strip()
            continue
        name = str(index[item_id].get("name") or "").strip()
        if not name:
            continue
        parent_id = parent_ids.get(item_id)
        if parent_id is not None and parent_id != module_id and _item_kind(index[item_id]) == "function":
            parent_name = str(index[parent_id].get("name") or "").strip()
            fragment = _cargo_docs_md_method_fragment(markdown, parent_name=parent_name, method_name=name)
        else:
            fragment = _cargo_docs_md_item_fragment(markdown, name=name)
        if fragment:
            fragments[item_id] = fragment
    return fragments


def _owning_module_id(
    item_id: str, *, index: Mapping[str, Mapping[str, Any]], parent_ids: Mapping[str, str]
) -> str | None:
    """Return the nearest module containing one rustdoc item.

    Args:
        item_id: Rustdoc item whose cargo-docs-md file is required.
        index: Rustdoc item records keyed by identifier.
        parent_ids: Structural child-to-parent links, including inherent impl items.

    Returns:
        Nearest containing module identifier, or ``None`` for detached items.
    """
    current: str | None = item_id
    visited: set[str] = set()
    while current is not None and current in index and current not in visited:
        visited.add(current)
        if _item_kind(index[current]) == "module":
            return current
        current = parent_ids.get(current)
    return None


def _cargo_docs_md_item_fragment(markdown: str, *, name: str) -> str:
    """Return one unchanged top-level item section from a module document.

    Args:
        markdown: Complete cargo-docs-md module Markdown.
        name: Exact Rust declaration name used in the level-three heading.

    Returns:
        Converter-owned section, or an empty string when it is absent.
    """
    lines = markdown.splitlines()
    target = f"### `{name}`"
    start = next((index for index, line in enumerate(lines) if line.strip() == target), None)
    if start is None:
        return ""
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## ") or lines[index].startswith("### "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def _cargo_docs_md_method_fragment(markdown: str, *, parent_name: str, method_name: str) -> str:
    """Return one unchanged associated-method entry from a module document.

    Args:
        markdown: Complete cargo-docs-md module Markdown.
        parent_name: Rust type that owns the inherent method.
        method_name: Exact associated method name.

    Returns:
        Converter-owned method entry, or an empty string when it is absent.
    """
    lines = markdown.splitlines()
    anchor = f'<span id="{_slug(parent_name)}-{_slug(method_name)}"></span>'
    start = next((index for index, line in enumerate(lines) if anchor in line), None)
    if start is None:
        return ""
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("- <span id=") or re.match(r"^#{2,6}\s", line):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def generate_rust_pages(
    *,
    rustdoc_json: Path,
    source_root: Path,
    rendered_markdown: Mapping[str, str],
    repository_url: str,
    crate: str,
    reviewed_modules: Sequence[str],
    excluded_paths: Sequence[str] = DEFAULT_EXCLUDED_SOURCE_PATHS,
) -> tuple[ReferencePage, ...]:
    """Generate deterministic crate, module, file, and selected-item Rust reference pages.

    Args:
        rustdoc_json: Rustdoc JSON emitted by the exact nightly with private items included.
        source_root: Repository root used only for source-location and PyO3-attribute inspection.
        rendered_markdown: Complete cargo-docs-md Markdown keyed by rustdoc item identifier.
        repository_url: Repository browser base URL for line-anchored source links.
        crate: Cargo crate provenance recorded in generated frontmatter.
        reviewed_modules: Maintained module names whose public declarations are in scope.
        excluded_paths: Generator-owned source paths that must never become reference pages.

    Returns:
        Deterministically path-sorted generated pages using the converter's Markdown unchanged.

    Raises:
        RustDocumentationError: Selected data has missing docs, arguments, renderer bodies, or provenance.

    Notes:
        This function statically reads Rust source to identify PyO3 attributes.  It does not import
        the Python package or initialize the native extension.
    """
    payload = json.loads(rustdoc_json.read_text(encoding="utf-8"))
    index = _index(payload)
    paths = _paths(payload)
    root_id = str(payload.get("root"))
    if root_id not in index:
        raise RustDocumentationError("rustdoc JSON root does not resolve to an index item")
    root_item = index[root_id]
    root_crate_id = root_item.get("crate_id")
    excluded = {_normalize_path(path) for path in excluded_paths}
    local_ids = tuple(
        item_id
        for item_id, item in index.items()
        if item.get("crate_id") == root_crate_id and _source_path(item) not in excluded
    )
    parent_ids = _parent_ids(index)
    qualified_names = {item_id: _qualified_name(item_id, index, paths, parent_ids) for item_id in local_ids}
    bindings = _python_bindings(index, local_ids, parent_ids, qualified_names, source_root)
    reviewed = {name for name in reviewed_modules if name}
    selected_ids = tuple(
        sorted(
            _selected_item_ids(
                index=index,
                local_ids=local_ids,
                root_id=root_id,
                parent_ids=parent_ids,
                qualified_names=qualified_names,
                bindings=bindings,
                reviewed_modules=reviewed,
            )
        )
    )
    _validate_selected_documentation(index, selected_ids, qualified_names)
    _validate_rendered_markdown(selected_ids, rendered_markdown, qualified_names)

    pages: list[ReferencePage] = []
    source_details = {
        item_id: _source_provenance(index[item_id], source_root=source_root, repository_url=repository_url)
        for item_id in selected_ids
    }
    children = _selected_children(selected_ids, parent_ids)
    for item_id in sorted(selected_ids, key=lambda value: (qualified_names[value], value)):
        item = index[item_id]
        kind = _item_kind(item)
        source_path, source_url, line = source_details[item_id]
        title = qualified_names[item_id]
        summary = _summary(item, title)
        binding = bindings.get(item_id)
        if kind == "module":
            body = _module_body(
                item_id=item_id,
                qualified_name=title,
                item=item,
                children=children.get(item_id, ()),
                qualified_names=qualified_names,
                rendered_markdown=rendered_markdown[item_id],
                crate=crate,
                source_path=source_path,
                source_url=source_url,
            )
            path = _module_page_path(title, crate)
            page_kind = "crate" if item_id == root_id else "module"
        else:
            body = _item_body(
                item=item,
                qualified_name=title,
                rendered_markdown=rendered_markdown[item_id],
                crate=crate,
                source_path=source_path,
                source_url=source_url,
                line=line,
                python_binding=binding,
            )
            path = _item_page_path(title, crate)
            page_kind = _page_kind(item, parent_ids, index)
        pages.append(
            ReferencePage(
                path=path,
                title=title,
                description=summary,
                language="rust",
                kind=page_kind,
                qualified_name=title,
                source_path=source_path,
                source_url=source_url,
                body=body,
                crate=crate,
                python_visible=binding is not None,
                aliases=(binding,) if binding is not None else (),
            )
        )
    pages.extend(
        _file_index_pages(
            selected_ids=selected_ids,
            index=index,
            qualified_names=qualified_names,
            source_details=source_details,
            crate=crate,
        )
    )
    return tuple(sorted(pages, key=lambda page: page.path))


def write_rust_reference_tree(
    *,
    output_root: Path,
    pages: Sequence[ReferencePage],
    toolchain: RustDocumentationToolchain,
    source_hashes: Mapping[str, str],
) -> None:
    """Write validated normalized pages and a deterministic reference manifest.

    Args:
        output_root: Destination root containing only the generated Rust reference tree.
        pages: Already normalized crate, module, file, and item pages.
        toolchain: Exact nightly and cargo-docs-md provenance for the manifest.
        source_hashes: Deterministic source-file hashes collected by the outer documentation workflow.
    """
    write_reference_tree(
        output_root,
        pages,
        tool_versions={"cargo-docs-md": toolchain.cargo_docs_md, "rustdoc": toolchain.nightly},
        source_hashes=source_hashes,
    )


def _index(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """Extract the rustdoc item index with a predictable identifier representation.

    Args:
        payload: Decoded rustdoc JSON artifact.

    Returns:
        Item mappings keyed by string rustdoc identifiers.

    Raises:
        RustDocumentationError: The JSON lacks a mapping-shaped item index.
    """
    raw_index = payload.get("index")
    if not isinstance(raw_index, Mapping):
        raise RustDocumentationError("rustdoc JSON lacks an item index")
    index = {str(item_id): item for item_id, item in raw_index.items() if isinstance(item, Mapping)}
    if not index:
        raise RustDocumentationError("rustdoc JSON item index contains no usable records")
    return index


def _paths(payload: Mapping[str, Any]) -> Mapping[str, Mapping[str, Any]]:
    """Extract optional rustdoc qualified-path metadata without accepting malformed entries.

    Args:
        payload: Decoded rustdoc JSON artifact.

    Returns:
        Usable path records keyed by string rustdoc identifiers.
    """
    raw_paths = payload.get("paths", {})
    if not isinstance(raw_paths, Mapping):
        return {}
    return {str(item_id): path for item_id, path in raw_paths.items() if isinstance(path, Mapping)}


def _parent_ids(index: Mapping[str, Mapping[str, Any]]) -> dict[str, str]:
    """Build parent links from rustdoc module item lists and explicit parent fields.

    Args:
        index: Rustdoc items keyed by identifier.

    Returns:
        Child-to-parent identifier mapping for locally described declarations.
    """
    parents: dict[str, str] = {}
    for item_id, item in index.items():
        parent = item.get("parent")
        if parent is not None:
            parents[item_id] = str(parent)
        module = item.get("inner", {}).get("module") if isinstance(item.get("inner"), Mapping) else None
        if isinstance(module, Mapping):
            items = module.get("items", ())
            if isinstance(items, Sequence) and not isinstance(items, (str, bytes)):
                for child_id in items:
                    parents.setdefault(str(child_id), item_id)
        inner = item.get("inner")
        implementation = inner.get("impl") if isinstance(inner, Mapping) else None
        if not isinstance(implementation, Mapping) or implementation.get("trait") is not None:
            continue
        target = implementation.get("for")
        resolved = target.get("resolved_path") if isinstance(target, Mapping) else None
        target_id = resolved.get("id") if isinstance(resolved, Mapping) else None
        items = implementation.get("items", ())
        if target_id is None or not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
            continue
        for child_id in items:
            parents.setdefault(str(child_id), str(target_id))
    return parents


def _qualified_name(
    item_id: str,
    index: Mapping[str, Mapping[str, Any]],
    paths: Mapping[str, Mapping[str, Any]],
    parent_ids: Mapping[str, str],
) -> str:
    """Return a stable Rust qualified name from rustdoc paths or structural ancestry.

    Args:
        item_id: Rustdoc identifier whose name is required.
        index: Rustdoc items keyed by identifier.
        paths: Rustdoc qualified-path metadata keyed by identifier.
        parent_ids: Child-to-parent structure links used as a conservative fallback.

    Returns:
        Double-colon-separated source identity.
    """
    path = paths.get(item_id, {}).get("path")
    if isinstance(path, Sequence) and not isinstance(path, (str, bytes)) and path:
        return "::".join(str(part) for part in path)
    names: list[str] = []
    current: str | None = item_id
    while current is not None and current in index:
        name = str(index[current].get("name") or "").strip()
        if name:
            names.append(name)
        current = parent_ids.get(current)
    return "::".join(reversed(names)) or item_id


def _python_bindings(
    index: Mapping[str, Mapping[str, Any]],
    local_ids: Sequence[str],
    parent_ids: Mapping[str, str],
    qualified_names: Mapping[str, str],
    source_root: Path,
) -> dict[str, str]:
    """Statically find direct PyO3 exports and inherited methods of PyO3 classes.

    Args:
        index: Rustdoc items keyed by identifier.
        local_ids: Root-crate, non-generated Rustdoc identifiers under consideration.
        parent_ids: Child-to-parent structural links for associated methods.
        qualified_names: Stable Rust names used only in diagnostic fallback labels.
        source_root: Repository root containing the Rust files referenced by rustdoc spans.

    Returns:
        Identifier-to-Python-qualified-name mapping for confirmed PyO3-visible declarations.
    """
    direct: dict[str, str] = {}
    for item_id in local_ids:
        binding = _direct_python_binding(index[item_id], source_root)
        if binding is not None:
            direct[item_id] = binding
    bindings = dict(direct)
    unresolved = set(local_ids)
    while unresolved:
        progressed = False
        for item_id in tuple(unresolved):
            parent_id = parent_ids.get(item_id)
            if parent_id is not None and parent_id in bindings and _item_kind(index[item_id]) == "function":
                bindings[item_id] = _python_method_binding(
                    index[item_id],
                    source_root=source_root,
                    parent_binding=bindings[parent_id],
                    fallback_name=str(index[item_id].get("name") or qualified_names[item_id]),
                )
                progressed = True
            unresolved.remove(item_id)
        if not progressed:
            break
    return bindings


def _python_method_binding(
    item: Mapping[str, Any], *, source_root: Path, parent_binding: str, fallback_name: str
) -> str:
    """Return the Python identity of one method inherited from a bound PyO3 class.

    Args:
        item: Rustdoc method item whose adjacent source attributes are inspected.
        source_root: Repository root used to resolve the method's source span.
        parent_binding: Confirmed Python-qualified name of the owning class.
        fallback_name: Rust method name used when PyO3 does not rename it.

    Returns:
        The class identity for ``#[new]`` constructors, otherwise the qualified
        exposed method name.
    """
    attributes = _method_attribute_source(item, source_root)
    if _PYMETHOD_NEW_ATTRIBUTE.search(attributes):
        return parent_binding
    exposed_name = fallback_name
    for attribute in _PYMETHOD_ATTRIBUTE.finditer(attributes):
        name_match = _PYTHON_NAME_OPTION.search(attribute.group("options"))
        if name_match is not None:
            exposed_name = name_match.group("name")
    return f"{parent_binding}.{exposed_name}"


def _method_attribute_source(item: Mapping[str, Any], source_root: Path) -> str:
    """Return source text between the preceding method and this declaration.

    Args:
        item: Rustdoc method item supplying a source path and declaration line.
        source_root: Repository root used to resolve that path.

    Returns:
        The narrow source prefix that can contain attributes for this method, or
        an empty string when source provenance is unavailable.
    """
    source_path = _source_path(item)
    line = _source_line(item)
    if not source_path or line is None:
        return ""
    source_file = source_root / source_path
    if not source_file.is_file():
        return ""
    lines = source_file.read_text(encoding="utf-8").splitlines()
    declaration_index = min(max(line - 1, 0), len(lines))
    preceding_declaration = 0
    function_pattern = re.compile(r"^\s*(?:pub(?:\s*\([^)]*\))?\s+)?fn\s+[A-Za-z_][A-Za-z0-9_]*\b")
    for index in range(declaration_index - 1, -1, -1):
        if function_pattern.match(lines[index]):
            preceding_declaration = index + 1
            break
    return "\n".join(lines[preceding_declaration : declaration_index + 1])


def _direct_python_binding(item: Mapping[str, Any], source_root: Path) -> str | None:
    """Return a confirmed PyO3 binding name from attributes adjacent to one declaration.

    Args:
        item: One rustdoc item with source span and declaration name.
        source_root: Repository root used to resolve a relative rustdoc source filename.

    Returns:
        Python-qualified export name, or ``None`` when no direct PyO3 attribute is evidenced.
    """
    source_path = _source_path(item)
    if not source_path:
        return None
    source_file = source_root / source_path
    if not source_file.is_file():
        return None
    source_text = source_file.read_text(encoding="utf-8")
    name = str(item.get("name") or "").strip()
    if not name:
        return None
    function_pattern = re.compile(r"\b(?:pub(?:\s*\([^)]*\))?\s+)?fn\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\b")
    for function_attribute in _PYFUNCTION_ATTRIBUTE.finditer(source_text):
        declaration_prefix = "\n".join(source_text[function_attribute.end() :].splitlines()[:12])
        declaration = function_pattern.search(declaration_prefix)
        if declaration is not None and declaration.group("name") == name:
            return _python_binding_name(function_attribute.group("options"), default_name=name)
    class_pattern = re.compile(r"\b(?:pub(?:\s*\([^)]*\))?\s+)?(?:struct|enum)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\b")
    for class_attribute in _PYCLASS_ATTRIBUTE.finditer(source_text):
        declaration_prefix = "\n".join(source_text[class_attribute.end() :].splitlines()[:12])
        declaration = class_pattern.search(declaration_prefix)
        if declaration is not None and declaration.group("name") == name:
            return _python_binding_name(class_attribute.group("options"), default_name=name)
    return None


def _python_binding_name(options: str | None, *, default_name: str) -> str:
    """Return a Python export name from PyO3 options without guessing unavailable metadata.

    Args:
        options: Attribute option text captured from a confirmed PyO3 attribute.
        default_name: Rust declaration name used when the attribute omits an explicit Python name.

    Returns:
        Qualified Python extension name, defaulting to ``miniproto._native`` provenance.
    """
    options = options or ""
    name_match = _PYTHON_NAME_OPTION.search(options)
    module_match = _PYTHON_MODULE_OPTION.search(options)
    name = name_match.group("name") if name_match is not None else default_name
    module = module_match.group("module") if module_match is not None else "miniproto._native"
    return f"{module}.{name}"


def _selected_item_ids(
    *,
    index: Mapping[str, Mapping[str, Any]],
    local_ids: Sequence[str],
    root_id: str,
    parent_ids: Mapping[str, str],
    qualified_names: Mapping[str, str],
    bindings: Mapping[str, str],
    reviewed_modules: set[str],
) -> set[str]:
    """Select root/public/PyO3 declarations and the modules required to index them.

    Args:
        index: Rustdoc items keyed by identifier.
        local_ids: Root-crate, non-generated item identifiers.
        root_id: Rustdoc identifier for the crate module.
        parent_ids: Child-to-parent structural links.
        qualified_names: Stable item names used to apply reviewed-module policy.
        bindings: Confirmed PyO3-visible declaration names.
        reviewed_modules: Explicit maintained module names admitting public Rust declarations.

    Returns:
        Identifiers that should receive crate/module/item pages.
    """
    selected = {root_id}
    for item_id in local_ids:
        item = index[item_id]
        kind = _item_kind(item)
        if kind not in _DOCUMENTABLE_KINDS or not _is_in_reviewed_surface(qualified_names[item_id], reviewed_modules):
            continue
        if _is_public(item) or item_id in bindings:
            selected.add(item_id)
    changed = True
    while changed:
        changed = False
        for item_id in tuple(selected):
            parent_id = parent_ids.get(item_id)
            if (
                parent_id is not None
                and parent_id in index
                and _item_kind(index[parent_id]) == "module"
                and parent_id not in selected
            ):
                selected.add(parent_id)
                changed = True
    return selected


def _is_in_reviewed_surface(qualified_name: str, reviewed_modules: set[str]) -> bool:
    """Apply the reviewed-module boundary while retaining crate-root public declarations.

    Args:
        qualified_name: Double-colon-separated Rust declaration identity.
        reviewed_modules: Explicit maintained module names approved for generated references.

    Returns:
        Whether the item is directly under the crate or belongs to a reviewed top-level module.
    """
    parts = qualified_name.split("::")
    return len(parts) <= 2 or (len(parts) > 2 and parts[1] in reviewed_modules)


def _validate_selected_documentation(
    index: Mapping[str, Mapping[str, Any]], selected_ids: Sequence[str], qualified_names: Mapping[str, str]
) -> None:
    """Reject selected declarations with absent prose or undocumented non-receiver parameters.

    Args:
        index: Rustdoc items keyed by identifier.
        selected_ids: Items included in the committed Rust reference surface.
        qualified_names: Stable source identities used in actionable failure messages.

    Raises:
        RustDocumentationError: A selected declaration lacks documentation or argument descriptions.
    """
    for item_id in sorted(selected_ids, key=lambda value: qualified_names[value]):
        item = index[item_id]
        source_path = _source_path(item)
        line = _source_line(item)
        docs = str(item.get("docs") or "").strip()
        if not docs:
            raise RustDocumentationError(
                f"missing Rust documentation for {qualified_names[item_id]} at {source_path}:{line}"
            )
        function = _function(item)
        if function is None:
            continue
        documented = _argument_descriptions(docs)
        missing = tuple(name for name in _function_argument_names(function) if name not in documented)
        if missing:
            names = ", ".join(f"`{name}`" for name in missing)
            raise RustDocumentationError(
                f"missing Rust argument documentation for {qualified_names[item_id]} at {source_path}:{line}: {names}"
            )


def _validate_rendered_markdown(
    selected_ids: Sequence[str], rendered_markdown: Mapping[str, str], qualified_names: Mapping[str, str]
) -> None:
    """Require converter-owned Markdown for every page instead of reconstructing it from JSON.

    Args:
        selected_ids: Items included in the committed Rust reference surface.
        rendered_markdown: Complete cargo-docs-md bodies keyed by rustdoc identifier.
        qualified_names: Stable source identities used in actionable failure messages.

    Raises:
        RustDocumentationError: A selected item lacks meaningful converter output.
    """
    for item_id in selected_ids:
        body = str(rendered_markdown.get(item_id) or "").strip()
        if not body:
            raise RustDocumentationError(f"cargo-docs-md output is missing for {qualified_names[item_id]}")


def _selected_children(selected_ids: Sequence[str], parent_ids: Mapping[str, str]) -> dict[str, tuple[str, ...]]:
    """Group selected child identifiers beneath their selected module parent.

    Args:
        selected_ids: Items included in the committed Rust reference surface.
        parent_ids: Child-to-parent structural links.

    Returns:
        Deterministically ordered child identifiers keyed by parent identifier.
    """
    children: dict[str, list[str]] = {}
    for item_id in selected_ids:
        parent_id = parent_ids.get(item_id)
        if parent_id is not None and parent_id in selected_ids:
            children.setdefault(parent_id, []).append(item_id)
    return {parent: tuple(sorted(items)) for parent, items in children.items()}


def _module_body(
    *,
    item_id: str,
    qualified_name: str,
    item: Mapping[str, Any],
    children: Sequence[str],
    qualified_names: Mapping[str, str],
    rendered_markdown: str,
    crate: str,
    source_path: str,
    source_url: str,
) -> str:
    """Create a wrapper around converter output for a crate or module index page.

    Args:
        item_id: Rustdoc identifier of the module being rendered.
        qualified_name: Stable Rust module identity.
        item: Rustdoc module record providing visibility metadata.
        children: Selected direct child identifiers linked from this index.
        qualified_names: Stable Rust names for each selected child.
        rendered_markdown: Complete cargo-docs-md module body before unpublished-link filtering.
        crate: Cargo crate provenance.
        source_path: Repository-relative module source path.
        source_url: Line-anchored module source browser URL.

    Returns:
        Normalized module body retaining converter-rendered prose while collapsing links to deliberately unpublished modules.
    """
    published_child_slugs = {_slug(qualified_names[child].rsplit("::", 1)[-1]) for child in children}
    filtered_markdown = _filter_unpublished_module_links(rendered_markdown, published_child_slugs=published_child_slugs)
    item_links = "\n".join(
        f"- [`{qualified_names[child]}`](./{_slug(qualified_names[child].rsplit('::', 1)[-1])}/)" for child in children
    )
    if not item_links:
        item_links = "- No selected public or PyO3-visible items are defined directly in this module."
    return "\n\n".join(
        (
            _provenance_body(
                crate=crate, item=item, source_path=source_path, source_url=source_url, python_binding=None
            ),
            "## Documented items\n\n" + item_links,
            "## cargo-docs-md rendering\n\n" + filtered_markdown.strip(),
        )
    )


def _filter_unpublished_module_links(markdown: str, *, published_child_slugs: set[str]) -> str:
    """Collapse cargo-docs-md module links whose generated destinations are intentionally unpublished.

    Args:
        markdown: Complete converter-owned module Markdown.
        published_child_slugs: Relative child-route slugs emitted beneath the current module page.

    Returns:
        Converter Markdown with valid module links preserved and unavailable destinations reduced to their original labels.
    """

    def replace(match: re.Match[str]) -> str:
        """Preserve one published module link or return its non-link label.

        Args:
            match: Regex match containing the converter label and relative module slug.

        Returns:
            Original Markdown for a published child, otherwise only the original visible label.
        """
        return match.group(0) if match.group("slug") in published_child_slugs else match.group("label")

    return _CARGO_DOCS_MODULE_LINK.sub(replace, markdown)


def _item_body(
    *,
    item: Mapping[str, Any],
    qualified_name: str,
    rendered_markdown: str,
    crate: str,
    source_path: str,
    source_url: str,
    line: int,
    python_binding: str | None,
) -> str:
    """Create structural metadata while retaining complete cargo-docs-md item rendering.

    Args:
        item: Rustdoc declaration record.
        qualified_name: Stable Rust declaration identity.
        rendered_markdown: Complete unchanged cargo-docs-md item body.
        crate: Cargo crate provenance.
        source_path: Repository-relative declaration source path.
        source_url: Line-anchored declaration source browser URL.
        line: One-based declaration line from rustdoc source provenance.
        python_binding: Confirmed Python-visible PyO3 name, when static attributes evidence one.

    Returns:
        Normalized item body with provenance, signature, arguments, and converter output.
    """
    sections = [
        _provenance_body(
            crate=crate, item=item, source_path=source_path, source_url=source_url, python_binding=python_binding
        )
    ]
    function = _function(item)
    if function is not None:
        sections.append(f"## Signature\n\n```rust\n{_function_signature(item, function)}\n```")
        descriptions = _argument_descriptions(str(item.get("docs") or ""))
        arguments = _function_argument_names(function)
        if arguments:
            argument_lines = "\n".join(f"- `{name}`: {descriptions[name]}" for name in arguments)
            sections.append("## Arguments\n\n" + argument_lines)
    sections.append("## cargo-docs-md rendering\n\n" + rendered_markdown.strip())
    return "\n\n".join(sections)


def _provenance_body(
    *, crate: str, item: Mapping[str, Any], source_path: str, source_url: str, python_binding: str | None
) -> str:
    """Render exact crate, source, visibility, and confirmed Python-exposure provenance.

    Args:
        crate: Cargo crate provenance recorded by the documentation workflow.
        item: Rustdoc declaration record supplying source-language visibility.
        source_path: Repository-relative source file path.
        source_url: Line-anchored browser URL for the source declaration.
        python_binding: Confirmed PyO3 export name, or ``None`` for Rust-only declarations.

    Returns:
        Markdown provenance section without unsupported runtime or performance claims.
    """
    visibility = _visibility_label(item)
    python = (
        f"`{python_binding}` (confirmed from adjacent PyO3 attributes)"
        if python_binding
        else "Not evidenced by static PyO3 attributes."
    )
    return "\n".join(
        (
            "## Provenance",
            "",
            f"- Crate: `{crate}`",
            f"- Rust visibility: `{visibility}`",
            f"- Source: [`{source_path}`]({source_url})",
            f"- Python exposure: {python}",
        )
    )


def _file_index_pages(
    *,
    selected_ids: Sequence[str],
    index: Mapping[str, Mapping[str, Any]],
    qualified_names: Mapping[str, str],
    source_details: Mapping[str, tuple[str, str, int]],
    crate: str,
) -> tuple[ReferencePage, ...]:
    """Create deterministic maintained-source file indexes from selected Rust items.

    Args:
        selected_ids: Items included in the committed Rust reference surface.
        index: Rustdoc items keyed by identifier.
        qualified_names: Stable Rust identities for selected items.
        source_details: Source path, source URL, and line provenance keyed by item identifier.
        crate: Cargo crate provenance recorded in generated frontmatter.

    Returns:
        One file index page for each selected source path.
    """
    by_source: dict[str, list[str]] = {}
    for item_id in selected_ids:
        by_source.setdefault(source_details[item_id][0], []).append(item_id)
    pages: list[ReferencePage] = []
    for source_path, item_ids in sorted(by_source.items()):
        ordered_ids = tuple(sorted(item_ids, key=lambda value: (source_details[value][2], qualified_names[value])))
        source_url = source_details[ordered_ids[0]][1]
        kind_counts: dict[str, int] = {}
        for item_id in ordered_ids:
            kind = _item_kind(index[item_id])
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
        kind_summary = ", ".join(f"{count} {kind}" for kind, count in sorted(kind_counts.items()))
        lines = ["## Documented declarations", ""]
        for item_id in ordered_ids:
            lines.append(f"- `{qualified_names[item_id]}` — `{_item_kind(index[item_id])}`")
        pages.append(
            ReferencePage(
                path=f"rust/{_slug(crate)}/files/{_slug(source_path.removesuffix('.rs').replace('/', '-'))}.md",
                title=source_path,
                description=f"{len(ordered_ids)} selected Rust declarations ({kind_summary}) from {source_path}, with source-span and available PyO3 binding provenance.",
                language="rust",
                kind="file",
                qualified_name=f"file:{source_path}",
                source_path=source_path,
                source_url=source_url,
                body="\n".join(lines),
                crate=crate,
            )
        )
    return tuple(pages)


def _source_provenance(item: Mapping[str, Any], *, source_root: Path, repository_url: str) -> tuple[str, str, int]:
    """Return source path, line-aware browser URL, and line for one selected Rust declaration.

    Args:
        item: Rustdoc declaration record with a local source span.
        source_root: Repository root used to make absolute spans repository-relative.
        repository_url: Repository browser base URL.

    Returns:
        Repository-relative source path, line-anchored URL, and one-based line number.

    Raises:
        RustDocumentationError: The selected declaration lacks usable source provenance.
    """
    source_path = _source_path(item)
    if not source_path:
        raise RustDocumentationError(f"selected Rust item lacks source provenance: {item.get('name')!r}")
    source = Path(source_path)
    if source.is_absolute():
        try:
            source_path = source.resolve().relative_to(source_root.resolve()).as_posix()
        except ValueError:
            source_path = source.as_posix()
    line = _source_line(item)
    return source_path, f"{repository_url.rstrip('/')}/blob/master/{source_path}#L{line}", line


def _source_path(item: Mapping[str, Any]) -> str:
    """Return a normalized rustdoc span filename, or an empty string when unavailable.

    Args:
        item: Rustdoc declaration record that may include a source span.

    Returns:
        Slash-normalized source filename, or an empty string for spanless records.
    """
    span = item.get("span")
    if not isinstance(span, Mapping):
        return ""
    filename = str(span.get("filename") or "")
    return _normalize_path(filename)


def _source_line(item: Mapping[str, Any]) -> int:
    """Return a safe one-based rustdoc span start line for diagnostics and source links.

    Args:
        item: Rustdoc declaration record that may include a source span.

    Returns:
        Positive source line, defaulting to one when rustdoc omits a usable beginning.
    """
    span = item.get("span")
    begin = span.get("begin") if isinstance(span, Mapping) else None
    if isinstance(begin, Sequence) and not isinstance(begin, (str, bytes)) and begin:
        try:
            return max(1, int(begin[0]))
        except (TypeError, ValueError):
            return 1
    return 1


def _item_kind(item: Mapping[str, Any]) -> str:
    """Return the rustdoc inner-record kind, using ``item`` for malformed declarations.

    Args:
        item: Rustdoc declaration record.

    Returns:
        First inner mapping key or the conservative generic kind.
    """
    inner = item.get("inner")
    if not isinstance(inner, Mapping) or not inner:
        return "item"
    return str(next(iter(inner)))


def _is_public(item: Mapping[str, Any]) -> bool:
    """Return whether rustdoc records a declaration as Rust-public.

    Args:
        item: Rustdoc declaration record containing a visibility representation.

    Returns:
        Whether the visibility is the public variant rather than crate/restricted/private.
    """
    visibility = item.get("visibility")
    if isinstance(visibility, str):
        return visibility == "public"
    return isinstance(visibility, Mapping) and "public" in visibility


def _visibility_label(item: Mapping[str, Any]) -> str:
    """Return a stable readable visibility label without promoting non-public declarations.

    Args:
        item: Rustdoc declaration record containing a visibility representation.

    Returns:
        Visibility label preserved from rustdoc, or ``unknown`` when it is absent.
    """
    visibility = item.get("visibility")
    if isinstance(visibility, str) and visibility:
        return visibility
    if isinstance(visibility, Mapping) and visibility:
        return ", ".join(sorted(str(key) for key in visibility))
    return "unknown"


def _function(item: Mapping[str, Any]) -> Mapping[str, Any] | None:
    """Return an item's rustdoc function record when it has one.

    Args:
        item: Rustdoc declaration record.

    Returns:
        Function mapping for functions and methods, or ``None`` for other item kinds.
    """
    inner = item.get("inner")
    function = inner.get("function") if isinstance(inner, Mapping) else None
    return function if isinstance(function, Mapping) else None


def _function_argument_names(function: Mapping[str, Any]) -> tuple[str, ...]:
    """Return named non-lifetime generics and non-receiver value arguments.

    Args:
        function: Rustdoc ``inner.function`` mapping.

    Returns:
        Type/const generics followed by value arguments, excluding lifetimes,
        receiver spellings, and anonymous placeholders.
    """
    names: list[str] = []
    generics = function.get("generics")
    parameters = generics.get("params", ()) if isinstance(generics, Mapping) else ()
    if isinstance(parameters, Sequence) and not isinstance(parameters, (str, bytes)):
        for parameter in parameters:
            if not isinstance(parameter, Mapping):
                continue
            kind = parameter.get("kind")
            if isinstance(kind, Mapping) and "lifetime" in kind:
                continue
            name = str(parameter.get("name") or "").strip().removeprefix("r#")
            if name:
                names.append(name)
    signature = function.get("sig")
    inputs = signature.get("inputs", ()) if isinstance(signature, Mapping) else ()
    if not isinstance(inputs, Sequence) or isinstance(inputs, (str, bytes)):
        return tuple(names)
    for input_item in inputs:
        if not isinstance(input_item, Sequence) or isinstance(input_item, (str, bytes)) or not input_item:
            continue
        name = str(input_item[0]).strip().removeprefix("r#")
        if not name or name in {"self", "slf", "_"} or "self" in name.split():
            continue
        names.append(name)
    return tuple(names)


def _argument_descriptions(documentation: str) -> dict[str, str]:
    """Extract non-empty Rustdoc Arguments/Parameters bullet descriptions by parameter name.

    Args:
        documentation: Markdown documentation copied from one rustdoc item.

    Returns:
        Argument-to-description mapping for prose directly beneath an arguments heading.
    """
    descriptions: dict[str, str] = {}
    in_arguments = False
    current_name: str | None = None
    current_parts: list[str] = []

    def flush() -> None:
        """Store the accumulated current description only when it contains meaningful prose."""
        nonlocal current_name, current_parts
        description = " ".join(part.strip() for part in current_parts if part.strip()).strip()
        if current_name is not None and description:
            descriptions[current_name.removeprefix("r#")] = description
        current_name = None
        current_parts = []

    for line in documentation.splitlines():
        if _ARGUMENTS_HEADING.match(line):
            flush()
            in_arguments = True
            continue
        if _HEADING.match(line):
            flush()
            in_arguments = False
            continue
        if not in_arguments:
            continue
        match = _ARGUMENT.match(line)
        if match is not None:
            flush()
            current_name = next(value for value in match.group("code", "bold", "plain") if value is not None)
            current_parts.append(match.group("description"))
        elif current_name is not None:
            current_parts.append(line)
    flush()
    return descriptions


def _function_signature(item: Mapping[str, Any], function: Mapping[str, Any]) -> str:
    """Render a compact structural Rust signature from rustdoc JSON types.

    Args:
        item: Rustdoc declaration record supplying the source-level function name.
        function: Rustdoc ``inner.function`` mapping supplying inputs and output.

    Returns:
        Rust-like signature that lists every rustdoc input in source order.
    """
    signature = function.get("sig")
    inputs = signature.get("inputs", ()) if isinstance(signature, Mapping) else ()
    rendered_inputs: list[str] = []
    if isinstance(inputs, Sequence) and not isinstance(inputs, (str, bytes)):
        for input_item in inputs:
            if not isinstance(input_item, Sequence) or isinstance(input_item, (str, bytes)) or len(input_item) < 2:
                continue
            rendered_inputs.append(f"{input_item[0]}: {_render_type(input_item[1])}")
    output = signature.get("output") if isinstance(signature, Mapping) else None
    output_suffix = "" if output is None else f" -> {_render_type(output)}"
    return f"fn {item.get('name') or 'anonymous'}({', '.join(rendered_inputs)}){output_suffix}"


def _render_type(type_data: Any) -> str:
    """Render common rustdoc JSON type nodes without claiming full compiler pretty-printing.

    Args:
        type_data: Rustdoc JSON type representation from a function signature.

    Returns:
        Deterministic readable type text, preserving unknown structured values as ``_``.
    """
    if type_data is None:
        return "()"
    if isinstance(type_data, str):
        return type_data
    if not isinstance(type_data, Mapping):
        return "_"
    for simple_key in ("primitive", "generic", "infer"):
        if simple_key in type_data:
            return str(type_data[simple_key])
    resolved = type_data.get("resolved_path")
    if isinstance(resolved, Mapping):
        return str(resolved.get("name") or "_")
    borrowed = type_data.get("borrowed_ref")
    if isinstance(borrowed, Mapping):
        mutable = "mut " if borrowed.get("is_mutable") else ""
        return f"&{mutable}{_render_type(borrowed.get('type'))}"
    raw_pointer = type_data.get("raw_pointer")
    if isinstance(raw_pointer, Mapping):
        mutable = "mut " if raw_pointer.get("is_mutable") else "const "
        return f"*{mutable}{_render_type(raw_pointer.get('type'))}"
    if "slice" in type_data:
        return f"[{_render_type(type_data['slice'])}]"
    if "array" in type_data and isinstance(type_data["array"], Mapping):
        array = type_data["array"]
        return f"[{_render_type(array.get('type'))}; {array.get('len') or '_'}]"
    if "tuple" in type_data and isinstance(type_data["tuple"], Sequence):
        return "(" + ", ".join(_render_type(member) for member in type_data["tuple"]) + ")"
    return "_"


def _module_page_path(qualified_name: str, crate: str) -> str:
    """Return the stable Markdown path for one crate or module index.

    Args:
        qualified_name: Double-colon-separated crate/module identity.
        crate: Cargo crate provenance used as the reference-root path segment.

    Returns:
        Relative Markdown index path.
    """
    parts = qualified_name.split("::")[1:]
    prefix = f"rust/{_slug(crate)}"
    return f"{prefix}/{'/'.join(_slug(part) for part in parts) + '/' if parts else ''}index.md"


def _item_page_path(qualified_name: str, crate: str) -> str:
    """Return the stable Markdown path for one Rust detail page.

    Args:
        qualified_name: Double-colon-separated Rust declaration identity.
        crate: Cargo crate provenance used as the reference-root path segment.

    Returns:
        Relative Markdown detail-page path.
    """
    parts = qualified_name.split("::")[1:]
    if not parts:
        return f"rust/{_slug(crate)}/item.md"
    parent = "/".join(_slug(part) for part in parts[:-1])
    filename = _slug(parts[-1])
    return f"rust/{_slug(crate)}/{parent + '/' if parent else ''}{filename}.md"


def _page_kind(item: Mapping[str, Any], parent_ids: Mapping[str, str], index: Mapping[str, Mapping[str, Any]]) -> str:
    """Label associated functions as methods while retaining rustdoc's ordinary declaration kinds.

    Args:
        item: Rustdoc declaration record being converted to a detail page.
        parent_ids: Child-to-parent structural links.
        index: Rustdoc item mapping used to inspect the item's parent kind.

    Returns:
        ``method`` for associated function records, otherwise the rustdoc inner kind.
    """
    item_id = next((key for key, value in index.items() if value is item), None)
    parent_id = parent_ids.get(item_id) if item_id is not None else None
    if (
        _item_kind(item) == "function"
        and parent_id is not None
        and _item_kind(index.get(parent_id, {})) in {"struct", "enum", "trait"}
    ):
        return "method"
    return _item_kind(item)


def _summary(item: Mapping[str, Any], qualified_name: str) -> str:
    """Return a selected item's first documentation line for page frontmatter.

    Args:
        item: Rustdoc item whose documentation is already known to be non-empty.
        qualified_name: Source identity used only in an impossible-input diagnostic.

    Returns:
        First non-empty Rustdoc line.

    Raises:
        RustDocumentationError: Documentation validation was bypassed or invalidated.
    """
    lines = [line.strip() for line in str(item.get("docs") or "").splitlines() if line.strip()]
    if not lines:
        raise RustDocumentationError(f"cannot derive page summary from missing docs: {qualified_name}")
    return lines[0]


def _normalize_path(value: str) -> str:
    """Normalize Rustdoc filenames to slash-separated repository-path form.

    Args:
        value: Rustdoc span filename or generator exclusion path.

    Returns:
        Slash-normalized trimmed path.
    """
    return value.replace("\\", "/").strip()


def _slug(value: str) -> str:
    """Convert Rust path segments to stable lowercase collision-readable route slugs.

    Args:
        value: Crate, module, declaration, or source-path segment to normalize.

    Returns:
        Route-safe slug, or ``item`` when no alphanumeric characters remain.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "item"


def _load_rendered_markdown(path: Path) -> dict[str, str]:
    """Load the adapter's rustdoc-id-to-cargo-docs-md Markdown staging manifest.

    Args:
        path: JSON mapping file created by the outer cargo-docs-md staging adapter.

    Returns:
        String body mapping keyed by rustdoc identifier.

    Raises:
        RustDocumentationError: The staging manifest is not a JSON object of Markdown strings.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping) or any(not isinstance(value, str) for value in payload.values()):
        raise RustDocumentationError(f"rendered Markdown manifest must map item identifiers to strings: {path}")
    return {str(item_id): body for item_id, body in payload.items()}


def _parse_arguments(argv: Sequence[str] | None) -> argparse.Namespace:
    """Parse standalone static-normalizer arguments without invoking Cargo or Python runtime code.

    Args:
        argv: Optional command-line arguments excluding the executable name.

    Returns:
        Parsed normalizer configuration.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rustdoc-json", type=Path, required=True, help="Pinned-nightly rustdoc JSON artifact.")
    parser.add_argument("--source-root", type=Path, required=True, help="Repository root for source/PyO3 provenance.")
    parser.add_argument(
        "--rendered-markdown", type=Path, required=True, help="cargo-docs-md staging manifest keyed by rustdoc id."
    )
    parser.add_argument("--output-root", type=Path, required=True, help="Destination generated reference tree.")
    parser.add_argument("--repository-url", required=True, help="Repository browser URL base.")
    parser.add_argument("--crate", required=True, help="Cargo crate provenance name.")
    parser.add_argument(
        "--reviewed-module", action="append", default=[], help="Maintained Rust module included in the public surface."
    )
    parser.add_argument(
        "--source-hashes", type=Path, required=True, help="JSON mapping of source paths to deterministic hashes."
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the static normalizer after an outer workflow produced pinned renderer artifacts.

    Args:
        argv: Optional command-line arguments excluding the executable name.

    Returns:
        Zero when validated normalized pages and their deterministic manifest are written.

    Raises:
        RustDocumentationError: Inputs do not provide a complete selected documentation surface.
        RustDocumentationPending: The checked-in exact toolchain pin is absent or invalid.
    """
    arguments = _parse_arguments(argv)
    toolchain = load_documentation_toolchain()
    pages = generate_rust_pages(
        rustdoc_json=arguments.rustdoc_json,
        source_root=arguments.source_root,
        rendered_markdown=_load_rendered_markdown(arguments.rendered_markdown),
        repository_url=arguments.repository_url,
        crate=arguments.crate,
        reviewed_modules=arguments.reviewed_module,
    )
    source_hashes = json.loads(arguments.source_hashes.read_text(encoding="utf-8"))
    if not isinstance(source_hashes, Mapping) or any(not isinstance(value, str) for value in source_hashes.values()):
        raise RustDocumentationError("source hashes must be a JSON object mapping paths to strings")
    write_rust_reference_tree(
        output_root=arguments.output_root,
        pages=pages,
        toolchain=toolchain,
        source_hashes={str(path): value for path, value in source_hashes.items()},
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DEFAULT_EXCLUDED_SOURCE_PATHS",
    "DEFAULT_TOOLCHAIN_FILE",
    "RustDocumentationError",
    "RustDocumentationPending",
    "RustDocumentationToolchain",
    "cargo_docs_md_command",
    "cargo_docs_md_install_command",
    "ensure_pinned_nightly_available",
    "generate_pinned_rustdoc_json",
    "generate_rust_pages",
    "load_cargo_docs_md_fragments",
    "load_documentation_toolchain",
    "main",
    "pinned_rustdoc_command",
    "render_rustdoc_with_cargo_docs_md",
    "verify_cargo_docs_md_version",
    "write_rust_reference_tree",
]
