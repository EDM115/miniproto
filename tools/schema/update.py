"""Fetch, validate, normalize, compare and pin upstream Telegram schema sources."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from tools.schema.parser import (
    TLEntry,
    TLParameter,
    TLSchema,
    TLSchemaParseError,
    parse_schema,
    parse_schema_json,
    schema_to_tl,
)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCHEMA_JSON_URL = "https://core.telegram.org/schema/json"
_SCHEMA_DOC_URL = "https://core.telegram.org/schema"
_ERRORS_JSON_URL = "https://core.telegram.org/api/errors.json"
_ERRORS_DOC_URL = "https://core.telegram.org/api/errors"
_LAYERS_URL = "https://core.telegram.org/api/layers"
_TDESKTOP_SCHEMA_URL = "https://raw.githubusercontent.com/telegramdesktop/tdesktop/refs/heads/dev/Telegram/SourceFiles/mtproto/scheme/api.tl"
_TDLIB_SCHEMA_URL = "https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl"
_USER_AGENT = "Mozilla/5.0 miniproto-schema-updater"
_PAGE_GENERATION_TIMING_RE = re.compile(rb"\r?\n?<!-- page generated in \d+(?:\.\d+)?ms -->\s*\Z")
_ALLOWED_FETCH_URLS = frozenset(
    {_SCHEMA_JSON_URL, _SCHEMA_DOC_URL, _ERRORS_JSON_URL, _LAYERS_URL, _TDESKTOP_SCHEMA_URL, _TDLIB_SCHEMA_URL}
)


@dataclass(frozen=True, slots=True)
class UpstreamSchemaSnapshot:
    """Validated upstream schema sources, normalized artifacts and provenance for one update.

    Attributes:
        schema_json: Normalized schema mapping structurally derived from the canonical TDLib declarations with merged documentation.
        schema_tl_text: Verbatim UTF-8 TL text fetched from the canonical TDLib structural source.
        schema_tl_source_kind: Provenance tag for ``schema_tl_text``; the current snapshot uses ``"tdlib_verbatim"``.
        tdesktop_tl_text: Verbatim UTF-8 Telegram Desktop TL text used for the layer marker and supporting documentation.
        core_schema_json: Decoded core.telegram.org schema JSON used for supporting documentation and drift comparison.
        core_schema_json_text: Original UTF-8 core schema JSON text retained for deterministic pinning.
        core_schema_tl_text: Core TL text extracted from supported HTML or deterministically derived from core schema JSON.
        core_schema_tl_source_kind: Provenance tag distinguishing ``"html_extracted"`` core TL text from ``"json_derived"`` fallback text.
        rpc_errors: Decoded core.telegram.org RPC-error database mapping.
        rpc_errors_text: Original UTF-8 RPC-error JSON text retained for deterministic pinning.
        schema_layer: Telegram layer number extracted from Telegram Desktop's strict end-of-file layer marker.
        changelog_latest_layer: Highest Telegram layer number found in the changelog HTML or ``None`` when no marker is found.
        fetch_date: ISO 8601 calendar-date string recorded as snapshot provenance.
        source_diff: Structural comparison mapping between canonical TDLib declarations and Telegram Desktop/core supporting schemas.
        source_metadata: Reproducible per-source URL, role, normalization, size, digest and declaration-count metadata.
    """

    schema_json: Mapping[str, Any]
    schema_tl_text: str
    schema_tl_source_kind: str
    tdesktop_tl_text: str
    core_schema_json: Mapping[str, Any]
    core_schema_json_text: str
    core_schema_tl_text: str
    core_schema_tl_source_kind: str
    rpc_errors: Mapping[str, Any]
    rpc_errors_text: str
    schema_layer: int
    changelog_latest_layer: int | None
    fetch_date: str
    source_diff: Mapping[str, Any]
    source_metadata: Mapping[str, Any]


def main(argv: Sequence[str] | None = None) -> int:
    """Update pinned upstream schema inputs or check them against current upstream content.

    Args:
        argv: Optional CLI arguments; defaults to process arguments.

    Returns:
        ``0`` when update/check succeeds or ``1`` when ``--check-upstream`` finds stale files.
    """
    parser = argparse.ArgumentParser(description="Update pinned Telegram schema inputs.")
    parser.add_argument(
        "--check-upstream", action="store_true", help="fetch upstream and fail when pinned schema inputs are stale"
    )
    parser.add_argument(
        "--report", type=Path, help="write a machine-readable upstream source and drift report to this path"
    )
    args = parser.parse_args(argv)

    snapshot = build_upstream_snapshot()
    files = render_pinned_files(snapshot, root=_REPO_ROOT)
    stale = stale_pinned_files(files)
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_upstream_report(snapshot, stale, root=_REPO_ROOT), encoding="utf-8", newline="")
        print(f"wrote upstream schema report: {args.report}")
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
    """Fetch all allowlisted upstream sources and derive a validated pinning snapshot.

    Args:
        fetch_url: Optional URL-to-bytes function for deterministic tests or alternate transport.
        fetch_date: Optional ISO date recorded in provenance; defaults to today.

    Returns:
        Normalized schema, error, layer, source-diff and provenance payloads.

    Raises:
        ValueError: An upstream payload lacks required schema or layer semantics.
        RuntimeError: Upstream schemas disagree on overlapping declarations or a required layer marker is absent or ambiguous.
        TLSchemaParseError: An upstream TL or normalized JSON schema is malformed.
        UnicodeDecodeError: A JSON payload expected to be UTF-8 cannot be decoded by its parser.
        TypeError: An upstream JSON payload is not an object.
        json.JSONDecodeError: An upstream JSON payload is malformed.
        OSError: Every bounded network transport fails to retrieve a required allowlisted source.
    """
    fetch = _fetch_url if fetch_url is None else fetch_url
    payloads = {url: fetch(url) for url in _ALLOWED_FETCH_URLS}
    tdlib_tl_text = _decode_utf8(payloads[_TDLIB_SCHEMA_URL], source=_TDLIB_SCHEMA_URL)
    tdesktop_tl_text = _decode_utf8(payloads[_TDESKTOP_SCHEMA_URL], source=_TDESKTOP_SCHEMA_URL)
    core_schema_json_text = _decode_utf8(payloads[_SCHEMA_JSON_URL], source=_SCHEMA_JSON_URL)
    rpc_errors_text = _decode_utf8(payloads[_ERRORS_JSON_URL], source=_ERRORS_JSON_URL)
    schema_html = _decode_utf8(payloads[_SCHEMA_DOC_URL], source=_SCHEMA_DOC_URL)
    layers_html = _decode_utf8(payloads[_LAYERS_URL], source=_LAYERS_URL)
    core_schema_json = _load_json(payloads[_SCHEMA_JSON_URL], source=_SCHEMA_JSON_URL)
    rpc_errors = _load_json(payloads[_ERRORS_JSON_URL], source=_ERRORS_JSON_URL)
    schema_layer = _extract_tdesktop_layer(tdesktop_tl_text)
    tdlib_schema = parse_schema(tdlib_tl_text)
    tdesktop_schema = parse_schema(tdesktop_tl_text)
    core_schema = parse_schema_json(core_schema_json)
    source_diff = _schema_source_diff(tdlib_schema, tdesktop_schema, core_schema)
    changed_overlap = source_diff["tdlib_vs_tdesktop"]["changed"]
    if changed_overlap:
        names = ", ".join(item["name"] for item in changed_overlap[:10])
        raise RuntimeError(f"TDLib and Telegram Desktop disagree on overlapping declarations: {names}")
    schema_json = _normalized_schema_json(tdlib_schema, tdesktop_schema, core_schema_json)
    core_schema_tl_text, core_schema_tl_source_kind = _schema_tl_from_html_or_json(schema_html, core_schema_json)
    source_metadata = _source_metadata(
        payloads=payloads,
        tdlib_schema=tdlib_schema,
        tdesktop_schema=tdesktop_schema,
        core_schema=core_schema,
        core_schema_tl_text=core_schema_tl_text,
        core_schema_tl_source_kind=core_schema_tl_source_kind,
    )
    return UpstreamSchemaSnapshot(
        schema_json=schema_json,
        schema_tl_text=tdlib_tl_text,
        schema_tl_source_kind="tdlib_verbatim",
        tdesktop_tl_text=tdesktop_tl_text,
        core_schema_json=core_schema_json,
        core_schema_json_text=core_schema_json_text,
        core_schema_tl_text=core_schema_tl_text,
        core_schema_tl_source_kind=core_schema_tl_source_kind,
        rpc_errors=rpc_errors,
        rpc_errors_text=rpc_errors_text,
        schema_layer=schema_layer,
        changelog_latest_layer=_extract_changelog_latest_layer(layers_html),
        fetch_date=fetch_date or date.today().isoformat(),
        source_diff=source_diff,
        source_metadata=source_metadata,
    )


def render_pinned_files(snapshot: UpstreamSchemaSnapshot, *, root: Path) -> dict[Path, str]:
    """Render deterministic pinned schema, metadata, error and provenance files.

    Args:
        snapshot: Validated upstream snapshot to pin.
        root: Repository root receiving pinned relative paths.

    Returns:
        Mapping of output paths to their complete expected content.
    """
    schema_json_text = _json_document(snapshot.schema_json)
    schema_tl_text = snapshot.schema_tl_text
    tdesktop_tl_text = snapshot.tdesktop_tl_text
    core_schema_tl_text = (
        snapshot.core_schema_tl_text
        if snapshot.core_schema_tl_text.endswith("\n")
        else snapshot.core_schema_tl_text + "\n"
    )
    metadata = {
        "layer": snapshot.schema_layer,
        "schema_layer": snapshot.schema_layer,
        "changelog_latest_layer": snapshot.changelog_latest_layer,
        "canonical_source": "tdlib",
        "source_url": _TDLIB_SCHEMA_URL,
        "schema_source_url": _TDLIB_SCHEMA_URL,
        "structural_source_url": _TDLIB_SCHEMA_URL,
        "layer_source_url": _TDESKTOP_SCHEMA_URL,
        "schema_doc_url": _SCHEMA_DOC_URL,
        "source_note": f"Canonical structure is the pinned TDLib telegram_api.tl; Layer {snapshot.schema_layer} comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.",
        "documentation_merge_precedence": ["tdlib", "tdesktop", "core_json"],
        "source_comparison_summary": _source_comparison_summary(snapshot.source_diff),
        "fetch_date": snapshot.fetch_date,
        "sha256": _sha256_text(schema_json_text),
        "schema_sha256": _sha256_text(schema_json_text),
        "schema_json_sha256": _sha256_text(schema_json_text),
        "schema_tl_sha256": _sha256_text(schema_tl_text),
        "schema_tl_source_kind": snapshot.schema_tl_source_kind,
        "schema_format": "json",
        "generator_version": "5",
        "constructor_count": len(snapshot.schema_json.get("constructors", ())),
        "function_count": len(snapshot.schema_json.get("methods", ())),
        "rpc_error_source_url": _ERRORS_DOC_URL,
        "rpc_error_download_url": _ERRORS_JSON_URL,
        "rpc_error_layer": snapshot.rpc_errors.get("layer"),
        "rpc_error_sha256": _sha256_text(snapshot.rpc_errors_text),
        "rpc_error_count": _rpc_error_count(snapshot.rpc_errors),
        "changelog_source_url": _LAYERS_URL,
        "sources": snapshot.source_metadata,
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
            "tools/schema/telegram-bindings.json",
            "src/miniproto/tl/fast_metadata.py",
            "rust/miniproto/src/generated_tl.rs",
        ],
    }
    return {
        root / "tools/schema/schema.json": schema_json_text,
        root / "tools/schema/schema.tl": schema_tl_text,
        root / "tools/schema/schema-tdesktop.tl": tdesktop_tl_text,
        root / "tools/schema/schema-core.json": snapshot.core_schema_json_text,
        root / "tools/schema/schema-core.tl": core_schema_tl_text,
        root / "tools/schema/rpc-errors.json": snapshot.rpc_errors_text,
        root / "tools/schema/schema-source-diff.json": _json_document(snapshot.source_diff),
        root / "tools/schema/schema-metadata.json": _json_document(metadata),
    }


def render_upstream_report(snapshot: UpstreamSchemaSnapshot, stale: Sequence[Path], *, root: Path) -> str:
    """Render a machine-readable report describing upstream provenance and stale pins.

    Args:
        snapshot: Validated upstream snapshot.
        stale: Output paths differing from their expected pinned content.
        root: Repository root used to make report paths relative.

    Returns:
        Deterministic JSON report text.
    """
    root = root.resolve()
    stale_inputs: list[str] = []
    for path in stale:
        resolved = path.resolve()
        try:
            stale_inputs.append(resolved.relative_to(root).as_posix())
        except ValueError:
            stale_inputs.append(resolved.as_posix())
    return _json_document(
        {
            "canonical_source": "tdlib",
            "fetch_date": snapshot.fetch_date,
            "schema_layer": snapshot.schema_layer,
            "changelog_latest_layer": snapshot.changelog_latest_layer,
            "stale_pinned_inputs": stale_inputs,
            "sources": snapshot.source_metadata,
            "comparisons": snapshot.source_diff,
        }
    )


def write_pinned_files(files: Mapping[Path, str]) -> None:
    """Write every expected pinned file with normalized newline semantics.

    Args:
        files: Destination paths and complete expected content.

    Raises:
        ValueError: The requested outputs do not share one destination directory.
        RuntimeError: A staged UTF-8 file does not round-trip to the expected bytes before replacement.
        OSError: Directory creation, staging or atomic replacement fails.
    """
    if not files:
        return
    parents = {path.parent.resolve() for path in files}
    if len(parents) != 1:
        raise ValueError("all pinned schema files must share one destination directory")
    destination = parents.pop()
    destination.mkdir(parents=True, exist_ok=True)
    staging_root = Path(tempfile.mkdtemp(prefix=".schema-update-", dir=destination))
    try:
        staged: dict[Path, Path] = {}
        for path, content in files.items():
            staged_path = staging_root / path.name
            staged_path.write_text(content, encoding="utf-8", newline="")
            if staged_path.read_bytes() != content.encode("utf-8"):
                raise RuntimeError(f"staged schema file did not round-trip exactly: {path.name}")
            staged[path] = staged_path
        for path, staged_path in staged.items():
            os.replace(staged_path, path)
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)


def stale_pinned_files(files: Mapping[Path, str]) -> tuple[Path, ...]:
    """Return pinned output paths that are absent or differ from expected content.

    Args:
        files: Destination paths and complete expected content.
    """
    stale: list[Path] = []
    for path, expected in files.items():
        if not path.exists() or not _pinned_file_matches(path, expected):
            stale.append(path)
    return tuple(stale)


def _pinned_file_matches(path: Path, expected: str) -> bool:
    """Compare one pinned file to expected content without exposing read errors.

    Args:
        path: Pinned destination path.
        expected: Deterministic expected content.
    """
    try:
        actual = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return False
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
    """Fetch an allowlisted upstream URL using Python transport with curl fallback.

    Args:
        url: Allowlisted upstream source URL.

    Raises:
        ValueError: The URL is outside the updater's fixed source allowlist.
        URLError: Python and curl transports cannot retrieve the source and the last Python failure is a URL error.
        TimeoutError: Python and curl transports cannot retrieve the source and the last Python failure is a timeout.
        ConnectionError: Python and curl transports cannot retrieve the source and the last Python failure is a connection error.
        RuntimeError: No transport produced a payload and no more specific failure was retained.
    """
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
    """Attempt a bounded curl fetch for an already allowlisted source URL.

    Args:
        url: Allowlisted upstream source URL.
    """
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
    """Decode a JSON object payload with source-specific diagnostics.

    Args:
        payload: UTF-8 JSON bytes.
        source: Source URL or label for validation errors.

    Raises:
        UnicodeDecodeError: ``payload`` is not valid UTF-8.
        json.JSONDecodeError: The decoded text is not valid JSON.
        TypeError: The decoded JSON value is not an object.
    """
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{source} must return a JSON object")
    return data


def _decode_utf8(payload: bytes, *, source: str) -> str:
    """Decode UTF-8 source bytes with source-specific diagnostics.

    Args:
        payload: Source bytes expected to be UTF-8.
        source: Source URL or label for decode errors.

    Raises:
        RuntimeError: ``payload`` is not valid UTF-8; the source label is retained in the error.
    """
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"{source} did not return valid UTF-8") from exc


def _extract_tdesktop_layer(schema_text: str) -> int:
    """Extract the required trailing Telegram Desktop schema layer marker.

    Args:
        schema_text: Telegram Desktop TL schema text.

    Raises:
        RuntimeError: The text does not contain exactly one strict ``// LAYER N`` marker at end of file.
    """
    marker = re.search(r"(?m)^// LAYER (?P<layer>[1-9]\d*)\r?\n?\Z", schema_text)
    if marker is None:
        raise RuntimeError("Telegram Desktop schema must end with a strict // LAYER N end-of-file LAYER marker")
    markers = re.findall(r"(?m)^// LAYER ([1-9]\d*)\s*$", schema_text)
    if markers != [marker.group("layer")]:
        raise RuntimeError("Telegram Desktop schema must contain exactly one end-of-file LAYER marker")
    return int(marker.group("layer"))


def _normalized_schema_json(
    canonical: TLSchema, tdesktop: TLSchema, core_schema_json: Mapping[str, Any]
) -> Mapping[str, Any]:
    """Normalize canonical TL entries and attach merged upstream documentation.

    Args:
        canonical: Canonical TDLib schema selected for structure.
        tdesktop: Telegram Desktop supporting schema used for documentation.
        core_schema_json: Core Telegram JSON supporting schema used for documentation.
    """
    tdlib_docs = _schema_documentation(canonical)
    tdesktop_docs = _schema_documentation(tdesktop)
    core_docs = _json_documentation(core_schema_json)
    constructors = [
        _normalized_json_entry(entry, "predicate", tdlib_docs, tdesktop_docs, core_docs)
        for entry in canonical.constructors
    ]
    methods = [
        _normalized_json_entry(entry, "method", tdlib_docs, tdesktop_docs, core_docs) for entry in canonical.functions
    ]
    return {"constructors": constructors, "methods": methods}


def _normalized_json_entry(
    entry: TLEntry,
    name_key: str,
    tdlib_docs: Mapping[str, Mapping[str, Any]],
    tdesktop_docs: Mapping[str, Mapping[str, Any]],
    core_docs: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any]:
    """Render one parsed entry as stable normalized JSON with optional documentation.

    Args:
        entry: Parsed canonical schema entry.
        name_key: Normalized JSON key, ``"predicate"`` or ``"method"``.
        tdlib_docs: Documentation parsed from canonical TDLib comments.
        tdesktop_docs: Documentation parsed from Telegram Desktop comments.
        core_docs: Documentation parsed from core Telegram JSON.
    """
    documentation = _merged_documentation(entry.name, tdlib_docs, tdesktop_docs, core_docs)
    params: list[dict[str, Any]] = []
    parameter_docs = documentation.get("parameters", {})
    for parameter in entry.params:
        if parameter.is_template or parameter.is_bare:
            continue
        item: dict[str, Any] = {"name": parameter.name, "type": _parameter_source_type(parameter)}
        description = parameter_docs.get(parameter.name)
        if description:
            item["description"] = description
        params.append(item)
    item = {
        "id": str(_signed_constructor_id(entry.constructor_id)),
        name_key: entry.name,
        "params": params,
        "type": entry.result_type,
    }
    description = documentation.get("description")
    if description:
        item["description"] = description
    return item


def _signed_constructor_id(constructor_id: int) -> int:
    """Convert an unsigned 32-bit constructor ID to Telegram's signed JSON form.

    Args:
        constructor_id: Unsigned constructor identifier.
    """
    return constructor_id if constructor_id < 0x80000000 else constructor_id - 0x100000000


def _parameter_source_type(parameter: TLParameter) -> str:
    """Reconstruct source type spelling, including optional flag prefixes.

    Args:
        parameter: Parsed TL parameter.
    """
    if parameter.is_flags_marker:
        return "#"
    if parameter.is_optional and parameter.flag is not None and parameter.flag_index is not None:
        return f"{parameter.flag}.{parameter.flag_index}?{parameter.type}"
    return parameter.type


def _schema_documentation(schema: TLSchema) -> Mapping[str, Mapping[str, Any]]:
    """Extract supported descriptions and parameter documentation from schema comments.

    Args:
        schema: Parsed supporting schema carrying declaration comments.
    """
    return {entry.name: _comment_documentation(entry.comments) for entry in schema.entries if entry.comments}


def _comment_documentation(comments: Sequence[str]) -> Mapping[str, Any]:
    """Parse supported declaration and parameter documentation comments.

    Args:
        comments: Comment text without source comment prefixes.
    """
    descriptions: list[str] = []
    parameters: dict[str, str] = {}
    for comment in comments:
        if comment.startswith("@description "):
            descriptions.append(comment.removeprefix("@description ").strip())
        elif comment.startswith("@param "):
            _, name, description = comment.split(maxsplit=2)
            parameters[name] = description.strip()
        elif not comment.startswith("@"):
            descriptions.append(comment.strip())
    result: dict[str, Any] = {}
    if descriptions:
        result["description"] = " ".join(part for part in descriptions if part)
    if parameters:
        result["parameters"] = parameters
    return result


def _json_documentation(schema_json: Mapping[str, Any]) -> Mapping[str, Mapping[str, Any]]:
    """Extract entry descriptions and parameter descriptions from core schema JSON.

    Args:
        schema_json: Parsed core Telegram schema JSON.
    """
    result: dict[str, Mapping[str, Any]] = {}
    for collection, name_key in (("constructors", "predicate"), ("methods", "method")):
        entries = schema_json.get(collection, ())
        if not isinstance(entries, Sequence) or isinstance(entries, str):
            continue
        for item in entries:
            if not isinstance(item, Mapping) or not isinstance(item.get(name_key), str):
                continue
            documentation: dict[str, Any] = {}
            if isinstance(item.get("description"), str) and item["description"].strip():
                documentation["description"] = item["description"].strip()
            parameters: dict[str, str] = {}
            for parameter in item.get("params", ()):
                if not isinstance(parameter, Mapping):
                    continue
                name = parameter.get("name")
                description = parameter.get("description")
                if isinstance(name, str) and isinstance(description, str) and description.strip():
                    parameters[name] = description.strip()
            if parameters:
                documentation["parameters"] = parameters
            if documentation:
                result[str(item[name_key])] = documentation
    return result


def _merged_documentation(name: str, *sources: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    """Merge entry documentation by stable source priority.

    Args:
        name: Qualified schema entry name.
        *sources: Documentation mappings in highest-to-lowest precedence order.
    """
    description = next(
        (str(source[name]["description"]) for source in sources if source.get(name, {}).get("description")), None
    )
    parameter_names = {
        parameter_name for source in sources for parameter_name in source.get(name, {}).get("parameters", {})
    }
    parameters = {
        parameter_name: next(
            str(source[name]["parameters"][parameter_name])
            for source in sources
            if parameter_name in source.get(name, {}).get("parameters", {})
        )
        for parameter_name in sorted(parameter_names)
    }
    result: dict[str, Any] = {}
    if description:
        result["description"] = description
    if parameters:
        result["parameters"] = parameters
    return result


def _schema_source_diff(tdlib: TLSchema, tdesktop: TLSchema, core: TLSchema) -> Mapping[str, Any]:
    """Compare canonical TDLib declarations with layer and core supporting sources.

    Args:
        tdlib: Canonical structural schema.
        tdesktop: Supporting Telegram Desktop layer/documentation schema.
        core: Supporting core Telegram schema.
    """
    return {
        "canonical_source": "tdlib",
        "tdlib_vs_tdesktop": _compare_schemas(tdlib, tdesktop, canonical_label="tdlib", other_label="tdesktop"),
        "tdlib_vs_core": _compare_schemas(tdlib, core, canonical_label="tdlib", other_label="core"),
    }


def _source_comparison_summary(source_diff: Mapping[str, Any]) -> Mapping[str, Any]:
    """Condense detailed source differences into stable metadata summary counts.

    Args:
        source_diff: Detailed canonical-versus-supporting source comparison.
    """
    desktop = source_diff["tdlib_vs_tdesktop"]
    core = source_diff["tdlib_vs_core"]
    return {
        "tdlib_vs_tdesktop": {
            "overlap_count": desktop["overlap_count"],
            "changed_count": len(desktop["changed"]),
            "tdlib_only": desktop["tdlib_only"],
            "tdesktop_only": desktop["tdesktop_only"],
        },
        "tdlib_vs_core": {
            "overlap_count": core["overlap_count"],
            "changed_count": len(core["changed"]),
            "tdlib_only_count": len(core["tdlib_only"]),
            "core_only_count": len(core["core_only"]),
        },
    }


def _compare_schemas(
    canonical: TLSchema, other: TLSchema, *, canonical_label: str, other_label: str
) -> Mapping[str, Any]:
    """Compare declarations by identity and structural signature.

    Args:
        canonical: Schema whose declarations are authoritative.
        other: Supporting schema compared against the canonical source.
        canonical_label: Stable label used for canonical-only keys.
        other_label: Stable label used for supporting-only keys.
    """
    canonical_entries = {(entry.kind, entry.name): entry for entry in canonical.entries}
    other_entries = {(entry.kind, entry.name): entry for entry in other.entries}
    shared = sorted(canonical_entries.keys() & other_entries.keys())
    changed = [
        {
            "kind": key[0],
            "name": key[1],
            f"{canonical_label}_signature": canonical_entries[key].source_line,
            f"{other_label}_signature": other_entries[key].source_line,
        }
        for key in shared
        if _structural_signature(canonical_entries[key]) != _structural_signature(other_entries[key])
    ]
    return {
        "overlap_count": len(shared),
        f"{canonical_label}_only": [
            key[1] for key in sorted(canonical_entries.keys() - other_entries.keys(), key=lambda item: item[1])
        ],
        f"{other_label}_only": [
            key[1] for key in sorted(other_entries.keys() - canonical_entries.keys(), key=lambda item: item[1])
        ],
        "changed": changed,
    }


def _structural_signature(entry: TLEntry) -> tuple[Any, ...]:
    """Return comparable declaration fields while excluding documentation-only data.

    Args:
        entry: Parsed schema entry to fingerprint structurally.
    """
    return (
        entry.kind,
        entry.constructor_id,
        entry.result_type,
        tuple(
            (
                parameter.name,
                parameter.type,
                parameter.flag,
                parameter.flag_index,
                parameter.is_template,
                parameter.is_bare,
                parameter.is_flags_marker,
            )
            for parameter in entry.params
        ),
    )


def _source_metadata(
    *,
    payloads: Mapping[str, bytes],
    tdlib_schema: TLSchema,
    tdesktop_schema: TLSchema,
    core_schema: TLSchema,
    core_schema_tl_text: str,
    core_schema_tl_source_kind: str,
) -> Mapping[str, Any]:
    """Build reproducible per-source provenance, normalization and declaration counts.

    Args:
        payloads: Raw bytes keyed by fixed upstream URL.
        tdlib_schema: Parsed canonical TDLib structure.
        tdesktop_schema: Parsed Telegram Desktop supporting schema.
        core_schema: Parsed core Telegram supporting schema.
        core_schema_tl_text: Extracted or derived core TL text.
        core_schema_tl_source_kind: Whether core TL text was extracted or JSON-derived.
    """

    def record(url: str, *, role: str, schema: TLSchema | None = None) -> Mapping[str, Any]:
        """Build normalized provenance for one fetched upstream source.

        Args:
            url: Fixed upstream URL used to select normalization and payload bytes.
            role: Source role recorded in generated provenance.
            schema: Optional parsed schema used for declaration counts.
        """
        payload = payloads[url]
        stable_payload, normalization = _stable_source_payload(url, payload)
        result = {
            "url": url,
            "role": role,
            "bytes": len(stable_payload),
            "sha256": hashlib.sha256(stable_payload).hexdigest(),
            "declaration_count": len(schema.entries) if schema is not None else 0,
            "constructor_count": len(schema.constructors) if schema is not None else 0,
            "function_count": len(schema.functions) if schema is not None else 0,
        }
        if normalization is not None:
            result["normalization"] = normalization
        return result

    return {
        "tdlib": record(_TDLIB_SCHEMA_URL, role="canonical_structure", schema=tdlib_schema),
        "tdesktop": record(_TDESKTOP_SCHEMA_URL, role="layer_and_documentation", schema=tdesktop_schema),
        "core_json": record(_SCHEMA_JSON_URL, role="documentation_and_drift", schema=core_schema),
        "core_schema_page": {
            **record(_SCHEMA_DOC_URL, role="documentation_and_tl_mirror"),
            "derived_tl_source_kind": core_schema_tl_source_kind,
            "derived_tl_sha256": _sha256_text(core_schema_tl_text),
        },
        "rpc_errors": record(_ERRORS_JSON_URL, role="rpc_error_database"),
        "layer_changelog": record(_LAYERS_URL, role="drift_context"),
    }


def _stable_source_payload(url: str, payload: bytes) -> tuple[bytes, str | None]:
    """Remove known volatile page-generation timing from HTML sources before hashing.

    Args:
        url: Fixed upstream URL that determines whether normalization applies.
        payload: Raw fetched source bytes.
    """
    if url not in {_SCHEMA_DOC_URL, _LAYERS_URL}:
        return payload, None
    normalized = _PAGE_GENERATION_TIMING_RE.sub(b"", payload)
    return normalized, "trailing_page_generation_timing_removed"


def _schema_tl_from_html_or_json(schema_html: str, schema_json: Mapping[str, Any]) -> tuple[str, str]:
    """Extract core TL text from HTML or deterministically derive it from schema JSON.

    Args:
        schema_html: Core schema documentation HTML.
        schema_json: Parsed core schema JSON fallback source.
    """
    extracted = _extract_tl_schema_from_html(schema_html)
    if extracted is not None:
        return extracted, "html_extracted"
    return schema_to_tl(parse_schema_json(schema_json)), "json_derived"


def _extract_tl_schema_from_html(schema_html: str) -> str | None:
    """Extract the first valid TL schema block from supported HTML containers.

    Args:
        schema_html: Core schema documentation HTML.
    """
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
    """Return the highest layer marker found in core schema HTML.

    Args:
        schema_html: Core schema documentation HTML.
    """
    layers = _extract_layers(schema_html)
    return max(layers) if layers else None


def _extract_changelog_latest_layer(layers_html: str) -> int | None:
    """Return the highest layer marker found in changelog HTML.

    Args:
        layers_html: Telegram layer changelog HTML.
    """
    layers = _extract_layers(layers_html)
    return max(layers) if layers else None


def _extract_layers(text: str) -> tuple[int, ...]:
    """Collect sorted unique textual and HTML-id layer markers.

    Args:
        text: HTML or plain text containing possible layer markers.
    """
    values = {int(value) for value in re.findall(r"\bLayer\s+(\d+)\b", text, flags=re.IGNORECASE)}
    values.update(int(value) for value in re.findall(r'id=["\']layer-(\d+)["\']', text))
    return tuple(sorted(values))


def _rpc_error_count(database: Mapping[str, Any]) -> int:
    """Count named RPC errors in a normalized error database.

    Args:
        database: Parsed RPC error mapping.
    """
    errors = database.get("errors", {})
    if not isinstance(errors, Mapping):
        return 0
    return sum(len(named_errors) for named_errors in errors.values() if isinstance(named_errors, Mapping))


def _sha256_text(text: str) -> str:
    """Return the UTF-8 SHA-256 digest of text.

    Args:
        text: Text to hash.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _json_document(data: Mapping[str, Any]) -> str:
    """Render deterministic pretty JSON with sorted keys and a final newline.

    Args:
        data: Mapping to serialize.
    """
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
