from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path
from typing import cast

import pytest
from tools.docs.audit import (
    find_missing_cli_help,
    find_missing_python_docs,
    find_missing_python_parameter_docs,
    find_missing_rustdoc_docs,
    find_missing_rustdoc_parameter_docs,
)
from tools.docs.generate_python import generate_python_pages
from tools.docs.manifest import build_reference_manifest, compare_reference_trees, write_reference_tree
from tools.docs.model import ReferenceLanguage, ReferencePage

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_release_facing_documents_cover_the_alpha_contract() -> None:
    """Require the README, changelog, and security policy to retain Wave 5's public contract."""
    readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (REPOSITORY_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    security = (REPOSITORY_ROOT / "SECURITY.md").read_text(encoding="utf-8")

    for required in (
        "docs-site/src/assets/brand/mark.svg",
        "0.1.x` Alpha",
        "sign_in_phone",
        "sign_in_bot",
        "get_me",
        "HelpGetConfig",
        "send_message",
        "send_file",
        "iter_updates",
        "download_media",
        "iter_download",
        "verify_plain_hashes",
        "`miniproto` versus `mpgram`",
        "https://miniproto.edm115.dev/",
        "SECURITY.md",
        "CONTRIBUTING.md",
    ):
        assert required in readme

    assert "## v0.1.0 — Alpha" in changelog
    assert "### Breaking changes" in changelog
    assert "Unreleased" not in changelog
    assert "pre-alpha" not in changelog.casefold()
    assert "**Full Changelog**" not in changelog
    for category in ("feat :", "perf :", "security :", "fix :", "docs :", "tests :", "ci :", "build :"):
        assert category in changelog

    for required in (
        "`0.1.x` line",
        "security/advisories/new",
        "miniproto@edm115.dev",
        "MINIPROTO_SESSION_KEY",
        "Telethon v1",
        "Pyrogram",
        "Live tests and benchmarks",
        "Dependencies, native code, and artifacts",
        "Do not open a public issue",
    ):
        assert required in security


def test_contribution_policy_requires_draft_first_pull_requests() -> None:
    """Repository and site guidance must explain when pull-request automation begins."""
    repository_policy = (REPOSITORY_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    site_policy = (REPOSITORY_ROOT / "docs/project/contributing.md").read_text(encoding="utf-8")

    for policy in (repository_policy, site_policy):
        assert "Open every pull request as a draft" in policy
        assert "Draft → Ready for review" in policy
        assert "ready_for_review" in policy
        assert "synchronize" in policy


def test_readme_python_examples_are_syntactically_valid() -> None:
    """Compile every README Python fence, including intentionally contextual async fragments."""
    readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
    blocks = tuple(section.split("```", 1)[0] for section in readme.split("```python\n")[1:])

    assert blocks
    for index, block in enumerate(blocks, start=1):
        compile(
            block, f"README.md:python-block-{index}", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT, dont_inherit=True
        )


def test_codebase_knowledge_documents_follow_the_repository_site_contract() -> None:
    """Require the adapted seven-document codebase map to remain complete and publishable."""
    root = REPOSITORY_ROOT / "docs" / "codebase"
    expected = {
        "ARCHITECTURE.md",
        "CONCERNS.md",
        "CONVENTIONS.md",
        "INTEGRATIONS.md",
        "STACK.md",
        "STRUCTURE.md",
        "TESTING.md",
    }

    assert {path.name for path in root.glob("*.md")} == expected
    for path in sorted(root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        slug = path.stem.casefold().replace("_", "-")
        assert text.startswith("---\n")
        assert "generated: false" in text
        assert f"slug: /project/codebase/{slug}/" in text
        assert "## Evidence" in text
        assert "- `" in text.split("## Evidence", 1)[1]
        assert "[VALUE]" not in text
        assert "[FILE_PATH]" not in text
        assert "[TODO]" not in text


def test_telegram_reference_extractor_module_is_available() -> None:
    """Require the static Telegram reference extractor to have an owned module."""
    assert importlib.util.find_spec("tools.docs.generate_telegram") is not None


def test_telegram_reference_extraction_is_static_complete_and_deterministic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Require schema pages to retain raw structure, provenance, and honest gaps.

    Args:
        tmp_path: Isolated directory in which to write minimal pinned JSON fixtures.
        monkeypatch: Pytest patch helper used to fail any unexpected network call.
    """
    schema_path = tmp_path / "schema.json"
    metadata_path = tmp_path / "schema-metadata.json"
    errors_path = tmp_path / "rpc-errors.json"
    bindings_path = tmp_path / "telegram-bindings.json"
    schema_path.write_text(
        json.dumps(
            {
                "constructors": [
                    {
                        "id": "-1",
                        "predicate": "widget",
                        "type": "Widget",
                        "description": "Represent a widget.",
                        "params": [
                            {"name": "flags", "type": "#"},
                            {"name": "active", "type": "flags.0?true"},
                            {"name": "label", "type": "string", "description": "Widget label."},
                        ],
                    }
                ],
                "methods": [
                    {
                        "id": "123",
                        "method": "messages.sendMessage",
                        "type": "Updates",
                        "description": "Send a message.",
                        "params": [
                            {"name": "flags", "type": "#"},
                            {"name": "no_webpage", "type": "flags.1?true"},
                            {"name": "message", "type": "string", "description": "Text to send."},
                            {"name": "input", "type": "Widget"},
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    metadata_path.write_text(
        json.dumps(
            {
                "canonical_source": "tdlib",
                "layer": 228,
                "schema_layer": 228,
                "constructor_count": 1,
                "function_count": 1,
                "rpc_error_count": 1,
                "structural_source_url": "https://example.invalid/tdlib.tl",
                "source_note": "TDLib supplies structure; other pins only enrich prose.",
                "documentation_merge_precedence": ["tdlib", "tdesktop", "core_json"],
                "source_comparison_summary": {"tdlib_vs_core": {"changed_count": 1, "tdlib_only_count": 2}},
            }
        ),
        encoding="utf-8",
    )
    errors_path.write_text(
        json.dumps(
            {
                "errors": {"420": {"FLOOD_WAIT_%d": ["messages.sendMessage"]}},
                "descriptions": {"FLOOD_WAIT_%d": "Wait %d seconds before retrying."},
            }
        ),
        encoding="utf-8",
    )
    bindings_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "layer": 228,
                "declarations": [
                    {
                        "kind": "function",
                        "qualified_name": "messages.sendMessage",
                        "constructor_id": "0x0000007b",
                        "python_module": "miniproto.raw.functions",
                        "python_name": "MessagesSendMessage",
                        "python_import": "from miniproto.raw.functions import MessagesSendMessage",
                        "public_access": "miniproto.raw.functions.MessagesSendMessage",
                    },
                    {
                        "kind": "type",
                        "qualified_name": "widget",
                        "constructor_id": "0xffffffff",
                        "python_module": "miniproto.raw.types",
                        "python_name": "Widget",
                        "python_import": "from miniproto.raw.types import Widget",
                        "public_access": "miniproto.raw.types.Widget",
                    },
                ],
                "errors": [
                    {
                        "code": 420,
                        "name": "FLOOD_WAIT_%d",
                        "python_module": "miniproto.errors",
                        "python_name": "FloodWait",
                        "python_import": "from miniproto.errors import FloodWait",
                        "public_access": "miniproto.errors.FloodWait",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    import socket

    def fail_network(*_args: object, **_kwargs: object) -> object:
        """Fail if static extraction unexpectedly attempts network access.

        Args:
            *_args: Ignored positional connection arguments from a prohibited call.
            **_kwargs: Ignored keyword connection arguments from a prohibited call.
        """
        raise AssertionError("Telegram documentation extraction must not use the network")

    monkeypatch.setattr(socket, "create_connection", fail_network)
    module = importlib.import_module("tools.docs.generate_telegram")
    extractor = getattr(module, "generate_telegram_pages", None)
    binding_loader = getattr(module, "load_telegram_binding_manifest", None)
    surface_generator = getattr(module, "generate_telegram_reference_surface", None)
    module_tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    imported_modules = {
        imported.name
        for statement in ast.walk(module_tree)
        if isinstance(statement, ast.Import)
        for imported in statement.names
    } | {
        statement.module
        for statement in ast.walk(module_tree)
        if isinstance(statement, ast.ImportFrom) and statement.module is not None
    }

    assert callable(extractor)
    assert callable(binding_loader)
    assert callable(surface_generator)
    assert not any(name == "miniproto" or name.startswith("miniproto.") for name in imported_modules)
    bindings = binding_loader(bindings_path)
    first = extractor(
        schema_path=schema_path,
        metadata_path=metadata_path,
        rpc_errors_path=errors_path,
        binding_manifest=bindings,
        repository_url="https://example.invalid/repository",
    )
    second = extractor(
        schema_path=schema_path,
        metadata_path=metadata_path,
        rpc_errors_path=errors_path,
        binding_manifest=bindings,
        repository_url="https://example.invalid/repository",
    )

    assert first == second
    assert [page.path for page in first] == sorted(page.path for page in first)
    pages = {page.path: page for page in first}
    function = pages["telegram/functions/messages/send-message.md"]
    widget = pages["telegram/types/base/widget.md"]
    error = pages["telegram/errors/flood-wait.md"]
    assert function.layer == 228
    assert function.schema_source == "tdlib"
    assert function.constructor_id == "0x0000007b"
    assert "messages.sendMessage#0000007b" in function.body
    assert "## Result type\n\n`Updates`" in function.body
    assert "| flags | # | flag word | — |" in function.body
    assert (
        "| no_webpage | flags.1?true | flags.1 | — | No description provided by the pinned schema. |" in function.body
    )
    assert "| message | string | — | — | Text to send. |" in function.body
    assert "FLOOD_WAIT_%d" in function.body
    assert "Wait %d seconds before retrying." in function.body
    assert "from miniproto.raw.functions import MessagesSendMessage" in function.body
    assert "from miniproto.raw.types import Widget" in widget.body
    assert "from miniproto.errors import FloodWait" in error.body
    assert "https://example.invalid/repository/blob/master/tools/schema/rpc-errors.json" in error.body
    assert "request_type = MessagesSendMessage" in function.body
    assert "constructor_type = Widget" in widget.body
    assert "[`FLOOD_WAIT_%d`](/reference/telegram/errors/flood-wait/)" in function.body
    assert "[`Widget`](/reference/telegram/types/results/widget/)" in function.body
    assert "[`messages.sendMessage`](/reference/telegram/functions/messages/send-message/)" in error.body
    assert "## Accepted types" in function.body
    assert "## Returned types" in function.body
    assert "TDLib → Telegram Desktop → Core JSON" in function.body
    assert "TDLib supplies structure; other pins only enrich prose." in function.body
    assert "input" in function.body
    assert "Accepted by" in widget.body
    assert "messages.sendMessage" in widget.body
    assert "parameterized: yes" in error.body
    assert 'language: "telegram"' in function.render()
    assert "telegram/errors/by-code/index.md" in pages
    assert "telegram/errors/by-name/index.md" in pages
    assert "telegram/errors/by-method/index.md" in pages
    assert (
        "Layer 228 Telegram raw API: 1 functions, 1 type constructors, and 1 pinned RPC errors from tdlib."
        in pages["telegram/index.md"].description
    )
    assert "Selected canonical functions: 1." in pages["telegram/functions/index.md"].body
    assert "Selected canonical constructors in this family: 1." in pages["telegram/types/results/widget/index.md"].body
    assert (
        "Layer 228 index of 1 pinned Telegram RPC errors sorted by numeric code."
        in pages["telegram/errors/by-code/index.md"].description
    )
    assert (
        "https://example.invalid/repository/blob/master/tools/schema/rpc-errors.json"
        in pages["telegram/errors/by-method/index.md"].body
    )

    surface = surface_generator(
        schema_path=schema_path,
        metadata_path=metadata_path,
        rpc_errors_path=errors_path,
        binding_manifest=bindings,
        repository_url="https://example.invalid/repository",
    )
    relationships = json.loads(surface.relationship_manifest)
    assert surface.relationship_manifest_path == "telegram/relationships.json"
    assert {
        "relation": "rpc_error",
        "source": {
            "kind": "function",
            "qualified_name": "messages.sendMessage",
            "constructor_id": "0x0000007b",
            "path": "telegram/functions/messages/send-message.md",
        },
        "target": {
            "kind": "error",
            "qualified_name": "420:FLOOD_WAIT_%d",
            "constructor_id": None,
            "path": "telegram/errors/flood-wait.md",
            "selected_layer": True,
        },
    } in relationships["relationships"]


def test_telegram_reference_routes_reserve_result_indexes_against_type_details(tmp_path: Path) -> None:
    """Require global route allocation to protect result indexes from a type-page collision.

    Args:
        tmp_path: Isolated directory containing the minimal selected-layer JSON inputs.
    """
    schema_path = tmp_path / "schema.json"
    metadata_path = tmp_path / "schema-metadata.json"
    errors_path = tmp_path / "rpc-errors.json"
    bindings_path = tmp_path / "telegram-bindings.json"
    schema_path.write_text(
        json.dumps(
            {"constructors": [{"id": "2", "predicate": "results.foo", "type": "foo", "params": []}], "methods": []}
        ),
        encoding="utf-8",
    )
    metadata_path.write_text(
        json.dumps(
            {
                "canonical_source": "tdlib",
                "layer": 228,
                "schema_layer": 228,
                "constructor_count": 1,
                "function_count": 0,
                "rpc_error_count": 0,
                "structural_source_url": "https://example.invalid/tdlib.tl",
                "documentation_merge_precedence": ["tdlib"],
            }
        ),
        encoding="utf-8",
    )
    errors_path.write_text(json.dumps({"errors": {}, "descriptions": {}}), encoding="utf-8")
    bindings_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "layer": 228,
                "declarations": [
                    {
                        "kind": "type",
                        "qualified_name": "results.foo",
                        "constructor_id": "0x00000002",
                        "python_module": "miniproto.raw.types",
                        "python_name": "ResultsFoo",
                        "python_import": "from miniproto.raw.types import ResultsFoo",
                        "public_access": "miniproto.raw.types.ResultsFoo",
                    }
                ],
                "errors": [],
            }
        ),
        encoding="utf-8",
    )
    module = importlib.import_module("tools.docs.generate_telegram")
    bindings = module.load_telegram_binding_manifest(bindings_path)
    pages = module.generate_telegram_pages(
        schema_path=schema_path,
        metadata_path=metadata_path,
        rpc_errors_path=errors_path,
        binding_manifest=bindings,
        repository_url="https://example.invalid/repository",
    )

    paths = {page.path for page in pages}
    routes = {page.path.removesuffix("index.md").removesuffix(".md").rstrip("/") for page in pages}
    assert "telegram/types/results/foo/index.md" in paths
    assert "telegram/types/results/foo-00000002.md" in paths
    assert len(paths) == len(routes)


def test_telegram_reference_real_pins_have_complete_unique_bound_surface() -> None:
    """Require the full selected-layer pins to reconcile with every generated binding.

    The test exercises the production-scale static extraction path without
    importing the miniproto package, contacting Telegram, or writing a docs tree.
    """
    module = importlib.import_module("tools.docs.generate_telegram")
    bindings = module.load_telegram_binding_manifest(REPOSITORY_ROOT / "tools" / "schema" / "telegram-bindings.json")
    surface = module.generate_telegram_reference_surface(
        schema_path=REPOSITORY_ROOT / "tools" / "schema" / "schema.json",
        metadata_path=REPOSITORY_ROOT / "tools" / "schema" / "schema-metadata.json",
        rpc_errors_path=REPOSITORY_ROOT / "tools" / "schema" / "rpc-errors.json",
        binding_manifest=bindings,
        repository_url="https://github.com/EDM115/miniproto",
    )

    assert len(bindings.declarations) == 2_460
    assert len(bindings.errors) == 818
    assert len(surface.pages) == 3_946
    assert sum(page.kind == "function" for page in surface.pages) == 811
    assert sum(page.kind == "type" for page in surface.pages) == 1_649
    assert sum(page.kind == "error" for page in surface.pages) == 818
    assert sum(page.kind == "index" for page in surface.pages) == 668
    paths = [page.path for page in surface.pages]
    routes = [page.path.removesuffix("index.md").removesuffix(".md").rstrip("/") for page in surface.pages]
    assert len(paths) == len(set(paths))
    assert len(routes) == len(set(routes))
    aliases_by_id = {
        constructor_id: {key[1] for key in bindings.declarations if key[0] == "function" and key[2] == constructor_id}
        for constructor_id in ("0xdd289f8e", "0x1df92984", "0x0dae54f8", "0xadbb0f94")
    }
    assert aliases_by_id == {
        "0xdd289f8e": {"invokeWithBusinessConnection", "invokeWithBusinessConnectionPrefix"},
        "0x1df92984": {"invokeWithGooglePlayIntegrity", "invokeWithGooglePlayIntegrityPrefix"},
        "0x0dae54f8": {"invokeWithApnsSecret", "invokeWithApnsSecretPrefix"},
        "0xadbb0f94": {"invokeWithReCaptcha", "invokeWithReCaptchaPrefix"},
    }


def test_python_doc_audit_reports_modules_and_nested_symbols(tmp_path: Path) -> None:
    source_root = tmp_path / "package"
    source_root.mkdir()
    (source_root / "documented.py").write_text(
        '"""A documented module."""\n\n'
        "def outer() -> None:\n"
        '    """Run the outer operation."""\n'
        "    def inner() -> None:\n"
        "        pass\n",
        encoding="utf-8",
    )
    (source_root / "missing.py").write_text(
        "class Example:\n    def method(self) -> None:\n        pass\n", encoding="utf-8"
    )

    missing = find_missing_python_docs((source_root,))

    assert [(item.kind, item.qualified_name) for item in missing] == [
        ("function", "documented.outer.inner"),
        ("module", "missing"),
        ("class", "missing.Example"),
        ("function", "missing.Example.method"),
    ]


def test_python_doc_audit_excludes_generator_owned_roots(tmp_path: Path) -> None:
    source_root = tmp_path / "package"
    generated_root = source_root / "raw"
    generated_root.mkdir(parents=True)
    (source_root / "maintained.py").write_text('"""Maintained."""\n', encoding="utf-8")
    (generated_root / "types.py").write_text("class Generated:\n    pass\n", encoding="utf-8")

    assert find_missing_python_docs((source_root,), excluded_roots=(generated_root,)) == ()


def test_python_doc_audit_rejects_empty_and_known_placeholder_prose(tmp_path: Path) -> None:
    """Require the source policy to reject present-but-empty or explicitly generic documentation.

    Args:
        tmp_path: Isolated directory containing the documentation fixtures.
    """
    source = tmp_path / "placeholders.py"
    source.write_text('"""Schema tooling."""\n\ndef empty() -> None:\n    """"""\n', encoding="utf-8")

    issues = find_missing_python_docs((source,))

    assert [(issue.kind, issue.qualified_name) for issue in issues] == [
        ("module", "placeholders"),
        ("function", "placeholders.empty"),
    ]


def test_python_parameter_audit_requires_a_meaningful_description_for_every_argument(tmp_path: Path) -> None:
    source = tmp_path / "module.py"
    source.write_text(
        '"""Parameter fixture."""\n\n'
        "def complete(alpha: int, /, beta: str, *values: bytes, gamma: bool, **options: object) -> None:\n"
        '    """Run a complete operation.\n\n'
        "    Args:\n"
        "        alpha: Numeric input.\n"
        "        beta: Text input.\n"
        "        *values: Additional byte payloads.\n"
        "        gamma: Whether to enable the operation.\n"
        "        **options: Additional named options.\n"
        '    """\n'
        "    return None\n\n"
        "def incomplete(one: int, two: int) -> None:\n"
        '    """Run an incomplete operation.\n\n'
        "    Args:\n"
        "        one: First input.\n"
        '    """\n'
        "    return None\n",
        encoding="utf-8",
    )

    issues = find_missing_python_parameter_docs((source,))

    assert [(issue.qualified_name, issue.arguments) for issue in issues] == [("module.incomplete", ("two",))]


def test_python_parameter_audit_rejects_documented_names_absent_from_the_signature(tmp_path: Path) -> None:
    """Require stale ``Args`` entries to fail the bidirectional signature contract.

    Args:
        tmp_path: Isolated directory containing the stale parameter fixture.
    """
    source = tmp_path / "stale.py"
    source.write_text(
        '"""Stale parameter fixture."""\n\ndef operation(value: int) -> None:\n    """Run one operation.\n\n    Args:\n        value: Value to process.\n        removed: Obsolete option that no longer exists.\n    """\n',
        encoding="utf-8",
    )

    issues = find_missing_python_parameter_docs((source,))

    assert [(issue.qualified_name, issue.arguments, issue.unexpected_arguments) for issue in issues] == [
        ("stale.operation", (), ("removed",))
    ]


def test_cli_help_audit_requires_static_meaningful_prose(tmp_path: Path) -> None:
    """Require every literal command-line option to explain itself in ``--help`` output.

    Args:
        tmp_path: Isolated directory containing parser-action fixtures.
    """
    source = tmp_path / "cli.py"
    source.write_text(
        '"""CLI help fixture."""\n\nimport argparse\n\nparser = argparse.ArgumentParser()\nparser.add_argument("--complete", help="number of samples to collect")\nparser.add_argument("--missing")\nparser.add_argument("--placeholder", help="Value.")\nparser.add_argument("destination")\n',
        encoding="utf-8",
    )

    issues = find_missing_cli_help((source,))

    assert [(issue.line, issue.options) for issue in issues] == [(7, ("--missing",)), (8, ("--placeholder",))]


def test_python_parameter_audit_covers_inherited_dataclass_constructor_fields(tmp_path: Path) -> None:
    source = tmp_path / "models.py"
    source.write_text(
        '"""Dataclass parameter fixture."""\n\n'
        "from dataclasses import dataclass, field\n\n"
        "@dataclass\n"
        "class Base:\n"
        '    """Store a base value.\n\n'
        "    Attributes:\n"
        "        base: Value inherited by child constructors.\n"
        '    """\n'
        "    base: int\n\n"
        "@dataclass\n"
        "class Child(Base):\n"
        '    """Store child values.\n\n'
        "    Attributes:\n"
        "        child: Child-specific value.\n"
        "        cached: Non-constructor cache value.\n"
        '    """\n'
        "    child: str\n"
        "    cached: bytes = field(init=False, default=b'')\n",
        encoding="utf-8",
    )

    issues = find_missing_python_parameter_docs((source,))

    assert [(issue.qualified_name, issue.arguments) for issue in issues] == [("models.Child", ("base",))]


def test_maintained_python_sources_meet_the_reference_documentation_policy() -> None:
    roots = (REPOSITORY_ROOT / "src" / "miniproto", REPOSITORY_ROOT / "tools")
    excluded = (REPOSITORY_ROOT / "src" / "miniproto" / "raw",)

    undocumented = find_missing_python_docs(roots, excluded_roots=excluded)
    undescribed = find_missing_python_parameter_docs(roots, excluded_roots=excluded)
    missing_cli_help = find_missing_cli_help((REPOSITORY_ROOT / "tools",))

    assert not undocumented, "\n".join(
        f"{issue.path}:{issue.line}: {issue.kind} {issue.qualified_name}" for issue in undocumented
    )
    assert not undescribed, "\n".join(
        f"{issue.path}:{issue.line}: {issue.qualified_name} missing {', '.join(issue.arguments)} unexpected {', '.join(issue.unexpected_arguments)}"
        for issue in undescribed
    )
    assert not missing_cli_help, "\n".join(
        f"{issue.path}:{issue.line}: {', '.join(issue.options)} lacks static help prose" for issue in missing_cli_help
    )


def test_rustdoc_audit_reports_only_maintained_undocumented_items(tmp_path: Path) -> None:
    payload = {
        "root": 0,
        "index": {
            "0": {
                "crate_id": 0,
                "name": "miniproto_native",
                "docs": "Crate docs.",
                "span": None,
                "inner": {"module": {}},
            },
            "1": {
                "crate_id": 0,
                "name": "register",
                "docs": None,
                "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [32, 0], "end": [52, 1]},
                "inner": {"function": {}},
            },
            "2": {
                "crate_id": 0,
                "name": "GeneratedSpec",
                "docs": None,
                "span": {"filename": "rust/miniproto/src/generated_tl.rs", "begin": [1, 0], "end": [2, 1]},
                "inner": {"struct": {}},
            },
            "3": {
                "crate_id": 1,
                "name": "DependencyItem",
                "docs": None,
                "span": {"filename": "dependency/src/lib.rs", "begin": [1, 0], "end": [2, 1]},
                "inner": {"function": {}},
            },
        },
        "paths": {"1": {"path": ["miniproto_native", "crypto", "register"], "kind": "function"}},
    }
    rustdoc_json = tmp_path / "miniproto_native.json"
    rustdoc_json.write_text(json.dumps(payload), encoding="utf-8")

    missing = find_missing_rustdoc_docs(rustdoc_json, excluded_paths=("rust/miniproto/src/generated_tl.rs",))

    assert [(item.kind, item.qualified_name, item.line) for item in missing] == [
        ("function", "miniproto_native::crypto::register", 32)
    ]


def test_rustdoc_parameter_audit_requires_descriptions_for_every_non_receiver_argument(tmp_path: Path) -> None:
    payload = {
        "root": 0,
        "index": {
            "0": {
                "crate_id": 0,
                "name": "miniproto_native",
                "docs": "Crate docs.",
                "span": None,
                "inner": {"module": {}},
            },
            "1": {
                "crate_id": 0,
                "name": "complete",
                "docs": "Complete an operation.\n\n# Arguments\n\n* `payload` - Bytes to process.\n* `limit` - Maximum output length.",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [10, 0], "end": [20, 1]},
                "inner": {
                    "function": {
                        "sig": {
                            "inputs": [
                                ["self", {"generic": "Self"}],
                                ["payload", {"primitive": "slice"}],
                                ["limit", {"primitive": "usize"}],
                            ],
                            "output": None,
                            "is_c_variadic": False,
                        }
                    }
                },
            },
            "2": {
                "crate_id": 0,
                "name": "incomplete",
                "docs": "Run an operation.\n\n# Arguments\n\n* `first` - First input.",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [30, 0], "end": [40, 1]},
                "inner": {
                    "function": {
                        "sig": {
                            "inputs": [["first", {"primitive": "u32"}], ["second", {"primitive": "u32"}]],
                            "output": None,
                            "is_c_variadic": False,
                        }
                    }
                },
            },
            "3": {
                "crate_id": 0,
                "name": "generated",
                "docs": None,
                "span": {"filename": "rust/miniproto/src/generated_tl.rs", "begin": [1, 0], "end": [2, 1]},
                "inner": {
                    "function": {
                        "sig": {"inputs": [["value", {"primitive": "u32"}]], "output": None, "is_c_variadic": False}
                    }
                },
            },
        },
        "paths": {
            "1": {"path": ["miniproto_native", "complete"], "kind": "function"},
            "2": {"path": ["miniproto_native", "incomplete"], "kind": "function"},
        },
    }
    rustdoc_json = tmp_path / "miniproto_native.json"
    rustdoc_json.write_text(json.dumps(payload), encoding="utf-8")

    missing = find_missing_rustdoc_parameter_docs(rustdoc_json, excluded_paths=("rust/miniproto/src/generated_tl.rs",))

    assert [(item.qualified_name, item.arguments) for item in missing] == [
        ("miniproto_native::incomplete", ("second",))
    ]


def test_reference_page_renders_deterministic_validated_frontmatter() -> None:
    page = ReferencePage(
        path="telegram/functions/messages/send-message.md",
        title="messages.sendMessage",
        description="Send a message to a chat.",
        language="telegram",
        kind="function",
        qualified_name="messages.sendMessage",
        source_path="tools/schema/schema.tl",
        source_url="https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.tl",
        body="## Signature\n\n```tl\nmessages.sendMessage#fe05dc9a = Updates;\n```",
        namespace="messages",
        layer=228,
        schema_source="tdlib",
        constructor_id="0xfe05dc9a",
        aliases=("SendMessage",),
    )

    rendered = page.render()

    assert rendered.startswith('---\ntitle: "messages.sendMessage"\ndescription: "Send a message to a chat."\n')
    assert 'generated: true\neditUrl: false\nlanguage: "telegram"\nkind: "function"\n' in rendered
    assert 'aliases: ["SendMessage"]\n' in rendered
    assert "layer: 228\n" in rendered
    assert rendered.endswith("```\n")
    assert page.route == "/reference/telegram/functions/messages/send-message/"


@pytest.mark.parametrize(
    ("language", "namespace", "message"),
    [("python", None, "module"), ("telegram", "messages", "layer"), ("rust", None, "crate")],
)
def test_reference_page_rejects_missing_language_provenance(
    language: ReferenceLanguage, namespace: str | None, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        ReferencePage(
            path=f"{language}/item.md",
            title="item",
            description="An item.",
            language=language,
            kind="function",
            qualified_name="item",
            source_path="source",
            source_url="https://example.invalid/source",
            body="Body.",
            namespace=namespace,
        )


def test_reference_page_rejects_missing_source_url() -> None:
    """Require generated pages to retain a non-empty browser provenance URL."""
    with pytest.raises(ValueError, match="source_url must not be empty"):
        ReferencePage(
            path="python/function.md",
            title="function",
            description="Document one function.",
            language="python",
            kind="function",
            qualified_name="package.function",
            source_path="src/package.py",
            source_url=cast(str, None),
            body="Reference body.",
            module="package",
        )


def test_reference_manifest_and_tree_are_deterministic(tmp_path: Path) -> None:
    first = ReferencePage(
        path="python/miniproto/client.md",
        title="Client",
        description="Connect to Telegram.",
        language="python",
        kind="class",
        qualified_name="miniproto.Client",
        source_path="src/miniproto/client.py",
        source_url="https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py",
        body="Client body.",
        module="miniproto.client",
    )
    second = ReferencePage(
        path="rust/miniproto-native/transport-codec.md",
        title="TransportCodec",
        description="Decode transport frames.",
        language="rust",
        kind="struct",
        qualified_name="miniproto_native::transport::TransportCodec",
        source_path="rust/miniproto/src/transport.rs",
        source_url="https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs",
        body="Rust body.",
        crate="miniproto-native",
        python_visible=True,
    )
    tools = {"griffe2md": "1.5.0", "griffe": "2.2.0"}
    sources = {"src/miniproto/client.py": "abc123"}

    forward = build_reference_manifest((first, second), tool_versions=tools, source_hashes=sources)
    reverse = build_reference_manifest(
        (second, first), tool_versions=dict(reversed(tuple(tools.items()))), source_hashes=sources
    )

    assert forward == reverse
    assert [page["path"] for page in json.loads(forward)["pages"]] == [first.path, second.path]
    output = tmp_path / "reference"
    write_reference_tree(output, (second, first), tool_versions=tools, source_hashes=sources)
    assert (output / first.path).read_text(encoding="utf-8") == first.render()
    assert (output / "manifest.json").read_text(encoding="utf-8") == forward
    assert compare_reference_trees(output, output).is_clean


def test_reference_manifest_rejects_duplicate_routes() -> None:
    page = ReferencePage(
        path="python/miniproto/index.md",
        title="miniproto",
        description="Public package.",
        language="python",
        kind="module",
        qualified_name="miniproto",
        source_path="src/miniproto/__init__.py",
        source_url="https://github.com/EDM115/miniproto/blob/master/src/miniproto/__init__.py",
        body="Package body.",
        module="miniproto",
    )

    with pytest.raises(ValueError, match="duplicate reference path"):
        build_reference_manifest((page, page), tool_versions={}, source_hashes={})


def test_python_reference_generation_is_static_and_splits_public_symbols(tmp_path: Path) -> None:
    package = tmp_path / "fixture"
    package.mkdir()
    (package / "__init__.py").write_text(
        '"""A static extraction fixture."""\n\n'
        "raise RuntimeError('the documentation generator imported fixture code')\n\n"
        "class Widget:\n"
        '    """Represent a widget."""\n\n'
        "    def activate(self, enabled: bool = True) -> bool:\n"
        '        """Set the widget activation state.\n\n'
        "        Args:\n"
        "            enabled: Whether the widget should be active.\n\n"
        "        Returns:\n"
        "            The resulting activation state.\n"
        '        """\n'
        "        return enabled\n\n"
        "def build(name: str) -> Widget:\n"
        '    """Build a named widget.\n\n'
        "    Args:\n"
        "        name: Human-readable widget name.\n\n"
        "    Returns:\n"
        "        A new widget.\n"
        '    """\n'
        "    return Widget()\n\n"
        "def _private(value: str) -> str:\n"
        '    """Return a private value.\n\n'
        "    Args:\n"
        "        value: Private input.\n\n"
        "    Returns:\n"
        "        The unchanged value.\n"
        '    """\n'
        "    return value\n",
        encoding="utf-8",
    )

    pages = generate_python_pages(
        source_root=tmp_path, module_names=("fixture",), repository_url="https://example.invalid/repository"
    )

    by_name = {page.qualified_name: page for page in pages}
    assert set(by_name) == {"fixture", "fixture.Widget", "fixture.Widget.activate", "fixture.build"}
    assert by_name["fixture"].path == "python/fixture/index.md"
    assert by_name["fixture.Widget"].path == "python/fixture/widget.md"
    assert by_name["fixture.Widget.activate"].path == "python/fixture/widget/activate.md"
    assert "enabled" in by_name["fixture.Widget.activate"].body
    assert "Human-readable widget name." in by_name["fixture.build"].body
