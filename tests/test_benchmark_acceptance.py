from __future__ import annotations

import asyncio

import tools.bench.benchmark_acceptance as acceptance
from pytest import MonkeyPatch
from tools.bench.benchmark_acceptance import (
    BenchmarkProfile,
    evaluate_acceptance_invariants,
    parse_args,
    resolve_profile,
    run_acceptance_benchmark,
)
from tools.bench.reporting import BENCHMARK_SCHEMA


def test_cli_arguments_override_benchmark_environment_defaults() -> None:
    args = parse_args(
        ["--mode", "smoke", "--samples", "2", "--json", ".tmp/explicit.json"],
        {"MINIPROTO_BENCH_MODE": "full", "MINIPROTO_BENCH_SAMPLES": "9", "MINIPROTO_BENCH_JSON": ".tmp/env.json"},
    )

    assert args.mode == "smoke"
    assert args.samples == 2
    assert args.json.as_posix() == ".tmp/explicit.json"


def test_full_profile_is_statistically_larger_than_smoke() -> None:
    smoke = resolve_profile(parse_args(["--mode", "smoke"], {}))
    full = resolve_profile(parse_args(["--mode", "full"], {}))

    assert full.samples > smoke.samples
    assert full.update_count > smoke.update_count
    assert full.media_bytes > smoke.media_bytes
    assert full.soak_cycles > smoke.soak_cycles


def test_acceptance_thresholds_use_correctness_invariants_instead_of_host_timings() -> None:
    failures = evaluate_acceptance_invariants(
        [
            {"name": "pending_rpc_burst", "configured": 8, "peak": 7, "remaining": 1},
            {
                "name": "scheduler_fairness",
                "fairness_ratio": 0.5,
                "peak_active_bytes": 9,
                "configured_max_bytes": 8,
                "leaked_bytes": 1,
            },
            {"name": "iterator_backpressure", "max_active_requests": 3, "requests_before_close": 3},
            {"name": "reconnect_transfer_cancel_soak", "pending_after": 1},
        ]
    )

    assert len(failures) == 8
    assert all(failure["type"] == "AcceptanceThresholdError" for failure in failures)
    assert not any("duration" in failure["message"] or "throughput" in failure["message"] for failure in failures)


def test_workload_exception_is_preserved_in_machine_readable_report(monkeypatch: MonkeyPatch) -> None:
    async def fail_measurement(*args: object, **kwargs: object) -> dict[str, object]:
        del args, kwargs
        raise RuntimeError("deterministic workload failed")

    monkeypatch.setattr(acceptance, "_measured_result", fail_measurement)
    profile = BenchmarkProfile(
        mode="smoke",
        warmup=0,
        samples=1,
        update_count=1,
        pending_count=1,
        generic_tl_count=1,
        media_bytes=1024,
        part_size=1024,
        scheduler_transfers=1,
        scheduler_parts=1,
        scheduler_max_bytes=1024,
        soak_cycles=1,
    )

    report = asyncio.run(run_acceptance_benchmark(profile, probe_loop_lag=False))

    assert report["results"] == []
    assert report["failures"] == [{"type": "RuntimeError", "message": "deterministic workload failed"}]


def test_tiny_acceptance_workload_exercises_real_paths_without_absolute_timing_gates() -> None:
    profile = BenchmarkProfile(
        mode="smoke",
        warmup=0,
        samples=1,
        update_count=20,
        pending_count=16,
        generic_tl_count=50,
        media_bytes=8 * 1024,
        part_size=1024,
        scheduler_transfers=2,
        scheduler_parts=2,
        scheduler_max_bytes=64 * 1024,
        soak_cycles=1,
    )

    report = asyncio.run(run_acceptance_benchmark(profile, probe_loop_lag=True))

    assert report["schema"] == BENCHMARK_SCHEMA
    assert report["benchmark"] == "runtime_acceptance"
    assert report["mode"] == "smoke"
    assert report["failures"] == []
    assert report["loop_lag"]["enabled"] is True
    results = {result["name"]: result for result in report["results"]}
    assert set(results) == {
        "generic_tl_roundtrip",
        "iterator_backpressure",
        "media_download",
        "media_upload",
        "pending_rpc_burst",
        "reconnect_transfer_cancel_soak",
        "scheduler_fairness",
        "update_dispatch",
    }
    assert results["generic_tl_roundtrip"]["operations"] == 50
    assert results["pending_rpc_burst"]["configured"] == 16
    assert results["pending_rpc_burst"]["peak"] == 16
    assert results["pending_rpc_burst"]["remaining"] == 0
    assert results["media_upload"]["bytes"] == 8 * 1024
    assert results["media_download"]["bytes"] == 8 * 1024
    assert results["iterator_backpressure"]["max_active_requests"] <= 2
    assert results["iterator_backpressure"]["requests_before_close"] <= 2
    assert results["scheduler_fairness"]["fairness_ratio"] == 1.0
    assert results["scheduler_fairness"]["leaked_bytes"] == 0
    assert results["reconnect_transfer_cancel_soak"]["cycles"] == 1
    assert results["reconnect_transfer_cancel_soak"]["connections"] >= 2
    assert results["reconnect_transfer_cancel_soak"]["pending_after"] == 0
