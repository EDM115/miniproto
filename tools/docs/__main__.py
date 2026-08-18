"""Generate, verify, and build miniproto's committed documentation website."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
import tomllib
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urljoin, urlsplit

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIGURATION = _REPOSITORY_ROOT / "docs/reference-surface.toml"
_GENERATOR_VERSION = "1"
_SURFACE_CONTRACT_MARKER = "miniproto-surface:user-pinned-packet-loom"
_REQUIRED_SITE_ROUTES = ("/", "/start/", "/guides/", "/concepts/", "/recipes/", "/faq/", "/reference/", "/project/")
_REQUIRED_PAGEFIND_FILTERS = {"crate", "kind", "language", "layer", "module", "namespace", "python_visible"}


class DocumentationConfigurationError(ValueError):
    """Report an invalid or unsafe checked-in documentation configuration."""


class DocumentationGenerationError(RuntimeError):
    """Report a failed reference-generation or static-site stage."""


@dataclass(frozen=True, slots=True)
class PythonDocumentationConfiguration:
    """Describe the statically reviewed maintained Python reference surface.

    Attributes:
        source_root: Static import-search root containing ``miniproto``.
        module_names: Explicit supported modules selected for reference pages.
        dynamic_all_modules: Modules allowed to use the conservative dynamic-``__all__`` fallback.
        excluded_roots: Generator-owned Python trees omitted from maintained-source audits.
    """

    source_root: Path
    module_names: tuple[str, ...]
    dynamic_all_modules: tuple[str, ...]
    excluded_roots: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class TelegramDocumentationConfiguration:
    """Describe immutable Telegram schema and binding inputs.

    Attributes:
        schema_path: Canonical normalized TDLib structural schema.
        metadata_path: Layer, source-precedence, digest, and count metadata.
        rpc_errors_path: Pinned Telegram RPC-error database.
        bindings_path: Generated schema-to-Python binding manifest.
        relationships_path: POSIX path for the generated relationship artifact relative to ``docs/reference``.
    """

    schema_path: Path
    metadata_path: Path
    rpc_errors_path: Path
    bindings_path: Path
    relationships_path: str


@dataclass(frozen=True, slots=True)
class RustDocumentationConfiguration:
    """Describe the exact Rust documentation extraction contract.

    Attributes:
        manifest_path: Cargo manifest for the native extension crate.
        source_root: Repository source root used for spans and PyO3 attributes.
        toolchain_path: Exact documentation-only nightly and converter pin.
        crate: Crate provenance and cargo-docs-md output name.
        artifact_stem: Rustdoc JSON artifact filename without its suffix.
        reviewed_modules: Modules whose supported public/PyO3 surface receives pages.
        excluded_paths: Generator-owned Rust sources omitted from audit and pages.
    """

    manifest_path: Path
    source_root: Path
    toolchain_path: Path
    crate: str
    artifact_stem: str
    reviewed_modules: tuple[str, ...]
    excluded_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SiteDocumentationConfiguration:
    """Describe the pinned local Astro/Starlight command sequence.

    Attributes:
        directory: Documentation-site package directory.
        package_manager: Expected package-manager executable name.
        install_command: Frozen-lockfile dependency installation command.
        check_command: Static Astro content/type validation command.
        build_command: Static production-site build command.
        test_command: Browser acceptance command against the built static artifact.
    """

    directory: Path
    package_manager: str
    install_command: tuple[str, ...]
    check_command: tuple[str, ...]
    build_command: tuple[str, ...]
    test_command: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DocumentationConfiguration:
    """Aggregate every reviewed input and owned output for the documentation pipeline.

    Attributes:
        schema_version: Configuration contract version.
        repository_root: Checkout root against which all paths were validated.
        repository_url: Browser URL used to construct source provenance links.
        output_root: Exact generated Markdown root owned by this command.
        python: Maintained Python surface configuration.
        telegram: Telegram raw-reference input configuration.
        rust: Native Rust reference configuration.
        site: Astro/Starlight frontend command configuration.
    """

    schema_version: int
    repository_root: Path
    repository_url: str
    output_root: Path
    python: PythonDocumentationConfiguration
    telegram: TelegramDocumentationConfiguration
    rust: RustDocumentationConfiguration
    site: SiteDocumentationConfiguration


@dataclass(frozen=True, slots=True)
class StaticSiteValidationReport:
    """Summarize deterministic validation of one built documentation artifact.

    Attributes:
        html_pages: Number of rendered HTML documents inspected.
        internal_links: Number of local links and assets whose destinations were checked.
        filter_names: Sorted Pagefind filter names discovered in rendered metadata.
    """

    html_pages: int
    internal_links: int
    filter_names: tuple[str, ...]


class _BuiltPageParser(HTMLParser):
    """Collect local references and Pagefind attributes from one rendered page.

    Attributes:
        local_references: Raw ``href`` and ``src`` values requiring destination validation.
        filter_names: Pagefind filter keys declared by rendered metadata.
        has_pagefind_body: Whether the page exposes an intentional indexable content region.
        has_surface_contract: Whether the root artifact retained the Packet Loom design contract marker.
    """

    def __init__(self) -> None:
        """Initialize empty parser state for one HTML document."""
        super().__init__(convert_charrefs=True)
        self.local_references: list[str] = []
        self.filter_names: set[str] = set()
        self.has_pagefind_body = False
        self.has_surface_contract = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Collect relevant link, asset, and Pagefind attributes from an opening tag.

        Args:
            tag: Lowercase HTML element name supplied by ``HTMLParser``.
            attrs: Attribute name/value pairs present on the element.
        """
        del tag
        values = dict(attrs)
        for name in ("href", "src"):
            value = values.get(name)
            if value:
                self.local_references.append(value)
        if "data-pagefind-body" in values:
            self.has_pagefind_body = True
        filter_expression = values.get("data-pagefind-filter")
        if filter_expression:
            for declaration in filter_expression.split(","):
                name = declaration.strip().split("[", 1)[0].split(":", 1)[0].strip()
                if name:
                    self.filter_names.add(name)

    def handle_comment(self, data: str) -> None:
        """Record whether an emitted HTML comment carries the visual direction contract.

        Args:
            data: Comment contents without the surrounding delimiter.
        """
        if _SURFACE_CONTRACT_MARKER in data:
            self.has_surface_contract = True


def load_documentation_configuration(path: Path, *, repository_root: Path) -> DocumentationConfiguration:
    """Load and validate the checked-in documentation surface manifest.

    Args:
        path: TOML configuration to decode.
        repository_root: Checkout root that bounds every resolved filesystem path.

    Returns:
        Validated immutable pipeline configuration.

    Raises:
        DocumentationConfigurationError: The schema, value types, path ownership, or reviewed lists are invalid.
    """
    repository_root = repository_root.resolve()
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    if int(payload.get("schema_version", 0)) != 1:
        raise DocumentationConfigurationError("reference surface schema_version must be exactly 1")
    repository_url = _required_string(payload, "repository_url").rstrip("/")
    output_root = _repository_path(repository_root, _required_string(payload, "output_root"), field="output_root")
    expected_output = (repository_root / "docs/reference").resolve()
    if output_root != expected_output:
        raise DocumentationConfigurationError(f"output_root must resolve exactly to {expected_output}")

    python = _required_mapping(payload, "python")
    telegram = _required_mapping(payload, "telegram")
    rust = _required_mapping(payload, "rust")
    site = _required_mapping(payload, "site")
    python_configuration = PythonDocumentationConfiguration(
        source_root=_repository_path(
            repository_root, _required_string(python, "source_root"), field="python.source_root"
        ),
        module_names=_unique_strings(python, "module_names"),
        dynamic_all_modules=_unique_strings(python, "dynamic_all_modules"),
        excluded_roots=tuple(
            _repository_path(repository_root, value, field="python.excluded_roots")
            for value in _unique_strings(python, "excluded_roots")
        ),
    )
    if tuple(sorted(python_configuration.module_names)) != python_configuration.module_names:
        raise DocumentationConfigurationError("python.module_names must be unique and lexicographically sorted")
    if not set(python_configuration.dynamic_all_modules).issubset(python_configuration.module_names):
        raise DocumentationConfigurationError("python.dynamic_all_modules must be selected module_names")

    relationships_path = _relative_artifact_path(_required_string(telegram, "relationships_path"))
    telegram_configuration = TelegramDocumentationConfiguration(
        schema_path=_repository_path(
            repository_root, _required_string(telegram, "schema_path"), field="telegram.schema_path"
        ),
        metadata_path=_repository_path(
            repository_root, _required_string(telegram, "metadata_path"), field="telegram.metadata_path"
        ),
        rpc_errors_path=_repository_path(
            repository_root, _required_string(telegram, "rpc_errors_path"), field="telegram.rpc_errors_path"
        ),
        bindings_path=_repository_path(
            repository_root, _required_string(telegram, "bindings_path"), field="telegram.bindings_path"
        ),
        relationships_path=relationships_path,
    )
    rust_configuration = RustDocumentationConfiguration(
        manifest_path=_repository_path(
            repository_root, _required_string(rust, "manifest_path"), field="rust.manifest_path"
        ),
        source_root=_repository_path(repository_root, _required_string(rust, "source_root"), field="rust.source_root"),
        toolchain_path=_repository_path(
            repository_root, _required_string(rust, "toolchain_path"), field="rust.toolchain_path"
        ),
        crate=_required_string(rust, "crate"),
        artifact_stem=_required_string(rust, "artifact_stem"),
        reviewed_modules=_unique_strings(rust, "reviewed_modules"),
        excluded_paths=tuple(_relative_artifact_path(value) for value in _unique_strings(rust, "excluded_paths")),
    )
    site_configuration = SiteDocumentationConfiguration(
        directory=_repository_path(repository_root, _required_string(site, "directory"), field="site.directory"),
        package_manager=_required_string(site, "package_manager"),
        install_command=_command(site, "install_command"),
        check_command=_command(site, "check_command"),
        build_command=_command(site, "build_command"),
        test_command=_command(site, "test_command"),
    )
    for name, command in (
        ("site.install_command", site_configuration.install_command),
        ("site.check_command", site_configuration.check_command),
        ("site.build_command", site_configuration.build_command),
        ("site.test_command", site_configuration.test_command),
    ):
        if command[0] != site_configuration.package_manager:
            raise DocumentationConfigurationError(f"{name} must invoke {site_configuration.package_manager!r}")
    return DocumentationConfiguration(
        schema_version=1,
        repository_root=repository_root,
        repository_url=repository_url,
        output_root=output_root,
        python=python_configuration,
        telegram=telegram_configuration,
        rust=rust_configuration,
        site=site_configuration,
    )


def _required_mapping(payload: Mapping[str, Any], field: str) -> Mapping[str, Any]:
    """Return one required mapping-shaped configuration field.

    Args:
        payload: Decoded TOML object containing the field.
        field: Configuration key used in errors.

    Returns:
        Mapping stored under ``field``.

    Raises:
        DocumentationConfigurationError: The field is absent or not a mapping.
    """
    value = payload.get(field)
    if not isinstance(value, Mapping):
        raise DocumentationConfigurationError(f"{field} must be a TOML table")
    return value


def _required_string(payload: Mapping[str, Any], field: str) -> str:
    """Return one required non-empty string configuration field.

    Args:
        payload: Decoded TOML object containing the field.
        field: Configuration key used in errors.

    Returns:
        Trimmed string value.

    Raises:
        DocumentationConfigurationError: The field is absent, non-string, or empty.
    """
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise DocumentationConfigurationError(f"{field} must be a non-empty string")
    return value.strip()


def _unique_strings(payload: Mapping[str, Any], field: str) -> tuple[str, ...]:
    """Return a required list of unique non-empty strings.

    Args:
        payload: Decoded TOML object containing the list.
        field: Configuration key used in errors.

    Returns:
        String values in declared order.

    Raises:
        DocumentationConfigurationError: The list is absent, malformed, empty, or contains duplicates.
    """
    value = payload.get(field)
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
        raise DocumentationConfigurationError(f"{field} must be a non-empty string array")
    result = tuple(item.strip() for item in value)
    if len(set(result)) != len(result):
        raise DocumentationConfigurationError(f"{field} must not contain duplicates")
    return result


def _command(payload: Mapping[str, Any], field: str) -> tuple[str, ...]:
    """Return a non-empty subprocess argv from configuration.

    Args:
        payload: Decoded TOML object containing the command.
        field: Configuration key used in errors.

    Returns:
        Immutable command argument vector.
    """
    return _unique_strings(payload, field)


def _repository_path(repository_root: Path, value: str, *, field: str) -> Path:
    """Resolve one repository-relative path without permitting checkout escape.

    Args:
        repository_root: Resolved checkout root.
        value: Relative path declared in TOML.
        field: Configuration key used in errors.

    Returns:
        Resolved path inside ``repository_root``.

    Raises:
        DocumentationConfigurationError: The declared path is absolute or escapes the checkout.
    """
    candidate = Path(value)
    if candidate.is_absolute():
        raise DocumentationConfigurationError(f"{field} must be repository-relative")
    resolved = (repository_root / candidate).resolve()
    if resolved != repository_root and not resolved.is_relative_to(repository_root):
        raise DocumentationConfigurationError(f"{field} escapes the repository: {value!r}")
    return resolved


def _relative_artifact_path(value: str) -> str:
    """Validate and normalize a generated artifact's repository-style relative path.

    Args:
        value: Slash-oriented relative path.

    Returns:
        Normalized POSIX path.

    Raises:
        DocumentationConfigurationError: The path is absolute, empty, or traverses a parent.
    """
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise DocumentationConfigurationError(f"generated artifact path must be relative and traversal-free: {value!r}")
    return path.as_posix()


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the public documentation command without importing generator dependencies.

    Args:
        argv: Optional command-line arguments excluding the executable name.

    Returns:
        Parsed command configuration.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=_DEFAULT_CONFIGURATION,
        help="reviewed reference-surface TOML (default: docs/reference-surface.toml)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="generate into isolation and fail on committed reference drift without modifying docs/reference",
    )
    parser.add_argument(
        "--build", action="store_true", help="after reference generation/checking, run the pinned frontend checks/build"
    )
    parser.add_argument(
        "--site-only", action="store_true", help="skip reference generation and run only the site build"
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="skip pnpm's frozen-lockfile install before checking/building the site",
    )
    return parser.parse_args(argv)


def _reconcile_reference_tree(*, staging: Path, output_root: Path, repository_root: Path, check: bool) -> bool:
    """Compare or atomically replace the exact generated reference directory.

    Args:
        staging: Fully generated task-owned tree.
        output_root: Exact committed ``docs/reference`` destination.
        repository_root: Checkout root used to enforce ownership boundaries.
        check: Whether to report drift without changing the destination.

    Returns:
        Whether the expected and committed trees differed.

    Raises:
        DocumentationGenerationError: Either path escapes its permitted owned root.
        RuntimeError: Check mode detects added, removed, or changed files.
    """
    from tools.docs.manifest import compare_reference_trees

    repository_root = repository_root.resolve()
    expected_output = (repository_root / "docs/reference").resolve()
    expected_staging_root = (repository_root / ".tmp/docs-reference").resolve()
    staging = staging.resolve()
    output_root = output_root.resolve()
    if output_root != expected_output:
        raise DocumentationGenerationError(f"refusing to reconcile unexpected output root: {output_root}")
    if staging == expected_staging_root or not staging.is_relative_to(expected_staging_root):
        raise DocumentationGenerationError(f"refusing to reconcile non-owned staging root: {staging}")
    difference = compare_reference_trees(staging, output_root)
    if difference.is_clean:
        return False
    summary = _format_reference_diff(difference.added, difference.removed, difference.changed)
    if check:
        raise RuntimeError(f"committed documentation reference is stale; {summary}")

    output_root.parent.mkdir(parents=True, exist_ok=True)
    backup = output_root.parent / f".reference-backup-{uuid.uuid4().hex}"
    if backup.exists():
        raise DocumentationGenerationError(f"unexpected generated-tree backup already exists: {backup}")
    moved_existing = False
    try:
        if output_root.exists():
            os.replace(output_root, backup)
            moved_existing = True
        os.replace(staging, output_root)
    except BaseException:
        if moved_existing and backup.exists() and not output_root.exists():
            os.replace(backup, output_root)
        raise
    if backup.exists():
        _remove_owned_tree(backup, owner=output_root.parent, prefix=".reference-backup-")
    print(f"updated committed documentation reference; {summary}")
    return True


def _format_reference_diff(added: Sequence[str], removed: Sequence[str], changed: Sequence[str]) -> str:
    """Render a concise deterministic generated-tree difference.

    Args:
        added: Expected files absent from the committed tree.
        removed: Committed files absent from the generated tree.
        changed: Shared files with different bytes.

    Returns:
        Semicolon-separated non-empty change groups.
    """
    groups = []
    for label, paths in (("added", added), ("removed", removed), ("changed", changed)):
        if paths:
            groups.append(f"{label}: {', '.join(paths)}")
    return "; ".join(groups) or "no changes"


def _remove_owned_tree(path: Path, *, owner: Path, prefix: str) -> None:
    """Remove one verified task-owned temporary directory.

    Args:
        path: Candidate temporary directory to remove recursively.
        owner: Exact parent directory that contains owned temporary children.
        prefix: Required basename prefix distinguishing task-owned paths.

    Raises:
        DocumentationGenerationError: The path is outside its owner or lacks the expected prefix.
    """
    path = path.resolve()
    owner = owner.resolve()
    if path.parent != owner or not path.name.startswith(prefix):
        raise DocumentationGenerationError(f"refusing to remove non-owned path: {path}")
    shutil.rmtree(path)


def _source_hashes(configuration: DocumentationConfiguration) -> dict[str, str]:
    """Hash every maintained generator input that can affect normalized references.

    Args:
        configuration: Validated documentation surface and repository paths.

    Returns:
        Repository-relative POSIX paths mapped to lowercase SHA-256 digests.

    Raises:
        DocumentationGenerationError: A configured maintained source input is missing or is not a file.
    """
    root = configuration.repository_root
    files: set[Path] = {
        root / "docs/reference-surface.toml",
        configuration.telegram.schema_path,
        configuration.telegram.metadata_path,
        configuration.telegram.rpc_errors_path,
        configuration.telegram.bindings_path,
        configuration.rust.toolchain_path,
    }
    files.update(path for path in (root / "tools/docs").glob("*.py") if path.is_file())
    files.update(
        path
        for path in (root / "src/miniproto").rglob("*.py")
        if path.is_file()
        and not any(path.resolve().is_relative_to(excluded) for excluded in configuration.python.excluded_roots)
        and path.name != "fast_metadata.py"
    )
    files.update(
        path
        for path in (root / "rust/miniproto/src").glob("*.rs")
        if path.is_file() and path.relative_to(root).as_posix() not in configuration.rust.excluded_paths
    )
    missing = [path for path in sorted(files, key=lambda item: item.as_posix()) if not path.is_file()]
    if missing:
        joined = ", ".join(path.relative_to(root).as_posix() for path in missing)
        raise DocumentationGenerationError(f"documentation source inputs are missing: {joined}")
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(files, key=lambda item: item.as_posix())
    }


def _tool_versions(configuration: DocumentationConfiguration, *, rust_toolchain: Any) -> dict[str, str]:
    """Collect exact extractor versions recorded in the committed reference manifest.

    Args:
        configuration: Validated pipeline configuration retained for future version sources.
        rust_toolchain: Loaded exact Rust documentation pin.

    Returns:
        Stable tool-name to exact-version mapping.
    """
    del configuration
    return {
        "cargo-docs-md": str(rust_toolchain.cargo_docs_md),
        "griffe": importlib.metadata.version("griffe"),
        "griffe2md": importlib.metadata.version("griffe2md"),
        "miniproto-docs": _GENERATOR_VERSION,
        "rustdoc": str(rust_toolchain.nightly),
    }


def _audit_python_sources(configuration: DocumentationConfiguration) -> None:
    """Enforce complete maintained Python and tooling docstrings before generation.

    Args:
        configuration: Validated roots and exclusions for the documentation pipeline.

    Raises:
        DocumentationGenerationError: A module, declaration, or explicit argument lacks meaningful prose.
    """
    from tools.docs.audit import find_missing_python_docs, find_missing_python_parameter_docs

    roots = (configuration.repository_root / "src/miniproto", configuration.repository_root / "tools")
    missing_docs = find_missing_python_docs(roots, excluded_roots=configuration.python.excluded_roots)
    missing_parameters = find_missing_python_parameter_docs(roots, excluded_roots=configuration.python.excluded_roots)
    if not missing_docs and not missing_parameters:
        return
    details = [f"{item.path}:{item.line} {item.qualified_name}" for item in missing_docs]
    details.extend(
        f"{item.path}:{item.line} {item.qualified_name} ({', '.join(item.arguments)})" for item in missing_parameters
    )
    raise DocumentationGenerationError("maintained Python documentation is incomplete:\n" + "\n".join(details))


def _generate_reference_tree(configuration: DocumentationConfiguration, *, staging: Path, scratch: Path) -> None:
    """Run all static extractors and write one validated combined staging tree.

    Args:
        configuration: Complete reviewed extraction and output contract.
        staging: Empty task-owned reference tree destination.
        scratch: Task-owned transient Rust artifact directory.

    Raises:
        DocumentationGenerationError: A required docs dependency, source, tool, or extraction stage is unavailable.
    """
    try:
        from tools.docs.audit import audit_maintained_rust_docs
        from tools.docs.generate_python import generate_python_pages
        from tools.docs.generate_rust import (
            generate_pinned_rustdoc_json,
            generate_rust_pages,
            load_cargo_docs_md_fragments,
            load_documentation_toolchain,
            render_rustdoc_with_cargo_docs_md,
        )
        from tools.docs.generate_telegram import generate_telegram_reference_surface, load_telegram_binding_manifest
        from tools.docs.manifest import write_reference_tree
    except ModuleNotFoundError as error:
        raise DocumentationGenerationError(
            "documentation extraction dependencies are missing; install the pinned docs dependency group"
        ) from error

    _audit_python_sources(configuration)
    python_pages = generate_python_pages(
        source_root=configuration.python.source_root,
        module_names=configuration.python.module_names,
        repository_url=configuration.repository_url,
        dynamic_all_modules=configuration.python.dynamic_all_modules,
    )
    telegram_surface = generate_telegram_reference_surface(
        schema_path=configuration.telegram.schema_path,
        metadata_path=configuration.telegram.metadata_path,
        rpc_errors_path=configuration.telegram.rpc_errors_path,
        binding_manifest=load_telegram_binding_manifest(configuration.telegram.bindings_path),
        repository_url=configuration.repository_url,
    )
    if telegram_surface.relationship_manifest_path != configuration.telegram.relationships_path:
        raise DocumentationGenerationError(
            "Telegram relationship artifact path disagrees with the reviewed reference-surface configuration"
        )

    rust_toolchain = load_documentation_toolchain(configuration.rust.toolchain_path)
    rust_target = scratch / "rustdoc-target"
    rustdoc_json = generate_pinned_rustdoc_json(
        toolchain=rust_toolchain,
        manifest_path=configuration.rust.manifest_path,
        target_dir=rust_target,
        artifact_stem=configuration.rust.artifact_stem,
    )
    rust_source_directory = configuration.rust.manifest_path.parent / "src"
    maintained_rust_paths = tuple(
        path.relative_to(configuration.rust.source_root).as_posix()
        for path in sorted(rust_source_directory.rglob("*.rs"), key=lambda candidate: candidate.as_posix())
        if path.relative_to(configuration.rust.source_root).as_posix() not in configuration.rust.excluded_paths
    )
    rust_audit = audit_maintained_rust_docs(
        rustdoc_json,
        source_root=configuration.rust.source_root,
        maintained_paths=maintained_rust_paths,
        excluded_paths=configuration.rust.excluded_paths,
    )
    if rust_audit.missing_docs or rust_audit.missing_parameter_docs:
        details = [f"{item.path}:{item.line} {item.qualified_name}" for item in rust_audit.missing_docs]
        details.extend(
            f"{item.path}:{item.line} {item.qualified_name} ({', '.join(item.arguments)})"
            for item in rust_audit.missing_parameter_docs
        )
        raise DocumentationGenerationError("maintained Rust documentation is incomplete:\n" + "\n".join(details))
    print(
        "maintained Rust documentation is complete "
        f"({rust_audit.documentation_unit_count} units, "
        f"{rust_audit.value_parameter_count + rust_audit.generic_parameter_count} explicit parameters)"
    )
    converter_output = scratch / "cargo-docs-md"
    render_rustdoc_with_cargo_docs_md(
        toolchain=rust_toolchain,
        json_directory=rustdoc_json.parent,
        output_directory=converter_output,
        crate=configuration.rust.crate,
    )
    rust_pages = generate_rust_pages(
        rustdoc_json=rustdoc_json,
        source_root=configuration.rust.source_root,
        rendered_markdown=load_cargo_docs_md_fragments(
            rustdoc_json=rustdoc_json, output_directory=converter_output, crate=configuration.rust.crate
        ),
        repository_url=configuration.repository_url,
        crate=configuration.rust.crate,
        reviewed_modules=configuration.rust.reviewed_modules,
        excluded_paths=configuration.rust.excluded_paths,
    )
    source_hashes = _source_hashes(configuration)
    write_reference_tree(
        staging,
        (*python_pages, *telegram_surface.pages, *rust_pages),
        tool_versions=_tool_versions(configuration, rust_toolchain=rust_toolchain),
        source_hashes=source_hashes,
        artifacts={configuration.telegram.relationships_path: telegram_surface.relationship_manifest},
    )


def _run_reference_pipeline(configuration: DocumentationConfiguration, *, check: bool) -> None:
    """Generate references in isolation and compare or reconcile the committed tree.

    Args:
        configuration: Validated documentation extraction contract.
        check: Whether committed byte drift must fail without replacement.
    """
    scratch_parent = configuration.repository_root / ".tmp/docs-reference"
    scratch_parent.mkdir(parents=True, exist_ok=True)
    scratch = scratch_parent / f"run-{uuid.uuid4().hex}"
    staging = scratch / "reference"
    scratch.mkdir()
    try:
        _generate_reference_tree(configuration, staging=staging, scratch=scratch)
        changed = _reconcile_reference_tree(
            staging=staging,
            output_root=configuration.output_root,
            repository_root=configuration.repository_root,
            check=check,
        )
        if check and not changed:
            print("committed documentation reference is fresh")
    finally:
        if scratch.exists():
            _remove_owned_tree(scratch, owner=scratch_parent, prefix="run-")


def _resolve_site_command(command: Sequence[str]) -> tuple[str, ...]:
    """Resolve a configured site command to a directly executable process vector.

    Args:
        command: Reviewed executable name and arguments from the documentation configuration.

    Returns:
        The command with its executable replaced by the platform-resolved absolute path.

    Raises:
        DocumentationGenerationError: The command is empty or its executable is unavailable on ``PATH``.
    """
    if not command:
        raise DocumentationGenerationError("documentation site command is empty")
    executable = shutil.which(command[0])
    if executable is None:
        raise DocumentationGenerationError(f"documentation site executable is unavailable: {command[0]}")
    return (executable, *command[1:])


def _verify_site_tool_versions(configuration: SiteDocumentationConfiguration) -> None:
    """Require the exact Node and pnpm versions declared by the site package.

    Args:
        configuration: Site directory and expected package-manager executable.

    Raises:
        DocumentationGenerationError: Package metadata is malformed or either executable reports a different version.
    """
    package = json.loads((configuration.directory / "package.json").read_text(encoding="utf-8"))
    engines = package.get("engines")
    if not isinstance(engines, Mapping):
        raise DocumentationGenerationError("docs-site/package.json lacks exact engine pins")
    expected_node = str(engines.get("node") or "")
    expected_package_manager = str(engines.get(configuration.package_manager) or "")
    checks = (
        ("node", ("node", "--version"), expected_node),
        (configuration.package_manager, (configuration.package_manager, "--version"), expected_package_manager),
    )
    for label, command, expected in checks:
        resolved_command = _resolve_site_command(command)
        result = subprocess.run(  # noqa: S603 - executable names are fixed by reviewed repository configuration.
            resolved_command, cwd=configuration.directory, capture_output=True, check=False, text=True
        )
        actual = result.stdout.strip().removeprefix("v")
        if result.returncode or not expected or actual != expected:
            raise DocumentationGenerationError(
                f"{label} must be exactly {expected or '<missing pin>'}, reported {actual or '<unavailable>'}"
            )


def _normalize_site_base(value: str) -> str:
    """Normalize a configured deployment path for local artifact validation.

    Args:
        value: Root or project-path deployment prefix.

    Returns:
        A leading-slash path with no trailing slash, except for the root value itself.
    """
    stripped = value.strip().strip("/")
    return "/" if not stripped else f"/{stripped}"


def _route_destination(output: Path, route: str) -> Path:
    """Map one base-free public route to its expected file in a static artifact.

    Args:
        output: Static-site output directory.
        route: Decoded absolute route after removal of the configured deployment base.

    Returns:
        Expected HTML or asset path beneath ``output``.
    """
    relative = route.lstrip("/")
    if not relative:
        return output / "index.html"
    candidate = output / Path(relative)
    if route.endswith("/") or not candidate.suffix:
        return candidate / "index.html"
    return candidate


def _local_route(reference: str, *, source_route: str, base: str) -> str | None:
    """Resolve one rendered local reference to a decoded base-free route.

    Args:
        reference: Raw ``href`` or ``src`` value from rendered HTML.
        source_route: Base-prefixed public route of the containing HTML page.
        base: Normalized deployment base path.

    Returns:
        Base-free absolute route, or ``None`` for fragments and external protocols.

    Raises:
        RuntimeError: An absolute local path escapes a non-root deployment base.
    """
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None
    if not parsed.path:
        return None
    resolved = unquote(urljoin(source_route, parsed.path))
    if base != "/":
        if resolved == base:
            resolved = "/"
        elif resolved.startswith(f"{base}/"):
            resolved = resolved[len(base) :]
        else:
            raise RuntimeError(f"local reference escapes configured site base {base}: {reference}")
    return resolved or "/"


def _html_route(path: Path, *, output: Path, base: str) -> str:
    """Return the base-prefixed browser route for one rendered HTML file.

    Args:
        path: HTML file beneath the static output directory.
        output: Static-site output directory.
        base: Normalized deployment base path.

    Returns:
        Absolute browser path suitable for resolving relative links.
    """
    relative = path.relative_to(output).as_posix()
    if relative == "index.html":
        route = "/"
    elif relative.endswith("/index.html"):
        route = f"/{relative.removesuffix('index.html')}"
    else:
        route = f"/{relative}"
    if base == "/":
        return route
    return f"{base}/" if route == "/" else f"{base}{route}"


def _validate_static_site(output: Path, *, base: str, required_routes: Sequence[str]) -> StaticSiteValidationReport:
    """Validate routes, local references, search metadata, and internal-content boundaries in a built site.

    Args:
        output: Static Astro output directory to inspect without modification.
        base: Configured public deployment prefix such as ``/miniproto`` or ``/``.
        required_routes: Base-free public routes that must exist in the artifact.

    Returns:
        Counts and Pagefind filter names from the validated artifact.

    Raises:
        RuntimeError: The artifact is incomplete, leaks the internal scratchpad, loses its design contract, or contains a broken local reference.
    """
    output = output.resolve()
    normalized_base = _normalize_site_base(base)
    if not output.is_dir():
        raise RuntimeError(f"documentation static output does not exist: {output}")
    html_paths = tuple(sorted(output.rglob("*.html"), key=lambda path: path.as_posix()))
    if not html_paths:
        raise RuntimeError("documentation static output contains no HTML pages")
    if not (output / "pagefind/pagefind.js").is_file():
        raise RuntimeError("documentation static output lacks the Pagefind browser bundle")
    for route in required_routes:
        destination = _route_destination(output, route)
        if not destination.is_file():
            raise RuntimeError(f"documentation static output lacks required route {route}: {destination}")

    filters: set[str] = set()
    internal_links = 0
    homepage_contract = False
    has_pagefind_body = False
    for path in html_paths:
        relative_path = path.relative_to(output).as_posix()
        if "thoughts" in relative_path.casefold():
            raise RuntimeError(f"THOUGHTS scratchpad leaked into the public artifact: {relative_path}")
        parser = _BuiltPageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        filters.update(parser.filter_names)
        has_pagefind_body = has_pagefind_body or parser.has_pagefind_body
        if relative_path == "index.html":
            homepage_contract = parser.has_surface_contract
        source_route = _html_route(path, output=output, base=normalized_base)
        for reference in parser.local_references:
            if "thoughts" in reference.casefold():
                raise RuntimeError(f"THOUGHTS scratchpad leaked through a public reference: {reference}")
            route = _local_route(reference, source_route=source_route, base=normalized_base)
            if route is None:
                continue
            internal_links += 1
            destination = _route_destination(output, route)
            if not destination.is_file():
                raise RuntimeError(f"broken local reference in {relative_path}: {reference} -> {destination}")

    if not homepage_contract:
        raise RuntimeError(f"homepage lacks the {_SURFACE_CONTRACT_MARKER!r} design contract")
    if not has_pagefind_body:
        raise RuntimeError("documentation static output lacks any data-pagefind-body content region")
    return StaticSiteValidationReport(
        html_pages=len(html_paths), internal_links=internal_links, filter_names=tuple(sorted(filters))
    )


def _run_site_pipeline(configuration: SiteDocumentationConfiguration, *, skip_install: bool) -> None:
    """Install, check, and build the pinned Astro/Starlight static site.

    Args:
        configuration: Exact site directory and command vectors.
        skip_install: Whether an existing frozen dependency installation may be reused.

    Raises:
        DocumentationGenerationError: An exact tool version or configured frontend stage fails.
    """
    _verify_site_tool_versions(configuration)
    commands = (configuration.check_command, configuration.build_command, configuration.test_command)
    if not skip_install:
        commands = (configuration.install_command, *commands)
    for command in commands:
        resolved_command = _resolve_site_command(command)
        result = subprocess.run(  # noqa: S603 - command vectors are fixed by reviewed repository configuration.
            resolved_command, cwd=configuration.directory, check=False
        )
        if result.returncode:
            raise DocumentationGenerationError(
                f"documentation site command failed ({result.returncode}): {' '.join(command)}"
            )
    report = _validate_static_site(
        configuration.directory / "dist",
        base=os.environ.get("MINIPROTO_DOCS_BASE", "/"),
        required_routes=_REQUIRED_SITE_ROUTES,
    )
    missing_filters = sorted(_REQUIRED_PAGEFIND_FILTERS.difference(report.filter_names))
    if missing_filters:
        raise RuntimeError(
            f"documentation Pagefind index metadata lacks required filters: {', '.join(missing_filters)}"
        )
    print(
        "documentation static artifact is valid "
        f"({report.html_pages} HTML pages, {report.internal_links} local references, "
        f"{len(report.filter_names)} Pagefind filters)"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run committed-reference generation/checking and the pinned static-site pipeline.

    Args:
        argv: Optional command-line arguments excluding the executable name.

    Returns:
        Zero when every selected stage succeeds; command-line failures return a concise non-zero status.
    """
    arguments = _parse_arguments(argv)
    configuration_path = arguments.config
    if not configuration_path.is_absolute():
        configuration_path = _REPOSITORY_ROOT / configuration_path
    try:
        configuration = load_documentation_configuration(configuration_path, repository_root=_REPOSITORY_ROOT)
        if not arguments.site_only:
            _run_reference_pipeline(configuration, check=arguments.check)
        if arguments.build or arguments.site_only:
            _run_site_pipeline(configuration.site, skip_install=arguments.skip_install)
    except (DocumentationConfigurationError, DocumentationGenerationError, RuntimeError) as error:
        print(f"documentation pipeline failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "DocumentationConfiguration",
    "DocumentationConfigurationError",
    "DocumentationGenerationError",
    "PythonDocumentationConfiguration",
    "RustDocumentationConfiguration",
    "SiteDocumentationConfiguration",
    "TelegramDocumentationConfiguration",
    "load_documentation_configuration",
    "main",
]
