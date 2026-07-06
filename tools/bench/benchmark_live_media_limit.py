from __future__ import annotations

import argparse
import asyncio
import hashlib
import html
import json
import math
import os
import secrets
import statistics
import sys
import threading
import time
from collections.abc import Callable, Mapping
from contextlib import suppress
from dataclasses import asdict, dataclass
from getpass import getpass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from queue import Empty, Full, Queue
from typing import Any, Literal
from urllib.parse import parse_qs

from miniproto import (
    Client,
    ClientConfig,
    EncryptedSQLiteSessionStorage,
    InMemoryMetrics,
    MemoryMonitor,
    TransportConfig,
    configure_logging,
    event_loop,
    get_metrics_sink,
    set_metrics_sink,
)
from miniproto.file_id import encode_file_id, media_from_file_id
from miniproto.invoke import load_session_record
from miniproto.media import DEFAULT_CHUNK_SIZE, MAX_DOWNLOAD_CHUNK_SIZE

TELEGRAM_DEFAULT_UPLOAD_PARTS = 4000
TELEGRAM_DEFAULT_LIMIT_BYTES = TELEGRAM_DEFAULT_UPLOAD_PARTS * DEFAULT_CHUNK_SIZE
BENCH_GUARD_ENV = "MINIPROTO_LIVE_BENCH"
DEFAULT_UPLOAD_REQUEST_TIMEOUT = 45.0
DEFAULT_DOWNLOAD_CONCURRENCY = 1

Actor = Literal["user", "bot"]
Operation = Literal["both", "upload", "download"]


@dataclass(frozen=True, slots=True)
class SampleStats:
    avg_mib_s: float
    median_mib_s: float
    p01_mib_s: float
    p05_mib_s: float
    p95_mib_s: float
    p99_mib_s: float
    min_mib_s: float
    max_mib_s: float
    slowest_1pct_avg_mib_s: float
    fastest_5pct_avg_mib_s: float
    stdev_mib_s: float
    samples: int


@dataclass(frozen=True, slots=True)
class TransferCounters:
    part_requests: int
    part_retries: int
    flood_waits: int
    flood_wait_seconds: float
    retry_sleep_seconds: float
    reconnects: int
    sender_drops: int
    sender_drop_skips: int
    media_lane_builds: int
    media_lane_drops: int
    media_lane_drop_skips: int
    media_lane_closes: int
    byte_window_waits: int
    writer_queue_seconds: float
    writer_write_seconds: float
    adaptive_part_size_changes: int
    range_cache_hits: int
    range_cache_misses: int
    range_cache_deduped: int
    requests_per_s: float


@dataclass(frozen=True, slots=True)
class TransferSummary:
    actor: Actor
    operation: Literal["upload", "download"]
    repeat_index: int
    dc_id: int
    media_dc_id: int | None
    bytes: int
    duration_s: float
    transfer_duration_s: float
    finalize_duration_s: float
    overall_mib_s: float
    transfer_mib_s: float
    samples: SampleStats
    counters: TransferCounters
    peer: str
    message_id: int | None = None
    path: str | None = None
    file_id: str | None = None


@dataclass(frozen=True, slots=True)
class MemorySummary:
    rss_start_bytes: int | None
    rss_end_bytes: int | None
    rss_peak_bytes: int | None
    rss_delta_bytes: int | None
    traced_current_delta_bytes: int | None
    traced_peak_bytes: int | None
    gc_objects_delta: int
    leak_suspected: bool


@dataclass(frozen=True, slots=True)
class BenchmarkSummary:
    generated_file: str
    generated_file_bytes: int
    chunk_size: int
    download_chunk_size: int
    upload_limit_parts: int
    operation: Operation
    upload_concurrency: int
    upload_media_lanes: int | None
    upload_request_timeout: float
    upload_part_retries: int
    download_concurrency: int
    download_media_lanes: int | None
    download_adaptive_concurrency: bool
    download_max_in_flight_bytes: int | None
    download_adaptive_part_size: bool
    download_max_chunk_size: int
    download_read_ahead_bytes: int
    download_range_cache_bytes: int
    download_request_timeout: float
    download_part_retries: int
    download_flood_sleep_threshold: int | None
    event_loop_backend: str
    repeat_count: int
    results: tuple[TransferSummary, ...]
    memory: MemorySummary | None = None


@dataclass(slots=True)
class TransferRecorder:
    total: int | None
    label: str
    progress_interval_s: float
    sample_interval_s: float = 5.0
    start: float = 0.0
    last_sample_time: float = 0.0
    last_report_time: float = 0.0
    last_sample_bytes: int = 0
    last_report_bytes: int = 0
    last_bytes: int = 0
    completed_at: float = 0.0
    samples_mib_s: list[float] | None = None

    def __post_init__(self) -> None:
        self.samples_mib_s = []

    def begin(self, *, now: float | None = None) -> None:
        now = time.perf_counter() if now is None else now
        self.start = now
        self.last_sample_time = now
        self.last_report_time = now
        self.last_sample_bytes = 0
        self.last_report_bytes = 0
        self.last_bytes = 0
        self.completed_at = 0.0
        assert self.samples_mib_s is not None
        self.samples_mib_s.clear()

    async def progress(self, current: int, total: int | None) -> None:
        self.record(current, total)
        await asyncio.sleep(0)

    def record(self, current: int, total: int | None, *, now: float | None = None) -> None:
        sampled_at = time.perf_counter() if now is None else now
        if self.start <= 0:
            self.start = sampled_at
            self.last_sample_time = sampled_at
            self.last_report_time = sampled_at
        if current < self.last_bytes:
            return
        self.last_bytes = current
        if total is not None and total > 0 and current >= total and self.completed_at <= 0:
            self.completed_at = sampled_at
        elapsed = sampled_at - self.last_sample_time
        if elapsed < self.sample_interval_s:
            return
        delta = current - self.last_sample_bytes
        if elapsed <= 0 or delta <= 0:
            self.last_sample_time = sampled_at
            self.last_sample_bytes = current
            return
        assert self.samples_mib_s is not None
        window_mib_s = _mib(delta) / elapsed
        self.samples_mib_s.append(window_mib_s)
        self.last_sample_time = sampled_at
        self.last_sample_bytes = current
        if (
            self.progress_interval_s > 0
            and sampled_at - self.last_report_time >= self.progress_interval_s
        ):
            self.last_report_time = sampled_at
            self.last_report_bytes = current
            print_progress(
                self.label,
                current=current,
                total=self.total,
                elapsed_s=sampled_at - self.start,
                window_mib_s=window_mib_s,
            )

    def report_heartbeat(self, *, now: float | None = None) -> None:
        if self.progress_interval_s <= 0 or self.start <= 0:
            return
        if self.last_bytes != self.last_report_bytes:
            return
        sampled_at = time.perf_counter() if now is None else now
        if sampled_at - self.last_report_time < self.progress_interval_s:
            return
        self.last_report_time = sampled_at
        print_progress(
            self.label,
            current=self.last_bytes,
            total=self.total,
            elapsed_s=sampled_at - self.start,
            window_mib_s=0.0,
        )

    def finish(self, bytes_done: int) -> tuple[float, float, SampleStats]:
        finished_at = time.perf_counter()
        duration = max(finished_at - self.start, 1e-9)
        transfer_end = self.completed_at if self.completed_at > 0 else finished_at
        transfer_duration = max(transfer_end - self.start, 1e-9)
        assert self.samples_mib_s is not None
        return (
            duration,
            transfer_duration,
            sample_stats(self.samples_mib_s, fallback_overall_mib_s=_mib(bytes_done) / duration),
        )


def main(argv: list[str] | None = None) -> int:
    env = load_dotenv()
    args = parse_args(argv, env)
    configure_standard_streams_line_buffering()
    if env_value(env, BENCH_GUARD_ENV) != "1":
        print(
            f"Refusing to run the live media-limit benchmark without {BENCH_GUARD_ENV}=1. "
            "This benchmark creates and transfers a roughly 2 GB file.",
            file=sys.stderr,
        )
        return 2
    configure_logging(args.log_level, format=args.log_format)
    print(
        f"event_loop_backend={event_loop.backend_name()} "
        f"installed={event_loop.installed()} version={event_loop.backend_version()}"
    )
    return event_loop.run(run_benchmark(args, env))


def configure_standard_streams_line_buffering() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        with suppress(TypeError, ValueError):
            reconfigure(line_buffering=True, write_through=True)


def parse_args(
    argv: list[str] | None = None, env: Mapping[str, str] | None = None
) -> argparse.Namespace:
    values = {} if env is None else env
    json_path = env_value(values, "MINIPROTO_LIVE_BENCH_JSON")
    parser = argparse.ArgumentParser(
        description="Run opt-in live Telegram media-limit upload/download benchmarks."
    )
    parser.add_argument(
        "--actor",
        choices=("user", "bot", "both"),
        default=env_value(values, "MINIPROTO_LIVE_BENCH_ACTOR", "both"),
        help="which authorized account to benchmark",
    )
    parser.add_argument(
        "--operation",
        choices=("both", "upload", "download"),
        default=env_value(values, "MINIPROTO_LIVE_BENCH_OPERATION", "both"),
        help="which transfer operation to run",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=int(env_value(values, "MINIPROTO_LIVE_BENCH_REPEAT", "1") or "1"),
        help="repeat each selected actor/profile this many times; useful because Telegram media throughput is noisy",
    )
    parser.add_argument(
        "--file-id",
        default=env_value(values, "MINIPROTO_LIVE_BENCH_FILE_ID"),
        help="miniproto benchmark file id printed by an earlier upload run; required for download-only unless an actor-specific file-id env var is set",
    )
    parser.add_argument(
        "--size",
        default=env_value(values, "MINIPROTO_LIVE_BENCH_SIZE", "telegram-default"),
        help="payload size, e.g. telegram-default, 2000mib, 2gb, or a byte count",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=Path(
            env_value(values, "MINIPROTO_LIVE_BENCH_FILE", ".tmp/miniproto-live-bench-2000mib.bin")
            or ".tmp/miniproto-live-bench-2000mib.bin"
        ),
        help="path to the deterministic benchmark payload",
    )
    parser.add_argument(
        "--download-dir",
        type=Path,
        default=Path(
            env_value(values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_DIR", ".tmp/live-bench-downloads")
            or ".tmp/live-bench-downloads"
        ),
        help="directory for downloaded benchmark payloads",
    )
    parser.add_argument(
        "--dc-id",
        type=int,
        default=int(
            env_value(values, "MINIPROTO_LIVE_BENCH_DC_ID")
            or env_value(values, "MINIPROTO_REAL_DC_ID")
            or "4"
        ),
        help="production DC id to use for both user and bot sessions",
    )
    upload_concurrency_default = env_value(
        values,
        "MINIPROTO_LIVE_BENCH_UPLOAD_CONCURRENCY",
        env_value(values, "MINIPROTO_LIVE_BENCH_CONCURRENCY", "8"),
    )
    parser.add_argument(
        "--upload-concurrency",
        dest="upload_concurrency",
        type=int,
        default=int(upload_concurrency_default or "8"),
        help="number of concurrent upload part requests on the active MTProto sender",
    )
    parser.add_argument(
        "--concurrency",
        dest="upload_concurrency",
        type=int,
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS,
    )
    upload_media_lanes = env_value(values, "MINIPROTO_LIVE_BENCH_UPLOAD_MEDIA_LANES")
    parser.add_argument(
        "--upload-media-lanes",
        type=int,
        default=int(upload_media_lanes) if upload_media_lanes else None,
        help="MTProto sender lanes for upload parts; default follows --upload-concurrency, set 0 for the legacy main-sender path",
    )
    parser.add_argument(
        "--download-concurrency",
        type=int,
        default=int(
            env_value(
                values,
                "MINIPROTO_LIVE_BENCH_DOWNLOAD_CONCURRENCY",
                str(DEFAULT_DOWNLOAD_CONCURRENCY),
            )
            or str(DEFAULT_DOWNLOAD_CONCURRENCY)
        ),
        help="maximum concurrent upload.getFile requests for known-size downloads; defaults to 1 because Telegram flood waits can erase concurrency gains",
    )
    download_media_lanes = env_value(values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_MEDIA_LANES")
    parser.add_argument(
        "--download-media-lanes",
        type=int,
        default=int(download_media_lanes) if download_media_lanes else None,
        help="MTProto sender lanes for download parts; default follows --download-concurrency, set 0 for the legacy main-sender path",
    )
    download_adaptive_default = env_bool(
        values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_CONCURRENCY", default=True
    )
    download_adaptive = parser.add_mutually_exclusive_group()
    download_adaptive.add_argument(
        "--download-adaptive-concurrency",
        dest="download_adaptive_concurrency",
        action="store_true",
        default=download_adaptive_default,
        help="adaptively reduce and slowly re-grow concurrent download requests after flood waits or disconnects",
    )
    download_adaptive.add_argument(
        "--no-download-adaptive-concurrency",
        dest="download_adaptive_concurrency",
        action="store_false",
        help="disable adaptive download request pacing for comparison runs",
    )
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=float(env_value(values, "MINIPROTO_LIVE_BENCH_REQUEST_TIMEOUT", "120") or "120"),
        help="per-request timeout in seconds",
    )
    upload_timeout = env_value(
        values, "MINIPROTO_LIVE_BENCH_UPLOAD_REQUEST_TIMEOUT", str(DEFAULT_UPLOAD_REQUEST_TIMEOUT)
    )
    parser.add_argument(
        "--upload-request-timeout",
        type=float,
        default=float(upload_timeout) if upload_timeout else None,
        help=f"per-upload-part timeout in seconds; defaults to {DEFAULT_UPLOAD_REQUEST_TIMEOUT:g}s for live media benchmarks",
    )
    parser.add_argument(
        "--upload-part-retries",
        type=int,
        default=int(env_value(values, "MINIPROTO_LIVE_BENCH_UPLOAD_PART_RETRIES", "6") or "6"),
        help="media-layer retries per upload part after transient failures",
    )
    download_timeout = env_value(values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_REQUEST_TIMEOUT")
    parser.add_argument(
        "--download-request-timeout",
        type=float,
        default=float(download_timeout) if download_timeout else None,
        help="per-download-part timeout in seconds; defaults to min(--request-timeout, 30)",
    )
    parser.add_argument(
        "--download-part-retries",
        type=int,
        default=int(env_value(values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_PART_RETRIES", "6") or "6"),
        help="media-layer retries per download part after transient failures",
    )
    parser.add_argument(
        "--download-chunk-size",
        type=int,
        default=int(
            env_value(values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_CHUNK_SIZE", str(DEFAULT_CHUNK_SIZE))
            or str(DEFAULT_CHUNK_SIZE)
        ),
        help=f"upload.getFile request size in bytes; defaults to 512 KiB for stable live runs; use {MAX_DOWNLOAD_CHUNK_SIZE} for 1 MiB comparison runs",
    )
    download_max_in_flight = env_value(values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_MAX_IN_FLIGHT_BYTES")
    parser.add_argument(
        "--download-max-in-flight-bytes",
        type=int,
        default=int(download_max_in_flight) if download_max_in_flight else None,
        help="cap in-flight download bytes across active upload.getFile requests; empty uses chunk_size * concurrency",
    )
    download_adaptive_part_default = env_bool(
        values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_ADAPTIVE_PART_SIZE", default=True
    )
    download_adaptive_part = parser.add_mutually_exclusive_group()
    download_adaptive_part.add_argument(
        "--download-adaptive-part-size",
        dest="download_adaptive_part_size",
        action="store_true",
        default=download_adaptive_part_default,
        help="try larger download chunks during large transfers and keep the fastest observed size",
    )
    download_adaptive_part.add_argument(
        "--no-download-adaptive-part-size",
        dest="download_adaptive_part_size",
        action="store_false",
        help="keep --download-chunk-size fixed for controlled comparison runs",
    )
    parser.add_argument(
        "--download-max-chunk-size",
        type=int,
        default=int(
            env_value(
                values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_MAX_CHUNK_SIZE", str(MAX_DOWNLOAD_CHUNK_SIZE)
            )
            or str(MAX_DOWNLOAD_CHUNK_SIZE)
        ),
        help=f"largest chunk size adaptive download part sizing may try; Telegram currently caps upload.getFile at {MAX_DOWNLOAD_CHUNK_SIZE} bytes",
    )
    parser.add_argument(
        "--download-read-ahead-bytes",
        type=int,
        default=int(
            env_value(values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_READ_AHEAD_BYTES", "0") or "0"
        ),
        help="optional range-cache read-ahead budget in bytes; useful for range/stream experiments, disabled by default",
    )
    parser.add_argument(
        "--download-range-cache-bytes",
        type=int,
        default=int(
            env_value(values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_RANGE_CACHE_BYTES", "0") or "0"
        ),
        help="optional in-memory range cache size in bytes; 0 disables benchmark range caching",
    )
    download_flood_sleep_threshold = env_value(
        values, "MINIPROTO_LIVE_BENCH_DOWNLOAD_FLOOD_SLEEP_THRESHOLD", "30"
    )
    parser.add_argument(
        "--download-flood-sleep-threshold",
        type=int,
        default=int(download_flood_sleep_threshold)
        if download_flood_sleep_threshold is not None
        else None,
        help="maximum FLOOD_WAIT seconds to sleep and retry per download chunk",
    )
    parser.add_argument(
        "--force-regenerate",
        action="store_true",
        default=env_value(values, "MINIPROTO_LIVE_BENCH_FORCE_REGENERATE") == "1",
        help="rewrite the payload even when the target path already has the expected size",
    )
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="create/validate the payload and exit without contacting Telegram",
    )
    parser.add_argument(
        "--verify-digest",
        action="store_true",
        default=env_value(values, "MINIPROTO_LIVE_BENCH_VERIFY_DIGEST") == "1",
        help="compare source/download BLAKE2b digests after each download; digest time is not included in transfer timings",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=Path(json_path) if json_path else None,
        help="optional path to write machine-readable benchmark results",
    )
    parser.add_argument(
        "--progress-interval",
        type=float,
        default=float(env_value(values, "MINIPROTO_LIVE_BENCH_PROGRESS_INTERVAL", "5") or "5"),
        help="seconds between upload/download progress lines; set 0 to keep quiet until each transfer finishes",
    )
    parser.add_argument(
        "--log-level",
        default=env_value(
            values,
            "MINIPROTO_LIVE_BENCH_LOG_LEVEL",
            env_value(values, "MINIPROTO_LOG_LEVEL", "INFO"),
        )
        or "INFO",
        help="miniproto log level for the benchmark run",
    )
    parser.add_argument(
        "--log-format",
        choices=("text", "json"),
        default=env_value(values, "MINIPROTO_LIVE_BENCH_LOG_FORMAT", "text") or "text",
        help="structured log output format",
    )
    parser.add_argument(
        "--trace-memory",
        action="store_true",
        default=env_value(values, "MINIPROTO_LIVE_BENCH_TRACE_MEMORY") == "1",
        help="enable tracemalloc while also reporting RSS and GC-object deltas",
    )
    args = parser.parse_args(argv)
    if args.repeat < 1:
        parser.error("--repeat must be positive")
    if args.download_max_chunk_size < args.download_chunk_size:
        parser.error(
            "--download-max-chunk-size must be greater than or equal to --download-chunk-size"
        )
    if (
        args.download_max_in_flight_bytes is not None
        and args.download_max_in_flight_bytes < args.download_chunk_size
    ):
        parser.error(
            "--download-max-in-flight-bytes must be greater than or equal to --download-chunk-size"
        )
    if args.download_read_ahead_bytes < 0:
        parser.error("--download-read-ahead-bytes must not be negative")
    if args.download_range_cache_bytes < 0:
        parser.error("--download-range-cache-bytes must not be negative")
    return args


async def run_benchmark(args: argparse.Namespace, env: Mapping[str, str]) -> int:
    limit_parts = upload_limit_parts_from_env_or_default(env, args.dc_id)
    size = parse_size(args.size, default_bytes=limit_parts * DEFAULT_CHUNK_SIZE)
    upload_needed = args.operation in {"both", "upload"}
    if upload_needed or args.prepare_only:
        print(
            f"payload: path={args.file} bytes={size} chunks={math.ceil(size / DEFAULT_CHUNK_SIZE)} "
            f"chunk_size={DEFAULT_CHUNK_SIZE}"
        )
        ensure_benchmark_file(
            args.file, size=size, chunk_size=DEFAULT_CHUNK_SIZE, force=args.force_regenerate
        )
    else:
        print(
            f"payload: operation=download source_file={args.file} fallback_bytes={size} "
            "local payload generation skipped"
        )
    if args.prepare_only:
        if upload_needed:
            print(f"prepared {args.file} ({size} bytes)")
        else:
            print("download-only mode does not prepare a local payload")
        return 0
    require_live_env(env, actor=args.actor)
    memory_monitor = MemoryMonitor(trace_allocations=args.trace_memory)
    memory_monitor.start()
    actors: tuple[Actor, ...] = ("user", "bot") if args.actor == "both" else (args.actor,)
    results: list[TransferSummary] = []
    upload_request_timeout = effective_upload_request_timeout(args)
    download_request_timeout = effective_download_request_timeout(args)
    for actor in actors:
        print(f"{actor}: authorizing session on DC {args.dc_id}")
        client = await authorized_client(actor, args, env)
        peer = benchmark_peer_for_actor(actor, env)
        try:
            for repeat_index in range(1, args.repeat + 1):
                if args.repeat > 1:
                    print(f"{actor}: starting repeat {repeat_index}/{args.repeat}")
                results.extend(
                    await benchmark_actor(
                        client,
                        actor=actor,
                        operation=args.operation,
                        repeat_index=repeat_index,
                        peer=peer,
                        source=args.file,
                        benchmark_size=size,
                        download_dir=args.download_dir,
                        dc_id=args.dc_id,
                        file_id=file_id_for_actor(args, env, actor),
                        upload_concurrency=args.upload_concurrency,
                        upload_media_lanes=args.upload_media_lanes,
                        download_concurrency=args.download_concurrency,
                        download_media_lanes=args.download_media_lanes,
                        download_adaptive_concurrency=args.download_adaptive_concurrency,
                        download_max_in_flight_bytes=args.download_max_in_flight_bytes,
                        download_adaptive_part_size=args.download_adaptive_part_size,
                        download_max_chunk_size=args.download_max_chunk_size,
                        download_read_ahead_bytes=args.download_read_ahead_bytes,
                        download_range_cache_bytes=args.download_range_cache_bytes,
                        upload_request_timeout=upload_request_timeout,
                        upload_part_retries=args.upload_part_retries,
                        download_request_timeout=download_request_timeout,
                        download_part_retries=args.download_part_retries,
                        download_flood_sleep_threshold=args.download_flood_sleep_threshold,
                        download_chunk_size=args.download_chunk_size,
                        verify_digest=args.verify_digest,
                        progress_interval_s=args.progress_interval,
                    )
                )
        finally:
            await client.disconnect()
    memory = memory_summary(memory_monitor.finish())
    summary = BenchmarkSummary(
        generated_file=str(args.file),
        generated_file_bytes=size,
        chunk_size=DEFAULT_CHUNK_SIZE,
        download_chunk_size=args.download_chunk_size,
        upload_limit_parts=limit_parts,
        operation=args.operation,
        upload_concurrency=args.upload_concurrency,
        upload_media_lanes=args.upload_media_lanes,
        upload_request_timeout=upload_request_timeout,
        upload_part_retries=args.upload_part_retries,
        download_concurrency=args.download_concurrency,
        download_media_lanes=args.download_media_lanes,
        download_adaptive_concurrency=args.download_adaptive_concurrency,
        download_max_in_flight_bytes=args.download_max_in_flight_bytes,
        download_adaptive_part_size=args.download_adaptive_part_size,
        download_max_chunk_size=args.download_max_chunk_size,
        download_read_ahead_bytes=args.download_read_ahead_bytes,
        download_range_cache_bytes=args.download_range_cache_bytes,
        download_request_timeout=download_request_timeout,
        download_part_retries=args.download_part_retries,
        download_flood_sleep_threshold=args.download_flood_sleep_threshold,
        event_loop_backend=event_loop.backend_name(),
        repeat_count=args.repeat,
        results=tuple(results),
        memory=memory,
    )
    print_summary(summary)
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(asdict(summary), indent=2), encoding="utf-8")
    return 0


async def benchmark_actor(
    client: Client,
    *,
    actor: Actor,
    operation: Operation,
    repeat_index: int,
    peer: str,
    source: Path,
    benchmark_size: int,
    download_dir: Path,
    dc_id: int,
    file_id: str | None,
    upload_concurrency: int,
    upload_media_lanes: int | None,
    download_concurrency: int,
    download_media_lanes: int | None,
    download_adaptive_concurrency: bool,
    download_max_in_flight_bytes: int | None,
    download_adaptive_part_size: bool,
    download_max_chunk_size: int,
    download_read_ahead_bytes: int,
    download_range_cache_bytes: int,
    upload_request_timeout: float,
    upload_part_retries: int,
    download_request_timeout: float,
    download_part_retries: int,
    download_flood_sleep_threshold: int | None,
    download_chunk_size: int,
    verify_digest: bool,
    progress_interval_s: float,
) -> tuple[TransferSummary, ...]:
    caption = f"miniproto live media limit bench {actor} r{repeat_index} {int(time.time())}"
    results: list[TransferSummary] = []
    media = None
    message_id: int | None = None
    active_file_id = file_id
    size = benchmark_size
    if operation in {"both", "upload"}:
        size = await asyncio.to_thread(lambda: source.stat().st_size)
        print(
            f"{actor}.upload: starting peer={peer} bytes={size} upload_concurrency={upload_concurrency} "
            f"upload_media_lanes={format_media_lanes(upload_media_lanes, upload_concurrency)} "
            f"upload_request_timeout={upload_request_timeout:g}s retries={upload_part_retries}"
        )
        upload_recorder = TransferRecorder(
            total=size,
            label=f"{actor}.upload",
            progress_interval_s=progress_interval_s,
            sample_interval_s=max(1.0, progress_interval_s or 1.0),
        )
        upload_recorder.begin()
        previous_sink, upload_metrics = begin_transfer_metrics()
        upload_heartbeat = start_progress_heartbeat(upload_recorder)
        try:
            sent = await client.send_file(
                peer,
                source,
                caption=caption,
                file_name=source.name,
                concurrency=upload_concurrency,
                media_lanes=upload_media_lanes,
                progress=upload_recorder.progress,
                request_timeout=upload_request_timeout,
                max_retries=upload_part_retries,
            )
        finally:
            await stop_progress_heartbeat(upload_heartbeat)
            set_metrics_sink(previous_sink)
        upload_duration, upload_transfer_duration, upload_stats = upload_recorder.finish(size)
        upload_counters = transfer_counters(upload_metrics, "upload", upload_duration)
        media = sent.media or await find_recent_media(client, peer, caption)
        if media is None:
            raise RuntimeError(
                f"{actor} upload completed but no media was found for the sent message"
            )
        active_file_id = media.file_id or encode_file_id(media)
        message_id = sent.id or None
        print(f"{actor}.upload: file_id={active_file_id}")
        upload = TransferSummary(
            actor=actor,
            operation="upload",
            repeat_index=repeat_index,
            dc_id=dc_id,
            media_dc_id=media.dc_id,
            bytes=size,
            duration_s=upload_duration,
            transfer_duration_s=upload_transfer_duration,
            finalize_duration_s=max(0.0, upload_duration - upload_transfer_duration),
            overall_mib_s=_mib(size) / upload_duration,
            transfer_mib_s=_mib(size) / upload_transfer_duration,
            samples=upload_stats,
            counters=upload_counters,
            peer=peer,
            message_id=message_id,
            path=str(source),
            file_id=active_file_id,
        )
        print_transfer(upload)
        results.append(upload)
        if operation == "upload":
            return tuple(results)
    else:
        if not active_file_id:
            raise RuntimeError(
                f"{actor} download-only benchmark requires --file-id or MINIPROTO_LIVE_BENCH_{actor.upper()}_FILE_ID"
            )
        media = media_from_file_id(active_file_id)
        size = media.size or benchmark_size
        print(f"{actor}.download: using file_id={active_file_id}")

    if media is None:
        raise RuntimeError(f"{actor} download has no media to download")
    await asyncio.to_thread(download_dir.mkdir, parents=True, exist_ok=True)
    target_name = media.file_name or source.name
    target = download_dir / f"{actor}-dc{dc_id}-{target_name}"
    await asyncio.to_thread(target.unlink, missing_ok=True)
    print(
        f"{actor}.download: starting media_dc={media.dc_id} target={target} "
        f"download_concurrency={download_concurrency} download_request_timeout={download_request_timeout:g}s "
        f"download_media_lanes={format_media_lanes(download_media_lanes, download_concurrency)} "
        f"adaptive={download_adaptive_concurrency} "
        f"retries={download_part_retries} flood_sleep_threshold={download_flood_sleep_threshold} "
        f"chunk_size={download_chunk_size} max_chunk_size={download_max_chunk_size} "
        f"max_in_flight_bytes={download_max_in_flight_bytes} "
        f"adaptive_part_size={download_adaptive_part_size} "
        f"read_ahead_bytes={download_read_ahead_bytes} range_cache_bytes={download_range_cache_bytes}"
    )
    download_recorder = TransferRecorder(
        total=size,
        label=f"{actor}.download",
        progress_interval_s=progress_interval_s,
        sample_interval_s=max(1.0, progress_interval_s or 1.0),
    )
    download_recorder.begin()
    previous_sink, download_metrics = begin_transfer_metrics()
    download_heartbeat = start_progress_heartbeat(download_recorder)
    try:
        downloaded = await client.download_media(
            media,
            target,
            limit=size,
            total_size=size,
            progress=download_recorder.progress,
            request_timeout=download_request_timeout,
            max_retries=download_part_retries,
            flood_sleep_threshold=download_flood_sleep_threshold,
            concurrency=download_concurrency,
            media_lanes=download_media_lanes,
            adaptive_concurrency=download_adaptive_concurrency,
            part_size=download_chunk_size,
            max_in_flight_bytes=download_max_in_flight_bytes,
            adaptive_part_size=download_adaptive_part_size,
            max_part_size=download_max_chunk_size,
            read_ahead_bytes=download_read_ahead_bytes,
            range_cache=download_range_cache_bytes > 0,
            range_cache_max_bytes=download_range_cache_bytes or 64 * 1024 * 1024,
        )
    finally:
        await stop_progress_heartbeat(download_heartbeat)
        set_metrics_sink(previous_sink)
    download_duration, download_transfer_duration, download_stats = download_recorder.finish(
        downloaded.bytes_downloaded
    )
    download_counters = transfer_counters(download_metrics, "download", download_duration)
    if downloaded.bytes_downloaded != size:
        raise RuntimeError(
            f"{actor} download size mismatch: expected {size}, got {downloaded.bytes_downloaded}"
        )
    if verify_digest:
        source_digest, target_digest = await asyncio.gather(
            file_digest(source), file_digest(target)
        )
        if source_digest != target_digest:
            raise RuntimeError(
                f"{actor} download digest mismatch: {source_digest} != {target_digest}"
            )
    download = TransferSummary(
        actor=actor,
        operation="download",
        repeat_index=repeat_index,
        dc_id=dc_id,
        media_dc_id=media.dc_id,
        bytes=downloaded.bytes_downloaded,
        duration_s=download_duration,
        transfer_duration_s=download_transfer_duration,
        finalize_duration_s=max(0.0, download_duration - download_transfer_duration),
        overall_mib_s=_mib(downloaded.bytes_downloaded) / download_duration,
        transfer_mib_s=_mib(downloaded.bytes_downloaded) / download_transfer_duration,
        samples=download_stats,
        counters=download_counters,
        peer=peer,
        message_id=message_id,
        path=str(target),
        file_id=active_file_id,
    )
    print_transfer(download)
    results.append(download)
    return tuple(results)


def start_progress_heartbeat(recorder: TransferRecorder) -> asyncio.Task[None] | None:
    if recorder.progress_interval_s <= 0:
        return None
    return asyncio.create_task(progress_heartbeat(recorder))


async def stop_progress_heartbeat(task: asyncio.Task[None] | None) -> None:
    if task is None:
        return
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


async def progress_heartbeat(recorder: TransferRecorder) -> None:
    try:
        while True:
            await asyncio.sleep(recorder.progress_interval_s)
            recorder.report_heartbeat()
    except asyncio.CancelledError:
        raise


async def authorized_client(
    actor: Actor, args: argparse.Namespace, env: Mapping[str, str]
) -> Client:
    storage = EncryptedSQLiteSessionStorage(
        Path(".tmp") / f"miniproto-live-bench-{actor}-dc{args.dc_id}.sqlite",
        key=required_env(env, "MINIPROTO_SESSION_KEY"),
    )
    client = Client(
        ClientConfig(
            api_id=int(required_env(env, "MINIPROTO_API_ID")),
            api_hash=required_env(env, "MINIPROTO_API_HASH"),
            session_storage=storage,
            transport=TransportConfig(
                read_timeout=args.request_timeout, write_timeout=args.request_timeout
            ),
            dc_id=args.dc_id,
            test_mode=False,
            request_timeout=args.request_timeout,
            max_request_retries=3,
            flood_sleep_threshold=int(
                env_value(env, "MINIPROTO_LIVE_BENCH_FLOOD_SLEEP_THRESHOLD") or "300"
            ),
        )
    )
    await client.connect()
    record = load_session_record(await storage.load(), client.config.dc_id)
    if actor == "bot":
        if record.user is None or not record.user.is_bot:
            await client.sign_in_bot(required_env(env, "MINIPROTO_BOT_TOKEN"))
        return client
    if record.user is None or record.user.is_bot:
        await client.sign_in_phone(
            required_env(env, "MINIPROTO_REAL_PHONE"),
            lambda: prompt_code(env),
            lambda: prompt_password(env),
        )
    return client


def upload_limit_parts_from_env_or_default(env: Mapping[str, str], dc_id: int) -> int:
    del dc_id
    configured = env_value(env, "MINIPROTO_LIVE_BENCH_UPLOAD_PARTS")
    if configured:
        return int(configured)
    return TELEGRAM_DEFAULT_UPLOAD_PARTS


def effective_upload_request_timeout(args: argparse.Namespace) -> float:
    configured = args.upload_request_timeout
    if configured is not None:
        return float(configured)
    return float(args.request_timeout)


def effective_download_request_timeout(args: argparse.Namespace) -> float:
    configured = args.download_request_timeout
    if configured is not None:
        return float(configured)
    return min(float(args.request_timeout), 30.0)


def benchmark_peer_for_actor(actor: Actor, env: Mapping[str, str]) -> str:
    configured = env_value(env, f"MINIPROTO_LIVE_BENCH_{actor.upper()}_PEER")
    if actor == "bot":
        if _is_self_peer(configured):
            raise SystemExit(
                "MINIPROTO_LIVE_BENCH_BOT_PEER must name a chat, user, or channel where the bot can send messages; bots cannot upload to Saved Messages/self."
            )
        assert configured is not None
        return configured.strip()
    return (configured or "self").strip()


def _is_self_peer(peer: str | None) -> bool:
    if peer is None:
        return True
    normalized = peer.strip().casefold().replace("_", " ")
    return normalized in {"", "self", "me", "saved messages"}


async def find_recent_media(client: Client, peer: str, caption: str) -> Any:
    history = await client.get_history(peer, limit=20)
    for message in history:
        if message.text == caption:
            return message.media
    return None


def ensure_benchmark_file(path: Path, *, size: int, chunk_size: int, force: bool = False) -> None:
    if path.exists() and path.stat().st_size == size and not force:
        print(f"payload: existing file has expected size, reusing {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp")
    print(f"payload: generating deterministic file {path}")
    remaining = size
    index = 0
    with temporary.open("wb") as handle:
        while remaining > 0:
            current_size = min(chunk_size, remaining)
            handle.write(deterministic_chunk(index, current_size))
            remaining -= current_size
            index += 1
    temporary.replace(path)
    print(f"payload: ready {path}")


def deterministic_chunk(index: int, size: int) -> bytes:
    seed = f"miniproto-live-media-limit:{index:016x}\n".encode("ascii")
    block = hashlib.blake2b(seed, digest_size=64).digest() + seed
    return (block * math.ceil(size / len(block)))[:size]


def sample_stats(samples: list[float], *, fallback_overall_mib_s: float) -> SampleStats:
    values = samples or [fallback_overall_mib_s]
    ordered = sorted(values)
    return SampleStats(
        avg_mib_s=statistics.fmean(values),
        median_mib_s=statistics.median(values),
        p01_mib_s=percentile(ordered, 0.01),
        p05_mib_s=percentile(ordered, 0.05),
        p95_mib_s=percentile(ordered, 0.95),
        p99_mib_s=percentile(ordered, 0.99),
        min_mib_s=ordered[0],
        max_mib_s=ordered[-1],
        slowest_1pct_avg_mib_s=tail_mean(ordered, 0.01, lowest=True),
        fastest_5pct_avg_mib_s=tail_mean(ordered, 0.05, lowest=False),
        stdev_mib_s=statistics.stdev(values) if len(values) > 1 else 0.0,
        samples=len(samples),
    )


def percentile(ordered: list[float], fraction: float) -> float:
    if not ordered:
        return 0.0
    index = min(len(ordered) - 1, max(0, math.ceil(len(ordered) * fraction) - 1))
    return ordered[index]


def tail_mean(ordered: list[float], fraction: float, *, lowest: bool) -> float:
    if not ordered:
        return 0.0
    count = max(1, math.ceil(len(ordered) * fraction))
    values = ordered[:count] if lowest else ordered[-count:]
    return statistics.fmean(values)


def begin_transfer_metrics() -> tuple[Any, InMemoryMetrics]:
    previous = get_metrics_sink()
    sink = InMemoryMetrics()
    set_metrics_sink(sink)
    return previous, sink


def transfer_counters(
    metrics: InMemoryMetrics, operation: Literal["upload", "download"], duration_s: float
) -> TransferCounters:
    part_requests = int(metric_sum(metrics, f"media.{operation}.part_requests"))
    return TransferCounters(
        part_requests=part_requests,
        part_retries=int(metric_sum(metrics, f"media.{operation}.part_retries")),
        flood_waits=int(metric_sum(metrics, f"media.{operation}.flood_waits")),
        flood_wait_seconds=metric_sum(metrics, f"media.{operation}.flood_wait_seconds"),
        retry_sleep_seconds=metric_sum(metrics, f"media.{operation}.retry_sleep_seconds"),
        reconnects=int(metric_sum(metrics, "sender.reconnects")),
        sender_drops=int(metric_sum(metrics, "client.sender_drops")),
        sender_drop_skips=int(metric_sum(metrics, "client.sender_drop_skipped")),
        media_lane_builds=int(metric_sum(metrics, "client.media_lane_builds")),
        media_lane_drops=int(
            metric_sum_where(
                metrics, "client.media_lane_drops", lambda attrs: attrs.get("reason") != "close"
            )
        ),
        media_lane_drop_skips=int(metric_sum(metrics, "client.media_lane_drop_skipped")),
        media_lane_closes=int(
            metric_sum_where(
                metrics, "client.media_lane_drops", lambda attrs: attrs.get("reason") == "close"
            )
        ),
        byte_window_waits=int(metric_sum(metrics, f"media.{operation}.byte_window_waits")),
        writer_queue_seconds=metric_sum(metrics, f"media.{operation}.writer_queue_seconds"),
        writer_write_seconds=metric_sum(metrics, f"media.{operation}.writer_write_seconds"),
        adaptive_part_size_changes=metric_count(metrics, f"media.{operation}.adaptive_part_size"),
        range_cache_hits=int(metric_sum(metrics, f"media.{operation}.range_cache_hits")),
        range_cache_misses=int(metric_sum(metrics, f"media.{operation}.range_cache_misses")),
        range_cache_deduped=int(metric_sum(metrics, f"media.{operation}.range_cache_deduped")),
        requests_per_s=part_requests / max(duration_s, 1e-9),
    )


def metric_sum(metrics: InMemoryMetrics, name: str) -> float:
    return sum(event.value for event in metrics.events if event.name == name)


def metric_count(metrics: InMemoryMetrics, name: str) -> int:
    return sum(1 for event in metrics.events if event.name == name)


def metric_sum_where(
    metrics: InMemoryMetrics, name: str, predicate: Callable[[Mapping[str, object]], bool]
) -> float:
    return sum(
        event.value
        for event in metrics.events
        if event.name == name and predicate(event.attributes)
    )


def parse_size(value: str, *, default_bytes: int = TELEGRAM_DEFAULT_LIMIT_BYTES) -> int:
    normalized = value.strip().casefold().replace("_", "").replace("-", "")
    if normalized in {"telegramdefault", "default", "limit", "telegramlimit", "2gbtelegram"}:
        return default_bytes
    suffixes = (
        ("gib", 1024**3),
        ("gb", 1000**3),
        ("mib", 1024**2),
        ("mb", 1000**2),
        ("kib", 1024),
        ("kb", 1000),
        ("b", 1),
    )
    for suffix, multiplier in suffixes:
        if normalized.endswith(suffix):
            number = normalized.removesuffix(suffix)
            return int(float(number) * multiplier)
    return int(normalized)


async def file_digest(path: Path) -> str:
    return await asyncio.to_thread(_file_digest_sync, path)


def _file_digest_sync(path: Path) -> str:
    digest = hashlib.blake2b(digest_size=32)
    with path.open("rb") as handle:
        while payload := handle.read(4 * 1024 * 1024):
            digest.update(payload)
    return digest.hexdigest()


def print_transfer(summary: TransferSummary) -> None:
    print(
        f"{summary.actor}.{summary.operation}: "
        f"repeat={summary.repeat_index} "
        f"{summary.bytes} bytes in {summary.duration_s:.3f}s "
        f"overall={summary.overall_mib_s:.3f}MiB/s ({_mib_s_to_mb_s(summary.overall_mib_s):.3f}MB/s) "
        f"transfer={summary.transfer_duration_s:.3f}s "
        f"transfer_rate={summary.transfer_mib_s:.3f}MiB/s ({_mib_s_to_mb_s(summary.transfer_mib_s):.3f}MB/s) "
        f"finalize={summary.finalize_duration_s:.3f}s "
        f"median_window={summary.samples.median_mib_s:.3f}MiB/s "
        f"p95_window={summary.samples.p95_mib_s:.3f}MiB/s "
        f"p01_window={summary.samples.p01_mib_s:.3f}MiB/s "
        f"fastest_5pct_window_avg={summary.samples.fastest_5pct_avg_mib_s:.3f}MiB/s "
        f"slowest_1pct_window_avg={summary.samples.slowest_1pct_avg_mib_s:.3f}MiB/s "
        f"window_samples={summary.samples.samples} media_dc={summary.media_dc_id} "
        f"part_requests={summary.counters.part_requests} part_retries={summary.counters.part_retries} "
        f"flood_waits={summary.counters.flood_waits} flood_wait_seconds={summary.counters.flood_wait_seconds:g} "
        f"retry_sleep_seconds={summary.counters.retry_sleep_seconds:g} reconnects={summary.counters.reconnects} "
        f"sender_drops={summary.counters.sender_drops} sender_drop_skips={summary.counters.sender_drop_skips} "
        f"media_lane_builds={summary.counters.media_lane_builds} "
        f"media_lane_drops={summary.counters.media_lane_drops} "
        f"media_lane_drop_skips={summary.counters.media_lane_drop_skips} "
        f"media_lane_closes={summary.counters.media_lane_closes} "
        f"byte_window_waits={summary.counters.byte_window_waits} "
        f"writer_queue_seconds={summary.counters.writer_queue_seconds:g} "
        f"writer_write_seconds={summary.counters.writer_write_seconds:g} "
        f"adaptive_part_size_changes={summary.counters.adaptive_part_size_changes} "
        f"range_cache_hits={summary.counters.range_cache_hits} "
        f"range_cache_misses={summary.counters.range_cache_misses} "
        f"range_cache_deduped={summary.counters.range_cache_deduped} "
        f"requests_per_s={summary.counters.requests_per_s:.3f}"
    )


def print_progress(
    label: str, *, current: int, total: int | None, elapsed_s: float, window_mib_s: float
) -> None:
    if total is None or total <= 0:
        print(
            f"{label}: {_mib(current):.1f}MiB transferred "
            f"elapsed={elapsed_s:.1f}s window={window_mib_s:.3f}MiB/s"
        )
        return
    percent = min(100.0, current / total * 100)
    overall_mib_s = _mib(current) / elapsed_s if elapsed_s > 0 else 0.0
    remaining_bytes = max(0, total - current)
    eta_s = _mib(remaining_bytes) / overall_mib_s if overall_mib_s > 0 else math.inf
    print(
        f"{label}: {percent:6.2f}% {_mib(current):.1f}/{_mib(total):.1f}MiB "
        f"elapsed={elapsed_s:.1f}s eta={format_duration(eta_s)} "
        f"avg={overall_mib_s:.3f}MiB/s window={window_mib_s:.3f}MiB/s"
    )


def format_duration(seconds: float) -> str:
    if math.isinf(seconds):
        return "unknown"
    bounded = max(0, int(seconds))
    minutes, secs = divmod(bounded, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes:02d}m{secs:02d}s"
    if minutes:
        return f"{minutes}m{secs:02d}s"
    return f"{secs}s"


def format_media_lanes(media_lanes: int | None, concurrency: int) -> str:
    if media_lanes is None:
        return f"auto({max(1, concurrency)})"
    return str(media_lanes)


def file_id_for_actor(args: argparse.Namespace, env: Mapping[str, str], actor: Actor) -> str | None:
    return env_value(env, f"MINIPROTO_LIVE_BENCH_{actor.upper()}_FILE_ID") or args.file_id


def print_summary(summary: BenchmarkSummary) -> None:
    print(
        f"benchmark_file={summary.generated_file} bytes={summary.generated_file_bytes} "
        f"chunk_size={summary.chunk_size} download_chunk_size={summary.download_chunk_size} "
        f"upload_limit_parts={summary.upload_limit_parts} "
        f"operation={summary.operation} upload_concurrency={summary.upload_concurrency} "
        f"upload_media_lanes={format_media_lanes(summary.upload_media_lanes, summary.upload_concurrency)} "
        f"upload_request_timeout={summary.upload_request_timeout:g} upload_part_retries={summary.upload_part_retries} "
        f"download_concurrency={summary.download_concurrency} "
        f"download_media_lanes={format_media_lanes(summary.download_media_lanes, summary.download_concurrency)} "
        f"download_adaptive_concurrency={summary.download_adaptive_concurrency} "
        f"download_max_in_flight_bytes={summary.download_max_in_flight_bytes} "
        f"download_adaptive_part_size={summary.download_adaptive_part_size} "
        f"download_max_chunk_size={summary.download_max_chunk_size} "
        f"download_read_ahead_bytes={summary.download_read_ahead_bytes} "
        f"download_range_cache_bytes={summary.download_range_cache_bytes} "
        f"download_request_timeout={summary.download_request_timeout:g} download_part_retries={summary.download_part_retries} "
        f"download_flood_sleep_threshold={summary.download_flood_sleep_threshold} "
        f"repeat_count={summary.repeat_count}"
    )
    for result in summary.results:
        print_transfer(result)
    if summary.memory is not None:
        print(
            "memory: "
            f"rss_start={summary.memory.rss_start_bytes} rss_end={summary.memory.rss_end_bytes} "
            f"rss_peak={summary.memory.rss_peak_bytes} rss_delta={summary.memory.rss_delta_bytes} "
            f"traced_delta={summary.memory.traced_current_delta_bytes} traced_peak={summary.memory.traced_peak_bytes} "
            f"gc_objects_delta={summary.memory.gc_objects_delta} leak_suspected={summary.memory.leak_suspected}"
        )


def load_dotenv() -> dict[str, str]:
    values: dict[str, str] = {}
    dotenv = Path(".env")
    if dotenv.exists():
        for raw_line in dotenv.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values.setdefault(key, value.strip().strip('"').strip("'"))
    values.update(os.environ)
    return values


def require_live_env(env: Mapping[str, str], *, actor: str) -> None:
    required = ["MINIPROTO_API_ID", "MINIPROTO_API_HASH", "MINIPROTO_SESSION_KEY"]
    if env_value(env, "MINIPROTO_INTEGRATION") != "1":
        raise SystemExit("set MINIPROTO_INTEGRATION=1 for live Telegram benchmarks")
    if env_value(env, "MINIPROTO_REAL_INTEGRATION") != "1":
        raise SystemExit("set MINIPROTO_REAL_INTEGRATION=1 for production Telegram benchmarks")
    if actor in {"bot", "both"}:
        required.append("MINIPROTO_BOT_TOKEN")
    if actor in {"user", "both"}:
        required.append("MINIPROTO_REAL_PHONE")
    missing = [name for name in required if not env_value(env, name)]
    if missing:
        raise SystemExit(f"missing live benchmark environment variables: {', '.join(missing)}")


def required_env(env: Mapping[str, str], name: str) -> str:
    value = env_value(env, name)
    if not value:
        raise SystemExit(f"missing required environment variable: {name}")
    return value


def env_value(env: Mapping[str, str], name: str, default: str | None = None) -> str | None:
    return env.get(name) or default


def env_bool(env: Mapping[str, str], name: str, *, default: bool) -> bool:
    value = env_value(env, name)
    if value is None:
        return default
    normalized = value.strip().casefold()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value, got {value!r}")


def prompt_code(env: Mapping[str, str]) -> str:
    if should_use_http_code_prompt(env):
        return prompt_code_http(env)
    if env_value(env, "MINIPROTO_LIVE_PROMPT_CODE") != "1" or not sys.stdin.isatty():
        raise SystemExit(
            "no stored user session; set MINIPROTO_LIVE_PROMPT_CODE=1 and run interactively to enter the current Telegram code, or set MINIPROTO_LIVE_BENCH_CODE_PROMPT=http for the temporary HTTP prompt"
        )
    return input("Telegram login code: ").strip()


def should_use_http_code_prompt(env: Mapping[str, str]) -> bool:
    mode = (env_value(env, "MINIPROTO_LIVE_BENCH_CODE_PROMPT") or "").strip().casefold()
    if mode in {"http", "web"}:
        return True
    return env_bool(env, "MINIPROTO_LIVE_BENCH_HTTP_CODE_PROMPT", default=False)


def prompt_code_http(env: Mapping[str, str]) -> str:
    host = env_value(env, "MINIPROTO_LIVE_BENCH_HTTP_CODE_HOST", "127.0.0.1") or "127.0.0.1"
    port = int(env_value(env, "MINIPROTO_LIVE_BENCH_HTTP_CODE_PORT", "8765") or "8765")
    timeout_s = float(env_value(env, "MINIPROTO_LIVE_BENCH_HTTP_CODE_TIMEOUT", "900") or "900")
    token = env_value(env, "MINIPROTO_LIVE_BENCH_HTTP_CODE_TOKEN") or secrets.token_urlsafe(24)
    code_queue: Queue[str] = Queue(maxsize=1)
    prompt_path = f"/{token}"
    server: ThreadingHTTPServer

    class CodeHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if not self._authorized_path():
                self._send(404, "not found")
                return
            self._send(200, _code_prompt_html(error=None), content_type="text/html; charset=utf-8")

        def do_POST(self) -> None:
            if not self._authorized_path():
                self._send(404, "not found")
                return
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length > 256:
                self._send(413, "request too large")
                return
            values = parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
            code = (values.get("code", [""])[0] or "").strip().replace(" ", "")
            if not code:
                self._send(
                    400,
                    _code_prompt_html(error="Enter the Telegram login code."),
                    content_type="text/html; charset=utf-8",
                )
                return
            with suppress(Full):
                code_queue.put_nowait(code)
            self._send(
                200,
                "<!doctype html><title>miniproto login code</title><p>Code received. You can close this tab.</p>",
                content_type="text/html; charset=utf-8",
            )
            threading.Thread(target=server.shutdown, daemon=True).start()

        def log_message(self, format: str, *args: object) -> None:
            return

        def _authorized_path(self) -> bool:
            return self.path.split("?", 1)[0] == prompt_path

        def _send(self, status: int, body: str, *, content_type: str = "text/plain") -> None:
            payload = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

    server = ThreadingHTTPServer((host, port), CodeHandler)
    thread = threading.Thread(
        target=server.serve_forever, name="miniproto-http-code-prompt", daemon=True
    )
    thread.start()
    actual_port = int(server.server_address[1])
    local_url = f"http://{host}:{actual_port}{prompt_path}"
    public_base = env_value(env, "MINIPROTO_LIVE_BENCH_HTTP_CODE_PUBLIC_BASE_URL")
    public_url = f"{public_base.rstrip('/')}{prompt_path}" if public_base else None
    print("Telegram login code HTTP prompt is waiting for one code.")
    print(f"Open locally: {local_url}")
    if public_url:
        print(f"Open through tunnel: {public_url}")
    print(f"Prompt expires in {int(timeout_s)} seconds.")
    try:
        return code_queue.get(timeout=timeout_s)
    except Empty as exc:
        raise SystemExit("timed out waiting for Telegram login code over HTTP") from exc
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _code_prompt_html(*, error: str | None) -> str:
    error_html = f"<p style='color:#b00020'>{html.escape(error)}</p>" if error else ""
    return (
        "<!doctype html><meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>miniproto Telegram login code</title>"
        "<main style='font-family:system-ui,sans-serif;max-width:32rem;margin:4rem auto;padding:0 1rem'>"
        "<h1>Telegram login code</h1>"
        "<p>Enter the current login code for this benchmark run.</p>"
        f"{error_html}"
        "<form method='post'>"
        "<input name='code' inputmode='numeric' autocomplete='one-time-code' autofocus "
        "style='font-size:1.2rem;padding:.5rem;width:12rem'> "
        "<button style='font-size:1.2rem;padding:.55rem 1rem'>Submit</button>"
        "</form>"
        "</main>"
    )


def prompt_password(env: Mapping[str, str]) -> str:
    password = env_value(env, "MINIPROTO_REAL_PASSWORD")
    if password:
        return password
    if env_value(env, "MINIPROTO_LIVE_PROMPT_CODE") == "1" and sys.stdin.isatty():
        return getpass("Telegram 2FA password, if requested: ")
    return ""


def _mib(value: int) -> float:
    return value / (1024 * 1024)


def _mib_s_to_mb_s(value: float) -> float:
    return value * 1024 * 1024 / 1_000_000


def memory_summary(delta: Any) -> MemorySummary:
    return MemorySummary(
        rss_start_bytes=delta.start.rss_bytes,
        rss_end_bytes=delta.end.rss_bytes,
        rss_peak_bytes=delta.peak.rss_bytes,
        rss_delta_bytes=delta.rss_delta_bytes,
        traced_current_delta_bytes=delta.traced_delta_bytes,
        traced_peak_bytes=delta.peak.traced_peak_bytes,
        gc_objects_delta=delta.end.gc_objects - delta.start.gc_objects,
        leak_suspected=delta.leak_suspected(),
    )


if __name__ == "__main__":
    raise SystemExit(main())
