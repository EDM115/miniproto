from __future__ import annotations

import socket
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pytest
from tools.bench.benchmark_live_media_limit import (
    DEFAULT_CHUNK_SIZE,
    MAX_DOWNLOAD_CHUNK_SIZE,
    TELEGRAM_DEFAULT_LIMIT_BYTES,
    TransferRecorder,
    benchmark_peer_for_actor,
    deterministic_chunk,
    effective_download_request_timeout,
    effective_upload_request_timeout,
    ensure_benchmark_file,
    file_id_for_actor,
    format_media_lanes,
    parse_args,
    parse_size,
    prompt_code_http,
    sample_stats,
    should_use_http_code_prompt,
    transfer_counters,
)

from miniproto.observability import InMemoryMetrics


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
    recorder.record(10 * one_mib, 10 * one_mib, now=11.0)
    assert recorder.samples_mib_s == pytest.approx([1.0, 1.0])
    duration, transfer_duration, _stats = recorder.finish(10 * one_mib)
    assert duration >= transfer_duration
    assert transfer_duration == pytest.approx(10.0)


def test_transfer_recorder_heartbeat_reports_stalled_progress(capsys) -> None:
    one_mib = 1024 * 1024
    recorder = TransferRecorder(
        total=10 * one_mib, label="bench", progress_interval_s=5, sample_interval_s=5
    )
    recorder.begin(now=1.0)
    recorder.report_heartbeat(now=6.1)
    captured = capsys.readouterr().out
    assert "bench:" in captured
    assert "0.00%" in captured
    recorder.report_heartbeat(now=7.0)
    assert capsys.readouterr().out == ""


def test_transfer_recorder_heartbeat_does_not_hide_moving_window(capsys) -> None:
    one_mib = 1024 * 1024
    recorder = TransferRecorder(
        total=10 * one_mib, label="bench", progress_interval_s=5, sample_interval_s=5
    )
    recorder.begin(now=1.0)
    recorder.record(one_mib, 10 * one_mib, now=3.0)
    recorder.report_heartbeat(now=6.1)
    assert capsys.readouterr().out == ""
    recorder.record(5 * one_mib, 10 * one_mib, now=6.2)
    captured = capsys.readouterr().out
    assert "bench:" in captured
    assert "window=0.962MiB/s" in captured
    recorder.report_heartbeat(now=11.3)
    stalled = capsys.readouterr().out
    assert "bench:" in stalled
    assert "window=0.000MiB/s" in stalled


def test_upload_request_timeout_defaults_to_shorter_part_timeout() -> None:
    args = parse_args(["--actor", "user"], {})
    assert args.request_timeout == 120
    assert args.upload_request_timeout == 45
    assert effective_upload_request_timeout(args) == 45
    overridden = parse_args(["--actor", "user", "--upload-request-timeout", "60"], {})
    assert effective_upload_request_timeout(overridden) == 60


def test_download_request_timeout_defaults_to_shorter_part_timeout() -> None:
    args = parse_args(["--actor", "user"], {})
    assert args.request_timeout == 120
    assert args.repeat == 1
    assert args.download_concurrency == 1
    assert args.download_request_timeout is None
    assert effective_download_request_timeout(args) == 30
    assert args.download_flood_sleep_threshold == 30
    assert args.download_chunk_size == DEFAULT_CHUNK_SIZE
    assert args.download_adaptive_concurrency is True
    assert args.download_max_in_flight_bytes is None
    assert args.download_adaptive_part_size is True
    assert args.download_max_chunk_size == MAX_DOWNLOAD_CHUNK_SIZE
    assert args.download_read_ahead_bytes == 0
    assert args.download_range_cache_bytes == 0
    overridden = parse_args(["--actor", "user", "--download-request-timeout", "45"], {})
    assert effective_download_request_timeout(overridden) == 45


def test_repeat_can_be_configured_from_env_and_cli() -> None:
    env_repeat = parse_args(["--actor", "user"], {"MINIPROTO_LIVE_BENCH_REPEAT": "3"})
    assert env_repeat.repeat == 3
    cli_repeat = parse_args(["--actor", "user", "--repeat", "2"], {})
    assert cli_repeat.repeat == 2
    with pytest.raises(SystemExit):
        parse_args(["--actor", "user", "--repeat", "0"], {})


def test_download_concurrency_is_independent_from_upload_concurrency() -> None:
    shared = parse_args(["--actor", "user"], {"MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY": "8"})
    assert shared.upload_concurrency == 8
    assert shared.download_concurrency == 1
    specific = parse_args(
        ["--actor", "user"],
        {
            "MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY": "8",
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY": "2",
        },
    )
    assert specific.upload_concurrency == 8
    assert specific.download_concurrency == 2
    overridden = parse_args(["--actor", "user", "--download-concurrency", "6"], {})
    assert overridden.download_concurrency == 6


def test_media_lanes_are_directional_and_use_measured_defaults() -> None:
    defaults = parse_args(["--actor", "user"], {})
    assert defaults.upload_media_lanes == 2
    assert defaults.download_media_lanes == 1
    assert format_media_lanes(defaults.upload_media_lanes, defaults.upload_concurrency) == "2"
    assert format_media_lanes(defaults.download_media_lanes, defaults.download_concurrency) == "1"
    specific = parse_args(
        ["--actor", "user"],
        {
            "MINIPROTO_LIVE_BENCH_UPLOAD_MEDIA_LANES": "0",
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_MEDIA_LANES": "2",
        },
    )
    assert specific.upload_media_lanes == 0
    assert specific.download_media_lanes == 2
    overridden = parse_args(
        ["--actor", "user", "--upload-media-lanes", "4", "--download-media-lanes", "0"], {}
    )
    assert overridden.upload_media_lanes == 4
    assert overridden.download_media_lanes == 0


def test_operation_and_file_id_options_support_download_only() -> None:
    args = parse_args(["--actor", "user", "--operation", "download", "--file-id", "mpf1_test"], {})
    assert args.operation == "download"
    assert args.file_id == "mpf1_test"
    assert file_id_for_actor(args, {}, "user") == "mpf1_test"
    assert (
        file_id_for_actor(args, {"MINIPROTO_LIVE_BENCH_USER_FILE_ID": "mpf1_user_specific"}, "user")
        == "mpf1_user_specific"
    )


def test_legacy_generic_upload_concurrency_aliases_still_work() -> None:
    env_alias = parse_args(["--actor", "user"], {"MINIPROTO_LIVE_BENCH_CONCURRENCY": "7"})
    assert env_alias.upload_concurrency == 7
    cli_alias = parse_args(["--actor", "user", "--concurrency", "9"], {})
    assert cli_alias.upload_concurrency == 9
    directional_cli = parse_args(["--actor", "user", "--upload-concurrency", "10"], {})
    assert directional_cli.upload_concurrency == 10


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


def test_download_chunk_size_uses_specific_env_and_cli() -> None:
    args = parse_args(["--actor", "user"], {"MINIPROTO_LIVE_BENCH_DOWNLOAD_CHUNK_SIZE": "1048576"})
    assert args.download_chunk_size == MAX_DOWNLOAD_CHUNK_SIZE
    overridden = parse_args(["--actor", "user", "--download-chunk-size", "1048576"], {})
    assert overridden.download_chunk_size == MAX_DOWNLOAD_CHUNK_SIZE


def test_download_byte_window_and_range_options_use_specific_env_and_cli() -> None:
    args = parse_args(
        ["--actor", "user"],
        {
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_MAX_IN_FLIGHT_BYTES": "2097152",
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_MAX_CHUNK_SIZE": "1048576",
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_READ_AHEAD_BYTES": "1048576",
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_RANGE_CACHE_BYTES": "4194304",
        },
    )
    assert args.download_max_in_flight_bytes == 2 * 1024 * 1024
    assert args.download_max_chunk_size == MAX_DOWNLOAD_CHUNK_SIZE
    assert args.download_read_ahead_bytes == MAX_DOWNLOAD_CHUNK_SIZE
    assert args.download_range_cache_bytes == 4 * 1024 * 1024
    overridden = parse_args(
        [
            "--actor",
            "user",
            "--download-max-in-flight-bytes",
            "1048576",
            "--download-max-chunk-size",
            "1048576",
            "--download-read-ahead-bytes",
            "524288",
            "--download-range-cache-bytes",
            "1048576",
        ],
        {},
    )
    assert overridden.download_max_in_flight_bytes == MAX_DOWNLOAD_CHUNK_SIZE
    assert overridden.download_max_chunk_size == MAX_DOWNLOAD_CHUNK_SIZE
    assert overridden.download_read_ahead_bytes == DEFAULT_CHUNK_SIZE
    assert overridden.download_range_cache_bytes == MAX_DOWNLOAD_CHUNK_SIZE
    with pytest.raises(SystemExit):
        parse_args(
            [
                "--actor",
                "user",
                "--download-chunk-size",
                "1048576",
                "--download-max-in-flight-bytes",
                "524288",
            ],
            {},
        )


def test_download_adaptive_concurrency_can_be_disabled() -> None:
    env_disabled = parse_args(
        ["--actor", "user"], {"MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY": "0"}
    )
    assert env_disabled.download_adaptive_concurrency is False
    cli_enabled = parse_args(
        ["--actor", "user", "--download-adaptive-concurrency"],
        {"MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY": "0"},
    )
    assert cli_enabled.download_adaptive_concurrency is True
    cli_disabled = parse_args(["--actor", "user", "--no-download-adaptive-concurrency"], {})
    assert cli_disabled.download_adaptive_concurrency is False


def test_download_adaptive_part_size_can_be_disabled() -> None:
    env_disabled = parse_args(
        ["--actor", "user"], {"MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_PART_SIZE": "0"}
    )
    assert env_disabled.download_adaptive_part_size is False
    cli_enabled = parse_args(
        ["--actor", "user", "--download-adaptive-part-size"],
        {"MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_PART_SIZE": "0"},
    )
    assert cli_enabled.download_adaptive_part_size is True
    cli_disabled = parse_args(["--actor", "user", "--no-download-adaptive-part-size"], {})
    assert cli_disabled.download_adaptive_part_size is False


def test_http_code_prompt_accepts_posted_code() -> None:
    port = free_local_port()
    path_secret = "test-code-path"  # noqa: S105 - local test route, not a credential
    env = {
        "MINIPROTO_LIVE_BENCH_HTTP_CODE_HOST": "127.0.0.1",
        "MINIPROTO_LIVE_BENCH_HTTP_CODE_PORT": str(port),
        "MINIPROTO_LIVE_BENCH_HTTP_CODE_TIMEOUT": "5",
        "MINIPROTO_LIVE_BENCH_HTTP_CODE_TOKEN": path_secret,
    }
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(prompt_code_http, env)
        url = f"http://127.0.0.1:{port}/{path_secret}"
        wait_for_http_prompt(url)
        payload = urlencode({"code": " 12345 "}).encode("ascii")
        with urlopen(url, data=payload, timeout=2) as response:  # noqa: S310
            assert response.status == 200
        assert future.result(timeout=3) == "12345"


def test_http_code_prompt_env_switch() -> None:
    assert should_use_http_code_prompt({"MINIPROTO_LIVE_BENCH_CODE_PROMPT": "http"})
    assert should_use_http_code_prompt({"MINIPROTO_LIVE_BENCH_HTTP_CODE_PROMPT": "1"})
    assert not should_use_http_code_prompt({})


def test_transfer_counters_aggregate_metrics() -> None:
    metrics = InMemoryMetrics()
    metrics.record_metric("media.download.part_requests", 4)
    metrics.record_metric("media.download.part_retries", 2)
    metrics.record_metric("media.download.flood_waits", 1)
    metrics.record_metric("media.download.flood_wait_seconds", 3)
    metrics.record_metric("media.download.retry_sleep_seconds", 3)
    metrics.record_metric("sender.reconnects", 1)
    metrics.record_metric("client.sender_drops", 1)
    metrics.record_metric("client.sender_drop_skipped", 1)
    metrics.record_metric("client.media_lane_builds", 3)
    metrics.record_metric("client.media_lane_drops", 1, attributes={"reason": "drop"})
    metrics.record_metric("client.media_lane_drops", 2, attributes={"reason": "close"})
    metrics.record_metric("client.media_lane_drop_skipped", 1, attributes={"reason": "drop"})
    metrics.record_metric("media.download.byte_window_waits", 3)
    metrics.record_metric("media.download.writer_queue_seconds", 0.5)
    metrics.record_metric("media.download.writer_write_seconds", 0.25)
    metrics.record_metric("media.download.adaptive_part_size", 1048576)
    metrics.record_metric("media.download.range_cache_hits", 2)
    metrics.record_metric("media.download.range_cache_misses", 3)
    metrics.record_metric("media.download.range_cache_deduped", 1)
    counters = transfer_counters(metrics, "download", 2.0)
    assert counters.part_requests == 4
    assert counters.part_retries == 2
    assert counters.flood_waits == 1
    assert counters.flood_wait_seconds == 3
    assert counters.retry_sleep_seconds == 3
    assert counters.reconnects == 1
    assert counters.sender_drops == 1
    assert counters.sender_drop_skips == 1
    assert counters.media_lane_builds == 3
    assert counters.media_lane_drops == 1
    assert counters.media_lane_closes == 2
    assert counters.media_lane_drop_skips == 1
    assert counters.byte_window_waits == 3
    assert counters.writer_queue_seconds == 0.5
    assert counters.writer_write_seconds == 0.25
    assert counters.adaptive_part_size_changes == 1
    assert counters.range_cache_hits == 2
    assert counters.range_cache_misses == 3
    assert counters.range_cache_deduped == 1
    assert counters.requests_per_s == 2.0


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


def free_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_http_prompt(url: str) -> None:
    deadline = time.monotonic() + 3
    last_error: BaseException | None = None
    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=0.2) as response:  # noqa: S310
                assert response.status == 200
                return
        except URLError as exc:
            last_error = exc
            time.sleep(0.05)
    raise AssertionError(f"HTTP prompt did not start: {last_error}")
