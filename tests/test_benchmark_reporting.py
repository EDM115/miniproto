from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest
from tools.bench.reporting import (
    BENCHMARK_SCHEMA,
    LoopLagProbe,
    _advance_probe_target,
    build_benchmark_report,
    sample_statistics,
    write_benchmark_report,
)


def test_loop_lag_probe_skips_missed_cadences_instead_of_emitting_a_catch_up_storm() -> None:
    assert _advance_probe_target(target=1.0, observed=1.026, interval=0.01) == pytest.approx(1.03)
    assert _advance_probe_target(target=1.0, observed=1.001, interval=0.01) == pytest.approx(1.01)


def test_sample_statistics_reports_hand_checked_percentiles() -> None:
    statistics = sample_statistics([1.0, 2.0, 3.0, 4.0, 100.0])

    assert statistics == {
        "count": 5,
        "min": 1.0,
        "max": 100.0,
        "mean": 22.0,
        "median": 3.0,
        "p50": 3.0,
        "p95": pytest.approx(80.8),
        "p99": pytest.approx(96.16),
    }


def test_benchmark_report_has_normalized_schema_and_redacts_feature_secrets() -> None:
    report = build_benchmark_report(
        benchmark="fixture",
        mode="smoke",
        warmup=2,
        samples=[1.0, 2.0, 3.0],
        unit="ms",
        configuration={"lanes": 2, "bot_token": "secret", "nested": {"api_hash": "secret"}},
        throughput={"bytes_per_second": 123.0},
        rss={"start_bytes": 10, "peak_bytes": 20, "end_bytes": 15},
        loop_lag={"enabled": False, "samples": 0},
        environment={"package_version": "0.1.0", "commit": "abc"},
    )

    assert report["schema"] == BENCHMARK_SCHEMA
    assert report["benchmark"] == "fixture"
    assert report["mode"] == "smoke"
    assert report["warmup"] == 2
    assert report["sample_unit"] == "ms"
    assert report["samples"] == [1.0, 2.0, 3.0]
    assert report["statistics"]["p95"] == pytest.approx(2.9)
    assert report["configuration"] == {"bot_token": "<redacted>", "lanes": 2, "nested": {"api_hash": "<redacted>"}}
    assert report["throughput"] == {"bytes_per_second": 123.0}
    assert report["rss"]["peak_bytes"] == 20
    assert report["environment"]["commit"] == "abc"


def test_write_benchmark_report_is_deterministic_and_creates_parent(tmp_path: Path) -> None:
    report = build_benchmark_report(
        benchmark="fixture",
        mode="full",
        warmup=0,
        samples=[3.0],
        unit="seconds",
        configuration={},
        environment={"package_version": "0.1.0"},
    )
    destination = tmp_path / "nested" / "report.json"

    write_benchmark_report(destination, report)

    assert destination.read_text(encoding="utf-8") == json.dumps(report, indent=2, sort_keys=True) + "\n"


def test_loop_lag_probe_reports_fixed_cadence_delays_and_stalls() -> None:
    async def scenario() -> dict[str, Any]:
        probe = LoopLagProbe(interval_s=0.001, stall_threshold_s=0.005)
        await probe.start()
        await asyncio.sleep(0.004)
        await asyncio.sleep(0.012)
        return await probe.stop()

    report = asyncio.run(scenario())

    assert report["enabled"] is True
    assert report["interval_ms"] == 1.0
    assert report["stall_threshold_ms"] == 5.0
    assert isinstance(report["samples"], int)
    assert report["samples"] > 0
    assert report["max_ms"] >= 0
    assert report["p50_ms"] >= 0
    assert report["p95_ms"] >= report["p50_ms"]
    assert report["p99_ms"] >= report["p95_ms"]
    assert report["callback_overhead_ns"]["count"] == report["samples"]


def test_loop_lag_probe_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="interval_s"):
        LoopLagProbe(interval_s=0)
    with pytest.raises(ValueError, match="stall_threshold_s"):
        LoopLagProbe(interval_s=0.001, stall_threshold_s=-1)
