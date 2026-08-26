from __future__ import annotations

import tools.bench.benchmark_native_fallback_crypto as benchmark


def test_native_fallback_cli_arguments_override_environment_defaults() -> None:
    args = benchmark.parse_args(
        ["--mode", "smoke", "--runs", "2", "--json", ".tmp/native.json"],
        {"MINIPROTO_BENCH_MODE": "full", "MINIPROTO_BENCH_RUNS": "9"},
    )

    assert args.mode == "smoke"
    assert args.runs == 2
    assert args.json.as_posix() == ".tmp/native.json"


def test_native_fallback_result_record_uses_distribution_statistics() -> None:
    record = benchmark.benchmark_result_record(
        benchmark.BenchmarkResult(name="case:native", samples_ms=(3.0, 1.0, 2.0))
    )

    assert record["runs"] == 3
    assert record["samples_ms"] == [3.0, 1.0, 2.0]
    assert record["statistics_ms"]["median"] == 2.0
    assert record["statistics_ms"]["p95"] == 2.9


def test_native_fallback_case_reports_an_unavailable_cryptography_fallback_without_hiding_native_results() -> None:
    case = benchmark.BenchmarkCase(name="native_only", native=lambda: b"result", python=None)

    record = benchmark._measure_case(case, runs=1)

    assert record["name"] == "native_only"
    assert record["fallback"] is None
    assert record["fallback_unavailable_reason"] == "cryptography is not installed on this platform"
    assert record["native"]["runs"] == 1
    assert record["fallback_over_native_median"] is None
