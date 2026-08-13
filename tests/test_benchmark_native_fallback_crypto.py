from __future__ import annotations

from tools.bench.benchmark_native_fallback_crypto import BenchmarkResult, benchmark_result_record, parse_args


def test_native_fallback_cli_arguments_override_environment_defaults() -> None:
    args = parse_args(
        ["--mode", "smoke", "--runs", "2", "--json", ".tmp/native.json"],
        {"MINIPROTO_BENCH_MODE": "full", "MINIPROTO_BENCH_RUNS": "9"},
    )

    assert args.mode == "smoke"
    assert args.runs == 2
    assert args.json.as_posix() == ".tmp/native.json"


def test_native_fallback_result_record_uses_distribution_statistics() -> None:
    record = benchmark_result_record(BenchmarkResult(name="case:native", samples_ms=(3.0, 1.0, 2.0)))

    assert record["runs"] == 3
    assert record["samples_ms"] == [3.0, 1.0, 2.0]
    assert record["statistics_ms"]["median"] == 2.0
    assert record["statistics_ms"]["p95"] == 2.9
