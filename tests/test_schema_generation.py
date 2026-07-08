from __future__ import annotations

from pathlib import Path

from tools.schema.generate import render_outputs, stale_outputs, write_outputs
from tools.schema.parser import parse_schema_file

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "tools" / "schema" / "schema.tl"
ERRORS = ROOT / "tools" / "schema" / "rpc-errors.json"
METADATA = ROOT / "tools" / "schema" / "schema-metadata.json"
FIXTURE = ROOT / "tests" / "fixtures" / "schema" / "layer223-slice.tl"


def test_generation_is_deterministic_for_real_schema_slice(tmp_path) -> None:
    first = render_outputs(
        FIXTURE,
        tmp_path / "schema-metadata.json",
        ERRORS,
        tmp_path / "raw",
        tmp_path / "raw-api.md",
    )
    second = render_outputs(
        FIXTURE,
        tmp_path / "schema-metadata.json",
        ERRORS,
        tmp_path / "raw",
        tmp_path / "raw-api.md",
    )
    assert first.files == second.files
    generated_types = first.files[tmp_path / "raw" / "types.py"]
    generated_functions = first.files[tmp_path / "raw" / "functions.py"]
    generated_base = first.files[tmp_path / "raw" / "base.py"]
    assert "RAW_API_LAYER = 214" in generated_base
    assert "class TrueValue" in generated_types
    assert "from_: Any | None = None" in generated_types
    assert "class MessagesSendMessage" in generated_functions
    assert "class help:" in generated_functions
    assert "GetConfig = HelpGetConfig" in generated_functions


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
        FIXTURE,
        tmp_path / "schema-metadata.json",
        ERRORS,
        tmp_path / "raw",
        tmp_path / "raw-api.md",
    )
    write_outputs(outputs)
    types_path = tmp_path / "raw" / "types.py"
    types_path.write_text(types_path.read_text(encoding="utf-8") + "\n# stale\n", encoding="utf-8")
    assert types_path in stale_outputs(outputs)


def test_generation_accepts_json_schema_and_preserves_upstream_layer_metadata(
    tmp_path: Path,
) -> None:
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

    outputs = render_outputs(
        schema_path, metadata_path, errors_path, tmp_path / "raw", tmp_path / "raw-api.md"
    )
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
