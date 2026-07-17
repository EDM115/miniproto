from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from tools.schema.parser import TLSchemaParseError, parse_schema, parse_schema_json, schema_to_tl

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCHEMA_JSON_URL = "https://core.telegram.org/schema/json"
_SCHEMA_DOC_URL = "https://core.telegram.org/schema"
_ERRORS_JSON_URL = "https://core.telegram.org/api/errors.json"
_ERRORS_DOC_URL = "https://core.telegram.org/api/errors"
_LAYERS_URL = "https://core.telegram.org/api/layers"
_USER_AGENT = "Mozilla/5.0 miniproto-schema-updater"
_ALLOWED_FETCH_URLS = frozenset({_SCHEMA_JSON_URL, _SCHEMA_DOC_URL, _ERRORS_JSON_URL, _LAYERS_URL})


@dataclass(frozen=True, slots=True)
class UpstreamSchemaSnapshot:
    schema_json: Mapping[str, Any]
    schema_tl_text: str
    schema_tl_source_kind: str
    rpc_errors: Mapping[str, Any]
    schema_layer: int
    changelog_latest_layer: int | None
    fetch_date: str


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update pinned Telegram schema inputs.")
    parser.add_argument(
        "--check-upstream", action="store_true", help="fetch upstream and fail when pinned schema inputs are stale"
    )
    args = parser.parse_args(argv)

    snapshot = build_upstream_snapshot()
    files = render_pinned_files(snapshot, root=_REPO_ROOT)
    stale = stale_pinned_files(files)
    if args.check_upstream:
        if stale:
            for path in stale:
                print(f"stale pinned schema input: {path}")
            return 1
        print("pinned schema inputs match upstream")
        return 0
    write_pinned_files(files)
    print(
        "updated pinned schema inputs "
        f"schema_layer={snapshot.schema_layer} "
        f"rpc_error_layer={snapshot.rpc_errors.get('layer')} "
        f"changelog_latest_layer={snapshot.changelog_latest_layer} "
        f"tl_source={snapshot.schema_tl_source_kind}"
    )
    return 0


def build_upstream_snapshot(
    *, fetch_url: Callable[[str], bytes] | None = None, fetch_date: str | None = None
) -> UpstreamSchemaSnapshot:
    fetch = _fetch_url if fetch_url is None else fetch_url
    schema_json = _load_json(fetch(_SCHEMA_JSON_URL), source=_SCHEMA_JSON_URL)
    rpc_errors = _load_json(fetch(_ERRORS_JSON_URL), source=_ERRORS_JSON_URL)
    schema_html = fetch(_SCHEMA_DOC_URL).decode("utf-8", errors="replace")
    layers_html = fetch(_LAYERS_URL).decode("utf-8", errors="replace")
    schema_layer = _extract_schema_layer(schema_html)
    if schema_layer is None:
        raise RuntimeError("could not determine schema layer from Telegram schema page")
    schema_tl_text, schema_tl_source_kind = _schema_tl_from_html_or_json(schema_html, schema_json)
    return UpstreamSchemaSnapshot(
        schema_json=schema_json,
        schema_tl_text=schema_tl_text,
        schema_tl_source_kind=schema_tl_source_kind,
        rpc_errors=rpc_errors,
        schema_layer=schema_layer,
        changelog_latest_layer=_extract_changelog_latest_layer(layers_html),
        fetch_date=fetch_date or date.today().isoformat(),
    )


def render_pinned_files(snapshot: UpstreamSchemaSnapshot, *, root: Path) -> dict[Path, str]:
    schema_json_text = _json_document(snapshot.schema_json)
    rpc_errors_text = _json_document(snapshot.rpc_errors)
    schema_tl_text = (
        snapshot.schema_tl_text if snapshot.schema_tl_text.endswith("\n") else snapshot.schema_tl_text + "\n"
    )
    metadata = {
        "layer": snapshot.schema_layer,
        "schema_layer": snapshot.schema_layer,
        "changelog_latest_layer": snapshot.changelog_latest_layer,
        "source_url": _SCHEMA_JSON_URL,
        "schema_source_url": _SCHEMA_JSON_URL,
        "schema_doc_url": _SCHEMA_DOC_URL,
        "source_note": "Official Telegram JSON schema fetched from core.telegram.org/schema/json and pinned in tools/schema/schema.json; tools/schema/schema.tl is kept as a mirror for review and interoperability.",
        "fetch_date": snapshot.fetch_date,
        "sha256": _sha256_text(schema_json_text),
        "schema_sha256": _sha256_text(schema_json_text),
        "schema_json_sha256": _sha256_text(schema_json_text),
        "schema_tl_sha256": _sha256_text(schema_tl_text),
        "schema_tl_source_kind": snapshot.schema_tl_source_kind,
        "schema_format": "json",
        "generator_version": "3",
        "constructor_count": len(snapshot.schema_json.get("constructors", ())),
        "function_count": len(snapshot.schema_json.get("methods", ())),
        "rpc_error_source_url": _ERRORS_DOC_URL,
        "rpc_error_download_url": _ERRORS_JSON_URL,
        "rpc_error_layer": snapshot.rpc_errors.get("layer"),
        "rpc_error_sha256": _sha256_text(rpc_errors_text),
        "rpc_error_count": _rpc_error_count(snapshot.rpc_errors),
        "changelog_source_url": _LAYERS_URL,
        "generated_file_manifest": [
            "src/miniproto/raw/base.py",
            "src/miniproto/raw/types.py",
            "src/miniproto/raw/types.pyi",
            "src/miniproto/raw/functions.py",
            "src/miniproto/raw/functions.pyi",
            "src/miniproto/raw/_registry.py",
            "src/miniproto/raw/_types_shards/*.py",
            "src/miniproto/raw/_function_shards/*.py",
            "src/miniproto/raw/errors.py",
            "docs/raw-api.md",
        ],
    }
    return {
        root / "tools/schema/schema.json": schema_json_text,
        root / "tools/schema/schema.tl": schema_tl_text,
        root / "tools/schema/rpc-errors.json": rpc_errors_text,
        root / "tools/schema/schema-metadata.json": _json_document(metadata),
    }


def write_pinned_files(files: Mapping[Path, str]) -> None:
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def stale_pinned_files(files: Mapping[Path, str]) -> tuple[Path, ...]:
    stale: list[Path] = []
    for path, expected in files.items():
        if not path.exists() or not _pinned_file_matches(path, expected):
            stale.append(path)
    return tuple(stale)


def _pinned_file_matches(path: Path, expected: str) -> bool:
    actual = path.read_text(encoding="utf-8")
    if path.name != "schema-metadata.json":
        return actual == expected
    actual_metadata = json.loads(actual)
    expected_metadata = json.loads(expected)
    if not isinstance(actual_metadata, dict) or not isinstance(expected_metadata, dict):
        return actual == expected
    actual_metadata.pop("fetch_date", None)
    expected_metadata.pop("fetch_date", None)
    return actual_metadata == expected_metadata


def _fetch_url(url: str) -> bytes:
    if url not in _ALLOWED_FETCH_URLS:
        raise ValueError(f"refusing to fetch non-allowlisted schema URL: {url}")
    delay = 0.5
    last_error: Exception | None = None
    for _attempt in range(4):
        request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})  # noqa: S310 - URL is checked against the hard-coded Telegram allowlist above.
        try:
            with urllib.request.urlopen(request, timeout=45) as response:  # noqa: S310 - URL is checked against the hard-coded Telegram allowlist above.
                return response.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            time.sleep(delay)
            delay *= 2
    curl_payload = _fetch_url_with_curl(url)
    if curl_payload is not None:
        return curl_payload
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"could not fetch {url}")


def _fetch_url_with_curl(url: str) -> bytes | None:
    curl = shutil.which("curl")
    if curl is None:
        return None
    result = subprocess.run(  # noqa: S603 - URL is checked against the hard-coded Telegram allowlist and curl path is resolved.
        [
            curl,
            "--fail",
            "--location",
            "--silent",
            "--show-error",
            "--connect-timeout",
            "15",
            "--max-time",
            "60",
            "--retry",
            "3",
            "--retry-delay",
            "1",
            "--user-agent",
            _USER_AGENT,
            url,
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout
    return None


def _load_json(payload: bytes, *, source: str) -> Mapping[str, Any]:
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{source} must return a JSON object")
    return data


def _schema_tl_from_html_or_json(schema_html: str, schema_json: Mapping[str, Any]) -> tuple[str, str]:
    extracted = _extract_tl_schema_from_html(schema_html)
    if extracted is not None:
        return extracted, "html_extracted"
    return schema_to_tl(parse_schema_json(schema_json)), "json_derived"


def _extract_tl_schema_from_html(schema_html: str) -> str | None:
    for pattern in (r"<pre[^>]*>(.*?)</pre>", r"<textarea[^>]*>(.*?)</textarea>"):
        for match in re.finditer(pattern, schema_html, flags=re.DOTALL | re.IGNORECASE):
            candidate = html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()
            if "#" not in candidate or " = " not in candidate:
                continue
            if "---functions---" not in candidate:
                continue
            try:
                parse_schema(candidate)
            except TLSchemaParseError:
                continue
            return candidate + "\n"
    return None


def _extract_schema_layer(schema_html: str) -> int | None:
    layers = _extract_layers(schema_html)
    return max(layers) if layers else None


def _extract_changelog_latest_layer(layers_html: str) -> int | None:
    layers = _extract_layers(layers_html)
    return max(layers) if layers else None


def _extract_layers(text: str) -> tuple[int, ...]:
    values = {int(value) for value in re.findall(r"\bLayer\s+(\d+)\b", text, flags=re.IGNORECASE)}
    values.update(int(value) for value in re.findall(r'id=["\']layer-(\d+)["\']', text))
    return tuple(sorted(values))


def _rpc_error_count(database: Mapping[str, Any]) -> int:
    errors = database.get("errors", {})
    if not isinstance(errors, Mapping):
        return 0
    return sum(len(named_errors) for named_errors in errors.values() if isinstance(named_errors, Mapping))


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _json_document(data: Mapping[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
