"""Build deterministic reference manifests and compare generated trees."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from tools.docs.model import ReferencePage

MANIFEST_NAME = "manifest.json"
MANIFEST_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class ReferenceTreeDiff:
    """Describe added, removed and byte-changed generated files.

    Attributes:
        added: Files present in the expected tree but absent from the actual tree.
        removed: Files present in the actual tree but absent from the expected tree.
        changed: Shared paths whose bytes differ.
    """

    added: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()
    changed: tuple[str, ...] = ()

    @property
    def is_clean(self) -> bool:
        """Return whether two reference trees contain identical files and bytes."""
        return not (self.added or self.removed or self.changed)


def build_reference_manifest(
    pages: Iterable[ReferencePage],
    *,
    source_hashes: Mapping[str, str],
    artifacts: Mapping[str, str | bytes] | None = None,
) -> str:
    """Render the deterministic manifest for a complete reference page set.

    Args:
        pages: Generated pages from every language extractor.
        source_hashes: SHA-256 values for immutable generator inputs.
        artifacts: Additional generated non-Markdown artifacts keyed by reference-relative path.

    Returns:
        UTF-8 JSON text with stable ordering and a final newline.

    Raises:
        ValueError: Pages collide by path, route or language/kind/qualified-name identity.
    """
    ordered_pages = _validated_pages(pages)
    normalized_artifacts = _validated_artifacts(artifacts or {}, page_paths={page.path for page in ordered_pages})
    manifest_pages = []
    for page in ordered_pages:
        rendered = page.render().encode("utf-8")
        manifest_pages.append(
            {
                "kind": page.kind,
                "language": page.language,
                "path": page.path,
                "qualified_name": page.qualified_name,
                "route": page.route,
                "sha256": hashlib.sha256(rendered).hexdigest(),
                "source_path": page.source_path,
            }
        )
    payload = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "sources": dict(sorted(source_hashes.items())),
        "artifacts": [
            {"path": path, "sha256": hashlib.sha256(content).hexdigest()}
            for path, content in normalized_artifacts.items()
        ],
        "pages": manifest_pages,
        "page_counts": {
            language: sum(page.language == language for page in ordered_pages)
            for language in ("python", "telegram", "rust")
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_reference_tree(
    output: Path,
    pages: Iterable[ReferencePage],
    *,
    source_hashes: Mapping[str, str],
    artifacts: Mapping[str, str | bytes] | None = None,
) -> None:
    """Write a complete generated reference tree into an empty staging directory.

    Args:
        output: Task-owned empty or absent staging directory.
        pages: Complete validated generated page collection.
        source_hashes: Hashes for generator inputs.
        artifacts: Additional generated non-Markdown artifacts keyed by reference-relative path.

    Raises:
        FileExistsError: The staging directory already contains data.
    """
    ordered_pages = _validated_pages(pages)
    normalized_artifacts = _validated_artifacts(artifacts or {}, page_paths={page.path for page in ordered_pages})
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"reference staging directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    for page in ordered_pages:
        destination = output / Path(page.path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(page.render().encode("utf-8"))
    for relative_path, content in normalized_artifacts.items():
        destination = output / Path(relative_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    manifest = build_reference_manifest(ordered_pages, source_hashes=source_hashes, artifacts=normalized_artifacts)
    (output / MANIFEST_NAME).write_bytes(manifest.encode("utf-8"))


def compare_reference_trees(expected: Path, actual: Path) -> ReferenceTreeDiff:
    """Compare relative file sets and exact bytes for two reference trees.

    Args:
        expected: Newly generated staging tree.
        actual: Committed reference tree to validate.

    Returns:
        Deterministically ordered file-set and byte differences.
    """
    expected_files = _tree_files(expected)
    actual_files = _tree_files(actual)
    expected_paths = set(expected_files)
    actual_paths = set(actual_files)
    shared = expected_paths & actual_paths
    return ReferenceTreeDiff(
        added=tuple(sorted(expected_paths - actual_paths)),
        removed=tuple(sorted(actual_paths - expected_paths)),
        changed=tuple(sorted(path for path in shared if expected_files[path] != actual_files[path])),
    )


def _validated_pages(pages: Iterable[ReferencePage]) -> tuple[ReferencePage, ...]:
    """Return deterministically ordered pages after collision validation.

    Args:
        pages: Complete candidate page collection.

    Returns:
        Pages sorted by relative Markdown path.

    Raises:
        ValueError: Two pages collide by path, route or source identity.
    """
    ordered = tuple(sorted(pages, key=lambda page: page.path))
    seen_paths: set[str] = set()
    seen_routes: set[str] = set()
    seen_identities: set[tuple[str, str, str]] = set()
    for page in ordered:
        if page.path in seen_paths:
            raise ValueError(f"duplicate reference path: {page.path}")
        if page.route in seen_routes:
            raise ValueError(f"duplicate reference route: {page.route}")
        identity = (page.language, page.kind, page.qualified_name)
        if identity in seen_identities:
            raise ValueError(f"duplicate reference identity: {identity!r}")
        seen_paths.add(page.path)
        seen_routes.add(page.route)
        seen_identities.add(identity)
    return ordered


def _validated_artifacts(artifacts: Mapping[str, str | bytes], *, page_paths: set[str]) -> dict[str, bytes]:
    """Validate, normalize and encode additional generated reference artifacts.

    Args:
        artifacts: Candidate non-Markdown artifacts keyed by reference-relative path.
        page_paths: Markdown page paths already reserved by the generated page set.

    Returns:
        Lexicographically ordered POSIX paths mapped to exact bytes.

    Raises:
        ValueError: An artifact path is unsafe, collides with a page or manifest or has an unsupported value.
    """
    normalized: dict[str, bytes] = {}
    for raw_path, raw_content in sorted(artifacts.items()):
        path = PurePosixPath(raw_path.replace("\\", "/"))
        relative_path = path.as_posix()
        if path.is_absolute() or not path.parts or ".." in path.parts:
            raise ValueError(f"reference artifact path must be relative and traversal-free: {raw_path!r}")
        if relative_path == MANIFEST_NAME or relative_path in page_paths:
            raise ValueError(f"reference artifact collides with a generated file: {relative_path}")
        if not isinstance(raw_content, str | bytes):
            raise ValueError(f"reference artifact must be text or bytes: {relative_path}")
        normalized[relative_path] = raw_content.encode("utf-8") if isinstance(raw_content, str) else raw_content
    return normalized


def _tree_files(root: Path) -> dict[str, bytes]:
    """Return relative POSIX paths and bytes for all files under a tree.

    Args:
        root: Tree whose regular files are read recursively.

    Returns:
        Mapping from relative POSIX path to exact file bytes.
    """
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"), key=lambda candidate: candidate.as_posix())
        if path.is_file()
    }


__all__ = [
    "MANIFEST_NAME",
    "ReferenceTreeDiff",
    "build_reference_manifest",
    "compare_reference_trees",
    "write_reference_tree",
]
