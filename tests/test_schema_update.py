from __future__ import annotations

import json
import subprocess
import urllib.error
from pathlib import Path

import pytest
from tools.schema import update as schema_update
from tools.schema.update import build_upstream_snapshot, render_pinned_files, stale_pinned_files, write_pinned_files

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_JSON = b"""{
  "constructors": [
    {"id": "-1720552011", "predicate": "boolTrue", "params": [], "type": "Bool", "description": "Core description."}
  ],
  "methods": [
    {"id": "3304659051", "method": "help.getConfig", "params": [], "type": "Config"}
  ]
}
"""
ERRORS_JSON = b"""{
  "errors": {"420": {"FLOOD_WAIT_%d": []}},
  "descriptions": {"FLOOD_WAIT_%d": "Please wait %d seconds before repeating the action."},
  "layer": 227
}
"""
SCHEMA_HTML_WITH_TL = b"""<html><body>
<h3><a id="layer-223"></a>Layer 223</h3>
<pre>boolTrue#997275b5 = Bool;
---functions---
help.getConfig#c4f9186b = Config;</pre>
</body></html>
"""
SCHEMA_HTML_WITHOUT_TL = b"""<html><body><h3><a id="layer-223"></a>Layer 223</h3></body></html>"""
LAYERS_HTML = b"""<html><body><h3><a id="layer-225"></a>Layer 225</h3></body></html>"""
TDESKTOP_TL = b"""boolTrue#997275b5 = Bool;
null#56730bcc = Null;
---functions---
help.getConfig#c4f9186b = Config;
// LAYER 228
"""
TDLIB_TL = b"""int ? = Int;
long ? = Long;
double ? = Double;
string ? = String;
bytes = Bytes;
int256 = Int256;
// @description TDLib description.
boolTrue#997275b5 = Bool;
inputPeerPhotoFileLocationLegacy#27d69997 flags:# big:flags.0?true peer:InputPeer volume_id:long local_id:int = InputFileLocation;
---functions---
test.useConfigSimple = help.ConfigSimple;
test.parseInputAppEvent = InputAppEvent;
help.getConfig#c4f9186b = Config;
ephemeral.editMessage#13f250ee peer:InputPeer id:int = Updates;
"""


def _upstream_payloads(*, schema_html: bytes = SCHEMA_HTML_WITH_TL) -> dict[str, bytes]:
    return {
        "https://raw.githubusercontent.com/telegramdesktop/tdesktop/refs/heads/dev/Telegram/SourceFiles/mtproto/scheme/api.tl": TDESKTOP_TL,
        "https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl": TDLIB_TL,
        "https://core.telegram.org/schema/json": SCHEMA_JSON,
        "https://core.telegram.org/schema": schema_html,
        "https://core.telegram.org/api/errors.json": ERRORS_JSON,
        "https://core.telegram.org/api/layers": LAYERS_HTML,
    }


def test_update_snapshot_uses_schema_json_and_extracts_tl_from_schema_html() -> None:
    def fetch_url(url: str) -> bytes:
        return _upstream_payloads()[url]

    snapshot = build_upstream_snapshot(fetch_url=fetch_url, fetch_date="2026-07-08")
    files = render_pinned_files(snapshot, root=Path("repo"))
    metadata = json.loads(files[Path("repo/tools/schema/schema-metadata.json")])

    canonical = json.loads(files[Path("repo/tools/schema/schema.json")])
    assert canonical["constructors"][0]["description"] == "TDLib description."
    assert files[Path("repo/tools/schema/schema.tl")] == TDLIB_TL.decode()
    assert files[Path("repo/tools/schema/schema-tdesktop.tl")] == TDESKTOP_TL.decode()
    assert files[Path("repo/tools/schema/schema-core.json")] == SCHEMA_JSON.decode()
    assert "boolTrue#997275b5 = Bool;" in files[Path("repo/tools/schema/schema.tl")]
    assert metadata["schema_layer"] == 228
    assert metadata["canonical_source"] == "tdlib"
    assert metadata["structural_source_url"].endswith("td/generate/scheme/telegram_api.tl")
    assert metadata["layer_source_url"].endswith("Telegram/SourceFiles/mtproto/scheme/api.tl")
    assert metadata["changelog_latest_layer"] == 225
    assert metadata["rpc_error_layer"] == 227
    assert metadata["schema_format"] == "json"
    assert metadata["schema_tl_source_kind"] == "tdlib_verbatim"
    assert metadata["source_comparison_summary"]["tdlib_vs_tdesktop"] == {
        "changed_count": 0,
        "overlap_count": 2,
        "tdesktop_only": ["null"],
        "tdlib_only": ["ephemeral.editMessage", "inputPeerPhotoFileLocationLegacy"],
    }
    assert metadata["source_comparison_summary"]["tdlib_vs_core"] == {
        "changed_count": 0,
        "core_only_count": 0,
        "overlap_count": 2,
        "tdlib_only_count": 2,
    }
    source_diff = json.loads(files[Path("repo/tools/schema/schema-source-diff.json")])
    assert source_diff["tdlib_vs_tdesktop"]["changed"] == []
    assert source_diff["tdlib_vs_tdesktop"]["tdlib_only"] == [
        "ephemeral.editMessage",
        "inputPeerPhotoFileLocationLegacy",
    ]
    assert source_diff["tdlib_vs_tdesktop"]["tdesktop_only"] == ["null"]


def test_update_snapshot_derives_tl_from_json_when_html_has_no_raw_schema() -> None:
    def fetch_url(url: str) -> bytes:
        return _upstream_payloads(schema_html=SCHEMA_HTML_WITHOUT_TL)[url]

    snapshot = build_upstream_snapshot(fetch_url=fetch_url, fetch_date="2026-07-08")

    assert snapshot.core_schema_tl_source_kind == "json_derived"
    assert (
        snapshot.core_schema_tl_text
        == "boolTrue#997275b5 = Bool;\n---functions---\nhelp.getConfig#c4f9186b = Config;\n"
    )


def test_update_preserves_tdlib_pin_without_adding_a_trailing_newline() -> None:
    payloads = _upstream_payloads()
    payloads[next(url for url in payloads if "tdlib" in url)] = TDLIB_TL.rstrip(b"\n")

    snapshot = build_upstream_snapshot(fetch_url=payloads.__getitem__, fetch_date="2026-08-12")
    files = render_pinned_files(snapshot, root=Path("repo"))

    assert files[Path("repo/tools/schema/schema.tl")] == TDLIB_TL.decode().rstrip("\n")


def test_update_metadata_source_note_uses_validated_dynamic_layer() -> None:
    payloads = _upstream_payloads()
    payloads[next(url for url in payloads if "tdesktop" in url)] = TDESKTOP_TL.replace(b"LAYER 228", b"LAYER 229")

    snapshot = build_upstream_snapshot(fetch_url=payloads.__getitem__, fetch_date="2026-08-12")
    files = render_pinned_files(snapshot, root=Path("repo"))
    metadata = json.loads(files[Path("repo/tools/schema/schema-metadata.json")])

    assert metadata["schema_layer"] == 229
    assert "Layer 229" in metadata["source_note"]


def test_check_upstream_writes_source_specific_report_without_updating_pins(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    snapshot = build_upstream_snapshot(fetch_url=_upstream_payloads().__getitem__, fetch_date="2026-08-12")
    report_path = tmp_path / "artifacts" / "schema-upstream-report.json"
    monkeypatch.setattr(schema_update, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr(schema_update, "build_upstream_snapshot", lambda: snapshot)

    result = schema_update.main(["--check-upstream", "--report", str(report_path)])

    assert result == 1
    assert not (tmp_path / "tools/schema/schema.tl").exists()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["schema_layer"] == 228
    assert report["sources"]["tdlib"]["role"] == "canonical_structure"
    assert report["comparisons"]["tdlib_vs_tdesktop"]["changed"] == []
    assert "tools/schema/schema.tl" in report["stale_pinned_inputs"]


def test_stale_pinned_files_reports_only_changed_inputs(tmp_path: Path) -> None:
    def fetch_url(url: str) -> bytes:
        return _upstream_payloads()[url]

    snapshot = build_upstream_snapshot(fetch_url=fetch_url, fetch_date="2026-07-08")
    files = render_pinned_files(snapshot, root=tmp_path)
    write_pinned_files(files)

    assert stale_pinned_files(files) == ()
    (tmp_path / "tools/schema/rpc-errors.json").write_text("{}\n", encoding="utf-8")
    assert stale_pinned_files(files) == (tmp_path / "tools/schema/rpc-errors.json",)


def test_stale_pinned_files_ignores_metadata_fetch_date(tmp_path: Path) -> None:
    def fetch_url(url: str) -> bytes:
        return _upstream_payloads()[url]

    snapshot = build_upstream_snapshot(fetch_url=fetch_url, fetch_date="2026-07-08")
    files = render_pinned_files(snapshot, root=tmp_path)
    write_pinned_files(files)

    metadata_path = tmp_path / "tools/schema/schema-metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["fetch_date"] = "2026-07-09"
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    assert stale_pinned_files(files) == ()


def test_volatile_core_page_generation_timing_does_not_change_pinned_metadata() -> None:
    first_payloads = _upstream_payloads()
    second_payloads = _upstream_payloads()
    for payloads, timing in ((first_payloads, b"10.25"), (second_payloads, b"987.60")):
        for url in ("https://core.telegram.org/schema", "https://core.telegram.org/api/layers"):
            payloads[url] += b"\n<!-- page generated in " + timing + b"ms -->\n"

    first = build_upstream_snapshot(fetch_url=first_payloads.__getitem__, fetch_date="2026-08-12")
    second = build_upstream_snapshot(fetch_url=second_payloads.__getitem__, fetch_date="2026-08-12")

    assert first.source_metadata == second.source_metadata
    assert first.source_metadata["core_schema_page"]["normalization"] == "trailing_page_generation_timing_removed"
    assert first.source_metadata["layer_changelog"]["normalization"] == "trailing_page_generation_timing_removed"


def test_update_rejects_tdesktop_layer_marker_that_is_not_at_eof() -> None:
    payloads = _upstream_payloads()
    payloads[next(url for url in payloads if "tdesktop" in url)] = TDESKTOP_TL + b"boolFalse#bc799737 = Bool;\n"

    with pytest.raises(RuntimeError, match="end-of-file LAYER marker"):
        build_upstream_snapshot(fetch_url=payloads.__getitem__, fetch_date="2026-08-12")


def test_update_rejects_changed_tdlib_tdesktop_overlap() -> None:
    payloads = _upstream_payloads()
    payloads[next(url for url in payloads if "tdesktop" in url)] = TDESKTOP_TL.replace(
        b"help.getConfig#c4f9186b = Config;", b"help.getConfig#c4f9186b hash:long = Config;"
    )

    with pytest.raises(RuntimeError, match="TDLib and Telegram Desktop disagree"):
        build_upstream_snapshot(fetch_url=payloads.__getitem__, fetch_date="2026-08-12")


def test_fetch_url_falls_back_to_curl_after_urllib_failures(monkeypatch) -> None:
    def fail_urlopen(*_args, **_kwargs):
        raise urllib.error.URLError("reset")

    def fake_run(args, **kwargs):
        assert args[-1] == "https://core.telegram.org/schema"
        assert kwargs["capture_output"] is True
        assert kwargs["check"] is False
        return subprocess.CompletedProcess(args, 0, stdout=b"schema html", stderr=b"")

    monkeypatch.setattr(schema_update.urllib.request, "urlopen", fail_urlopen)
    monkeypatch.setattr(schema_update.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(schema_update.shutil, "which", lambda command: command)
    monkeypatch.setattr(schema_update.subprocess, "run", fake_run)

    assert schema_update._fetch_url("https://core.telegram.org/schema") == b"schema html"


def test_upstream_schema_workflow_is_scheduled_manual_and_uploads_report() -> None:
    workflow = (ROOT / ".github/workflows/schema-upstream.yml").read_text(encoding="utf-8")

    assert "schedule:" in workflow
    assert "workflow_dispatch:" in workflow
    assert "python -m tools.schema.update --check-upstream --report" in workflow
    assert "actions/upload-artifact@v4" in workflow
    assert "if: always()" in workflow
