"""Verify static canonical Python reference generation and alias indexing."""

from __future__ import annotations

from pathlib import Path

import pytest
from tools.docs.generate_python import generate_python_pages


def _write_alias_fixture(tmp_path: Path) -> Path:
    """Write a static package containing canonical objects and public re-exports.

    Args:
        tmp_path: Isolated directory in which to create the fixture package.

    Returns:
        Static import-search root containing the fixture package.
    """
    package = tmp_path / "fixture"
    package.mkdir()
    (package / "__init__.py").write_text(
        '"""Expose the reviewed fixture API."""\n\n'
        "from .api import Widget as PublicWidget\n"
        "from .api import build as hidden_build\n"
        "from .bridge import Widget as ExportedWidget\n\n"
        '__all__ = ["PublicWidget", "ExportedWidget"]\n',
        encoding="utf-8",
    )
    (package / "bridge.py").write_text(
        '"""Re-export selected canonical objects."""\n\nfrom .api import Widget\n\n__all__ = ["Widget"]\n',
        encoding="utf-8",
    )
    (package / "api.py").write_text(
        '"""Define the canonical fixture API."""\n\n'
        "class Widget:\n"
        '    """Represent a canonical widget."""\n\n'
        "    def activate(self, enabled: bool = True) -> bool:\n"
        '        """Set the widget activation state.\n\n'
        "        Args:\n"
        "            enabled: Whether the widget should be active.\n\n"
        "        Returns:\n"
        "            The resulting activation state.\n"
        '        """\n'
        "        return enabled\n\n"
        "def build(name: str) -> Widget:\n"
        '    """Build a canonical widget.\n\n'
        "    Args:\n"
        "        name: Human-readable widget name.\n\n"
        "    Returns:\n"
        "        A new widget.\n"
        '    """\n'
        "    return Widget()\n\n"
        "def _private_helper() -> None:\n"
        '    """Run a private helper."""\n',
        encoding="utf-8",
    )
    return tmp_path


def test_python_reference_resolves_public_reexports_to_canonical_pages(tmp_path: Path) -> None:
    """Require public aliases to index one canonical object page.

    Args:
        tmp_path: Isolated directory in which to create the fixture package.
    """
    source_root = _write_alias_fixture(tmp_path)

    pages = generate_python_pages(
        source_root=source_root, module_names=("fixture",), repository_url="https://example.invalid/repository"
    )

    by_name = {page.qualified_name: page for page in pages}
    assert set(by_name) == {"fixture", "fixture.api.Widget", "fixture.api.Widget.activate"}
    widget = by_name["fixture.api.Widget"]
    method = by_name["fixture.api.Widget.activate"]
    assert widget.path == "python/fixture/api/widget.md"
    assert widget.aliases == ("fixture.ExportedWidget", "fixture.PublicWidget", "fixture.bridge.Widget")
    assert method.aliases == (
        "fixture.ExportedWidget.activate",
        "fixture.PublicWidget.activate",
        "fixture.bridge.Widget.activate",
    )
    assert "- [`ExportedWidget`](./api/widget/)" in by_name["fixture"].body
    assert "- [`PublicWidget`](./api/widget/)" in by_name["fixture"].body
    assert "hidden_build" not in by_name["fixture"].body
    assert all("_private_helper" not in page.qualified_name for page in pages)


def test_python_reference_deduplicates_overlapping_canonical_and_alias_modules(tmp_path: Path) -> None:
    """Require overlapping reviewed modules to emit each canonical route once.

    Args:
        tmp_path: Isolated directory in which to create the fixture package.
    """
    source_root = _write_alias_fixture(tmp_path)

    pages = generate_python_pages(
        source_root=source_root,
        module_names=("fixture", "fixture.api", "fixture.bridge"),
        repository_url="https://example.invalid/repository",
    )

    assert len({page.path for page in pages}) == len(pages)
    assert [page.qualified_name for page in pages].count("fixture.api.Widget") == 1
    assert [page.qualified_name for page in pages].count("fixture.api.Widget.activate") == 1
    by_name = {page.qualified_name: page for page in pages}
    assert "- [`Widget`](../api/widget/)" in by_name["fixture.bridge"].body
    assert "- [`Widget`](./widget/)" in by_name["fixture.api"].body
    assert by_name["fixture.api.build"].aliases == ()


def test_python_reference_generation_never_imports_fixture_code(tmp_path: Path) -> None:
    """Require static generation to leave import-time code unexecuted.

    Args:
        tmp_path: Isolated directory in which to create the sentinel package.
    """
    package = tmp_path / "runtime_sentinel"
    package.mkdir()
    (package / "__init__.py").write_text(
        '"""Fail if documentation generation imports this package."""\n\n'
        "raise RuntimeError('documentation generation executed fixture code')\n\n"
        "def documented() -> None:\n"
        '    """Perform a documented operation."""\n',
        encoding="utf-8",
    )

    pages = generate_python_pages(
        source_root=tmp_path, module_names=("runtime_sentinel",), repository_url="https://example.invalid/repository"
    )

    assert {page.qualified_name for page in pages} == {"runtime_sentinel", "runtime_sentinel.documented"}


def test_python_reference_ignores_unresolved_and_ordinary_import_aliases(tmp_path: Path) -> None:
    """Require only explicit public re-exports to resolve to canonical pages.

    Args:
        tmp_path: Isolated directory in which to create the import fixture.
    """
    package = tmp_path / "import_fixture"
    package.mkdir()
    (package / "__init__.py").write_text(
        '"""Expose the reviewed import fixture API."""\n\n'
        "from __future__ import annotations\n\n"
        "from collections.abc import Iterable\n\n"
        "from .api import Widget as PublicWidget\n"
        "from .api import build as ordinary_import\n\n"
        '__all__ = ["PublicWidget"]\n',
        encoding="utf-8",
    )
    (package / "consumer.py").write_text(
        '"""Consume canonical objects without re-exporting imports."""\n\n'
        "from __future__ import annotations\n\n"
        "from collections.abc import Sequence\n\n"
        "from .api import Widget\n\n"
        "def consume(widgets: Sequence[Widget]) -> int:\n"
        '    """Count imported widgets.\n\n'
        "    Args:\n"
        "        widgets: Imported widgets to count.\n\n"
        "    Returns:\n"
        "        Number of widgets.\n"
        '    """\n'
        "    return len(widgets)\n",
        encoding="utf-8",
    )
    (package / "api.py").write_text(
        '"""Define canonical import-fixture objects."""\n\n'
        "class Widget:\n"
        '    """Represent a canonical widget."""\n\n'
        "def build() -> Widget:\n"
        '    """Build a canonical widget.\n\n'
        "    Returns:\n"
        "        A new widget.\n"
        '    """\n'
        "    return Widget()\n",
        encoding="utf-8",
    )

    pages = generate_python_pages(
        source_root=tmp_path,
        module_names=("import_fixture", "import_fixture.consumer"),
        repository_url="https://example.invalid/repository",
    )

    by_name = {page.qualified_name: page for page in pages}
    assert set(by_name) == {
        "import_fixture",
        "import_fixture.api.Widget",
        "import_fixture.consumer",
        "import_fixture.consumer.consume",
    }
    assert by_name["import_fixture.api.Widget"].aliases == ("import_fixture.PublicWidget",)
    assert "PublicWidget" in by_name["import_fixture"].body
    assert "Iterable" not in by_name["import_fixture"].body
    assert "ordinary_import" not in by_name["import_fixture"].body
    assert "Widget" not in by_name["import_fixture.consumer"].body
    assert "Sequence" not in by_name["import_fixture.consumer"].body


def test_python_reference_indexes_and_splits_every_static_all_export(tmp_path: Path) -> None:
    """Require constants, type aliases, and module aliases to remain visible.

    Args:
        tmp_path: Isolated directory in which to create the public-surface fixture.
    """
    package = tmp_path / "surface_fixture"
    package.mkdir()
    (package / "__init__.py").write_text(
        '"""Expose every statically representable public member kind."""\n\n'
        "from . import api as public_api\n"
        "from .api import Callback as Handler\n"
        "from .api import PUBLIC_CONSTANT as PREFIX\n"
        "from .api import build as ordinary_import\n\n"
        '__all__ = ["PREFIX", "Handler", "public_api"]\n',
        encoding="utf-8",
    )
    (package / "api.py").write_text(
        '"""Define canonical public-surface objects."""\n\n'
        "from collections.abc import Callable\n\n"
        'PUBLIC_CONSTANT = "prefix_"\n'
        "type Callback = Callable[[int], None]\n\n"
        "def build() -> str:\n"
        '    """Build a public value.\n\n'
        "    Returns:\n"
        "        Built value.\n"
        '    """\n'
        "    return PUBLIC_CONSTANT\n\n"
        '__all__ = ["PUBLIC_CONSTANT", "Callback", "build"]\n',
        encoding="utf-8",
    )

    pages = generate_python_pages(
        source_root=tmp_path,
        module_names=("surface_fixture", "surface_fixture.api"),
        repository_url="https://example.invalid/repository",
    )

    assert len({page.path for page in pages}) == len(pages)
    by_name = {page.qualified_name: page for page in pages}
    assert set(by_name) == {
        "surface_fixture",
        "surface_fixture.api",
        "surface_fixture.api.Callback",
        "surface_fixture.api.PUBLIC_CONSTANT",
        "surface_fixture.api.build",
    }
    root = by_name["surface_fixture"]
    assert "- [`PREFIX`](./api/public-constant/)" in root.body
    assert "- [`Handler`](./api/callback/)" in root.body
    assert "- [`public_api`](./api/)" in root.body
    assert "ordinary_import" not in root.body
    assert by_name["surface_fixture.api.PUBLIC_CONSTANT"].kind == "attribute"
    assert by_name["surface_fixture.api.PUBLIC_CONSTANT"].aliases == ("surface_fixture.PREFIX",)
    assert "PUBLIC_CONSTANT = 'prefix_'" in by_name["surface_fixture.api.PUBLIC_CONSTANT"].body
    assert by_name["surface_fixture.api.Callback"].kind == "type"
    assert by_name["surface_fixture.api.Callback"].aliases == ("surface_fixture.Handler",)
    assert "type Callback = Callable[[int], None]" in by_name["surface_fixture.api.Callback"].body
    assert by_name["surface_fixture.api"].aliases == ("surface_fixture.public_api",)


def test_python_reference_rejects_dynamic_all_instead_of_silently_omitting_exports(tmp_path: Path) -> None:
    """Require an explicit error when static analysis cannot expand ``__all__``.

    Args:
        tmp_path: Isolated directory in which to create the dynamic export fixture.
    """
    package = tmp_path / "dynamic_fixture"
    package.mkdir()
    (package / "__init__.py").write_text(
        '"""Build public errors dynamically."""\n\nNAMES = {"CreatedError"}\n__all__ = tuple(sorted(NAMES))\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=r"dynamic_fixture.*dynamically computed __all__"):
        generate_python_pages(
            source_root=tmp_path, module_names=("dynamic_fixture",), repository_url="https://example.invalid/repository"
        )


def test_python_reference_opt_in_dynamic_all_uses_only_direct_source_declarations(tmp_path: Path) -> None:
    """Require the reviewed dynamic fallback to exclude imports and generated names.

    Args:
        tmp_path: Isolated directory in which to create the errors-style fixture.
    """
    package = tmp_path / "dynamic_errors"
    package.mkdir()
    (package / "dependency.py").write_text(
        '"""Provide an ordinary imported error."""\n\n'
        "class ImportedError(Exception):\n"
        '    """Represent an imported error that is not locally public."""\n',
        encoding="utf-8",
    )
    (package / "__init__.py").write_text(
        '"""Define source errors and schema-created errors."""\n\n'
        "from .dependency import ImportedError\n\n"
        "class DirectError(Exception):\n"
        '    """Represent a directly defined error."""\n\n'
        "def classify_error() -> str:\n"
        '    """Classify a directly defined error.\n\n'
        "    Returns:\n"
        "        Static classification marker.\n"
        '    """\n'
        '    return "direct"\n\n'
        '_GENERATED_NAMES = {"SchemaCreatedError"}\n'
        "for _generated_name in _GENERATED_NAMES:\n"
        "    globals()[_generated_name] = type(_generated_name, (DirectError,), {})\n\n"
        'SchemaCreatedError = globals()["SchemaCreatedError"]\n\n'
        '__all__ = tuple(sorted({"DirectError", "ImportedError", "classify_error", *_GENERATED_NAMES}))\n',
        encoding="utf-8",
    )

    pages = generate_python_pages(
        source_root=tmp_path,
        module_names=("dynamic_errors",),
        repository_url="https://example.invalid/repository",
        dynamic_all_modules=("dynamic_errors",),
    )

    by_name = {page.qualified_name: page for page in pages}
    assert set(by_name) == {"dynamic_errors", "dynamic_errors.DirectError", "dynamic_errors.classify_error"}
    assert "ImportedError" not in by_name["dynamic_errors"].body
    assert "SchemaCreatedError" not in by_name["dynamic_errors"].body
