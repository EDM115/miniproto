from __future__ import annotations

import tomllib
from pathlib import Path
from typing import TypeGuard

from tools.schema import generate
from tools.schema.generate import render_outputs, stale_outputs, write_outputs
from tools.schema.parser import parse_schema_file

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "tools" / "schema" / "schema.tl"
ERRORS = ROOT / "tools" / "schema" / "rpc-errors.json"
METADATA = ROOT / "tools" / "schema" / "schema-metadata.json"
FIXTURE = ROOT / "tests" / "fixtures" / "schema" / "layer223-slice.tl"


def test_generated_facade_stub_ruff_ignores_are_narrow() -> None:
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    per_file_ignores = config["tool"]["ruff"]["lint"]["per-file-ignores"]

    assert per_file_ignores["src/miniproto/raw/functions.pyi"] == ["N801"]
    assert per_file_ignores["src/miniproto/raw/types.pyi"] == ["N801", "N803", "N815"]


def _is_registry_specs(value: object) -> TypeGuard[dict[str, tuple[str, str]]]:
    return isinstance(value, dict) and all(
        isinstance(name, str)
        and isinstance(spec, tuple)
        and len(spec) == 2
        and all(isinstance(part, str) for part in spec)
        for name, spec in value.items()
    )


def _is_constructor_registry(value: object) -> TypeGuard[dict[int, str]]:
    return isinstance(value, dict) and all(
        isinstance(constructor_id, int) and isinstance(name, str) for constructor_id, name in value.items()
    )


def test_constructor_bucket_assignment_depends_only_on_id() -> None:
    assert generate._bucket_for_constructor_id(0x997275B5, 64) == 0x35
    assert generate._bucket_for_constructor_id(0x997275B5, 32) == 0x15
    assert generate._bucket_for_constructor_id(0xFFFFFFFF, 64) == 0x3F


def test_generation_emits_stable_constructor_id_shards(tmp_path: Path) -> None:
    outputs = render_outputs(
        FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", tmp_path / "raw-api.md"
    )

    assert tmp_path / "raw" / "_types_shards" / "bucket_53.py" in outputs.files
    assert tmp_path / "raw" / "_function_shards" / "bucket_13.py" in outputs.files
    assert "class BoolTrue" in outputs.files[tmp_path / "raw" / "_types_shards" / "bucket_53.py"]
    assert "class InvokeWithLayer" in outputs.files[tmp_path / "raw" / "_function_shards" / "bucket_13.py"]


def test_generation_emits_compact_registry_and_valid_python_shards(tmp_path: Path) -> None:
    outputs = render_outputs(
        FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", tmp_path / "raw-api.md"
    )

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


def test_generation_emits_compact_lazy_facades(tmp_path: Path) -> None:
    outputs = render_outputs(
        FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", tmp_path / "raw-api.md"
    )

    generated_types = outputs.files[tmp_path / "raw" / "types.py"]
    generated_functions = outputs.files[tmp_path / "raw" / "functions.py"]
    assert "class BoolTrue" not in generated_types
    assert "class InvokeWithLayer" not in generated_functions
    assert "def __getattr__(name: str)" in generated_types
    assert "def __dir__()" in generated_types
    assert "ALL_TYPES = LazyClassSequence" in generated_types
    assert "CONSTRUCTOR_ID_MAP = LazyConstructorMap" in generated_functions


def test_generated_raw_api_docs_describe_current_runtime_and_lazy_loading(tmp_path: Path) -> None:
    docs_path = tmp_path / "raw-api.md"
    outputs = render_outputs(FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", docs_path)

    docs = outputs.files[docs_path]
    assert "gzip-packed payloads, message containers, transport framing, and RPC response correlation" in docs
    assert "Facade imports stay lightweight" in docs
    assert "Requested symbols load and cache their generated shard" in docs
    assert "Mapping and sequence iteration may realize classes as needed" in docs
    assert "later runtime phases" not in docs


def test_generation_emits_public_type_stubs_and_manifest_entries(tmp_path: Path) -> None:
    outputs = render_outputs(
        FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", tmp_path / "raw-api.md"
    )

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
    outputs = render_outputs(
        FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", tmp_path / "raw-api.md"
    )
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
    first = render_outputs(
        FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", tmp_path / "raw-api.md"
    )
    second = render_outputs(
        FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", tmp_path / "raw-api.md"
    )
    assert first.files == second.files
    generated_types = first.files[tmp_path / "raw" / "types.py"]
    generated_functions = first.files[tmp_path / "raw" / "functions.py"]
    generated_base = first.files[tmp_path / "raw" / "base.py"]
    assert "RAW_API_LAYER = 214" in generated_base
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


def test_generated_committed_raw_modules_match_full_schema_metadata() -> None:
    schema = parse_schema_file(SCHEMA)
    metadata = __import__("json").loads(METADATA.read_text(encoding="utf-8"))
    assert metadata["schema_layer"] == 223
    assert metadata["changelog_latest_layer"] == 225
    assert metadata["rpc_error_layer"] == 227
    outputs = render_outputs(
        ROOT / "tools" / "schema" / "schema.json",
        METADATA,
        ERRORS,
        ROOT / "src" / "miniproto" / "raw",
        ROOT / "docs" / "raw-api.md",
    )
    assert not stale_outputs(outputs)
    assert len(schema.constructors) == 1546
    assert len(schema.functions) == 757


def test_stale_generation_detection_reports_modified_output(tmp_path) -> None:
    outputs = render_outputs(
        FIXTURE, tmp_path / "schema-metadata.json", ERRORS, tmp_path / "raw", tmp_path / "raw-api.md"
    )
    write_outputs(outputs)
    types_path = tmp_path / "raw" / "types.py"
    types_path.write_text(types_path.read_text(encoding="utf-8") + "\n# stale\n", encoding="utf-8")
    assert types_path in stale_outputs(outputs)


def test_generation_accepts_json_schema_and_preserves_upstream_layer_metadata(tmp_path: Path) -> None:
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
  "changelog_latest_layer": 225,
  "fetch_date": "2026-07-08",
  "schema_layer": 223,
  "schema_tl_sha256": "tl-sha",
  "schema_tl_source_kind": "json_derived"
}
""",
        encoding="utf-8",
    )

    outputs = render_outputs(schema_path, metadata_path, errors_path, tmp_path / "raw", tmp_path / "raw-api.md")
    metadata = __import__("json").loads(outputs.files[metadata_path])

    assert metadata["layer"] == 223
    assert metadata["schema_layer"] == 223
    assert metadata["schema_format"] == "json"
    assert metadata["source_url"] == "https://core.telegram.org/schema/json"
    assert metadata["rpc_error_layer"] == 227
    assert metadata["rpc_error_download_url"] == "https://core.telegram.org/api/errors.json"
    assert metadata["changelog_latest_layer"] == 225
    assert metadata["schema_tl_source_kind"] == "json_derived"
    assert "RAW_API_LAYER = 223" in outputs.files[tmp_path / "raw" / "base.py"]
    assert "Telegram Schema Layer 223" in outputs.files[tmp_path / "raw-api.md"]
    assert "RPC errors layer: 227" in outputs.files[tmp_path / "raw-api.md"]


def test_import_benchmark_covers_required_fresh_process_cases() -> None:
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
