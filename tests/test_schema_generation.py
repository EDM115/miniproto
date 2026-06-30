from __future__ import annotations

from pathlib import Path

from tools.schema.generate import render_outputs, stale_outputs, write_outputs
from tools.schema.parser import parse_schema_file

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "tools" / "schema" / "schema.tl"
ERRORS = ROOT / "tools" / "schema" / "rpc-errors.json"
METADATA = ROOT / "tools" / "schema" / "schema-metadata.json"
FIXTURE = ROOT / "tests" / "fixtures" / "schema" / "layer214-slice.tl"


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
    assert "class TrueValue" in generated_types
    assert "from_: Any | None = None" in generated_types
    assert "class MessagesSendMessage" in generated_functions
    assert "class help:" in generated_functions
    assert "GetConfig = HelpGetConfig" in generated_functions


def test_generated_committed_raw_modules_match_full_schema_metadata() -> None:
    schema = parse_schema_file(SCHEMA)
    assert int(METADATA.read_text(encoding="utf-8").split('"layer": ')[1].split(",", 1)[0]) == 214
    outputs = render_outputs(
        SCHEMA, METADATA, ERRORS, ROOT / "src" / "miniproto" / "raw", ROOT / "docs" / "raw-api.md"
    )
    assert not stale_outputs(outputs)
    assert len(schema.constructors) == 1479
    assert len(schema.functions) == 727


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
