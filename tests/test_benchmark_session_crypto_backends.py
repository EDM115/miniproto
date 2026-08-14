from __future__ import annotations

import json
from pathlib import Path

import pytest
import tools.bench.benchmark_session_crypto_backends as benchmark


def test_session_crypto_cli_arguments_override_environment_defaults() -> None:
    args = benchmark.parse_args(
        ["--mode", "smoke", "--runs", "2", "--json", ".tmp/session-crypto.json"],
        {"MINIPROTO_BENCH_MODE": "full", "MINIPROTO_BENCH_RUNS": "9"},
    )

    assert args.mode == "smoke"
    assert args.runs == 2
    assert args.json.as_posix() == ".tmp/session-crypto.json"


def test_session_crypto_cli_rejects_non_positive_runs() -> None:
    with pytest.raises(SystemExit):
        benchmark.parse_args(["--runs", "0"], {})


def test_session_crypto_result_record_uses_per_operation_distribution_statistics() -> None:
    record = benchmark.benchmark_result_record(benchmark.BenchmarkResult(samples_ms=(3.0, 1.0, 2.0)))

    assert record["runs"] == 3
    assert record["samples_ms"] == [3.0, 1.0, 2.0]
    assert record["statistics_ms"]["median"] == 2.0
    assert record["statistics_ms"]["p95"] == 2.9


def test_session_crypto_case_reports_native_results_when_cryptography_is_unavailable() -> None:
    case = benchmark.BenchmarkCase(
        name="native_only",
        native=lambda: b"result",
        cryptography=None,
        selected=lambda: b"result",
        selected_backend="native",
        smoke_iterations=1,
        full_iterations=1,
    )

    record = benchmark._measure_case(case, mode="smoke", runs=1, warmup=0)

    assert record["native"]["runs"] == 1
    assert record["cryptography"] is None
    assert record["cryptography_unavailable_reason"] == "cryptography is not installed on this platform"
    assert record["selected"]["runs"] == 1
    assert record["selected_backend"] == "native"
    assert record["winner"] == "native"
    assert record["cryptography_over_native_median"] is None


def test_session_crypto_smoke_report_measures_explicit_and_selected_backends(tmp_path: Path) -> None:
    report_path = tmp_path / "session-crypto.json"

    assert benchmark.main(["--mode", "smoke", "--runs", "1", "--json", str(report_path)]) == 0

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["schema"] == "miniproto.benchmark.v1"
    assert report["benchmark"] == "session_crypto_backends"
    assert report["mode"] == "smoke"
    assert report["configuration"]["scrypt"] == {"length": 32, "n": 16384, "p": 1, "r": 8}
    assert report["configuration"]["selection_policy"] == "native-first for protected-session operations"

    results = {result["name"]: result for result in report["results"]}
    assert set(results) == {
        "aes_gcm_decrypt_1024",
        "aes_gcm_decrypt_65536",
        "aes_gcm_decrypt_1048576",
        "aes_gcm_encrypt_1024",
        "aes_gcm_encrypt_65536",
        "aes_gcm_encrypt_1048576",
        "protected_session_crypto_roundtrip",
        "scrypt_session_parameters",
    }
    for result in results.values():
        assert result["cryptography"]["runs"] == 1
        assert result["selected"]["runs"] == 1
        assert result["selected_backend"] in {"native", "cryptography", "hybrid"}
        assert result["winner"] in {"native", "cryptography"}
        if result["native"] is not None:
            assert result["native"]["runs"] == 1
            assert result["cryptography_over_native_median"] > 0
