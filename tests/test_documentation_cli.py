"""Contracts for the unified documentation generator and site command."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from tools.docs.__main__ import (
    DocumentationConfigurationError,
    SiteDocumentationConfiguration,
    _parse_arguments,
    _reconcile_reference_tree,
    _run_site_pipeline,
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


def test_docs_help_is_available_without_optional_documentation_dependencies() -> None:
    """The installed help path must not require Griffe or another documentation extra."""
    result = subprocess.run(
        (
            sys.executable,
            "-S",
            "-c",
            "import sys; sys.argv = ['miniproto-docs', '--help']; from tools.docs.__main__ import main; raise SystemExit(main())",
        ),
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout
    assert "miniproto-docs" in result.stdout


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


def test_static_site_validator_accepts_a_portable_filtered_page_set(tmp_path: Path) -> None:
    """The docs pipeline must accept a complete base-prefixed site with search filters and valid internal links."""
    from tools.docs import __main__ as documentation_cli

    validate = getattr(documentation_cli, "_validate_static_site", None)
    assert callable(validate), "the documentation CLI must validate the built static artifact"

    output = tmp_path / "dist"
    (output / "start").mkdir(parents=True)
    (output / "pagefind").mkdir()
    (output / "assets").mkdir()
    (output / "index.html").write_text(
        """<!doctype html>
<html><body>
<!-- miniproto-surface:user-pinned-packet-loom -->
<main data-pagefind-body>
<img src="/miniproto/assets/mark.svg" alt="Packet Loom mark">
<a href="/miniproto/start/">Start</a>
<a href="./start/">Relative start</a>
</main>
</body></html>
""",
        encoding="utf-8",
    )
    (output / "start/index.html").write_text(
        """<!doctype html>
<html><head>
<meta data-pagefind-filter="language[content]" content="python">
<meta data-pagefind-filter="kind[content]" content="function">
</head><body><main data-pagefind-body><a href="../">Home</a></main></body></html>
""",
        encoding="utf-8",
    )
    (output / "assets/mark.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>\n', encoding="utf-8")
    (output / "pagefind/pagefind.js").write_text("export {};\n", encoding="utf-8")

    report = validate(output, base="/miniproto", required_routes=("/", "/start/"))

    assert report.html_pages == 2
    assert report.internal_links == 4
    assert report.filter_names == ("kind", "language")


def test_static_site_validator_rejects_a_leaked_internal_scratchpad(tmp_path: Path) -> None:
    """A rendered route or link to THOUGHTS.md must make the static artifact invalid."""
    from tools.docs import __main__ as documentation_cli

    validate = getattr(documentation_cli, "_validate_static_site", None)
    assert callable(validate), "the documentation CLI must validate the built static artifact"

    output = tmp_path / "dist"
    (output / "pagefind").mkdir(parents=True)
    (output / "index.html").write_text(
        """<!doctype html><html><body>
<!-- miniproto-surface:user-pinned-packet-loom -->
<main data-pagefind-body><a href="/thoughts/">Internal notes</a></main>
</body></html>""",
        encoding="utf-8",
    )
    (output / "pagefind/pagefind.js").write_text("export {};\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="THOUGHTS"):
        validate(output, base="/", required_routes=("/",))


def test_site_pipeline_validates_the_artifact_after_frontend_commands(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A successful pnpm exit must not let a missing or malformed static artifact pass the unified docs command."""
    from tools.docs import __main__ as documentation_cli

    site = tmp_path / "docs-site"
    site.mkdir()
    calls: list[tuple[str, ...]] = []
    configuration = SiteDocumentationConfiguration(
        directory=site,
        package_manager="pnpm",
        install_command=("pnpm", "install"),
        check_command=("pnpm", "check"),
        build_command=("pnpm", "build"),
        test_command=("pnpm", "test:site"),
    )
    monkeypatch.setattr(documentation_cli, "_resolve_site_command", lambda command: tuple(command))
    monkeypatch.setattr(
        documentation_cli.subprocess,
        "run",
        lambda command, **_kwargs: calls.append(tuple(command)) or SimpleNamespace(returncode=0),
    )

    with pytest.raises(RuntimeError, match="static output"):
        _run_site_pipeline(configuration, skip_install=False)

    assert calls == [("pnpm", "install"), ("pnpm", "check"), ("pnpm", "build"), ("pnpm", "test:site")]


def test_site_command_resolution_uses_the_platform_executable_shim(monkeypatch: pytest.MonkeyPatch) -> None:
    """The Python orchestrator must launch a Windows ``.CMD`` package-manager shim without relying on shell lookup."""
    from tools.docs import __main__ as documentation_cli

    resolve = getattr(documentation_cli, "_resolve_site_command", None)
    assert callable(resolve), "the documentation CLI must resolve package-manager launchers before subprocess execution"
    monkeypatch.setattr(documentation_cli.shutil, "which", lambda executable: f"C:/tools/{executable}.CMD")

    assert resolve(("pnpm", "run", "check")) == ("C:/tools/pnpm.CMD", "run", "check")


def test_site_command_resolution_rejects_an_unavailable_executable(monkeypatch: pytest.MonkeyPatch) -> None:
    """A missing site executable must become a concise documentation failure instead of leaking ``FileNotFoundError``."""
    from tools.docs import __main__ as documentation_cli

    resolve = getattr(documentation_cli, "_resolve_site_command", None)
    assert callable(resolve), "the documentation CLI must resolve package-manager launchers before subprocess execution"
    monkeypatch.setattr(documentation_cli.shutil, "which", lambda _executable: None)

    with pytest.raises(documentation_cli.DocumentationGenerationError, match="site executable is unavailable: pnpm"):
        resolve(("pnpm", "run", "check"))


def test_documentation_site_uses_typed_jiti_clis_with_help_and_progress_contracts() -> None:
    """Every maintained Node-side CLI must be typed, expose help and announce long-running work."""
    site = ROOT / "docs-site"
    maintained_mjs = [
        path.relative_to(site).as_posix()
        for path in site.rglob("*.mjs")
        if not {".astro", "dist", "node_modules", "playwright-report", "test-results"}.intersection(path.parts)
    ]

    assert maintained_mjs == []
    assert (site / "astro.config.ts").is_file()
    assert (site / "src/remark-local-markdown-links.ts").is_file()
    assert (site / "src/sidebar.ts").is_file()


def test_external_documentation_uses_base_safe_links_and_a_complete_handwritten_sidebar() -> None:
    """External Markdown content must not depend on trailing-slash redirects or Starlight autogeneration."""
    astro = (ROOT / "docs-site/astro.config.ts").read_text(encoding="utf-8")
    remark = (ROOT / "docs-site/src/remark-local-markdown-links.ts").read_text(encoding="utf-8")
    sidebar = (ROOT / "docs-site/src/sidebar.ts").read_text(encoding="utf-8")

    assert "buildDocumentationSidebar" in astro
    assert "autogenerate:" not in astro
    assert "{ docsRoot, base }" in astro
    assert "applyBase(targetRoute, base)" in remark
    for directory in ("start", "guides", "concepts", "recipes", "faq", "project", "codebase"):
        assert f'"{directory}"' in sidebar
    for root_page in ("media.md", "session-security.md", "raw-api.md", "development.md", "faked-methods.md"):
        assert f'"{root_page}"' in sidebar
    for route in (
        "/reference/",
        "/reference/python/miniproto/",
        "/reference/rust/miniproto-native/",
        "/reference/telegram/functions/",
        "/reference/telegram/types/",
        "/reference/telegram/errors/",
    ):
        assert route in sidebar
