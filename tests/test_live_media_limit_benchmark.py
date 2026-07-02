from __future__ import annotations

import pytest
from tools.bench.benchmark_live_media_limit import (
    DEFAULT_CHUNK_SIZE,
    TELEGRAM_DEFAULT_LIMIT_BYTES,
    TransferRecorder,
    benchmark_peer_for_actor,
    deterministic_chunk,
    ensure_benchmark_file,
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
