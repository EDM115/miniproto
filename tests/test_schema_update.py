from __future__ import annotations

import json
import subprocess
import urllib.error
from pathlib import Path

from tools.schema import update as schema_update
from tools.schema.update import build_upstream_snapshot, render_pinned_files, stale_pinned_files

SCHEMA_JSON = b"""{
  "constructors": [
    {"id": "-1720552011", "predicate": "boolTrue", "params": [], "type": "Bool"}
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


def test_update_snapshot_uses_schema_json_and_extracts_tl_from_schema_html() -> None:
    def fetch_url(url: str) -> bytes:
        return {
            "https://core.telegram.org/schema/json": SCHEMA_JSON,
            "https://core.telegram.org/schema": SCHEMA_HTML_WITH_TL,
            "https://core.telegram.org/api/errors.json": ERRORS_JSON,
            "https://core.telegram.org/api/layers": LAYERS_HTML,
        }[url]

    snapshot = build_upstream_snapshot(fetch_url=fetch_url, fetch_date="2026-07-08")
    files = render_pinned_files(snapshot, root=Path("repo"))
    metadata = json.loads(files[Path("repo/tools/schema/schema-metadata.json")])

    assert files[Path("repo/tools/schema/schema.json")].startswith("{\n")
    assert "boolTrue#997275b5 = Bool;" in files[Path("repo/tools/schema/schema.tl")]
    assert metadata["schema_layer"] == 223
    assert metadata["changelog_latest_layer"] == 225
    assert metadata["rpc_error_layer"] == 227
    assert metadata["schema_format"] == "json"
    assert metadata["schema_tl_source_kind"] == "html_extracted"


def test_update_snapshot_derives_tl_from_json_when_html_has_no_raw_schema() -> None:
    def fetch_url(url: str) -> bytes:
        return {
            "https://core.telegram.org/schema/json": SCHEMA_JSON,
            "https://core.telegram.org/schema": SCHEMA_HTML_WITHOUT_TL,
            "https://core.telegram.org/api/errors.json": ERRORS_JSON,
            "https://core.telegram.org/api/layers": LAYERS_HTML,
        }[url]

    snapshot = build_upstream_snapshot(fetch_url=fetch_url, fetch_date="2026-07-08")

    assert snapshot.schema_tl_source_kind == "json_derived"
    assert (
        snapshot.schema_tl_text
        == "boolTrue#997275b5 = Bool;\n---functions---\nhelp.getConfig#c4f9186b = Config;\n"
    )


def test_stale_pinned_files_reports_only_changed_inputs(tmp_path: Path) -> None:
    def fetch_url(url: str) -> bytes:
        return {
            "https://core.telegram.org/schema/json": SCHEMA_JSON,
            "https://core.telegram.org/schema": SCHEMA_HTML_WITH_TL,
            "https://core.telegram.org/api/errors.json": ERRORS_JSON,
            "https://core.telegram.org/api/layers": LAYERS_HTML,
        }[url]

    snapshot = build_upstream_snapshot(fetch_url=fetch_url, fetch_date="2026-07-08")
    files = render_pinned_files(snapshot, root=tmp_path)
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    assert stale_pinned_files(files) == ()
    (tmp_path / "tools/schema/rpc-errors.json").write_text("{}\n", encoding="utf-8")
    assert stale_pinned_files(files) == (tmp_path / "tools/schema/rpc-errors.json",)


def test_stale_pinned_files_ignores_metadata_fetch_date(tmp_path: Path) -> None:
    def fetch_url(url: str) -> bytes:
        return {
            "https://core.telegram.org/schema/json": SCHEMA_JSON,
            "https://core.telegram.org/schema": SCHEMA_HTML_WITH_TL,
            "https://core.telegram.org/api/errors.json": ERRORS_JSON,
            "https://core.telegram.org/api/layers": LAYERS_HTML,
        }[url]

    snapshot = build_upstream_snapshot(fetch_url=fetch_url, fetch_date="2026-07-08")
    files = render_pinned_files(snapshot, root=tmp_path)
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    metadata_path = tmp_path / "tools/schema/schema-metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["fetch_date"] = "2026-07-09"
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    assert stale_pinned_files(files) == ()


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
