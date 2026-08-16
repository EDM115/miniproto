"""Contracts for the unified documentation generator and site command."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from tools.docs.__main__ import (
    DocumentationConfigurationError,
    _parse_arguments,
    _reconcile_reference_tree,
    load_documentation_configuration,
)

ROOT = Path(__file__).parents[1]


def test_checked_in_reference_surface_is_explicit_and_complete() -> None:
    """The public reference surface must remain a reviewed compatibility declaration."""
    configuration = load_documentation_configuration(ROOT / "docs/reference-surface.toml", repository_root=ROOT)

    assert configuration.schema_version == 1
    assert configuration.output_root == ROOT / "docs/reference"
    assert len(configuration.python.module_names) == 32
    assert configuration.python.module_names[0] == "miniproto"
    assert configuration.python.module_names[-1] == "miniproto.updates"
    assert configuration.python.dynamic_all_modules == ("miniproto.errors",)
    assert configuration.telegram.bindings_path == ROOT / "tools/schema/telegram-bindings.json"
    assert configuration.telegram.relationships_path == "telegram/relationships.json"
    assert configuration.rust.reviewed_modules == ("crypto", "mtproto", "tl", "transport")
    assert configuration.site.install_command == ("pnpm", "install", "--frozen-lockfile")


def test_reference_surface_rejects_paths_outside_the_repository(tmp_path: Path) -> None:
    """Configuration must not authorize generated writes outside the selected checkout."""
    configuration = tmp_path / "surface.toml"
    configuration.write_text(
        'schema_version = 1\nrepository_url = "https://example.invalid/repository"\noutput_root = "../outside"\n',
        encoding="utf-8",
    )

    with pytest.raises(DocumentationConfigurationError, match="output_root"):
        load_documentation_configuration(configuration, repository_root=tmp_path)


def test_docs_help_parses_before_generation_or_frontend_work() -> None:
    """The installed command help path must remain side-effect free."""
    with pytest.raises(SystemExit) as exit_info:
        _parse_arguments(["--help"])

    assert exit_info.value.code == 0


def test_reference_reconciliation_replaces_only_the_owned_tree(tmp_path: Path) -> None:
    """Generation may replace the exact reference tree without touching handwritten siblings."""
    docs = tmp_path / "docs"
    committed = docs / "reference"
    staging = tmp_path / ".tmp/docs-reference/staging/reference"
    docs.mkdir()
    (docs / "handwritten.md").write_text("keep\n", encoding="utf-8")
    committed.mkdir()
    (committed / "old.md").write_text("old\n", encoding="utf-8")
    staging.mkdir(parents=True)
    (staging / "manifest.json").write_text(json.dumps({"new": True}) + "\n", encoding="utf-8")

    changed = _reconcile_reference_tree(staging=staging, output_root=committed, repository_root=tmp_path, check=False)

    assert changed
    assert not (committed / "old.md").exists()
    assert json.loads((committed / "manifest.json").read_text(encoding="utf-8")) == {"new": True}
    assert (docs / "handwritten.md").read_text(encoding="utf-8") == "keep\n"


def test_reference_check_reports_drift_without_mutating_committed_bytes(tmp_path: Path) -> None:
    """The check mode must fail on exact-byte drift and leave both trees untouched."""
    committed = tmp_path / "docs/reference"
    staging = tmp_path / ".tmp/docs-reference/staging/reference"
    committed.mkdir(parents=True)
    staging.mkdir(parents=True)
    (committed / "page.md").write_text("committed\n", encoding="utf-8")
    (staging / "page.md").write_text("expected\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match=r"changed: page\.md"):
        _reconcile_reference_tree(staging=staging, output_root=committed, repository_root=tmp_path, check=True)

    assert (committed / "page.md").read_text(encoding="utf-8") == "committed\n"
    assert (staging / "page.md").read_text(encoding="utf-8") == "expected\n"
