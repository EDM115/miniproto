from __future__ import annotations

import asyncio
import importlib.util
import io
import json
import socket
import sys
import threading
import time
import warnings
from collections.abc import Generator, Mapping
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from html.parser import HTMLParser
from http.client import HTTPResponse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from queue import Queue
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pytest
import tools.bench.benchmark_live_media_limit as benchmark
from tools.bench import secret_prompt
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
    resolved_benchmark_file,
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


@pytest.mark.parametrize("available", [True, False])
def test_benchmark_json_reports_observed_native_availability(
    available: bool, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []
    source = tmp_path / "synthetic.bin"
    destination = tmp_path / "report.json"

    class OfflineClient:
        async def disconnect(self) -> None:
            calls.append("disconnect")

    client = OfflineClient()

    def forbid_live_work(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("offline report test must not read credentials, create sessions or perform live work")

    def validate_offline_inputs(env: Mapping[str, str], *, actor: str) -> None:
        assert env == {} and actor == "user"
        calls.append("guard")

    async def authorize(actor: str, _args: object, env: Mapping[str, str]) -> OfflineClient:
        assert env == {} and actor == "user"
        calls.append("authorize")
        return client

    async def transfer(actual_client: OfflineClient, **kwargs: object) -> tuple[()]:
        assert actual_client is client
        assert kwargs["operation"] == "download"
        assert kwargs["source"] == source
        assert kwargs["file_id"] == "mpf1_synthetic"
        calls.append("transfer")
        return ()

    monkeypatch.setattr(benchmark.os, "environ", {})
    for name in ("Client", "EncryptedSQLiteSessionStorage", "ensure_benchmark_file", "load_dotenv"):
        monkeypatch.setattr(benchmark, name, forbid_live_work)
    monkeypatch.setattr(benchmark, "require_live_env", validate_offline_inputs)
    monkeypatch.setattr(benchmark, "authorized_client", authorize)
    monkeypatch.setattr(benchmark, "benchmark_actor", transfer)
    monkeypatch.setattr(benchmark, "native_available", lambda: available)
    args = parse_args(
        [
            "--actor",
            "user",
            "--operation",
            "download",
            "--size",
            "1024",
            "--file",
            str(source),
            "--file-id",
            "mpf1_synthetic",
            "--json",
            str(destination),
        ],
        {},
    )

    assert asyncio.run(benchmark._run_benchmark(args, {}, None)) == 0
    report = json.loads(destination.read_text(encoding="utf-8"))
    assert report["native_available"] is available
    assert report["operation"] == "download"
    assert report["results"] == []
    assert calls == ["guard", "authorize", "transfer", "disconnect"]
    assert not source.exists()


def test_default_benchmark_file_name_follows_requested_size() -> None:
    args = parse_args(["--actor", "user", "--size", "1000mib"], {})
    assert resolved_benchmark_file(args, {}) == Path(".tmp/miniproto-live-bench-1000mib.bin")


def test_explicit_benchmark_file_name_is_preserved() -> None:
    args = parse_args(["--actor", "user", "--size", "1000mib", "--file", ".tmp/custom.bin"], {})
    assert resolved_benchmark_file(args, {}) == Path(".tmp/custom.bin")
    env_args = parse_args(["--actor", "user", "--size", "1000mib"], {"MINIPROTO_LIVE_BENCH_FILE": ".tmp/from-env.bin"})
    assert resolved_benchmark_file(env_args, {}) == Path(".tmp/from-env.bin")


def test_live_benchmark_loop_lag_and_matrix_controls_prefer_explicit_cli_values() -> None:
    args = parse_args(
        [
            "--loop-lag",
            "--no-download-launch-stagger",
            "--download-destination",
            "memory",
            "--warmup-repeat",
            "1",
            "--operation",
            "download",
        ],
        {
            "MINIPROTO_LIVE_BENCH_LOOP_LAG": "0",
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_LAUNCH_STAGGER": "1",
            "MINIPROTO_LIVE_BENCH_DOWNLOAD_DESTINATION": "file",
        },
    )

    assert args.loop_lag is True
    assert args.download_launch_stagger is False
    assert args.download_destination == "memory"
    assert args.warmup_repeat == 1


def test_legacy_example_benchmark_file_env_does_not_pin_smaller_size() -> None:
    args = parse_args(
        ["--actor", "user", "--size", "1000mib"], {"MINIPROTO_LIVE_BENCH_FILE": ".tmp/miniproto-live-bench-2000mib.bin"}
    )
    assert resolved_benchmark_file(args, {}) == Path(".tmp/miniproto-live-bench-1000mib.bin")


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
    recorder = TransferRecorder(total=15 * one_mib, label="bench", progress_interval_s=0, sample_interval_s=5)
    recorder.begin(now=1.0)
    recorder.record(one_mib, None, now=1.1)
    recorder.record(5 * one_mib, None, now=6.0)
    recorder.record(15 * one_mib, 15 * one_mib, now=11.0)
    assert recorder.samples_mib_s == pytest.approx([1.0, 2.0])
    duration, transfer_duration, _stats = recorder.finish(15 * one_mib)
    assert duration >= transfer_duration
    assert transfer_duration == pytest.approx(10.0)


def test_transfer_recorder_heartbeat_reports_stalled_progress(capsys) -> None:
    one_mib = 1024 * 1024
    recorder = TransferRecorder(total=10 * one_mib, label="bench", progress_interval_s=5, sample_interval_s=5)
    recorder.begin(now=1.0)
    recorder.report_heartbeat(now=6.1)
    captured = capsys.readouterr().out
    assert "bench:" in captured
    assert "0.00%" in captured
    recorder.report_heartbeat(now=7.0)
    assert capsys.readouterr().out == ""


def test_transfer_recorder_heartbeat_does_not_hide_moving_window(capsys) -> None:
    one_mib = 1024 * 1024
    recorder = TransferRecorder(total=10 * one_mib, label="bench", progress_interval_s=5, sample_interval_s=5)
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
    assert args.download_concurrency == 6
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
    assert shared.download_concurrency == 6
    specific = parse_args(
        ["--actor", "user"],
        {"MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY": "8", "MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY": "2"},
    )
    assert specific.upload_concurrency == 8
    assert specific.download_concurrency == 2
    overridden = parse_args(["--actor", "user", "--download-concurrency", "6"], {})
    assert overridden.download_concurrency == 6


def test_media_lanes_are_directional_and_use_measured_defaults() -> None:
    defaults = parse_args(["--actor", "user"], {})
    assert defaults.upload_media_lanes == 2
    assert defaults.download_media_lanes == 2
    assert format_media_lanes(defaults.upload_media_lanes, defaults.upload_concurrency) == "2"
    assert format_media_lanes(defaults.download_media_lanes, defaults.download_concurrency) == "2"
    specific = parse_args(
        ["--actor", "user"],
        {"MINIPROTO_LIVE_BENCH_UPLOAD_MEDIA_LANES": "0", "MINIPROTO_LIVE_BENCH_DOWNLOAD_MEDIA_LANES": "2"},
    )
    assert specific.upload_media_lanes == 0
    assert specific.download_media_lanes == 2
    overridden = parse_args(["--actor", "user", "--upload-media-lanes", "4", "--download-media-lanes", "0"], {})
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
        {"MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD": "9", "MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD": "3"},
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
            ["--actor", "user", "--download-chunk-size", "1048576", "--download-max-in-flight-bytes", "524288"], {}
        )


def test_download_adaptive_concurrency_can_be_disabled() -> None:
    env_disabled = parse_args(["--actor", "user"], {"MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY": "0"})
    assert env_disabled.download_adaptive_concurrency is False
    cli_enabled = parse_args(
        ["--actor", "user", "--download-adaptive-concurrency"],
        {"MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY": "0"},
    )
    assert cli_enabled.download_adaptive_concurrency is True
    cli_disabled = parse_args(["--actor", "user", "--no-download-adaptive-concurrency"], {})
    assert cli_disabled.download_adaptive_concurrency is False


def test_download_adaptive_part_size_can_be_disabled() -> None:
    env_disabled = parse_args(["--actor", "user"], {"MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_PART_SIZE": "0"})
    assert env_disabled.download_adaptive_part_size is False
    cli_enabled = parse_args(
        ["--actor", "user", "--download-adaptive-part-size"], {"MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_PART_SIZE": "0"}
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
        with urlopen(url, data=payload, timeout=2) as response:
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
    metrics.record_metric("media.download.flood_waits", 1, attributes={"error_type": "FloodWait"})
    metrics.record_metric("media.download.flood_waits", 2, attributes={"error_type": "FloodPremiumWait"})
    metrics.record_metric("media.download.flood_wait_seconds", 3, attributes={"error_type": "FloodWait"})
    metrics.record_metric("media.download.flood_wait_seconds", 5, attributes={"error_type": "FloodPremiumWait"})
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
    metrics.record_metric("media.download.launch_pace_wait_seconds", 0.25)
    metrics.record_metric("media.download.launch_pace_wait_seconds", 0.5)
    metrics.record_metric("media.download.launch_pace_rate", 4.0)
    metrics.record_metric("media.download.launch_pace_rate", 2.0)
    metrics.record_metric("media.download.adaptive_part_size", 1048576)
    metrics.record_metric("media.download.range_cache_hits", 2)
    metrics.record_metric("media.download.range_cache_misses", 3)
    metrics.record_metric("media.download.range_cache_deduped", 1)
    counters = transfer_counters(metrics, "download", 2.0)
    assert counters.part_requests == 4
    assert counters.part_retries == 2
    assert counters.flood_waits == 3
    assert counters.flood_wait_seconds == 8
    assert counters.flood_waits_by_type == {"FloodPremiumWait": 2, "FloodWait": 1}
    assert counters.flood_wait_seconds_by_type == {"FloodPremiumWait": 5, "FloodWait": 3}
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
    assert counters.launch_pace_waits == 2
    assert counters.launch_pace_wait_seconds == 0.75
    assert counters.launch_pace_rate_updates == 2
    assert counters.launch_pace_last_rate_per_s == 2.0
    assert counters.launch_pace_min_rate_per_s == 2.0
    assert counters.adaptive_part_size_changes == 1
    assert counters.range_cache_hits == 2
    assert counters.range_cache_misses == 3
    assert counters.range_cache_deduped == 1
    assert counters.requests_per_s == 2.0


def test_bot_peer_must_not_default_to_self() -> None:
    assert benchmark_peer_for_actor("user", {}) == "self"
    assert benchmark_peer_for_actor("bot", {"MINIPROTO_LIVE_BENCH_BOT_PEER": "@benchchat"}) == "@benchchat"
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


@pytest.fixture
def live_helpers(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    path = Path(__file__).parent / "integration" / "live_helpers.py"
    spec = importlib.util.spec_from_file_location("security_prompt_live_helpers", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    vars(module).update(_LOADED_DOTENV=True, _DOTENV_VALUES={})
    monkeypatch.delenv("MINIPROTO_REAL_PASSWORD", raising=False)
    monkeypatch.delenv("MINIPROTO_LIVE_PROMPT_CODE", raising=False)
    return module


def unexpected_prompt(*args: object, **kwargs: object) -> str:
    pytest.fail("credential input was not permitted on this path")


@pytest.mark.parametrize("source", ["integration", "benchmark"])
def test_terminal_credentials_use_hidden_input_and_preserve_password_whitespace(
    source: str, live_helpers: ModuleType, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("MINIPROTO_LIVE_PROMPT_CODE", "1")
    monkeypatch.setattr(benchmark.sys, "stdin", SimpleNamespace(isatty=lambda: True))
    monkeypatch.setattr("builtins.input", unexpected_prompt)
    entered = iter([" 482761 ", "  synthetic 2FA value\t "])
    prompts: list[str] = []

    def hidden_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(entered)

    monkeypatch.setattr(secret_prompt.getpass, "getpass", hidden_input)
    if source == "integration":
        code_reader = live_helpers.code_callback()
        password_reader = live_helpers.password_callback()
        assert password_reader is not None
        assert prompts == []
        assert code_reader() == "482761"
        assert password_reader() == "  synthetic 2FA value\t "
    else:
        env = {"MINIPROTO_LIVE_PROMPT_CODE": "1"}
        assert benchmark.prompt_code(env) == "482761"
        assert benchmark.prompt_password(env) == "  synthetic 2FA value\t "
    assert len(prompts) == 2
    captured = capsys.readouterr()
    assert "482761" not in captured.out + captured.err
    assert "synthetic 2FA value" not in captured.out + captured.err


@pytest.mark.parametrize("flag,is_tty", [(None, True), ("0", True), ("1", False)])
def test_terminal_prompt_gates_still_block_both_credentials(
    flag: str | None, is_tty: bool, live_helpers: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    env: dict[str, str] = {}
    if flag is not None:
        monkeypatch.setenv("MINIPROTO_LIVE_PROMPT_CODE", flag)
        env["MINIPROTO_LIVE_PROMPT_CODE"] = flag
    monkeypatch.setattr(benchmark.sys, "stdin", SimpleNamespace(isatty=lambda: is_tty))
    monkeypatch.setattr(secret_prompt.getpass, "getpass", unexpected_prompt)
    monkeypatch.setattr("builtins.input", unexpected_prompt)
    with pytest.raises(pytest.skip.Exception):
        live_helpers.code_callback()
    assert live_helpers.password_callback() is None
    with pytest.raises(SystemExit):
        benchmark.prompt_code(env)
    assert benchmark.prompt_password(env) == ""


@pytest.mark.parametrize("is_tty", [True, False])
def test_configured_password_wins_without_a_prompt(
    is_tty: bool, live_helpers: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MINIPROTO_LIVE_PROMPT_CODE", "1")
    monkeypatch.setenv("MINIPROTO_REAL_PASSWORD", "  environment value\t ")
    live_helpers._DOTENV_VALUES["MINIPROTO_REAL_PASSWORD"] = "different dotenv value"  # noqa: S105 - synthetic prompt fixture
    monkeypatch.setattr(benchmark.sys, "stdin", SimpleNamespace(isatty=lambda: is_tty))
    monkeypatch.setattr(secret_prompt.getpass, "getpass", unexpected_prompt)
    monkeypatch.setattr("builtins.input", unexpected_prompt)
    callback = live_helpers.password_callback()
    assert callback is not None
    assert callback() == "  environment value\t "
    assert benchmark.prompt_password({"MINIPROTO_REAL_PASSWORD": "  environment value\t "}) == "  environment value\t "
    monkeypatch.delenv("MINIPROTO_REAL_PASSWORD")
    dotenv_callback = live_helpers.password_callback()
    assert dotenv_callback is not None
    assert dotenv_callback() == "different dotenv value"


def test_hidden_input_failure_stops_before_fallback_reads(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    terminal = io.StringIO("synthetic fallback value\n")
    monkeypatch.setattr(sys, "stdin", terminal)
    monkeypatch.setattr(secret_prompt.getpass, "getpass", vars(secret_prompt.getpass)["fallback_getpass"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", secret_prompt.getpass.GetPassWarning)
        original_filters = list(warnings.filters)
        with pytest.raises(RuntimeError, match="Cannot hide terminal input"):
            secret_prompt.prompt_secret("Synthetic credential: ")
        assert warnings.filters == original_filters
    assert terminal.tell() == 0
    captured = capsys.readouterr()
    assert "synthetic fallback value" not in captured.out + captured.err


@pytest.mark.parametrize("failure", [EOFError, KeyboardInterrupt])
def test_hidden_input_interruption_propagates_without_retry(
    failure: type[BaseException], monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = 0

    def interrupted_input(prompt: str) -> str:
        nonlocal calls
        calls += 1
        raise failure

    monkeypatch.setattr(secret_prompt.getpass, "getpass", interrupted_input)
    monkeypatch.setattr("builtins.input", unexpected_prompt)
    with pytest.raises(failure):
        secret_prompt.prompt_secret("Synthetic credential: ")
    assert calls == 1


def test_stored_user_session_skips_credential_callbacks(
    live_helpers: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = SimpleNamespace(connect=AsyncMock(), sign_in_phone=AsyncMock())
    monkeypatch.setattr(live_helpers, "live_client", lambda name: client)
    monkeypatch.setattr(live_helpers, "stored_user", AsyncMock(return_value=SimpleNamespace(is_bot=False)))
    monkeypatch.setattr(live_helpers, "code_callback", unexpected_prompt)
    monkeypatch.setattr(live_helpers, "password_callback", unexpected_prompt)
    assert asyncio.run(live_helpers.authorized_user_client()) is client
    client.connect.assert_awaited_once()
    client.sign_in_phone.assert_not_called()


def test_http_mode_still_bypasses_terminal_prompt_gates(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(benchmark.sys, "stdin", SimpleNamespace(isatty=lambda: False))
    monkeypatch.setattr(secret_prompt.getpass, "getpass", unexpected_prompt)
    monkeypatch.setattr("builtins.input", unexpected_prompt)
    monkeypatch.setattr(benchmark, "prompt_code_http", lambda env: "639281")
    assert benchmark.prompt_code({"MINIPROTO_LIVE_BENCH_CODE_PROMPT": "http"}) == "639281"


def test_http_login_code_field_is_masked_and_keeps_submission_controls() -> None:
    class FormParser(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.fields: list[dict[str, str | None]] = []
            self.forms: list[dict[str, str | None]] = []

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            if tag == "input":
                self.fields.append(dict(attrs))
            if tag == "form":
                self.forms.append(dict(attrs))

    parser = FormParser()
    parser.feed(benchmark._code_prompt_html(error=None))
    code_fields = [field for field in parser.fields if field.get("name") == "code"]
    assert len(code_fields) == 1
    assert code_fields[0]["type"] == "password"
    assert code_fields[0]["inputmode"] == "numeric"
    assert code_fields[0]["autocomplete"] == "one-time-code"
    assert "autofocus" in code_fields[0]
    assert [form.get("method") for form in parser.forms] == ["post"]


@dataclass
class Prompt:
    address: tuple[str, int]
    result: Future[str]
    reading_body: threading.Event

    def connect(self) -> socket.socket:
        return socket.create_connection(self.address, timeout=2)

    def submit(self, body: bytes) -> tuple[int, bytes, dict[str, str]]:
        with self.connect() as connection:
            send_headers(connection, [f"Content-Length: {len(body)}".encode("ascii")])
            connection.sendall(body)
            return receive_response(connection)


def send_headers(connection: socket.socket, headers: list[bytes], *, path: bytes = b"/local-test-route") -> None:
    connection.sendall(b"POST " + path + b" HTTP/1.1\r\nHost: localhost\r\n" + b"\r\n".join(headers) + b"\r\n\r\n")


def receive_response(connection: socket.socket) -> tuple[int, bytes, dict[str, str]]:
    with HTTPResponse(connection) as response:
        response.begin()
        return response.status, response.read(), dict(response.getheaders())


@contextmanager
def running_prompt(monkeypatch: pytest.MonkeyPatch, *, timeout: float = 5) -> Generator[Prompt]:
    servers: Queue[ThreadingHTTPServer] = Queue()
    reading_body = threading.Event()

    def create_server(address: tuple[str, int], handler: type[BaseHTTPRequestHandler]) -> ThreadingHTTPServer:
        original_read_body = vars(handler)["_read_body"]

        def read_body(self: BaseHTTPRequestHandler, length: int) -> bytes | None:
            reading_body.set()
            return original_read_body(self, length)

        monkeypatch.setattr(handler, "_read_body", read_body)
        server = ThreadingHTTPServer(address, handler)
        servers.put(server)
        return server

    monkeypatch.setattr(benchmark, "ThreadingHTTPServer", create_server)
    env = {
        "MINIPROTO_LIVE_BENCH_HTTP_CODE_HOST": "127.0.0.1",
        "MINIPROTO_LIVE_BENCH_HTTP_CODE_PORT": "0",
        "MINIPROTO_LIVE_BENCH_HTTP_CODE_TIMEOUT": str(timeout),
        "MINIPROTO_LIVE_BENCH_HTTP_CODE_TOKEN": "local-test-route",
    }
    with ThreadPoolExecutor(max_workers=1) as pool:
        result = pool.submit(benchmark.prompt_code_http, env)
        server = servers.get(timeout=3)
        prompt = Prompt(("127.0.0.1", int(server.server_address[1])), result, reading_body)
        try:
            yield prompt
        finally:
            if not result.done():
                with suppress(OSError):
                    prompt.submit(b"code=cleanup")
            with suppress(SystemExit):
                result.result(timeout=3)


@pytest.mark.parametrize(
    "headers,status",
    [
        ([], 400),
        ([b"Content-Length:"], 400),
        ([b"Content-Length: -1"], 400),
        ([b"Content-Length: +12"], 400),
        ([b"Content-Length: 1_2"], 400),
        ([b"Content-Length: invalid"], 400),
        ([b"Content-Length: 12, 12"], 400),
        ([b"Content-Length: 12", b"Content-Length: 12"], 400),
        ([b"Content-Length: 12", b"Content-Length: 256"], 400),
        ([b"Transfer-Encoding: chunked"], 400),
        ([b"Content-Length: 12", b"Transfer-Encoding: chunked"], 400),
        ([b"Content-Length: 12", b"Transfer-Encoding:"], 400),
        ([b"Content-Length: 257"], 413),
        ([b"Content-Length: " + b"9" * 5000], 413),
    ],
)
def test_invalid_framing_is_rejected_without_waiting_for_body(
    headers: list[bytes], status: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    with running_prompt(monkeypatch) as prompt:
        with prompt.connect() as connection:
            send_headers(connection, headers)
            actual, _, response_headers = receive_response(connection)
            assert actual == status
            assert response_headers["Cache-Control"] == "no-store"
            assert connection.recv(1) == b""
        assert not prompt.reading_body.is_set()
        assert not prompt.result.done()
        assert prompt.submit(b"code=482761")[0] == 200
        assert prompt.result.result(timeout=2) == "482761"


def test_unknown_capability_is_rejected_before_length_or_body_handling(monkeypatch: pytest.MonkeyPatch) -> None:
    with running_prompt(monkeypatch) as prompt:
        with prompt.connect() as connection:
            send_headers(connection, [b"Content-Length: -1"], path=b"/wrong-route")
            assert receive_response(connection)[0] == 404
        assert not prompt.reading_body.is_set()
        assert not prompt.result.done()


def test_empty_body_does_not_complete_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    with running_prompt(monkeypatch) as prompt:
        assert prompt.submit(b"")[0] == 400
        assert not prompt.result.done()
        assert prompt.submit(b"code=582619")[0] == 200
        assert prompt.result.result(timeout=2) == "582619"


def test_exactly_256_bytes_and_leading_zero_length_preserve_form_submission(monkeypatch: pytest.MonkeyPatch) -> None:
    body = b"padding=" + b"x" * 235 + b"&code=48+2761"
    assert len(body) == 256
    with running_prompt(monkeypatch) as prompt:
        with prompt.connect() as connection:
            send_headers(connection, [b"Content-Length: " + b"0" * 5000 + b"256"])
            connection.sendall(body + b"unframed-extra")
            status, response_body, response_headers = receive_response(connection)
            assert status == 200
            assert b"482761" not in response_body
            assert response_headers["Cache-Control"] == "no-store"
        assert prompt.result.result(timeout=2) == "482761"


def test_short_body_is_rejected_before_parsing_partial_code(monkeypatch: pytest.MonkeyPatch) -> None:
    with running_prompt(monkeypatch) as prompt:
        with prompt.connect() as connection:
            send_headers(connection, [b"Content-Length: 20"])
            connection.sendall(b"code=12345")
            connection.shutdown(socket.SHUT_WR)
            assert receive_response(connection)[0] == 400
        assert not prompt.result.done()
        assert prompt.submit(b"code=693815")[0] == 200
        assert prompt.result.result(timeout=2) == "693815"


def test_body_deadline_expires_despite_regular_small_writes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(benchmark, "HTTP_CODE_BODY_TIMEOUT_SECONDS", 0.25)
    with running_prompt(monkeypatch) as prompt:
        with prompt.connect() as connection:
            send_headers(connection, [b"Content-Length: 256"])
            assert prompt.reading_body.wait(timeout=1)
            stopped = threading.Event()

            def drip_body() -> None:
                while not stopped.wait(0.03):
                    try:
                        connection.sendall(b"x")
                    except OSError:
                        return

            thread = threading.Thread(target=drip_body, daemon=True)
            thread.start()
            started = time.monotonic()
            try:
                assert receive_response(connection)[0] == 408
                assert time.monotonic() - started < 1
                assert connection.recv(1) == b""
            finally:
                stopped.set()
                thread.join(timeout=1)
        assert not prompt.result.done()


def test_success_closes_another_active_body_reader(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(benchmark, "HTTP_CODE_BODY_TIMEOUT_SECONDS", 30)
    with running_prompt(monkeypatch, timeout=10) as prompt, prompt.connect() as stalled:
        send_headers(stalled, [b"Content-Length: 256"])
        assert prompt.reading_body.wait(timeout=1)
        assert prompt.submit(b"code=267951")[0] == 200
        assert prompt.result.result(timeout=2) == "267951"
        assert stalled.recv(1) == b""


def test_prompt_expiry_closes_an_active_body_reader(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(benchmark, "HTTP_CODE_BODY_TIMEOUT_SECONDS", 30)
    with running_prompt(monkeypatch, timeout=0.3) as prompt, prompt.connect() as stalled:
        send_headers(stalled, [b"Content-Length: 256"])
        assert prompt.reading_body.wait(timeout=1)
        with pytest.raises(SystemExit, match="timed out waiting"):
            prompt.result.result(timeout=2)
        response = bytearray()
        while chunk := stalled.recv(1024):
            response.extend(chunk)
        assert not response or bytes(response).startswith(b"HTTP/1.0 408 ")
