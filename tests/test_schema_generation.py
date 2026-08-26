"""Verify deterministic schema generation, ownership and freshness behavior."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import TypeGuard

import pytest
from tools.schema import generate
from tools.schema.generate import render_outputs, stale_outputs, write_outputs
from tools.schema.parser import parse_schema_file

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
