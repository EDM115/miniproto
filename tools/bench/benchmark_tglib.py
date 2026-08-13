from __future__ import annotations

import argparse
import json
import os
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from miniproto import event_loop
from miniproto.file_id import media_from_file_id
from tools.bench.benchmark_live_media_limit import authorized_client, load_dotenv, require_live_env
from tools.bench.reporting import LoopLagProbe, build_benchmark_report, collect_environment, write_benchmark_report

TGLIB_DEFAULT_SIZE = 2_097_152_000
TGLIB_GUARD_ENV = "MINIPROTO_TGLIB_BENCH"


def build_tglib_compatibility_payload(
    *, size: int, download_started: float, download_finished: float, upload_started: float, upload_finished: float
) -> list[Any]:
    """Build the exact tglib-bench `[size, [t0,t1,t2,t3]]` result payload."""
    if size <= 0:
        raise ValueError("size must be positive")
    if download_finished < download_started:
        raise ValueError("download timestamps are reversed")
    if upload_finished < upload_started:
        raise ValueError("upload timestamps are reversed")
    return [size, [download_started, download_finished, upload_started, upload_finished]]


def build_tglib_report(
    *,
    size: int,
    timestamps: Sequence[float],
    finalize_finished: float,
    configuration: Mapping[str, Any],
    environment: Mapping[str, Any] | None = None,
    loop_lag: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build miniproto's rich companion report without changing the compatibility payload."""
    if len(timestamps) != 4:
        raise ValueError("timestamps must contain t0, t1, t2, and t3")
    compatibility = build_tglib_compatibility_payload(
        size=size,
        download_started=timestamps[0],
        download_finished=timestamps[1],
        upload_started=timestamps[2],
        upload_finished=timestamps[3],
    )
    if finalize_finished < timestamps[3]:
        raise ValueError("finalize timestamp precedes upload completion")
    download_duration = timestamps[1] - timestamps[0]
    upload_duration = timestamps[3] - timestamps[2]
    mib = size / (1024 * 1024)
    return build_benchmark_report(
        benchmark="tglib_compatibility",
        mode="tglib",
        warmup=0,
        samples=[download_duration, upload_duration],
        unit="seconds",
        configuration=configuration,
        environment=environment or collect_environment(),
        throughput={
            "download_mib_per_second": mib / max(download_duration, 1e-9),
            "upload_mib_per_second": mib / max(upload_duration, 1e-9),
        },
        loop_lag=loop_lag,
        results=[
            {
                "compatibility": compatibility,
                "download_duration_s": download_duration,
                "upload_duration_s": upload_duration,
                "finalize_duration_s": finalize_finished - timestamps[3],
                "timing_boundaries": {
                    "t0": "download started after connection and file-reference decoding",
                    "t1": "download bytes fully materialized",
                    "t2": "upload started",
                    "t3": "last upload byte accepted; final sendMedia excluded",
                    "finalize_finished": "final message submission completed",
                },
            }
        ],
    )


def parse_args(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> argparse.Namespace:
    """Parse the guarded compatibility runner without accepting secrets as CLI arguments."""
    values = os.environ if env is None else env
    parser = argparse.ArgumentParser(description="Run a guarded tglib-bench-compatible bot transfer")
    parser.add_argument(
        "--file-id",
        default=values.get("MINIPROTO_TGLIB_FILE_ID"),
        required=not bool(values.get("MINIPROTO_TGLIB_FILE_ID")),
    )
    parser.add_argument(
        "--peer", default=values.get("MINIPROTO_TGLIB_PEER"), required=not bool(values.get("MINIPROTO_TGLIB_PEER"))
    )
    parser.add_argument("--dc-id", type=int, default=int(values.get("MINIPROTO_TGLIB_DC_ID", "0")) or None)
    parser.add_argument("--size", type=int, default=int(values.get("MINIPROTO_TGLIB_SIZE", str(TGLIB_DEFAULT_SIZE))))
    parser.add_argument(
        "--request-timeout", type=float, default=float(values.get("MINIPROTO_TGLIB_REQUEST_TIMEOUT", "300"))
    )
    parser.add_argument(
        "--download-concurrency", type=int, default=int(values.get("MINIPROTO_TGLIB_DOWNLOAD_CONCURRENCY", "6"))
    )
    parser.add_argument(
        "--upload-concurrency", type=int, default=int(values.get("MINIPROTO_TGLIB_UPLOAD_CONCURRENCY", "8"))
    )
    parser.add_argument(
        "--download-chunk-size",
        type=int,
        default=int(values.get("MINIPROTO_TGLIB_DOWNLOAD_CHUNK_SIZE", str(512 * 1024))),
    )
    parser.add_argument(
        "--compat-json", type=Path, default=Path(values.get("MINIPROTO_TGLIB_COMPAT_JSON", "results.json"))
    )
    parser.add_argument(
        "--json", type=Path, default=Path(values.get("MINIPROTO_TGLIB_JSON", ".tmp/tglib/miniproto.json"))
    )
    parser.add_argument("--work-dir", type=Path, default=Path(values.get("MINIPROTO_TGLIB_WORK_DIR", ".tmp/tglib")))
    parser.add_argument(
        "--loop-lag", action=argparse.BooleanOptionalAction, default=values.get("MINIPROTO_TGLIB_LOOP_LAG", "1") == "1"
    )
    args = parser.parse_args(argv)
    if args.size <= 0 or args.request_timeout <= 0 or args.download_concurrency <= 0 or args.upload_concurrency <= 0:
        parser.error("size, timeout, and concurrency values must be positive")
    return args


async def run_tglib_benchmark(args: argparse.Namespace, env: Mapping[str, str]) -> tuple[list[Any], dict[str, Any]]:
    """Run one bot download/upload using tglib-compatible transfer timing boundaries."""
    media = media_from_file_id(args.file_id)
    media_dc_id = media.dc_id
    if media_dc_id is None and args.dc_id is None:
        raise SystemExit("the file ID does not contain a DC; pass --dc-id explicitly")
    if args.dc_id is not None and media_dc_id is not None and args.dc_id != media_dc_id:
        raise SystemExit(f"--dc-id {args.dc_id} does not match the file's encoded DC {media_dc_id}")
    args.dc_id = media_dc_id or args.dc_id
    args.work_dir.mkdir(parents=True, exist_ok=True)
    destination = args.work_dir / "tglib-download.bin"
    client = await authorized_client("bot", args, env)
    probe = LoopLagProbe(interval_s=0.01, stall_threshold_s=0.005) if args.loop_lag else None
    probe_started = False
    loop_lag: Mapping[str, Any] = {"enabled": False, "samples": 0}
    upload_finished: float | None = None

    async def upload_progress(current: int, total: int | None) -> None:
        nonlocal upload_finished
        if total is not None and current >= total and upload_finished is None:
            upload_finished = time.time()

    try:
        if probe is not None:
            await probe.start()
            probe_started = True
        download_started = time.time()
        downloaded = await client.download_media(
            media,
            destination=destination,
            part_size=args.download_chunk_size,
            concurrency=args.download_concurrency,
            adaptive_part_size=False,
        )
        download_finished = time.time()
        if downloaded.bytes_downloaded != args.size:
            raise RuntimeError(f"downloaded {downloaded.bytes_downloaded} bytes, expected {args.size}")
        upload_started = time.time()
        await client.send_file(
            args.peer,
            destination,
            file_name=destination.name,
            concurrency=args.upload_concurrency,
            progress=upload_progress,
        )
        finalize_finished = time.time()
        if upload_finished is None:
            raise RuntimeError("upload completed without a terminal progress callback")
    finally:
        try:
            if probe is not None and probe_started:
                loop_lag = await probe.stop()
        finally:
            await client.disconnect()
    compatibility = build_tglib_compatibility_payload(
        size=args.size,
        download_started=download_started,
        download_finished=download_finished,
        upload_started=upload_started,
        upload_finished=upload_finished,
    )
    report = build_tglib_report(
        size=args.size,
        timestamps=compatibility[1],
        finalize_finished=finalize_finished,
        configuration={
            "file_id": args.file_id,
            "peer": args.peer,
            "dc_id": args.dc_id,
            "download_concurrency": args.download_concurrency,
            "upload_concurrency": args.upload_concurrency,
            "download_chunk_size": args.download_chunk_size,
        },
        loop_lag=loop_lag,
    )
    return compatibility, report


def main(argv: Sequence[str] | None = None, *, env: Mapping[str, str] | None = None) -> int:
    values = load_dotenv() if env is None else dict(env)
    args = parse_args(argv, values)
    if values.get(TGLIB_GUARD_ENV) != "1":
        print(f"Refusing to run without {TGLIB_GUARD_ENV}=1; this mode transfers an existing 2 GiB fixture.")
        return 2
    require_live_env(values, actor="bot")
    compatibility, report = event_loop.run(run_tglib_benchmark(args, values))
    args.compat_json.parent.mkdir(parents=True, exist_ok=True)
    args.compat_json.write_text(json.dumps(compatibility) + "\n", encoding="utf-8", newline="\n")
    write_benchmark_report(args.json, report)
    print(json.dumps(compatibility))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
