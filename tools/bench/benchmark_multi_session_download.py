"""Run an explicitly guarded live Telegram benchmark splitting one file across independent sessions.

This is not a fake benchmark: it can authenticate accounts, read encrypted SQLite sessions, issue live media requests, write/replace selected part and output files, and optionally compare a local source digest. It refuses to run unless both live-benchmark guard environment variables are set. Results distinguish transfer-only throughput from total throughput including local assembly and optional digest work.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import time
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from miniproto import (
    Client,
    ClientConfig,
    EncryptedSQLiteSessionStorage,
    TransportConfig,
    configure_logging,
    event_loop,
    set_metrics_sink,
)
from miniproto.crypto import auth_key_id, native_available
from miniproto.file_id import media_from_file_id
from miniproto.invoke import load_session_record
from miniproto.media import DEFAULT_CHUNK_SIZE, MAX_DOWNLOAD_CHUNK_SIZE
from miniproto.types import Media
from tools.bench.benchmark_live_media_limit import (
    BENCH_GUARD_ENV,
    TransferCounters,
    TransferRecorder,
    begin_transfer_metrics,
    configure_standard_streams_line_buffering,
    env_bool,
    env_value,
    format_duration,
    load_dotenv,
    parse_size,
    prompt_code,
    required_env,
    start_progress_heartbeat,
    stop_progress_heartbeat,
    transfer_counters,
)

MIB = 1024 * 1024
MULTI_SESSION_GUARD_ENV = "MINIPROTO_MULTI_SESSION_DOWNLOAD_BENCH"
DEFAULT_CLIENT_COUNT = 2
DEFAULT_DOWNLOAD_DIR = Path(".tmp/multi-session-downloads")
DEFAULT_PER_SESSION_CONCURRENCY = 1
DEFAULT_PER_SESSION_MEDIA_LANES = 1

Actor = Literal["user", "bot"]


@dataclass(frozen=True, slots=True)
class DownloadRange:
    """One contiguous byte range assigned to an active session worker.

    Attributes:
        index: Zero-based worker/session index.
        offset: Starting byte offset.
        limit: Exact number of bytes this worker must download.
    """

    index: int
    offset: int
    limit: int


@dataclass(frozen=True, slots=True)
class SessionSummary:
    """Redacted benchmark identity for one selected encrypted session file.

    The summary exposes an auth-key identifier for duplicate detection, never the key material itself.

    Attributes:
        index: Zero-based selected session index.
        session_path: Local encrypted-session database path, not its decrypted contents.
        auth_key_id_hex: Redacted derived key identifier for duplicate detection, or ``None``.
        user_id: Authorized Telegram user identifier when available.
        is_bot: Whether the authorized identity is a bot, when known.
        duplicate_auth_key: Whether another selected session shares this derived identifier.
    """

    index: int
    session_path: str
    auth_key_id_hex: str | None
    user_id: int | None
    is_bot: bool | None
    duplicate_auth_key: bool


@dataclass(frozen=True, slots=True)
class WorkerSummary:
    """Completed per-range transfer measurements for one active worker.

    ``mib_s`` is range bytes divided by the worker's own request duration, excluding later assembly.

    Attributes:
        index: Zero-based active worker/session index.
        session_path: Local encrypted-session database path assigned to the worker.
        part_path: Local output file containing the worker's contiguous byte range.
        offset: Inclusive file byte offset assigned to the worker.
        limit: Exact assigned range size in bytes.
        bytes: Bytes reported by the completed range download.
        duration_s: Worker request duration in seconds, excluding assembly/digest finalization.
        mib_s: Worker range bytes divided by ``duration_s`` in binary MiB/s.
    """

    index: int
    session_path: str
    part_path: str
    offset: int
    limit: int
    bytes: int
    duration_s: float
    mib_s: float


@dataclass(frozen=True, slots=True)
class MultiSessionDownloadSummary:
    """Serializable result of one live multi-session download benchmark.

    ``transfer_mib_s`` excludes assembly and digest verification, while ``overall_mib_s`` uses total duration. ``counters`` are metric-sink observations from this run; they are not server-side accounting.

    Attributes:
        actor: Requested live account role.
        file_id: Remote media identifier used for the live range requests.
        dc_id: Configured production data-center identifier.
        media_dc_id: Data center encoded by the remote media when available.
        bytes: Sum of worker-reported range bytes.
        clients_requested: Number of session paths requested before range-size capping.
        clients_active: Number of non-empty ranges and connected workers actually used.
        per_session_concurrency: Concurrent part requests allowed within each worker.
        per_session_media_lanes: Optional dedicated sender lanes per worker.
        download_chunk_size: Initial file-part size in bytes.
        download_max_chunk_size: Adaptive file-part size ceiling in bytes.
        download_max_in_flight_bytes: Optional per-worker request byte-window bound.
        download_adaptive_concurrency: Whether each worker adapts active request slots.
        download_adaptive_part_size: Whether each worker probes larger legal chunks.
        download_request_timeout: Per-request timeout in seconds.
        download_part_retries: Non-flood transient retry budget per worker part.
        download_flood_sleep_threshold: Maximum automatic flood-wait sleep in seconds.
        allow_duplicate_auth_keys: Whether duplicate authorized sessions were explicitly permitted.
        duplicate_auth_key_groups: Derived key IDs mapped to their repeated session indexes.
        event_loop_backend: Active local event-loop backend label.
        native_available: Whether miniproto's local native extension was available.
        duration_s: End-to-end duration in seconds, including enabled finalization.
        finalize_duration_s: Assembly/digest time included after all network workers finish.
        overall_mib_s: Full-file bytes divided by ``duration_s`` in binary MiB/s.
        transfer_mib_s: Full-file bytes divided by request-only duration in binary MiB/s.
        counters: Local metric-sink observations, not Telegram server accounting.
        sessions: Redacted selected-session identities.
        workers: Per-range observed request measurements.
        output_path: Assembled output path, or ``None`` when assembly is disabled.
        part_paths: Retained part paths after finalization policy is applied.
        digest_verified: Whether an optional local source/output digest comparison matched.
    """

    actor: Actor
    file_id: str
    dc_id: int
    media_dc_id: int | None
    bytes: int
    clients_requested: int
    clients_active: int
    per_session_concurrency: int
    per_session_media_lanes: int | None
    download_chunk_size: int
    download_max_chunk_size: int
    download_max_in_flight_bytes: int | None
    download_adaptive_concurrency: bool
    download_adaptive_part_size: bool
    download_request_timeout: float
    download_part_retries: int
    download_flood_sleep_threshold: int | None
    allow_duplicate_auth_keys: bool
    duplicate_auth_key_groups: dict[str, tuple[int, ...]]
    event_loop_backend: str
    native_available: bool
    duration_s: float
    finalize_duration_s: float
    overall_mib_s: float
    transfer_mib_s: float
    counters: TransferCounters
    sessions: tuple[SessionSummary, ...]
    workers: tuple[WorkerSummary, ...]
    output_path: str | None
    part_paths: tuple[str, ...]
    digest_verified: bool


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and run the live benchmark only after both explicit safety guards.

    Returns:
        ``2`` when either guard is missing, otherwise the asynchronous benchmark status.

    Args:
        argv: Optional non-secret CLI arguments excluding the executable name.
    """
    env = load_dotenv()
    args = parse_args(argv, env)
    configure_standard_streams_line_buffering()
    if env_value(env, BENCH_GUARD_ENV) != "1" or env_value(env, MULTI_SESSION_GUARD_ENV) != "1":
        print(
            f"Refusing to run the multi-session download benchmark without {BENCH_GUARD_ENV}=1 and {MULTI_SESSION_GUARD_ENV}=1."
        )
        return 2
    configure_logging(args.log_level, format=args.log_format)
    print(
        f"event_loop_backend={event_loop.backend_name()} installed={event_loop.installed()} version={event_loop.backend_version()}"
    )
    return event_loop.run(run_benchmark(args, env))


def parse_args(argv: list[str] | None = None, env: Mapping[str, str] | None = None) -> argparse.Namespace:
    """Parse and validate live benchmark options plus their environment defaults.

    Args:
        argv: Optional command-line arguments.
        env: Optional environment mapping, primarily for deterministic callers and tests.

    Returns:
        Validated namespace including file/session/output, transfer, and reporting options.

    Raises:
        ValueError: A numeric ``MINIPROTO_MULTI_SESSION_DOWNLOAD_*`` or inherited live-benchmark default cannot be parsed before argparse validation.
        SystemExit: If argparse validation fails, an option violates its resource bound, or no file ID is configured.

    Safety:
        Parsing does not authenticate or perform network I/O. Guard variables are checked by ``main`` and common live credentials by ``run_benchmark``.
    """
    values = {} if env is None else env
    json_path = env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_JSON") or env_value(
        values, "MINIPROTO_LIVE_BENCH_JSON"
    )
    output_path = env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_OUTPUT")
    verify_digest_against = env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_VERIFY_DIGEST_AGAINST")
    parser = argparse.ArgumentParser(
        description="Run an opt-in live benchmark that splits one Telegram download across multiple independent miniproto session files."
    )
    parser.add_argument(
        "--actor",
        choices=("user", "bot"),
        default=env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_ACTOR", "user"),
        help="authorized actor represented by all session files",
    )
    parser.add_argument(
        "--clients",
        type=int,
        default=int(
            env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_CLIENTS", str(DEFAULT_CLIENT_COUNT))
            or str(DEFAULT_CLIENT_COUNT)
        ),
        help=f"number of default session files to use when --session/env paths are not supplied; defaults to {DEFAULT_CLIENT_COUNT}",
    )
    parser.add_argument(
        "--session",
        action="append",
        default=[],
        type=Path,
        help="encrypted SQLite session DB path; repeat for each independent Telegram session/auth key",
    )
    parser.add_argument(
        "--file-id",
        default=env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_FILE_ID")
        or env_value(values, "MINIPROTO_LIVE_BENCH_FILE_ID"),
        help="miniproto file id to download; actor-specific env vars are also supported",
    )
    parser.add_argument(
        "--dc-id",
        type=int,
        default=int(
            env_value(
                values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_DC_ID", env_value(values, "MINIPROTO_LIVE_BENCH_DC_ID", "2")
            )
            or "2"
        ),
        help="initial Telegram DC id for session bootstrap",
    )
    parser.add_argument(
        "--size",
        default=env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_SIZE"),
        help="download size override when the miniproto file id does not carry size metadata",
    )
    parser.add_argument(
        "--download-dir",
        type=Path,
        default=Path(
            env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_DIR", str(DEFAULT_DOWNLOAD_DIR))
            or str(DEFAULT_DOWNLOAD_DIR)
        ),
        help=f"directory for parts and assembled output; defaults to {DEFAULT_DOWNLOAD_DIR}",
    )
    parser.add_argument(
        "--output", type=Path, default=Path(output_path) if output_path else None, help="optional assembled output path"
    )
    parser.add_argument(
        "--no-assemble",
        action="store_true",
        default=env_bool(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_NO_ASSEMBLE", default=False),
        help="leave only per-session part files and skip final concatenation",
    )
    parser.add_argument(
        "--keep-parts",
        action="store_true",
        default=env_bool(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_KEEP_PARTS", default=False),
        help="keep per-session part files after successful assembly",
    )
    parser.add_argument(
        "--verify-digest-against",
        type=Path,
        default=Path(verify_digest_against) if verify_digest_against else None,
        help="optional local source file whose SHA-256 digest must match the assembled output",
    )
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=float(env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_REQUEST_TIMEOUT", "120") or "120"),
        help="base MTProto request timeout in seconds",
    )
    parser.add_argument(
        "--download-request-timeout",
        type=float,
        default=float(env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_PART_TIMEOUT", "30") or "30"),
        help="per upload.getFile part timeout in seconds",
    )
    parser.add_argument(
        "--per-session-concurrency",
        type=int,
        default=int(
            env_value(
                values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_PER_SESSION_CONCURRENCY", str(DEFAULT_PER_SESSION_CONCURRENCY)
            )
            or str(DEFAULT_PER_SESSION_CONCURRENCY)
        ),
        help=f"download concurrency inside each independent session; defaults to {DEFAULT_PER_SESSION_CONCURRENCY} to isolate auth-key scaling",
    )
    media_lanes = env_value(
        values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_PER_SESSION_MEDIA_LANES", str(DEFAULT_PER_SESSION_MEDIA_LANES)
    )
    parser.add_argument(
        "--per-session-media-lanes",
        type=int,
        default=int(media_lanes) if media_lanes else None,
        help=f"media sender lanes inside each independent session; defaults to {DEFAULT_PER_SESSION_MEDIA_LANES}",
    )
    parser.add_argument(
        "--download-chunk-size",
        type=int,
        default=int(
            env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_CHUNK_SIZE", str(DEFAULT_CHUNK_SIZE))
            or str(DEFAULT_CHUNK_SIZE)
        ),
        help=f"initial upload.getFile chunk size; defaults to {DEFAULT_CHUNK_SIZE}",
    )
    parser.add_argument(
        "--download-max-chunk-size",
        type=int,
        default=int(
            env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_MAX_CHUNK_SIZE", str(MAX_DOWNLOAD_CHUNK_SIZE))
            or str(MAX_DOWNLOAD_CHUNK_SIZE)
        ),
        help=f"adaptive maximum upload.getFile chunk size; defaults to {MAX_DOWNLOAD_CHUNK_SIZE}",
    )
    max_in_flight = env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_MAX_IN_FLIGHT_BYTES")
    parser.add_argument(
        "--download-max-in-flight-bytes",
        type=int,
        default=int(max_in_flight) if max_in_flight else None,
        help="optional rolling byte window per independent session",
    )
    default_adaptive_concurrency = env_bool(
        values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_ADAPTIVE_CONCURRENCY", default=True
    )
    parser.set_defaults(download_adaptive_concurrency=default_adaptive_concurrency)
    parser.add_argument(
        "--download-adaptive-concurrency",
        action="store_true",
        dest="download_adaptive_concurrency",
        help="enable per-session adaptive concurrency",
    )
    parser.add_argument(
        "--no-download-adaptive-concurrency",
        action="store_false",
        dest="download_adaptive_concurrency",
        help="disable per-session adaptive concurrency",
    )
    default_adaptive_part_size = env_bool(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_ADAPTIVE_PART_SIZE", default=True)
    parser.set_defaults(download_adaptive_part_size=default_adaptive_part_size)
    parser.add_argument(
        "--download-adaptive-part-size",
        action="store_true",
        dest="download_adaptive_part_size",
        help="enable per-session adaptive part sizing",
    )
    parser.add_argument(
        "--no-download-adaptive-part-size",
        action="store_false",
        dest="download_adaptive_part_size",
        help="disable per-session adaptive part sizing",
    )
    parser.add_argument(
        "--download-part-retries",
        type=int,
        default=int(env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_PART_RETRIES", "6") or "6"),
        help="transient retry budget per part",
    )
    parser.add_argument(
        "--download-flood-sleep-threshold",
        type=int,
        default=int(env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_FLOOD_SLEEP_THRESHOLD", "30") or "30"),
        help="maximum FLOOD_WAIT seconds to sleep and retry inside each part",
    )
    parser.add_argument(
        "--allow-duplicate-auth-keys",
        action="store_true",
        default=env_bool(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_ALLOW_DUPLICATE_AUTH_KEYS", default=False),
        help="allow running even when two session files contain the same MTProto auth key id",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=Path(json_path) if json_path else None,
        help="optional path for machine-readable benchmark results",
    )
    parser.add_argument(
        "--progress-interval",
        type=float,
        default=float(env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_PROGRESS_INTERVAL", "5") or "5"),
        help="seconds between progress lines; set 0 to disable",
    )
    parser.add_argument(
        "--log-level",
        default=env_value(
            values,
            "MINIPROTO_MULTI_SESSION_DOWNLOAD_LOG_LEVEL",
            env_value(values, "MINIPROTO_LIVE_BENCH_LOG_LEVEL", "WARNING"),
        )
        or "WARNING",
        help="miniproto log level for the benchmark run",
    )
    parser.add_argument(
        "--log-format",
        choices=("text", "json"),
        default=env_value(
            values,
            "MINIPROTO_MULTI_SESSION_DOWNLOAD_LOG_FORMAT",
            env_value(values, "MINIPROTO_LIVE_BENCH_LOG_FORMAT", "text"),
        )
        or "text",
        help="miniproto log format for the benchmark run",
    )
    args = parser.parse_args(argv)
    if not args.session:
        configured_sessions = env_value(values, "MINIPROTO_MULTI_SESSION_DOWNLOAD_SESSIONS")
        if configured_sessions:
            args.session = [Path(item) for item in split_session_paths(configured_sessions)]
    if args.clients < 1:
        parser.error("--clients must be positive")
    if args.per_session_concurrency < 1:
        parser.error("--per-session-concurrency must be positive")
    if args.per_session_media_lanes is not None and args.per_session_media_lanes < 0:
        parser.error("--per-session-media-lanes must not be negative")
    if args.download_chunk_size <= 0:
        parser.error("--download-chunk-size must be positive")
    if args.download_max_chunk_size < args.download_chunk_size:
        parser.error("--download-max-chunk-size must be greater than or equal to --download-chunk-size")
    if args.download_max_in_flight_bytes is not None and args.download_max_in_flight_bytes < args.download_chunk_size:
        parser.error("--download-max-in-flight-bytes must be greater than or equal to --download-chunk-size")
    if args.download_part_retries < 0:
        parser.error("--download-part-retries must not be negative")
    if args.download_flood_sleep_threshold < 0:
        parser.error("--download-flood-sleep-threshold must not be negative")
    if file_id_for_args(args, values) is None:
        parser.error("--file-id or MINIPROTO_MULTI_SESSION_DOWNLOAD_FILE_ID is required")
    return args


async def run_benchmark(args: argparse.Namespace, env: Mapping[str, str]) -> int:
    """Authorize independent live clients, reject duplicate keys by default, and run a guarded split download.

    Session clients are always disconnected in ``finally``. Sessions may be authorized or updated by normal client operations; ``run_download_split`` may create, replace, or remove files under the selected part and output paths.

    Args:
        args: Validated non-secret benchmark options including file, session, and output paths.
        env: Environment-only live credentials, session key, and explicit opt-in flags.

    Returns:
        Zero after a completed live benchmark and any selected report write.

    Live Boundary:
        This function opens encrypted sessions and issues real Telegram requests;
        callers must have passed both CLI guard checks before invoking it.

    Raises:
        SystemExit: If live credentials are absent or duplicate auth keys are disallowed.
        Exception: Propagates file-ID, session, authentication, transfer, and output failures.
    """
    require_common_live_env(env)
    file_id = file_id_for_args(args, env)
    assert file_id is not None
    media = media_from_file_id(file_id)
    size = download_size(args, media)
    session_paths = resolve_session_paths(args, env)
    ranges = plan_contiguous_ranges(size, requested_workers=len(session_paths))
    active_paths = session_paths[: len(ranges)]
    print(
        f"multi-session.download: actor={args.actor} bytes={size} requested_clients={len(session_paths)} active_clients={len(ranges)} "
        f"per_session_concurrency={args.per_session_concurrency} per_session_media_lanes={args.per_session_media_lanes} "
        f"chunk_size={args.download_chunk_size} max_chunk_size={args.download_max_chunk_size}"
    )
    for shard, path in zip(ranges, active_paths, strict=True):
        print(f"worker {shard.index}: session={path} offset={shard.offset} limit={shard.limit}")
    clients: list[Client] = []
    try:
        session_summaries = []
        for shard, path in zip(ranges, active_paths, strict=True):
            client, session = await authorized_client_for_session(
                actor=args.actor, session_path=path, session_index=shard.index, args=args, env=env
            )
            clients.append(client)
            session_summaries.append(session)
        duplicate_groups = duplicate_auth_key_groups(tuple(session.auth_key_id_hex for session in session_summaries))
        if duplicate_groups and not args.allow_duplicate_auth_keys:
            groups = ", ".join(f"{key}:{indices}" for key, indices in duplicate_groups.items())
            raise SystemExit(
                "duplicate MTProto auth keys detected across session files; this would not test independent device sessions. "
                f"Pass --allow-duplicate-auth-keys to force the run. groups={groups}"
            )
        session_summaries = [
            SessionSummary(
                index=session.index,
                session_path=session.session_path,
                auth_key_id_hex=session.auth_key_id_hex,
                user_id=session.user_id,
                is_bot=session.is_bot,
                duplicate_auth_key=session.auth_key_id_hex in duplicate_groups
                if session.auth_key_id_hex is not None
                else False,
            )
            for session in session_summaries
        ]
        summary = await run_download_split(
            args=args,
            file_id=file_id,
            media=media,
            size=size,
            clients=tuple(clients),
            sessions=tuple(session_summaries),
            ranges=ranges,
            clients_requested=len(session_paths),
            duplicate_groups=duplicate_groups,
        )
    finally:
        await asyncio.gather(*(client.disconnect() for client in clients), return_exceptions=True)
    print_summary(summary)
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(asdict(summary), indent=2), encoding="utf-8")
    return 0


async def run_download_split(
    *,
    args: argparse.Namespace,
    file_id: str,
    media: Media,
    size: int,
    clients: tuple[Client, ...],
    sessions: tuple[SessionSummary, ...],
    ranges: tuple[DownloadRange, ...],
    clients_requested: int,
    duplicate_groups: dict[str, tuple[int, ...]],
) -> MultiSessionDownloadSummary:
    """Download contiguous ranges concurrently, optionally assemble them, and return measured results.

    Existing selected part paths and the selected assembled output path are unlinked before transfer. Worker failures cancel and await every sibling task. Assembly concatenates parts in range order and verifies total size; optional digest verification compares a local source file only after assembly. Parts are removed after successful assembly unless ``keep_parts`` is set, but remain for ``no_assemble`` runs.

    Returns:
        Transfer and finalization timings, local metric counters, worker/session summaries, and retained artifact paths.

    Resource semantics:
        Each worker receives the configured per-session concurrency, lane count, chunk sizing, in-flight-byte window, retry, and flood-wait settings. Aggregate throughput therefore includes concurrent independent sessions and is not normalized to a single auth key.

    Args:
        args: Validated live transfer, path-ownership, assembly, and comparison settings.
        file_id: Remote media identifier supplied to the result and live requests.
        media: Parsed remote media metadata used for all worker range requests.
        size: Exact file size in bytes partitioned across ``ranges``.
        clients: Already-connected authorized clients, disconnected by the caller.
        sessions: Redacted summaries aligned by worker index with ``clients``.
        ranges: Ordered contiguous non-empty byte ranges to download concurrently.
        clients_requested: Selected session count before short-file range capping.
        duplicate_groups: Repeated derived auth-key IDs retained as comparison context.
    """
    await asyncio.to_thread(args.download_dir.mkdir, parents=True, exist_ok=True)
    run_id = int(time.time())
    target_name = safe_file_name(media.file_name or f"telegram-file-{size}.bin")
    part_paths = tuple(
        args.download_dir / f"multi-session-{args.actor}-{run_id}-worker{shard.index:02d}.part" for shard in ranges
    )
    output_path = (
        None
        if args.no_assemble
        else args.output or args.download_dir / f"multi-session-{args.actor}-{run_id}-{target_name}"
    )
    await asyncio.gather(*(asyncio.to_thread(path.unlink, missing_ok=True) for path in part_paths))
    if output_path is not None:
        await asyncio.to_thread(output_path.unlink, missing_ok=True)
    recorder = TransferRecorder(
        total=size,
        label="multi-session.download",
        progress_interval_s=args.progress_interval,
        sample_interval_s=max(1.0, args.progress_interval or 1.0),
    )
    progress_by_worker = [0 for _ in ranges]
    progress_lock = asyncio.Lock()

    async def progress_for(worker_index: int, current: int, total: int | None) -> None:
        """Aggregate worker byte progress under a lock before updating the shared recorder.

        Args:
            worker_index: Range/worker position whose latest callback value is replaced.
            current: Worker-reported transferred bytes within its own range.
            total: Ignored worker range total retained for progress-callback compatibility.
        """
        del total
        async with progress_lock:
            progress_by_worker[worker_index] = current
            aggregate = sum(progress_by_worker)
        await recorder.progress(aggregate, size)

    recorder.begin()
    previous_sink, metrics = begin_transfer_metrics()
    heartbeat = start_progress_heartbeat(recorder)
    transfer_started = time.perf_counter()
    tasks = [
        asyncio.create_task(
            download_worker(
                client=client,
                media=media,
                shard=shard,
                session_path=Path(sessions[shard.index].session_path),
                part_path=part_path,
                total_size=size,
                args=args,
                progress=progress_for,
            )
        )
        for client, shard, part_path in zip(clients, ranges, part_paths, strict=True)
    ]
    try:
        try:
            worker_summaries = tuple(await asyncio.gather(*tasks))
        except BaseException:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise
    finally:
        await stop_progress_heartbeat(heartbeat)
        set_metrics_sink(previous_sink)
    transfer_duration = max(time.perf_counter() - transfer_started, 1e-9)
    duration = transfer_duration
    digest_verified = False
    if output_path is not None:
        finalize_started = time.perf_counter()
        await asyncio.to_thread(assemble_parts, part_paths, output_path, expected_size=size)
        if args.verify_digest_against is not None:
            source_digest, target_digest = await asyncio.gather(
                asyncio.to_thread(file_digest, args.verify_digest_against), asyncio.to_thread(file_digest, output_path)
            )
            if source_digest != target_digest:
                raise RuntimeError(f"assembled digest mismatch: {source_digest} != {target_digest}")
            digest_verified = True
        if not args.keep_parts:
            await asyncio.gather(*(asyncio.to_thread(path.unlink, missing_ok=True) for path in part_paths))
        duration += max(time.perf_counter() - finalize_started, 0.0)
    counters = transfer_counters(metrics, "download", transfer_duration)
    return MultiSessionDownloadSummary(
        actor=args.actor,
        file_id=file_id,
        dc_id=args.dc_id,
        media_dc_id=media.dc_id,
        bytes=sum(worker.bytes for worker in worker_summaries),
        clients_requested=clients_requested,
        clients_active=len(ranges),
        per_session_concurrency=args.per_session_concurrency,
        per_session_media_lanes=args.per_session_media_lanes,
        download_chunk_size=args.download_chunk_size,
        download_max_chunk_size=args.download_max_chunk_size,
        download_max_in_flight_bytes=args.download_max_in_flight_bytes,
        download_adaptive_concurrency=args.download_adaptive_concurrency,
        download_adaptive_part_size=args.download_adaptive_part_size,
        download_request_timeout=args.download_request_timeout,
        download_part_retries=args.download_part_retries,
        download_flood_sleep_threshold=args.download_flood_sleep_threshold,
        allow_duplicate_auth_keys=args.allow_duplicate_auth_keys,
        duplicate_auth_key_groups=duplicate_groups,
        event_loop_backend=event_loop.backend_name(),
        native_available=native_available(),
        duration_s=duration,
        finalize_duration_s=max(duration - transfer_duration, 0.0),
        overall_mib_s=(size / MIB) / max(duration, 1e-9),
        transfer_mib_s=(size / MIB) / transfer_duration,
        counters=counters,
        sessions=sessions,
        workers=worker_summaries,
        output_path=str(output_path) if output_path is not None else None,
        part_paths=tuple(str(path) for path in part_paths if args.keep_parts or output_path is None),
        digest_verified=digest_verified,
    )


async def download_worker(
    *,
    client: Client,
    media: Media,
    shard: DownloadRange,
    session_path: Path,
    part_path: Path,
    total_size: int,
    args: argparse.Namespace,
    progress,
) -> WorkerSummary:
    """Download one exact range through one already-authorized session client.

    Raises:
        RuntimeError: If the media helper reports a byte count different from this worker's range.
        Exception: Propagates live request, retry, flood-wait, and destination-write failures.

    Args:
        client: Connected authorized client assigned to this one range.
        media: Remote media metadata converted by the client to a file location.
        shard: Contiguous byte range owned solely by this worker.
        session_path: Redacted path reported for the already-authorized session.
        part_path: New/replaced local part destination owned by the caller workflow.
        total_size: Complete remote file size used for range download planning.
        args: Per-session request, retry, flood, and resource-bound configuration.
        progress: Async aggregate callback receiving worker index, current, and total bytes.
    """
    started = time.perf_counter()
    result = await client.download_media(
        media,
        part_path,
        offset=shard.offset,
        limit=shard.limit,
        total_size=total_size,
        progress=lambda current, total: progress(shard.index, current, total),
        request_timeout=args.download_request_timeout,
        max_retries=args.download_part_retries,
        flood_sleep_threshold=args.download_flood_sleep_threshold,
        concurrency=args.per_session_concurrency,
        media_lanes=args.per_session_media_lanes,
        adaptive_concurrency=args.download_adaptive_concurrency,
        part_size=args.download_chunk_size,
        max_in_flight_bytes=args.download_max_in_flight_bytes,
        adaptive_part_size=args.download_adaptive_part_size,
        max_part_size=args.download_max_chunk_size,
    )
    duration = max(time.perf_counter() - started, 1e-9)
    if result.bytes_downloaded != shard.limit:
        raise RuntimeError(f"worker {shard.index} size mismatch: expected {shard.limit}, got {result.bytes_downloaded}")
    return WorkerSummary(
        index=shard.index,
        session_path=str(session_path),
        part_path=str(part_path),
        offset=shard.offset,
        limit=shard.limit,
        bytes=result.bytes_downloaded,
        duration_s=duration,
        mib_s=(result.bytes_downloaded / MIB) / duration,
    )


async def authorized_client_for_session(
    *, actor: Actor, session_path: Path, session_index: int, args: argparse.Namespace, env: Mapping[str, str]
) -> tuple[Client, SessionSummary]:
    """Open one encrypted session, ensure its requested actor identity, and return a connected client.

    The storage key, API hash, bot token, password/code data, and auth-key bytes are consumed from environment-backed helpers and are never included in the returned summary. A missing or wrong identity is authorized through the appropriate live sign-in flow before final validation.

    Raises:
        RuntimeError: If the final session identity does not match ``actor``.
        Exception: Propagates storage decryption, connection, authentication, and session failures.

    Args:
        actor: Required user or bot identity for this live client.
        session_path: Encrypted local SQLite session path opened with the environment key.
        session_index: Stable index preserved in the returned redacted summary.
        args: Validated DC and request-timeout configuration.
        env: Environment-only API, storage, phone/token, and prompt credentials.
    """
    storage = EncryptedSQLiteSessionStorage(session_path, key=required_env(env, "MINIPROTO_SESSION_KEY"))
    client = Client(
        ClientConfig(
            api_id=int(required_env(env, "MINIPROTO_API_ID")),
            api_hash=required_env(env, "MINIPROTO_API_HASH"),
            session_storage=storage,
            transport=TransportConfig(read_timeout=args.request_timeout, write_timeout=args.request_timeout),
            dc_id=args.dc_id,
            test_mode=False,
            request_timeout=args.request_timeout,
            max_request_retries=3,
            flood_sleep_threshold=300,
        )
    )
    await client.connect()
    record = load_session_record(await storage.load(), client.config.dc_id)
    if actor == "bot":
        if record.user is None or not record.user.is_bot:
            await client.sign_in_bot(required_env(env, "MINIPROTO_BOT_TOKEN"))
    elif record.user is None or record.user.is_bot:
        await client.sign_in_phone(required_env(env, "MINIPROTO_REAL_PHONE"), lambda: prompt_code(env))
    record = load_session_record(await storage.load(), client.config.dc_id)
    if actor == "bot" and (record.user is None or not record.user.is_bot):
        raise RuntimeError(f"session {session_path} is not authorized as a bot")
    if actor == "user" and (record.user is None or record.user.is_bot):
        raise RuntimeError(f"session {session_path} is not authorized as a user")
    return client, SessionSummary(
        index=session_index,
        session_path=str(session_path),
        auth_key_id_hex=session_auth_key_id_hex(record),
        user_id=record.user.id if record.user is not None else None,
        is_bot=record.user.is_bot if record.user is not None else None,
        duplicate_auth_key=False,
    )


def file_id_for_args(args: argparse.Namespace, env: Mapping[str, str]) -> str | None:
    """Select actor-specific, legacy live-benchmark, or command-line file ID in priority order.

    Args:
        args: Parsed actor and optional CLI media identifier.
        env: Environment mapping holding actor-specific compatibility defaults.
    """
    return (
        env_value(env, f"MINIPROTO_MULTI_SESSION_DOWNLOAD_{str(args.actor).upper()}_FILE_ID")
        or env_value(env, f"MINIPROTO_LIVE_BENCH_{str(args.actor).upper()}_FILE_ID")
        or args.file_id
    )


def download_size(args: argparse.Namespace, media: Media) -> int:
    """Return explicit parsed size or the size embedded in ``media``.

    Raises:
        SystemExit: If neither source provides size metadata.

    Args:
        args: Parsed optional explicit size selection.
        media: Parsed remote metadata whose embedded size is the fallback.
    """
    if args.size:
        return parse_size(str(args.size))
    if media.size is None:
        raise SystemExit("file id does not include size metadata; pass --size or MINIPROTO_MULTI_SESSION_DOWNLOAD_SIZE")
    return int(media.size)


def resolve_session_paths(args: argparse.Namespace, env: Mapping[str, str]) -> tuple[Path, ...]:
    """Choose explicit, environment-configured, or generated per-client session paths.

    Generated paths are only candidates; a live run may create or update their encrypted session databases during authorization.

    Args:
        args: Parsed explicit session paths, actor, client count, and DC.
        env: Environment mapping containing optional delimited session-path defaults.
    """
    if args.session:
        return tuple(Path(path) for path in args.session)
    configured = env_value(env, "MINIPROTO_MULTI_SESSION_DOWNLOAD_SESSIONS")
    if configured:
        paths = tuple(Path(item) for item in split_session_paths(configured))
        if paths:
            return paths
    return tuple(
        Path(".tmp") / f"miniproto-multi-session-download-{args.actor}-{index}-dc{args.dc_id}.sqlite"
        for index in range(args.clients)
    )


def split_session_paths(raw: str) -> tuple[str, ...]:
    """Split comma- or semicolon-delimited session paths, omitting blank components.

    Args:
        raw: Environment-provided delimited path string.
    """
    items: list[str] = []
    for chunk in raw.replace(",", ";").split(";"):
        item = chunk.strip()
        if item:
            items.append(item)
    return tuple(items)


def plan_contiguous_ranges(
    total_size: int, *, requested_workers: int, alignment: int = MIB
) -> tuple[DownloadRange, ...]:
    """Partition positive size into contiguous aligned ranges without zero-length workers.

    The final active worker receives the non-aligned tail. Files smaller than one alignment unit use one complete range regardless of requested workers.

    Raises:
        ValueError: If total size, requested worker count, or alignment is not positive.

    Args:
        total_size: Positive complete remote file size in bytes.
        requested_workers: Requested session count before empty ranges are eliminated.
        alignment: Positive byte alignment for every non-tail worker range.
    """
    if total_size <= 0:
        raise ValueError("total_size must be positive")
    if requested_workers <= 0:
        raise ValueError("requested_workers must be positive")
    if alignment <= 0:
        raise ValueError("alignment must be positive")
    full_units, tail = divmod(total_size, alignment)
    if full_units == 0:
        return (DownloadRange(index=0, offset=0, limit=total_size),)
    active_workers = min(requested_workers, full_units)
    base_units, extra_units = divmod(full_units, active_workers)
    ranges: list[DownloadRange] = []
    offset = 0
    for index in range(active_workers):
        units = base_units + (1 if index < extra_units else 0)
        limit = units * alignment
        if index == active_workers - 1:
            limit += tail
        ranges.append(DownloadRange(index=index, offset=offset, limit=limit))
        offset += limit
    return tuple(ranges)


def duplicate_auth_key_groups(auth_key_ids: Sequence[str | None]) -> dict[str, tuple[int, ...]]:
    """Return non-null auth-key identifiers assigned to more than one session index.

    Args:
        auth_key_ids: Derived redacted key identifiers aligned by session index.
    """
    grouped: dict[str, list[int]] = {}
    for index, auth_key in enumerate(auth_key_ids):
        if auth_key is None:
            continue
        grouped.setdefault(auth_key, []).append(index)
    return {key: tuple(indices) for key, indices in grouped.items() if len(indices) > 1}


def session_auth_key_id_hex(record) -> str | None:
    """Return a non-secret little-endian auth-key identifier, or ``None`` without a key.

    Args:
        record: Decrypted session record inspected only to derive an identifier, never key bytes for output.
    """
    if record.auth_key is None:
        return None
    if record.auth_key.key_id is not None:
        return int(record.auth_key.key_id).to_bytes(8, "little", signed=False).hex()
    return auth_key_id(record.auth_key.key).hex()


def require_common_live_env(env: Mapping[str, str]) -> None:
    """Require opt-in and essential live Telegram environment values.

    Raises:
        SystemExit: If either live guard or API/session-key configuration is missing.

    Args:
        env: Environment-only opt-in, API, and encrypted-session-key configuration.
    """
    if env_value(env, "MINIPROTO_INTEGRATION") != "1":
        raise SystemExit("set MINIPROTO_INTEGRATION=1 for live Telegram benchmarks")
    if env_value(env, "MINIPROTO_REAL_INTEGRATION") != "1":
        raise SystemExit("set MINIPROTO_REAL_INTEGRATION=1 for production Telegram benchmarks")
    missing = [
        name for name in ("MINIPROTO_API_ID", "MINIPROTO_API_HASH", "MINIPROTO_SESSION_KEY") if not env_value(env, name)
    ]
    if missing:
        raise SystemExit(f"missing live benchmark environment variables: {', '.join(missing)}")


def assemble_parts(part_paths: Sequence[Path], output_path: Path, *, expected_size: int) -> None:
    """Concatenate part files in order using 4 MiB reads and verify the final byte count.

    The output path is opened for writing and therefore overwritten if it exists.

    Raises:
        RuntimeError: If concatenated bytes differ from ``expected_size``.

    Args:
        part_paths: Completed worker output paths consumed in contiguous range order.
        output_path: Caller-selected assembled destination, whose parent is created and file overwritten.
        expected_size: Required assembled byte count before the result is accepted.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with output_path.open("wb") as output:
        for part_path in part_paths:
            with part_path.open("rb") as part:
                while chunk := part.read(4 * MIB):
                    output.write(chunk)
                    written += len(chunk)
    if written != expected_size:
        raise RuntimeError(f"assembled size mismatch: expected {expected_size}, wrote {written}")


def file_digest(path: Path) -> str:
    """Return the SHA-256 hexadecimal digest of one local file using 4 MiB reads.

    Args:
        path: Local file read for optional post-transfer comparison only.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(4 * MIB):
            digest.update(chunk)
    return digest.hexdigest()


def safe_file_name(value: str) -> str:
    """Replace unsafe filename characters with underscores, retaining a nonempty fallback.

    Args:
        value: Remote-provided or fallback filename component to make path-safe.
    """
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in value)
    return cleaned or "telegram-file.bin"


def print_summary(summary: MultiSessionDownloadSummary) -> None:
    """Print human-readable aggregate counters and one line per completed worker.

    Args:
        summary: Redacted observed live benchmark result; values are comparison evidence, not a guarantee.
    """
    print(
        f"multi-session.download: bytes={summary.bytes} clients_active={summary.clients_active}/{summary.clients_requested} "
        f"duration={summary.duration_s:.3f}s transfer={summary.transfer_mib_s:.3f}MiB/s overall={summary.overall_mib_s:.3f}MiB/s "
        f"finalize={summary.finalize_duration_s:.3f}s output={summary.output_path}"
    )
    if summary.duplicate_auth_key_groups:
        print(f"duplicate_auth_key_groups={summary.duplicate_auth_key_groups}")
    print(
        f"download counters: part_requests={summary.counters.part_requests} part_retries={summary.counters.part_retries} "
        f"flood_waits={summary.counters.flood_waits} flood_wait_seconds={summary.counters.flood_wait_seconds:g} "
        f"flood_waits_by_type={summary.counters.flood_waits_by_type} requests_per_s={summary.counters.requests_per_s:.3f} "
        f"launch_pace_waits={summary.counters.launch_pace_waits} launch_pace_wait_seconds={summary.counters.launch_pace_wait_seconds:g}"
    )
    for worker in summary.workers:
        eta = format_duration(worker.duration_s)
        print(
            f"worker {worker.index}: offset={worker.offset} limit={worker.limit} bytes={worker.bytes} "
            f"duration={worker.duration_s:.3f}s ({eta}) speed={worker.mib_s:.3f}MiB/s part={worker.part_path}"
        )


if __name__ == "__main__":
    raise SystemExit(main())
