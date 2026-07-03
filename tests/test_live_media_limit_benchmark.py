from __future__ import annotations

import pytest
from tools.bench.benchmark_live_media_limit import (
    DEFAULT_CHUNK_SIZE,
    TELEGRAM_DEFAULT_LIMIT_BYTES,
    TransferRecorder,
    benchmark_peer_for_actor,
    deterministic_chunk,
    effective_download_request_timeout,
    effective_upload_request_timeout,
    ensure_benchmark_file,
    parse_args,
    parse_size,
    sample_stats,
)


def test_parse_size_accepts_telegram_default_and_units() -> None:
    assert parse_size("telegram-default") == TELEGRAM_DEFAULT_LIMIT_BYTES
    assert parse_size("2gb") == 2_000_000_000
    assert parse_size("2000mib") == 2000 * 1024 * 1024
    assert parse_size("512kb") == 512_000
    assert parse_size("524288") == DEFAULT_CHUNK_SIZE


def test_deterministic_chunk_is_stable_and_indexed() -> None:
    first = deterministic_chunk(1, 1024)
    assert len(first) == 1024
    assert first == deterministic_chunk(1, 1024)
    assert first != deterministic_chunk(2, 1024)


def test_ensure_benchmark_file_writes_expected_pattern(tmp_path) -> None:
    path = tmp_path / "bench.bin"
    ensure_benchmark_file(path, size=2500, chunk_size=1024, force=False)
    data = path.read_bytes()
    assert len(data) == 2500
    assert data[:1024] == deterministic_chunk(0, 1024)
    assert data[1024:2048] == deterministic_chunk(1, 1024)
    assert data[2048:] == deterministic_chunk(2, 452)


def test_sample_stats_reports_tails_and_percentiles() -> None:
    stats = sample_stats([10.0, 20.0, 30.0, 40.0, 50.0], fallback_overall_mib_s=1.0)
    assert stats.samples == 5
    assert stats.avg_mib_s == 30.0
    assert stats.median_mib_s == 30.0
    assert stats.p01_mib_s == 10.0
    assert stats.p95_mib_s == 50.0
    assert stats.slowest_1pct_avg_mib_s == 10.0
    assert stats.fastest_5pct_avg_mib_s == 50.0


def test_transfer_recorder_samples_fixed_time_windows() -> None:
    one_mib = 1024 * 1024
    recorder = TransferRecorder(
        total=10 * one_mib, label="bench", progress_interval_s=0, sample_interval_s=5
    )
    recorder.begin(now=1.0)
    recorder.record(one_mib, None, now=1.1)
    recorder.record(5 * one_mib, None, now=6.0)
    recorder.record(10 * one_mib, None, now=11.0)
    assert recorder.samples_mib_s == pytest.approx([1.0, 1.0])


def test_upload_request_timeout_defaults_to_shorter_part_timeout() -> None:
    args = parse_args(["--actor", "user"], {})
    assert args.request_timeout == 120
    assert args.upload_request_timeout is None
    assert effective_upload_request_timeout(args) == 30
    overridden = parse_args(["--actor", "user", "--upload-request-timeout", "45"], {})
    assert effective_upload_request_timeout(overridden) == 45


def test_download_request_timeout_defaults_to_shorter_part_timeout() -> None:
    args = parse_args(["--actor", "user"], {})
    assert args.request_timeout == 120
    assert args.download_concurrency == 4
    assert args.download_request_timeout is None
    assert effective_download_request_timeout(args) == 30
    assert args.download_flood_sleep_threshold == 30
    overridden = parse_args(["--actor", "user", "--download-request-timeout", "45"], {})
    assert effective_download_request_timeout(overridden) == 45


def test_download_concurrency_is_independent_from_upload_concurrency() -> None:
    shared = parse_args(["--actor", "user"], {"MINIPROTO_LIVE_BENCH_CONCURRENCY": "8"})
    assert shared.concurrency == 8
    assert shared.download_concurrency == 4
    specific = parse_args(
        ["--actor", "user"],
        {"MINIPROTO_LIVE_BENCH_CONCURRENCY": "8", "MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY": "2"},
    )
    assert specific.concurrency == 8
    assert specific.download_concurrency == 2
    overridden = parse_args(["--actor", "user", "--download-concurrency", "6"], {})
    assert overridden.download_concurrency == 6


def test_download_flood_sleep_threshold_uses_download_specific_env_only() -> None:
    shared = parse_args(["--actor", "user"], {"MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD": "9"})
    assert shared.download_flood_sleep_threshold == 30
    specific = parse_args(
        ["--actor", "user"],
        {
            "MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD": "9",
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD": "3",
        },
    )
    assert specific.download_flood_sleep_threshold == 3
    overridden = parse_args(["--actor", "user", "--download-flood-sleep-threshold", "5"], {})
    assert overridden.download_flood_sleep_threshold == 5


def test_bot_peer_must_not_default_to_self() -> None:
    assert benchmark_peer_for_actor("user", {}) == "self"
    assert (
        benchmark_peer_for_actor("bot", {"MINIPROTO_LIVE_BENCH_BOT_PEER": "@benchchat"})
        == "@benchchat"
    )
    with pytest.raises(SystemExit, match="BOT_PEER"):
        benchmark_peer_for_actor("bot", {})
    with pytest.raises(SystemExit, match="BOT_PEER"):
        benchmark_peer_for_actor("bot", {"MINIPROTO_LIVE_BENCH_BOT_PEER": "self"})
