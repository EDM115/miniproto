"""Validated, deterministic Markdown page model shared by all generators."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Literal

ReferenceLanguage = Literal["python", "telegram", "rust"]
_GENERATED_SOURCE_LOCATION = re.compile(
    r"^(?P<prefix>\s*\*Defined in `)(?P<path>[^`\r\n]+)(?P<suffix>`\*\s*)$", re.MULTILINE
)


def canonical_markdown_path(value: str) -> str:
    """Return a generated Markdown path with platform-independent POSIX separators.

    Args:
        value: Structural page path or repository-relative source path produced by a generator.

    Returns:
        The path with every Windows separator replaced by ``/``.
    """
    return value.replace("\\", "/")


def normalize_generated_markdown_paths(markdown: str) -> str:
    """Canonicalize generated source-location paths without rewriting prose or code examples.

    Args:
        markdown: Generated Markdown that may contain renderer-owned ``Defined in`` records.

    Returns:
        Markdown whose generated source-location records use POSIX separators.
    """
    return _GENERATED_SOURCE_LOCATION.sub(_normalize_source_location_match, markdown)


def _normalize_source_location_match(match: re.Match[str]) -> str:
    """Render one generated source-location match with a canonical path.

    Args:
        match: Regex match containing the source-location prefix, path and suffix.

    Returns:
        The reconstructed source-location record with POSIX separators.
    """
    return f"{match.group('prefix')}{canonical_markdown_path(match.group('path'))}{match.group('suffix')}"


@dataclass(frozen=True, slots=True)
class ReferencePage:
    """Represent one committed generated reference page and its provenance.

    Attributes:
        path: Markdown path relative to the committed reference root.
        title: Human-readable page heading.
        description: Concise search and frontmatter summary.
        language: Extractor family that generated the page.
        kind: Source-language declaration kind.
        qualified_name: Stable fully qualified source identity.
        source_path: Repository-relative provenance path.
        source_url: Line-aware browser URL for the source declaration.
        body: Generated Markdown body without frontmatter.
        module: Python module provenance when ``language`` is ``python``.
        namespace: Telegram namespace when ``language`` is ``telegram``.
        schema_source: Canonical Telegram structural source identifier.
        constructor_id: Telegram constructor or method identifier when present.
        python_visible: Whether a Rust declaration is exposed through PyO3.
        aliases: Additional names indexed for search and compatibility.
    """

    path: str
    title: str
    description: str
    language: ReferenceLanguage
    kind: str
    qualified_name: str
    source_path: str
    source_url: str
    body: str
    module: str | None = None
    namespace: str | None = None
    schema_source: str | None = None
    constructor_id: str | None = None
    python_visible: bool | None = None
    aliases: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate route safety, required text and language-specific provenance.

        Raises:
            ValueError: The route is unsafe, a required text field is absent or empty or language-specific provenance is incomplete.
        """
        object.__setattr__(self, "path", canonical_markdown_path(self.path))
        object.__setattr__(self, "source_path", canonical_markdown_path(self.source_path))
        object.__setattr__(self, "body", normalize_generated_markdown_paths(self.body))
        page_path = PurePosixPath(self.path)
        if page_path.is_absolute() or ".." in page_path.parts or page_path.suffix != ".md":
            raise ValueError(f"reference page path must be a relative Markdown path: {self.path!r}")
        for field_name in ("title", "description", "kind", "qualified_name", "source_path", "source_url"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must not be empty")
        if self.language == "python" and not self.module:
            raise ValueError("Python reference pages require module provenance")
        if self.language == "telegram" and not self.schema_source:
            raise ValueError("Telegram reference pages require schema_source provenance")

    @property
    def route(self) -> str:
        """Return the stable Starlight route for this reference page."""
        page_path = PurePosixPath(self.path)
        route_path = page_path.parent if page_path.name == "index.md" else page_path.with_suffix("")
        route = "/".join(route_path.parts)
        return f"/reference/{route}/" if route else "/reference/"

    def render(self) -> str:
        """Render deterministic YAML-compatible frontmatter and Markdown body."""
        frontmatter: list[tuple[str, object]] = [
            ("title", self.title),
            ("description", self.description),
            ("generated", True),
            ("editUrl", False),
            ("language", self.language),
            ("kind", self.kind),
            ("qualified_name", self.qualified_name),
            ("source_path", self.source_path),
            ("source_url", self.source_url),
        ]
        if self.aliases:
            frontmatter.append(("aliases", list(self.aliases)))
        for name in ("module", "namespace", "schema_source", "constructor_id", "python_visible"):
            value = getattr(self, name)
            if value is not None:
                frontmatter.append((name, value))
        header = "\n".join(f"{name}: {_yaml_scalar(value)}" for name, value in frontmatter)
        body = self.body.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
        return f"---\n{header}\n---\n\n{body}"


def _yaml_scalar(value: object) -> str:
    """Render a JSON scalar or sequence, which is valid YAML frontmatter.

    Args:
        value: JSON-compatible scalar, mapping or sequence to encode; booleans and integers use an explicit compact representation.

    Returns:
        Deterministic YAML-compatible scalar text.

    Raises:
        TypeError: ``value`` is not JSON serializable.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(value, ensure_ascii=False, separators=(",", ": "))


__all__ = ["ReferenceLanguage", "ReferencePage"]
