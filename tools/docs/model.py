"""Validated, deterministic Markdown page model shared by all generators."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Literal

ReferenceLanguage = Literal["python", "telegram", "rust"]


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
        layer: Telegram API layer when ``language`` is ``telegram``.
        schema_source: Canonical Telegram structural source identifier.
        constructor_id: Telegram constructor or method identifier when present.
        crate: Cargo crate provenance when ``language`` is ``rust``.
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
    layer: int | None = None
    schema_source: str | None = None
    constructor_id: str | None = None
    crate: str | None = None
    python_visible: bool | None = None
    aliases: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate route safety, required text, and language-specific provenance.

        Raises:
            ValueError: The route is unsafe, a required text field is absent or empty, or language-specific provenance is incomplete.
        """
        page_path = PurePosixPath(self.path)
        if page_path.is_absolute() or ".." in page_path.parts or page_path.suffix != ".md":
            raise ValueError(f"reference page path must be a relative Markdown path: {self.path!r}")
        for field_name in ("title", "description", "kind", "qualified_name", "source_path", "source_url"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must not be empty")
        if self.language == "python" and not self.module:
            raise ValueError("Python reference pages require module provenance")
        if self.language == "telegram":
            if self.layer is None:
                raise ValueError("Telegram reference pages require a layer")
            if not self.schema_source:
                raise ValueError("Telegram reference pages require schema_source provenance")
        if self.language == "rust" and not self.crate:
            raise ValueError("Rust reference pages require crate provenance")

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
        for name in ("module", "namespace", "layer", "schema_source", "constructor_id", "crate", "python_visible"):
            value = getattr(self, name)
            if value is not None:
                frontmatter.append((name, value))
        header = "\n".join(f"{name}: {_yaml_scalar(value)}" for name, value in frontmatter)
        body = self.body.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
        return f"---\n{header}\n---\n\n{body}"


def _yaml_scalar(value: object) -> str:
    """Render a JSON scalar or sequence, which is valid YAML frontmatter.

    Args:
        value: JSON-compatible scalar, mapping, or sequence to encode; booleans and integers use an explicit compact representation.

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
