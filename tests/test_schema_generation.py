"""Verify deterministic schema generation, ownership and freshness behavior."""

from __future__ import annotations

import ast
import hashlib
import json
import keyword
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from typing import Any, TypeGuard

import pytest
from tools.schema import generate, rust_fast
from tools.schema.generate import render_outputs, stale_outputs, write_outputs
from tools.schema.parser import TLSchema, TLSchemaParseError, parse_schema, parse_schema_file, parse_schema_json
from tools.schema.rust_fast import FastEntry, load_fast_entries, render_rust

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "tools" / "schema" / "schema.tl"
ERRORS = ROOT / "tools" / "schema" / "rpc-errors.json"
METADATA = ROOT / "tools" / "schema" / "schema-metadata.json"
BINDINGS = ROOT / "tools" / "schema" / "telegram-bindings.json"
FIXTURE = ROOT / "tests" / "fixtures" / "schema" / "layer223-slice.tl"
FIXTURE_LAYER = 223
TDLIB_FIXTURE_LAYER = 228


def _fixture_metadata_path(tmp_path: Path, *, layer: int = FIXTURE_LAYER) -> Path:
    """Create stable metadata owned by a schema fixture rather than the live Telegram snapshot."""
    path = tmp_path / "schema-metadata.json"
    if not path.exists():
        path.write_text(json.dumps({"layer": layer, "schema_layer": layer}), encoding="utf-8")
    return path


def test_generation_requires_schema_layer_metadata(tmp_path: Path) -> None:
    """Reject generation when no upstream layer accompanies the supplied schema."""
    with pytest.raises(ValueError, match="schema metadata must define schema_layer or layer"):
        render_outputs(FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw")


def _is_registry_specs(value: object) -> TypeGuard[dict[str, tuple[str, str]]]:
    """Recognize the generated registry specification mapping shape.

    Args:
        value: Namespace value produced by executing generated registry source.
    """
    return isinstance(value, dict) and all(
        isinstance(name, str)
        and isinstance(spec, tuple)
        and len(spec) == 2
        and all(isinstance(part, str) for part in spec)
        for name, spec in value.items()
    )


def _is_constructor_registry(value: object) -> TypeGuard[dict[int, str]]:
    """Recognize the generated constructor-ID registry mapping shape.

    Args:
        value: Namespace value produced by executing generated registry source.
    """
    return isinstance(value, dict) and all(
        isinstance(constructor_id, int) and isinstance(name, str) for constructor_id, name in value.items()
    )


def test_constructor_bucket_assignment_depends_only_on_id() -> None:
    """Pin deterministic power-of-two shard selection for representative IDs."""
    assert generate._bucket_for_constructor_id(0x997275B5, 64) == 0x35
    assert generate._bucket_for_constructor_id(0x997275B5, 32) == 0x15
    assert generate._bucket_for_constructor_id(0xFFFFFFFF, 64) == 0x3F


def test_generation_emits_stable_constructor_id_shards(tmp_path: Path) -> None:
    """Place fixture constructors in shards derived solely from their IDs.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    outputs = render_outputs(FIXTURE, _fixture_metadata_path(tmp_path), ERRORS, tmp_path / "raw")

    assert tmp_path / "raw" / "_types_shards" / "bucket_53.py" in outputs.files
    assert tmp_path / "raw" / "_function_shards" / "bucket_13.py" in outputs.files
    assert "class BoolTrue" in outputs.files[tmp_path / "raw" / "_types_shards" / "bucket_53.py"]
    assert "class InvokeWithLayer" in outputs.files[tmp_path / "raw" / "_function_shards" / "bucket_13.py"]


def test_generation_emits_compact_registry_and_valid_python_shards(tmp_path: Path) -> None:
    """Produce executable lazy registry metadata and syntactically valid shards.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    outputs = render_outputs(FIXTURE, _fixture_metadata_path(tmp_path), ERRORS, tmp_path / "raw")

    registry = outputs.files[tmp_path / "raw" / "_registry.py"]
    namespace: dict[str, object] = {}
    exec(  # noqa: S102 - validates generated registry source in an isolated namespace.
        compile(registry, str(tmp_path / "raw" / "_registry.py"), "exec"), namespace
    )
    type_specs = namespace["TYPE_SPECS"]
    type_constructors = namespace["TYPE_CONSTRUCTORS"]
    function_specs = namespace["FUNCTION_SPECS"]
    assert _is_registry_specs(type_specs)
    assert _is_constructor_registry(type_constructors)
    assert _is_registry_specs(function_specs)
    assert type_specs["BoolTrue"] == ("miniproto.raw._types_shards.bucket_53", "BoolTrue")
    assert type_constructors[0x997275B5] == "BoolTrue"
    assert function_specs["InvokeWithLayer"] == ("miniproto.raw._function_shards.bucket_13", "InvokeWithLayer")
    for path, content in outputs.files.items():
        if path.parent.name in {"_types_shards", "_function_shards"}:
            compile(content, str(path), "exec")


def test_generation_emits_sorted_source_owned_telegram_binding_manifest(tmp_path: Path) -> None:
    """Emit exact public Python bindings beside the generated raw surface.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    bindings_path = tmp_path / "telegram-bindings.json"
    outputs = render_outputs(FIXTURE, _fixture_metadata_path(tmp_path), ERRORS, tmp_path / "raw")

    assert bindings_path in outputs.files
    manifest = json.loads(outputs.files[bindings_path])
    assert manifest["schema_version"] == 1
    assert manifest["layer"] == FIXTURE_LAYER
    assert manifest["declarations"] == sorted(
        manifest["declarations"],
        key=lambda record: (record["kind"], record["qualified_name"], record["constructor_id"]),
    )
    assert {
        "kind": "function",
        "qualified_name": "help.getConfig",
        "constructor_id": "0xc4f9186b",
        "python_module": "miniproto.raw.functions",
        "python_name": "HelpGetConfig",
        "python_import": "from miniproto.raw.functions import HelpGetConfig",
        "public_access": "miniproto.raw.functions.HelpGetConfig",
    } in manifest["declarations"]
    assert {
        "code": 420,
        "name": "FLOOD_WAIT_%d",
        "python_module": "miniproto.errors",
        "python_name": "FloodWait",
        "python_import": "from miniproto.errors import FloodWait",
        "public_access": "miniproto.errors.FloodWait",
    } in manifest["errors"]


def test_generation_emits_compact_lazy_facades(tmp_path: Path) -> None:
    """Keep facades lazy while exposing the compact public registry surfaces.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    outputs = render_outputs(FIXTURE, _fixture_metadata_path(tmp_path), ERRORS, tmp_path / "raw")

    generated_types = outputs.files[tmp_path / "raw" / "types.py"]
    generated_functions = outputs.files[tmp_path / "raw" / "functions.py"]
    assert "class BoolTrue" not in generated_types
    assert "class InvokeWithLayer" not in generated_functions
    assert "def __getattr__(name: str)" in generated_types
    assert "def __dir__()" in generated_types
    assert "ALL_TYPES = LazyClassSequence" in generated_types
    assert "CONSTRUCTOR_ID_MAP = LazyConstructorMap" in generated_functions


def test_generation_does_not_own_handwritten_raw_api_docs(tmp_path: Path) -> None:
    """Exclude handwritten raw API Markdown from generated outputs.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    outputs = render_outputs(FIXTURE, _fixture_metadata_path(tmp_path), ERRORS, tmp_path / "raw")

    assert all(path.name != "raw-api.md" for path in outputs.files)


def test_stale_generation_ignores_legacy_handwritten_docs_manifest_entry(tmp_path: Path) -> None:
    """Treat only the retired handwritten-doc manifest entry as migration-compatible.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    metadata_path = _fixture_metadata_path(tmp_path)
    outputs = render_outputs(FIXTURE, metadata_path, ERRORS, tmp_path / "raw")
    write_outputs(outputs)
    metadata = __import__("json").loads(metadata_path.read_text(encoding="utf-8"))
    metadata["generated_file_manifest"].append("docs/raw-api.md")
    metadata_path.write_text(__import__("json").dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    assert metadata_path not in stale_outputs(render_outputs(FIXTURE, metadata_path, ERRORS, tmp_path / "raw"))


def test_generation_emits_public_type_stubs_and_manifest_entries(tmp_path: Path) -> None:
    """Emit public type stubs and retain their generated manifest entries.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    outputs = render_outputs(FIXTURE, _fixture_metadata_path(tmp_path), ERRORS, tmp_path / "raw")

    generated_types = outputs.files[tmp_path / "raw" / "types.pyi"]
    generated_functions = outputs.files[tmp_path / "raw" / "functions.pyi"]
    metadata = __import__("json").loads(outputs.files[tmp_path / "schema-metadata.json"])
    assert "class BoolTrue(TLConstructor):" in generated_types
    assert "def __init__(self) -> None: ..." in generated_types
    assert "self_: bool = ..." in generated_types
    assert "first_name: str | None = ..." in generated_types
    assert "class MessagesSendMessage(TLRequest):" in generated_functions
    assert "entities: tuple[Any, ...] | None = ..." in generated_functions
    assert "class help:" in generated_functions
    assert "GetConfig = HelpGetConfig" in generated_functions
    assert "src/miniproto/raw/types.pyi" in metadata["generated_file_manifest"]
    assert "src/miniproto/raw/functions.pyi" in metadata["generated_file_manifest"]


def test_generation_reports_and_removes_only_owned_stale_shards(tmp_path: Path) -> None:
    """Remove header-marked obsolete shards while preserving handwritten neighbors.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    outputs = render_outputs(FIXTURE, _fixture_metadata_path(tmp_path), ERRORS, tmp_path / "raw")
    write_outputs(outputs)
    stale_shard = tmp_path / "raw" / "_types_shards" / "bucket_00.py"
    stale_shard.write_text("# Generated by tools/schema/generate.py; do not edit by hand.\n", encoding="utf-8")
    unowned_file = tmp_path / "raw" / "_types_shards" / "notes.py"
    unowned_file.write_text("# maintained by hand\n", encoding="utf-8")

    assert stale_shard in stale_outputs(outputs)
    assert unowned_file not in stale_outputs(outputs)
    write_outputs(outputs)
    assert not stale_shard.exists()
    assert unowned_file.exists()


def test_generation_is_deterministic_for_real_schema_slice(tmp_path) -> None:
    """Render an identical lazy raw surface for repeated fixture generations.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    metadata_path = _fixture_metadata_path(tmp_path)
    first = render_outputs(FIXTURE, metadata_path, ERRORS, tmp_path / "raw")
    second = render_outputs(FIXTURE, metadata_path, ERRORS, tmp_path / "raw")
    assert first.files == second.files
    generated_types = first.files[tmp_path / "raw" / "types.py"]
    generated_functions = first.files[tmp_path / "raw" / "functions.py"]
    generated_base = first.files[tmp_path / "raw" / "base.py"]
    assert f"RAW_API_LAYER = {FIXTURE_LAYER}" in generated_base
    assert "class TrueValue" not in generated_types
    assert "class MessagesSendMessage" not in generated_functions
    assert any(
        "class TrueValue" in content for path, content in first.files.items() if path.parent.name == "_types_shards"
    )
    assert any(
        "from_: Any | None = None" in content
        for path, content in first.files.items()
        if path.parent.name == "_types_shards"
    )
    assert any(
        "class MessagesSendMessage" in content
        for path, content in first.files.items()
        if path.parent.name == "_function_shards"
    )
    assert 'help = lazy_namespace("functions", "help")' in generated_functions


def test_generation_refreshes_rust_fast_path_schema_pins_without_changing_reviewed_selection(tmp_path: Path) -> None:
    """Refresh derived manifest pins while preserving the reviewed fast-path selection.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    schema_path = ROOT / "tools" / "schema" / "schema.json"
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    reviewed_manifest = json.loads((ROOT / "tools" / "schema" / "rust-fast-paths.json").read_text(encoding="utf-8"))
    stale_manifest = dict(reviewed_manifest)
    stale_manifest["schema_layer"] = 0
    stale_manifest["schema_json_sha256"] = "0" * 64
    manifest_path = tmp_path / "rust-fast-paths.json"
    manifest_path.write_text(json.dumps(stale_manifest, indent=2) + "\n", encoding="utf-8")

    outputs = render_outputs(
        schema_path,
        METADATA,
        ERRORS,
        tmp_path / "raw",
        manifest_path,
        tmp_path / "generated_tl.rs",
        tmp_path / "fast_metadata.py",
    )

    assert manifest_path in stale_outputs(outputs)
    refreshed_manifest = json.loads(outputs.files[manifest_path])
    assert refreshed_manifest["schema_layer"] == metadata["schema_layer"]
    assert refreshed_manifest["schema_json_sha256"] == hashlib.sha256(schema_path.read_bytes()).hexdigest()
    assert refreshed_manifest["api"] == reviewed_manifest["api"]
    assert refreshed_manifest["mtproto"] == reviewed_manifest["mtproto"]


def test_generated_committed_raw_modules_match_full_schema_metadata() -> None:
    """Keep committed generated raw, Rust and fast-path outputs fresh."""
    schema = parse_schema_file(SCHEMA)
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    outputs = render_outputs(
        ROOT / "tools" / "schema" / "schema.json",
        METADATA,
        ERRORS,
        ROOT / "src" / "miniproto" / "raw",
        ROOT / "tools" / "schema" / "rust-fast-paths.json",
        ROOT / "rust" / "miniproto" / "src" / "generated_tl.rs",
        ROOT / "src" / "miniproto" / "tl" / "fast_metadata.py",
    )
    assert not stale_outputs(outputs)
    assert BINDINGS.exists()
    bindings = json.loads(BINDINGS.read_text(encoding="utf-8"))
    assert bindings["layer"] == metadata["schema_layer"]
    assert len(bindings["declarations"]) == len(schema.constructors) + len(schema.functions)
    assert len(bindings["errors"]) == metadata["rpc_error_count"]


def test_generation_preserves_tdlib_prefix_aliases_and_decodes_to_canonical_function(tmp_path: Path) -> None:
    """Preserve TDLib prefix aliases while decoding by canonical constructor ID.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    outputs = render_outputs(
        ROOT / "tests" / "fixtures" / "schema" / "tdlib-layer228-slice.tl",
        _fixture_metadata_path(tmp_path, layer=TDLIB_FIXTURE_LAYER),
        ERRORS,
        tmp_path / "raw",
    )
    namespace: dict[str, object] = {}
    exec(  # noqa: S102 - validates generated registry source in an isolated namespace.
        compile(outputs.files[tmp_path / "raw" / "_registry.py"], str(tmp_path / "raw" / "_registry.py"), "exec"),
        namespace,
    )

    function_specs = namespace["FUNCTION_SPECS"]
    function_constructors = namespace["FUNCTION_CONSTRUCTORS"]

    assert _is_registry_specs(function_specs)
    assert _is_constructor_registry(function_constructors)
    assert "InvokeWithReCaptchaPrefix" in function_specs
    assert "InvokeWithReCaptcha" in function_specs
    assert function_constructors[0xADBB0F94] == "InvokeWithReCaptcha"


def test_binding_manifest_retains_shared_tdlib_constructor_id_aliases(tmp_path: Path) -> None:
    """Retain each TDLib prefix wrapper when several functions share one ID.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    bindings_path = tmp_path / "telegram-bindings.json"
    outputs = render_outputs(
        ROOT / "tests" / "fixtures" / "schema" / "tdlib-layer228-slice.tl",
        _fixture_metadata_path(tmp_path, layer=TDLIB_FIXTURE_LAYER),
        ERRORS,
        tmp_path / "raw",
    )

    assert bindings_path in outputs.files
    declarations = json.loads(outputs.files[bindings_path])["declarations"]
    aliases = [
        item
        for item in declarations
        if item["constructor_id"] == "0xadbb0f94"
        and item["qualified_name"] in {"invokeWithReCaptchaPrefix", "invokeWithReCaptcha"}
    ]
    assert aliases == [
        {
            "kind": "function",
            "qualified_name": "invokeWithReCaptcha",
            "constructor_id": "0xadbb0f94",
            "python_module": "miniproto.raw.functions",
            "python_name": "InvokeWithReCaptcha",
            "python_import": "from miniproto.raw.functions import InvokeWithReCaptcha",
            "public_access": "miniproto.raw.functions.InvokeWithReCaptcha",
        },
        {
            "kind": "function",
            "qualified_name": "invokeWithReCaptchaPrefix",
            "constructor_id": "0xadbb0f94",
            "python_module": "miniproto.raw.functions",
            "python_name": "InvokeWithReCaptchaPrefix",
            "python_import": "from miniproto.raw.functions import InvokeWithReCaptchaPrefix",
            "public_access": "miniproto.raw.functions.InvokeWithReCaptchaPrefix",
        },
    ]


def test_stale_generation_detection_reports_modified_output(tmp_path) -> None:
    """Report a manually modified generated output as stale.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    outputs = render_outputs(FIXTURE, _fixture_metadata_path(tmp_path), ERRORS, tmp_path / "raw")
    write_outputs(outputs)
    types_path = tmp_path / "raw" / "types.py"
    types_path.write_text(types_path.read_text(encoding="utf-8") + "\n# stale\n", encoding="utf-8")
    assert types_path in stale_outputs(outputs)


def test_generation_accepts_json_schema_and_preserves_upstream_layer_metadata(tmp_path: Path) -> None:
    """Preserve pinned provenance when rendering an equivalent JSON schema.

    Args:
        tmp_path: Isolated filesystem root supplied by pytest.
    """
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(
        """{
  "constructors": [
    {"id": "-1720552011", "predicate": "boolTrue", "params": [], "type": "Bool"}
  ],
  "methods": [
    {"id": "3304659051", "method": "help.getConfig", "params": [], "type": "Config"}
  ]
}
""",
        encoding="utf-8",
    )
    errors_path = tmp_path / "rpc-errors.json"
    errors_path.write_text(
        """{
  "errors": {"420": {"FLOOD_WAIT_%d": []}},
  "descriptions": {"FLOOD_WAIT_%d": "Please wait %d seconds before repeating the action."},
  "layer": 227
}
""",
        encoding="utf-8",
    )
    metadata_path = tmp_path / "schema-metadata.json"
    metadata_path.write_text(
        """{
  "canonical_source": "tdlib",
  "changelog_latest_layer": 225,
  "documentation_merge_precedence": ["tdlib", "tdesktop", "core_json"],
  "fetch_date": "2026-07-08",
  "layer_source_url": "https://raw.githubusercontent.com/telegramdesktop/tdesktop/refs/heads/dev/Telegram/SourceFiles/mtproto/scheme/api.tl",
  "schema_layer": 223,
  "schema_source_url": "https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl",
  "schema_tl_sha256": "tl-sha",
  "schema_tl_source_kind": "tdlib_verbatim",
  "source_note": "TDLib is canonical; Telegram Desktop supplies the validated layer.",
  "source_url": "https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl",
  "source_comparison_summary": {
    "tdlib_vs_tdesktop": {
      "changed_count": 0,
      "overlap_count": 2,
      "tdesktop_only": ["null"],
      "tdlib_only": ["invokeWithReCaptchaPrefix"]
    },
    "tdlib_vs_core": {
      "changed_count": 1,
      "core_only_count": 1,
      "overlap_count": 1,
      "tdlib_only_count": 1
    }
  },
  "sources": {"tdlib": {"declaration_count": 2}}
}
""",
        encoding="utf-8",
    )

    outputs = render_outputs(schema_path, metadata_path, errors_path, tmp_path / "raw")
    metadata = __import__("json").loads(outputs.files[metadata_path])

    assert metadata["layer"] == 223
    assert metadata["schema_layer"] == 223
    assert metadata["schema_format"] == "json"
    assert metadata["canonical_source"] == "tdlib"
    assert metadata["source_url"].endswith("td/generate/scheme/telegram_api.tl")
    assert metadata["layer_source_url"].endswith("Telegram/SourceFiles/mtproto/scheme/api.tl")
    assert metadata["documentation_merge_precedence"] == ["tdlib", "tdesktop", "core_json"]
    assert metadata["sources"] == {"tdlib": {"declaration_count": 2}}
    assert metadata["rpc_error_layer"] == 227
    assert metadata["rpc_error_download_url"] == "https://core.telegram.org/api/errors.json"
    assert metadata["changelog_latest_layer"] == 225
    assert metadata["schema_tl_source_kind"] == "tdlib_verbatim"
    assert metadata["source_comparison_summary"]["tdlib_vs_tdesktop"]["tdesktop_only"] == ["null"]
    assert "RAW_API_LAYER = 223" in outputs.files[tmp_path / "raw" / "base.py"]


def test_import_benchmark_covers_required_fresh_process_cases() -> None:
    """Keep import benchmarking focused on required fresh-process scenarios."""
    from tools.bench.benchmark_imports import CASES, summarize

    assert tuple(CASES) == ("import_miniproto", "import_client", "first_raw_attribute", "first_decode")
    summary = summarize(
        [
            {"seconds": 3.0, "retained_bytes": 30, "peak_bytes": 40, "raw_modules": ["b"]},
            {"seconds": 1.0, "retained_bytes": 10, "peak_bytes": 20, "raw_modules": ["a"]},
            {"seconds": 2.0, "retained_bytes": 20, "peak_bytes": 30, "raw_modules": ["a"]},
        ]
    )
    assert summary["median_seconds"] == 2.0
    assert summary["median_retained_bytes"] == 20
    assert summary["median_peak_bytes"] == 30
    assert summary["raw_modules"] == ["a", "b"]


def _named_schema_data(name: str, *, method: bool = False) -> dict[str, object]:
    return {
        "methods" if method else "constructors": [
            {"id": "1", "method" if method else "predicate": name, "params": [], "type": "Object"}
        ]
    }


@pytest.mark.parametrize("method", [False, True])
@pytest.mark.parametrize("formatter_available", [False, True])
@pytest.mark.parametrize("name", ["Payload[T:Any(0)]", "scope\nprint(0)\nalias.item"])
def test_cli_rejects_names_before_rendering_or_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str, method: bool, formatter_available: bool
) -> None:
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(json.dumps(_named_schema_data(name, method=method)), encoding="utf-8")
    existing_path = tmp_path / "raw" / "_types_shards" / "bucket_00.py"
    existing_path.parent.mkdir(parents=True)
    existing_path.write_text(
        "# Generated by tools/schema/generate.py\n# Preserve this existing output\n", encoding="utf-8"
    )
    original_files = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}

    def format_python(_path: Path, content: str) -> str:
        if not formatter_available:
            return content
        pytest.fail("Invalid schema names reached the formatter")

    monkeypatch.setattr(generate, "_format_python", format_python)
    with pytest.raises(TLSchemaParseError, match="invalid declaration name"):
        generate.main(
            [
                "--schema",
                str(schema_path),
                "--metadata",
                str(tmp_path / "metadata.json"),
                "--errors",
                str(tmp_path / "errors.json"),
                "--raw-dir",
                str(tmp_path / "raw"),
                "--telegram-bindings",
                str(tmp_path / "bindings.json"),
                "--rust-fast-manifest",
                str(tmp_path / "fast.json"),
                "--generated-rust",
                str(tmp_path / "generated.rs"),
                "--fast-metadata",
                str(tmp_path / "fast.py"),
            ]
        )

    assert {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()} == original_files


def test_valid_names_keep_text_json_bindings_and_safe_ast_without_ruff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    data = {
        "constructors": [
            {
                "id": "1",
                "predicate": "custom.deep.item_name",
                "params": [{"name": "from", "type": "int"}, {"name": "self", "type": "int"}],
                "type": "Object",
            },
            {"id": "2", "predicate": "true", "params": [], "type": "Bool"},
            {"id": "3", "predicate": "custom.deep.true", "params": [], "type": "Bool"},
        ],
        "methods": [{"id": "4", "method": "custom.deep.getHTTP2", "params": [], "type": "Object"}],
    }
    text = "custom.deep.item_name#00000001 from:int self:int = Object;\ntrue#00000002 = Bool;\ncustom.deep.true#00000003 = Bool;\n---functions---\ncustom.deep.getHTTP2#00000004 = Object;\n"
    json_schema = parse_schema_json(data)
    text_schema = parse_schema(text)
    expected_classes = ["CustomDeepItemName", "TrueValue", "CustomDeepTrue", "CustomDeepGetHTTP2"]
    assert [entry.python_class_name for entry in json_schema.entries] == expected_classes
    assert [entry.python_class_name for entry in text_schema.entries] == expected_classes
    assert [field.python_name for field in json_schema.entries[0].params] == ["from_", "self_"]
    assert [field.python_name for field in text_schema.entries[0].params] == ["from_", "self_"]

    def unavailable_ruff(*_args: object, **_kwargs: object) -> None:
        raise FileNotFoundError("Ruff is unavailable")

    monkeypatch.setattr(generate.subprocess, "run", unavailable_ruff)
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(json.dumps(data), encoding="utf-8")
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text('{"layer": 1}', encoding="utf-8")
    raw_dir = tmp_path / "raw"
    outputs = generate.render_outputs(schema_path, metadata_path, ROOT / "tools/schema/rpc-errors.json", raw_dir)
    collection_names: set[str] = set()
    for path, content in outputs.files.items():
        if path.suffix not in {".py", ".pyi"}:
            continue
        tree = ast.parse(content, filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                assert node.name.isidentifier() and not keyword.iskeyword(node.name)
                assert node.type_params == []
            if (
                isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id in {"ALL_TYPES", "ALL_FUNCTIONS"}
                and isinstance(node.value, ast.Tuple)
            ):
                assert all(isinstance(item, ast.Name) for item in node.value.elts)
                collection_names.update(item.id for item in node.value.elts if isinstance(item, ast.Name))
    assert collection_names == set(expected_classes)
    facade = ast.parse(outputs.files[raw_dir / "types.py"])
    namespace_assignment = next(node for node in facade.body if isinstance(node, ast.Assign))
    assert [target.id for target in namespace_assignment.targets if isinstance(target, ast.Name)] == ["custom_deep"]
    stub = ast.parse(outputs.files[raw_dir / "types.pyi"])
    namespace_class = next(node for node in stub.body if isinstance(node, ast.ClassDef) and node.name == "custom_deep")
    aliases = {
        node.targets[0].id: node.value.id
        for node in namespace_class.body
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Name)
    }
    assert aliases == {"ItemName": "CustomDeepItemName", "TrueValue": "CustomDeepTrue"}
    generate.write_outputs(outputs)
    assert generate.stale_outputs(outputs) == ()


@pytest.mark.parametrize("suffix", [".py", ".pyi"])
def test_writer_compiles_all_python_before_any_changes(tmp_path: Path, suffix: str) -> None:
    stale_path = tmp_path / "shards" / "old.py"
    stale_path.parent.mkdir()
    stale_source = "# Generated by tools/schema/generate.py\n# Keep until every replacement passes validation\n"
    stale_path.write_text(stale_source, encoding="utf-8")
    new_path = tmp_path / "first.py"
    invalid_path = tmp_path / f"invalid{suffix}"
    outputs = generate.GeneratedOutputs(
        files={new_path: "value = 1\n", invalid_path: "return 1\n"}, owned_directories=(stale_path.parent,)
    )

    with pytest.raises(SyntaxError):
        generate.write_outputs(outputs)

    assert not new_path.exists()
    assert not invalid_path.exists()
    assert stale_path.read_text(encoding="utf-8") == stale_source


def _flag_schema_data(params: list[tuple[str, str]], *, method: bool = False) -> dict[str, object]:
    return {
        "methods" if method else "constructors": [
            {
                "id": str(0x10203040),
                "method" if method else "predicate": "sample",
                "params": [{"name": name, "type": type_name} for name, type_name in params],
                "type": "Sample",
            }
        ]
    }


def _parse_flag_schema(params: list[tuple[str, str]], *, json_input: bool, method: bool = False) -> TLSchema:
    if json_input:
        return parse_schema_json(_flag_schema_data(params, method=method))
    declaration = "sample#10203040 " + " ".join(f"{name}:{type_name}" for name, type_name in params) + " = Sample;\n"
    return parse_schema(("---functions---\n" if method else "") + declaration)


@pytest.mark.parametrize("true_flag", [False, True])
def test_python_renderer_revalidates_tampered_models_before_mask_construction(true_flag: bool) -> None:
    schema = _parse_flag_schema(
        [("flags", "#"), ("value", f"flags.0?{'true' if true_flag else 'int'}")], json_input=False
    )
    field = schema.entries[0].params[1]
    object.__setattr__(field, "flag_index", 32)
    with pytest.raises(TLSchemaParseError, match=r"flag index.*0 through 31"):
        generate._render_entries_module(schema.entries, module_kind="types", fast_directions={})
    with pytest.raises(TLSchemaParseError, match=r"flag index.*0 through 31"):
        generate._codec_methods((field,), (), fast_directions=frozenset())
    with pytest.raises(TLSchemaParseError, match=r"flag index.*0 through 31"):
        rust_fast._api_fields(schema.entries[0])


def test_native_renderer_revalidates_tampered_field_descriptors() -> None:
    field = rust_fast.FastField("value", "value", "true", "true", 0, flag_group=0, flag_index=0)
    object.__setattr__(field, "flag_index", 32)
    entry = rust_fast.FastEntry(
        "api", "type", "sample", "Sample", 0x10203040, frozenset({"encode", "decode"}), (field,)
    )
    with pytest.raises(TLSchemaParseError, match=r"flag index.*0 through 31"):
        rust_fast.render_rust((entry,), 1, "0" * 64)


@pytest.mark.parametrize("json_input", [False, True])
def test_generation_rejects_invalid_schema_before_formatting_or_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, json_input: bool
) -> None:
    schema_path = tmp_path / ("schema.json" if json_input else "schema.tl")
    params = [("flags", "#"), ("value", "flags.1000000000?true")]
    content = (
        json.dumps(_flag_schema_data(params))
        if json_input
        else "sample#10203040 flags:# value:flags.1000000000?true = Sample;\n"
    )
    schema_path.write_text(content, encoding="utf-8")
    existing_path = tmp_path / "raw" / "_types_shards" / "bucket_00.py"
    existing_path.parent.mkdir(parents=True)
    existing_path.write_text("# Existing output\n", encoding="utf-8")
    before = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}

    def unexpected_render(*_args: object, **_kwargs: object) -> None:
        pytest.fail("Invalid flag index reached output rendering")

    monkeypatch.setattr(generate, "_render_shards", unexpected_render)
    monkeypatch.setattr(generate, "_format_python", unexpected_render)
    with pytest.raises(TLSchemaParseError, match=r"flag index.*0 through 31"):
        generate.render_outputs(schema_path, tmp_path / "metadata.json", tmp_path / "errors.json", tmp_path / "raw")
    assert {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()} == before


def _generated_flag_class(schema: TLSchema, monkeypatch: pytest.MonkeyPatch) -> Any:
    module = ModuleType("_optional_flags_generated")
    monkeypatch.setitem(sys.modules, module.__name__, module)
    content = generate._render_entries_module(schema.entries, module_kind="types", fast_directions={})
    exec(compile(content, "<optional-flags-generated>", "exec"), module.__dict__)  # noqa: S102 - execute only the controlled valid fixture
    return module.__dict__["Sample"]


@pytest.mark.parametrize("json_input", [False, True])
@pytest.mark.parametrize("index,word", [(0, "01000000"), (30, "00000040"), (31, "00000080")])
@pytest.mark.parametrize("true_flag", [False, True])
def test_generated_boundary_bits_match_independent_wire_bytes(
    monkeypatch: pytest.MonkeyPatch, json_input: bool, index: int, word: str, true_flag: bool
) -> None:
    schema = _parse_flag_schema(
        [("flags", "#"), ("value", f"flags.{index}?{'true' if true_flag else 'int'}")], json_input=json_input
    )
    cls = _generated_flag_class(schema, monkeypatch)
    present = cls(value=True if true_flag else -9)
    expected = bytes.fromhex("40302010" + word + ("" if true_flag else "f7ffffff"))
    assert present.serialize() == expected
    assert cls.deserialize(expected) == present
    absent = cls(value=False if true_flag else None)
    assert absent.serialize() == bytes.fromhex("4030201000000000")
    assert cls.deserialize(bytes.fromhex("4030201000000000")) == absent


def test_multiple_flags_words_keep_independent_bit31_values(monkeypatch: pytest.MonkeyPatch) -> None:
    schema = _parse_flag_schema(
        [
            ("flags", "#"),
            ("low", "flags.0?int"),
            ("high", "flags.31?true"),
            ("flags2", "#"),
            ("upper", "flags2.31?int"),
        ],
        json_input=True,
    )
    cls = _generated_flag_class(schema, monkeypatch)
    expected = bytes.fromhex("40302010 01000080 07000000 00000080 f7ffffff")
    value = cls(low=7, high=True, upper=-9)
    assert value.serialize() == expected
    assert cls.deserialize(expected) == value
    upper_absent = bytes.fromhex("40302010 01000080 07000000 00000000")
    assert replace(value, upper=None).serialize() == upper_absent
    assert cls.deserialize(upper_absent) == replace(value, upper=None)


INJECTION = 'probe", encode: false, decode: false, value_count: 99, fields: &[] }, FastConstructorSpec { constructor_id: 999, name: "extra'


def _manifest_fixture(tmp_path: Path) -> tuple[Path, Path, dict[str, Any]]:
    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"constructors": [], "methods": []}', encoding="utf-8")
    manifest = {
        "version": 1,
        "schema_layer": 1,
        "schema_json_sha256": hashlib.sha256(schema_path.read_bytes()).hexdigest(),
        "mtproto": [
            {
                "name": f"service_{index}",
                "constructor_id": hex(0x12340000 + index),
                "python_type": f"Service{index}",
                "fields": [{"name": f"value_{field}", "type": "int"} for field in range(index % 3)],
                "directions": [["encode"], ["decode"], ["encode", "decode"]][index % 3],
            }
            for index in range(30)
        ],
    }
    return schema_path, tmp_path / "fast.json", manifest


@pytest.mark.parametrize(
    "name",
    [
        None,
        17,
        True,
        "",
        'service"',
        "service'",
        "service\\",
        "service\n",
        "service\r",
        "service\x00",
        "caf\u00e9",
        "\ud800",
        ".service",
        "service.",
        "scope..service",
        "7service",
        INJECTION,
    ],
)
def test_manifest_rejects_invalid_service_names(tmp_path: Path, name: object) -> None:
    schema_path, manifest_path, manifest = _manifest_fixture(tmp_path)
    manifest["mtproto"][-1]["name"] = name
    with pytest.raises(ValueError, match="invalid Rust TL fast-path service name"):
        load_fast_entries(
            manifest_path, schema_path, 1, parse_schema_file(schema_path), manifest_text=json.dumps(manifest)
        )


@pytest.mark.parametrize("formatter_available", [False, True])
def test_cli_rejects_injection_before_formatting_or_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, formatter_available: bool
) -> None:
    schema_path, manifest_path, manifest = _manifest_fixture(tmp_path)
    manifest["mtproto"][-1]["name"] = INJECTION
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text('{"schema_layer": 1}', encoding="utf-8")
    (tmp_path / "errors.json").write_text('{"errors": {}}', encoding="utf-8")
    output_path = tmp_path / "generated.rs"
    output_path.write_text("// Keep existing output\n", encoding="utf-8")
    original_files = {path: path.read_bytes() for path in tmp_path.iterdir()}

    def format_rust(_path: Path, content: str) -> str:
        if not formatter_available:
            return content
        pytest.fail("Invalid service names reached the Rust formatter")

    monkeypatch.setattr(generate, "_format_rust", format_rust)
    monkeypatch.setattr(generate, "_format_python", lambda _path, content: content)
    with pytest.raises(ValueError, match="invalid Rust TL fast-path service name"):
        generate.main(
            [
                "--schema",
                str(schema_path),
                "--metadata",
                str(metadata_path),
                "--errors",
                str(tmp_path / "errors.json"),
                "--raw-dir",
                str(tmp_path / "raw"),
                "--telegram-bindings",
                str(tmp_path / "bindings.json"),
                "--rust-fast-manifest",
                str(manifest_path),
                "--generated-rust",
                str(output_path),
                "--fast-metadata",
                str(tmp_path / "fast.py"),
            ]
        )
    assert {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()} == original_files


def test_supported_service_names_and_reviewed_manifest_remain_accepted(tmp_path: Path) -> None:
    schema_path, manifest_path, manifest = _manifest_fixture(tmp_path)
    manifest["mtproto"][-1]["name"] = "custom.deep._Service9"
    entries = load_fast_entries(
        manifest_path, schema_path, 1, parse_schema_file(schema_path), manifest_text=json.dumps(manifest)
    )
    assert entries[-1].name == "custom.deep._Service9"
    schema_path = ROOT / "tools/schema/schema.json"
    manifest_path = ROOT / "tools/schema/rust-fast-paths.json"
    reviewed = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = load_fast_entries(manifest_path, schema_path, reviewed["schema_layer"], parse_schema_file(schema_path))
    assert len(entries) == 30
    assert [entry.name for entry in entries] == [item["name"] for item in reviewed["api"] + reviewed["mtproto"]]


def _compile_descriptor_assertions(tmp_path: Path, rustc: str, source: str, entries: tuple[FastEntry, ...]) -> None:
    """Ask Rust to compare actual descriptor values with independent UTF-8 byte arrays."""
    declarations = """
#![allow(dead_code)]
mod tl {
    pub(crate) enum FastWireType { Int }
    pub(crate) enum FastFieldSpec { Value { value: usize, wire_type: FastWireType } }
    pub(crate) struct FastConstructorSpec {
        pub(crate) constructor_id: u32,
        pub(crate) name: &'static str,
        pub(crate) encode: bool,
        pub(crate) decode: bool,
        pub(crate) value_count: usize,
        pub(crate) fields: &'static [FastFieldSpec],
    }
}
mod generated_tl {
"""
    assertions = [f"assert!(generated_tl::FAST_CONSTRUCTORS.len() == {len(entries)});"]
    for index, entry in enumerate(entries):
        expected_bytes = ", ".join(str(byte) for byte in entry.name.encode("utf-8"))
        assertions.extend(
            [
                f"let spec = &generated_tl::FAST_CONSTRUCTORS[{index}];",
                f"assert!(spec.constructor_id == {entry.constructor_id});",
                f"assert!(spec.encode == {str('encode' in entry.directions).lower()});",
                f"assert!(spec.decode == {str('decode' in entry.directions).lower()});",
                f"assert!(spec.value_count == {index % 3});",
                f"assert!(spec.fields.len() == {index % 3});",
                f"let expected: &[u8] = &[{expected_bytes}];",
                "let actual = spec.name.as_bytes();",
                "assert!(actual.len() == expected.len());",
                "let mut byte = 0;",
                "while byte < expected.len() { assert!(actual[byte] == expected[byte]); byte += 1; }",
            ]
        )
    source_path = tmp_path / "literal_check.rs"
    source_path.write_text(
        declarations + source + "}\nconst _: () = {\n" + "\n".join(assertions) + "\n};\n", encoding="utf-8"
    )
    result = subprocess.run(  # noqa: S603 - compile only the isolated fixture and harmless descriptor text
        [
            rustc,
            "--edition",
            "2024",
            "--crate-type",
            "lib",
            "--emit",
            "metadata",
            str(source_path),
            "-o",
            str(tmp_path / "literal_check.rmeta"),
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("formatter_available", [False, True])
@pytest.mark.parametrize("escape_characters", [False, True])
def test_rust_compiler_preserves_literal_values_and_descriptor_shape(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, formatter_available: bool, escape_characters: bool
) -> None:
    rustc = shutil.which("rustc")
    if rustc is None:
        pytest.skip("Rust compiler is unavailable")
    rustfmt = shutil.which("rustfmt")
    if formatter_available and rustfmt is None:
        pytest.skip("Rust formatter is unavailable")
    schema_path, manifest_path, manifest = _manifest_fixture(tmp_path)
    entries = load_fast_entries(
        manifest_path, schema_path, 1, parse_schema_file(schema_path), manifest_text=json.dumps(manifest)
    )
    names = [
        "",
        "apostrophe'",
        'double"quote',
        "both'\"\\n\\u{41}\\",
        "control\n\r\t\x00\x08\x0c\x1f\x7f",
        "unicode\u0085\u00e9\u2028\ud7ff\ue000\U0001f680\U0010ffff",
    ]
    if escape_characters:
        entries = tuple(
            replace(entry, name=names[index]) if index < len(names) else entry for index, entry in enumerate(entries)
        )
    entries = (*entries[:-1], replace(entries[-1], name=INJECTION))
    source = render_rust(entries, 1, "0" * 64)
    if formatter_available:
        assert rustfmt is not None
        formatted = subprocess.run(  # noqa: S603 - format the isolated harmless generated fixture
            [rustfmt, "--emit", "stdout", "--edition", "2024"],
            input=source,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        assert formatted.returncode == 0, formatted.stderr
        source = formatted.stdout
    else:
        monkeypatch.setattr(generate.shutil, "which", lambda _name: None)
        source = generate._format_rust(tmp_path / "generated.rs", source)
    _compile_descriptor_assertions(tmp_path, rustc, source, entries)


@pytest.mark.parametrize("surrogate", ["\ud800", "\udfff"])
def test_renderer_rejects_non_scalar_unicode(tmp_path: Path, surrogate: str) -> None:
    schema_path, manifest_path, manifest = _manifest_fixture(tmp_path)
    entries = load_fast_entries(
        manifest_path, schema_path, 1, parse_schema_file(schema_path), manifest_text=json.dumps(manifest)
    )
    with pytest.raises(ValueError, match="surrogate"):
        render_rust((replace(entries[0], name=surrogate),), 1, "0" * 64)
