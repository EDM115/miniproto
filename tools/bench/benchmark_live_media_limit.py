from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import statistics
import sys
import time
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from getpass import getpass
from pathlib import Path
from typing import Any, Literal

from miniproto import Client, ClientConfig, EncryptedSQLiteSessionStorage, event_loop
from miniproto.invoke import load_session_record
from miniproto.media import DEFAULT_CHUNK_SIZE

TELEGRAM_DEFAULT_UPLOAD_PARTS = 4000
TELEGRAM_DEFAULT_LIMIT_BYTES = TELEGRAM_DEFAULT_UPLOAD_PARTS * DEFAULT_CHUNK_SIZE
BENCH_GUARD_ENV = "MINIPROTO_LIVE_BENCH"

Actor = Literal["user", "bot"]


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
class TransferSummary:
    actor: Actor
    operation: Literal["upload", "download"]
    dc_id: int
    media_dc_id: int | None
    bytes: int
    duration_s: float
    overall_mib_s: float
    samples: SampleStats
    peer: str
    message_id: int | None = None
    path: str | None = None


@dataclass(frozen=True, slots=True)
class BenchmarkSummary:
    generated_file: str
    generated_file_bytes: int
    chunk_size: int
    upload_limit_parts: int
    event_loop_backend: str
    results: tuple[TransferSummary, ...]


@dataclass(slots=True)
class TransferRecorder:
    total: int | None
    label: str
    progress_interval_s: float
    start: float = 0.0
    last_time: float = 0.0
    last_report_time: float = 0.0
    last_bytes: int = 0
    samples_mib_s: list[float] | None = None

    def __post_init__(self) -> None:
        self.samples_mib_s = []

    def begin(self) -> None:
        now = time.perf_counter()
        self.start = now
        self.last_time = now
        self.last_report_time = now
        self.last_bytes = 0

    async def progress(self, current: int, total: int | None) -> None:
        self.record(current, total)
        await asyncio.sleep(0)

    def record(self, current: int, total: int | None, *, now: float | None = None) -> None:
        del total
        sampled_at = time.perf_counter() if now is None else now
        if self.start <= 0:
            self.start = sampled_at
            self.last_time = sampled_at
        elapsed = sampled_at - self.last_time
        delta = current - self.last_bytes
        if elapsed > 0 and delta > 0:
            assert self.samples_mib_s is not None
            instant_mib_s = _mib(delta) / elapsed
            self.samples_mib_s.append(instant_mib_s)
            if (
                self.progress_interval_s > 0
                and sampled_at - self.last_report_time >= self.progress_interval_s
            ):
                self.last_report_time = sampled_at
                print_progress(
                    self.label,
                    current=current,
                    total=self.total,
                    elapsed_s=sampled_at - self.start,
                    instant_mib_s=instant_mib_s,
                )
        self.last_time = sampled_at
        self.last_bytes = current

    def finish(self, bytes_done: int) -> tuple[float, SampleStats]:
        finished_at = time.perf_counter()
        duration = max(finished_at - self.start, 1e-9)
        assert self.samples_mib_s is not None
        return duration, sample_stats(
            self.samples_mib_s, fallback_overall_mib_s=_mib(bytes_done) / duration
        )


def main(argv: list[str] | None = None) -> int:
    env = load_dotenv()
    args = parse_args(argv, env)
    if env_value(env, BENCH_GUARD_ENV) != "1":
        print(
            f"Refusing to run the live media-limit benchmark without {BENCH_GUARD_ENV}=1. "
            "This benchmark creates and transfers a roughly 2 GB file.",
            file=sys.stderr,
        )
        return 2
    print(
        f"event_loop_backend={event_loop.backend_name()} "
        f"installed={event_loop.installed()} version={event_loop.backend_version()}"
    )
    return event_loop.run(run_benchmark(args, env))


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
    parser.add_argument(
        "--concurrency",
        type=int,
        default=int(env_value(values, "MINIPROTO_LIVE_BENCH_CONCURRENCY", "8") or "8"),
        help="number of concurrent upload part requests on the active MTProto sender",
    )
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=float(env_value(values, "MINIPROTO_LIVE_BENCH_REQUEST_TIMEOUT", "120") or "120"),
        help="per-request timeout in seconds",
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
    return parser.parse_args(argv)


async def run_benchmark(args: argparse.Namespace, env: Mapping[str, str]) -> int:
    limit_parts = upload_limit_parts_from_env_or_default(env, args.dc_id)
    size = parse_size(args.size, default_bytes=limit_parts * DEFAULT_CHUNK_SIZE)
    print(
        f"payload: path={args.file} bytes={size} chunks={math.ceil(size / DEFAULT_CHUNK_SIZE)} "
        f"chunk_size={DEFAULT_CHUNK_SIZE}"
    )
    ensure_benchmark_file(
        args.file, size=size, chunk_size=DEFAULT_CHUNK_SIZE, force=args.force_regenerate
    )
    if args.prepare_only:
        print(f"prepared {args.file} ({size} bytes)")
        return 0
    require_live_env(env, actor=args.actor)
    actors: tuple[Actor, ...] = ("user", "bot") if args.actor == "both" else (args.actor,)
    results: list[TransferSummary] = []
    for actor in actors:
        print(f"{actor}: authorizing session on DC {args.dc_id}")
        client = await authorized_client(actor, args, env)
        peer = env_value(env, f"MINIPROTO_LIVE_BENCH_{actor.upper()}_PEER") or "self"
        try:
            results.extend(
                await benchmark_actor(
                    client,
                    actor=actor,
                    peer=peer,
                    source=args.file,
                    download_dir=args.download_dir,
                    dc_id=args.dc_id,
                    concurrency=args.concurrency,
                    request_timeout=args.request_timeout,
                    verify_digest=args.verify_digest,
                    progress_interval_s=args.progress_interval,
                )
            )
        finally:
            await client.disconnect()
    summary = BenchmarkSummary(
        generated_file=str(args.file),
        generated_file_bytes=size,
        chunk_size=DEFAULT_CHUNK_SIZE,
        upload_limit_parts=limit_parts,
        event_loop_backend=event_loop.backend_name(),
        results=tuple(results),
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
    peer: str,
    source: Path,
    download_dir: Path,
    dc_id: int,
    concurrency: int,
    request_timeout: float,
    verify_digest: bool,
    progress_interval_s: float,
) -> tuple[TransferSummary, TransferSummary]:
    caption = f"miniproto live media limit bench {actor} {int(time.time())}"
    size = await asyncio.to_thread(lambda: source.stat().st_size)
    print(
        f"{actor}.upload: starting peer={peer} bytes={size} concurrency={concurrency} "
        f"request_timeout={request_timeout:g}s"
    )
    upload_recorder = TransferRecorder(
        total=size, label=f"{actor}.upload", progress_interval_s=progress_interval_s
    )
    upload_recorder.begin()
    sent = await client.send_file(
        peer,
        source,
        caption=caption,
        file_name=source.name,
        concurrency=concurrency,
        progress=upload_recorder.progress,
        request_timeout=request_timeout,
    )
    upload_duration, upload_stats = upload_recorder.finish(size)
    media = sent.media or await find_recent_media(client, peer, caption)
    if media is None:
        raise RuntimeError(f"{actor} upload completed but no media was found for the sent message")
    upload = TransferSummary(
        actor=actor,
        operation="upload",
        dc_id=dc_id,
        media_dc_id=media.dc_id,
        bytes=size,
        duration_s=upload_duration,
        overall_mib_s=_mib(size) / upload_duration,
        samples=upload_stats,
        peer=peer,
        message_id=sent.id or None,
        path=str(source),
    )
    print_transfer(upload)
    await asyncio.to_thread(download_dir.mkdir, parents=True, exist_ok=True)
    target = download_dir / f"{actor}-dc{dc_id}-{source.name}"
    await asyncio.to_thread(target.unlink, missing_ok=True)
    print(f"{actor}.download: starting media_dc={media.dc_id} target={target}")
    download_recorder = TransferRecorder(
        total=size, label=f"{actor}.download", progress_interval_s=progress_interval_s
    )
    download_recorder.begin()
    downloaded = await client.download_media(
        media,
        target,
        limit=size,
        total_size=size,
        progress=download_recorder.progress,
        request_timeout=request_timeout,
    )
    download_duration, download_stats = download_recorder.finish(downloaded.bytes_downloaded)
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
        dc_id=dc_id,
        media_dc_id=media.dc_id,
        bytes=downloaded.bytes_downloaded,
        duration_s=download_duration,
        overall_mib_s=_mib(downloaded.bytes_downloaded) / download_duration,
        samples=download_stats,
        peer=peer,
        message_id=sent.id or None,
        path=str(target),
    )
    print_transfer(download)
    return upload, download


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
        f"{summary.bytes} bytes in {summary.duration_s:.3f}s "
        f"overall={summary.overall_mib_s:.3f}MiB/s "
        f"median={summary.samples.median_mib_s:.3f}MiB/s "
        f"p95={summary.samples.p95_mib_s:.3f}MiB/s "
        f"p01={summary.samples.p01_mib_s:.3f}MiB/s "
        f"fastest_5pct_avg={summary.samples.fastest_5pct_avg_mib_s:.3f}MiB/s "
        f"slowest_1pct_avg={summary.samples.slowest_1pct_avg_mib_s:.3f}MiB/s "
        f"samples={summary.samples.samples} media_dc={summary.media_dc_id}"
    )


def print_progress(
    label: str, *, current: int, total: int | None, elapsed_s: float, instant_mib_s: float
) -> None:
    if total is None or total <= 0:
        print(
            f"{label}: {_mib(current):.1f}MiB transferred "
            f"elapsed={elapsed_s:.1f}s instant={instant_mib_s:.3f}MiB/s"
        )
        return
    percent = min(100.0, current / total * 100)
    overall_mib_s = _mib(current) / elapsed_s if elapsed_s > 0 else 0.0
    remaining_bytes = max(0, total - current)
    eta_s = _mib(remaining_bytes) / overall_mib_s if overall_mib_s > 0 else math.inf
    print(
        f"{label}: {percent:6.2f}% {_mib(current):.1f}/{_mib(total):.1f}MiB "
        f"elapsed={elapsed_s:.1f}s eta={format_duration(eta_s)} "
        f"avg={overall_mib_s:.3f}MiB/s instant={instant_mib_s:.3f}MiB/s"
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


def print_summary(summary: BenchmarkSummary) -> None:
    print(
        f"benchmark_file={summary.generated_file} bytes={summary.generated_file_bytes} "
        f"chunk_size={summary.chunk_size} upload_limit_parts={summary.upload_limit_parts}"
    )
    for result in summary.results:
        print_transfer(result)


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


def prompt_code(env: Mapping[str, str]) -> str:
    if env_value(env, "MINIPROTO_LIVE_PROMPT_CODE") != "1" or not sys.stdin.isatty():
        raise SystemExit(
            "no stored user session; set MINIPROTO_LIVE_PROMPT_CODE=1 and run interactively to enter the current Telegram code"
        )
    return input("Telegram login code: ").strip()


def prompt_password(env: Mapping[str, str]) -> str:
    password = env_value(env, "MINIPROTO_REAL_PASSWORD")
    if password:
        return password
    if env_value(env, "MINIPROTO_LIVE_PROMPT_CODE") == "1" and sys.stdin.isatty():
        return getpass("Telegram 2FA password, if requested: ")
    return ""


def _mib(value: int) -> float:
    return value / (1024 * 1024)


if __name__ == "__main__":
    raise SystemExit(main())
