from __future__ import annotations

import json
from pathlib import Path

import pytest
from tools.bench.benchmark_tglib import (
    TGLIB_DEFAULT_SIZE,
    build_tglib_compatibility_payload,
    build_tglib_report,
    main,
    parse_args,
)
from tools.bench.reporting import BENCHMARK_SCHEMA


def test_tglib_payload_matches_reference_harness_shape_and_seconds() -> None:
    payload = build_tglib_compatibility_payload(
        size=2_097_152_000,
        download_started=1_786_092_651.340,
        download_finished=1_786_092_769.834,
        upload_started=1_786_092_772.181,
        upload_finished=1_786_092_895.469,
    )

    assert payload == [2_097_152_000, [1_786_092_651.340, 1_786_092_769.834, 1_786_092_772.181, 1_786_092_895.469]]


@pytest.mark.parametrize(
    ("timestamps", "message"), [((2.0, 1.0, 3.0, 4.0), "download"), ((1.0, 2.0, 4.0, 3.0), "upload")]
)
def test_tglib_payload_rejects_reversed_transfer_windows(timestamps: tuple[float, ...], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        build_tglib_compatibility_payload(
            size=1,
            download_started=timestamps[0],
            download_finished=timestamps[1],
            upload_started=timestamps[2],
            upload_finished=timestamps[3],
        )


def test_tglib_cli_arguments_override_environment_and_default_to_reference_size() -> None:
    args = parse_args(
        ["--file-id", "explicit", "--peer", "@explicit", "--dc-id", "4"],
        {
            "MINIPROTO_TGLIB_FILE_ID": "environment",
            "MINIPROTO_TGLIB_PEER": "@environment",
            "MINIPROTO_TGLIB_DC_ID": "2",
        },
    )

    assert args.file_id == "explicit"
    assert args.peer == "@explicit"
    assert args.dc_id == 4
    assert args.size == TGLIB_DEFAULT_SIZE


def test_tglib_mode_refuses_to_touch_outputs_without_explicit_live_guard(tmp_path: Path) -> None:
    compat = tmp_path / "results.json"
    rich = tmp_path / "miniproto.json"

    result = main(
        ["--file-id", "explicit", "--peer", "@bench", "--compat-json", str(compat), "--json", str(rich)], env={}
    )

    assert result == 2
    assert not compat.exists()
    assert not rich.exists()


def test_tglib_rich_report_keeps_transfer_and_finalization_boundaries_separate() -> None:
    report = build_tglib_report(
        size=2_097_152_000,
        timestamps=[100.0, 110.0, 112.0, 120.0],
        finalize_finished=123.5,
        configuration={"file_id": "secret-reference", "dc_id": 4, "peer": "@bench"},
        environment={"package_version": "0.1.0"},
        loop_lag={"enabled": False, "samples": 0},
    )

    assert report["schema"] == BENCHMARK_SCHEMA
    assert report["mode"] == "tglib"
    assert report["configuration"]["file_id"] == "<redacted>"
    assert report["results"][0]["download_duration_s"] == 10.0
    assert report["results"][0]["upload_duration_s"] == 8.0
    assert report["results"][0]["finalize_duration_s"] == 3.5
    assert json.dumps(report)
