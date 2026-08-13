from __future__ import annotations

import argparse
import asyncio
import json
import time
from collections.abc import Sequence
from typing import Any

from miniproto.media.scheduler import MEDIA_SCHEDULER_UNIT, MediaSchedulerRegistry


async def run_scheduler_benchmark(
    *, transfers: int = 10, parts_per_transfer: int = 64, part_size: int = 512 * 1024, max_bytes: int = 8 * 1024 * 1024
) -> dict[str, Any]:
    if transfers <= 0 or parts_per_transfer <= 0 or part_size <= 0 or max_bytes < MEDIA_SCHEDULER_UNIT:
        raise ValueError("benchmark dimensions and limits must be positive")
    registry = MediaSchedulerRegistry(
        download_max_bytes=max_bytes,
        upload_max_bytes=max_bytes,
        download_small_limit=max(1, transfers),
        download_large_limit=max(1, transfers),
    )
    handles = [
        registry.open_transfer(dc_id=2, direction="download", total_size=parts_per_transfer * part_size)
        for _ in range(transfers)
    ]
    peak_active_bytes = 0
    started = time.perf_counter()
    transfer_results: list[dict[str, Any] | None] = [None] * transfers
    queue_wait_seconds: list[float] = []

    async def run_transfer(index: int) -> None:
        nonlocal peak_active_bytes
        handle = handles[index]
        transfer_started = time.perf_counter()
        transfer_wait_seconds = 0.0
        for _part in range(parts_per_transfer):
            wait_started = time.perf_counter()
            permit = await handle.acquire(part_size)
            wait_seconds = max(time.perf_counter() - wait_started, 0.0)
            transfer_wait_seconds += wait_seconds
            queue_wait_seconds.append(wait_seconds)
            peak_active_bytes = max(peak_active_bytes, handle.scheduler_snapshot.active_bytes)
            await asyncio.sleep(0)
            permit.release()
        duration = max(time.perf_counter() - transfer_started, 1e-9)
        transferred = parts_per_transfer * part_size
        transfer_results[index] = {
            "transfer_id": handle.transfer_id,
            "bytes": transferred,
            "parts": parts_per_transfer,
            "duration_seconds": duration,
            "throughput_bytes_per_second": transferred / duration,
            "queue_wait_seconds": transfer_wait_seconds,
        }

    await asyncio.gather(*(run_transfer(index) for index in range(transfers)))
    duration = max(time.perf_counter() - started, 1e-9)
    primary_snapshot = handles[0].scheduler_snapshot

    isolation_blocker = registry.open_transfer(dc_id=2, direction="download", total_size=part_size)
    blocker = await isolation_blocker.acquire(max_bytes)
    other_dc = registry.open_transfer(dc_id=4, direction="download", total_size=part_size)
    upload = registry.open_transfer(dc_id=2, direction="upload", total_size=part_size)
    other_dc_permit, upload_permit = await asyncio.gather(other_dc.acquire(part_size), upload.acquire(part_size))
    different_dc_progressed = not other_dc_permit.released
    upload_progressed = not upload_permit.released
    other_dc_permit.release()
    upload_permit.release()

    cancelled_transfer = registry.open_transfer(dc_id=2, direction="download", total_size=part_size)
    cancelled_waiter = asyncio.create_task(cancelled_transfer.acquire(part_size))
    await asyncio.sleep(0)
    cancelled_waiter.cancel()
    cancellation_result = await asyncio.gather(cancelled_waiter, return_exceptions=True)
    queued_waiter_cancelled = isinstance(cancellation_result[0], asyncio.CancelledError)
    blocker.release()
    drained_snapshot = cancelled_transfer.scheduler_snapshot

    for handle in (*handles, isolation_blocker, other_dc, upload, cancelled_transfer):
        await handle.close()
    # All scheduler instances remove themselves when the final transfer closes;
    # zero registry entries proves both active and queued accounting drained.
    if registry.scheduler_count != 0:
        raise RuntimeError("scheduler benchmark leaked an idle scheduler")
    grants = tuple(primary_snapshot.grants_by_transfer.values())
    minimum_grants = min(grants, default=0)
    maximum_grants = max(grants, default=0)
    aggregate_bytes = transfers * parts_per_transfer * part_size
    return {
        "schema": "miniproto.media-scheduler-benchmark.v1",
        "workload": {
            "transfers": transfers,
            "parts_per_transfer": parts_per_transfer,
            "part_size": part_size,
            "max_bytes": max_bytes,
        },
        "aggregate": {
            "bytes": aggregate_bytes,
            "duration_seconds": duration,
            "throughput_bytes_per_second": aggregate_bytes / duration,
        },
        "transfers": [item for item in transfer_results if item is not None],
        "fairness": {
            "minimum_grants": minimum_grants,
            "maximum_grants": maximum_grants,
            "grant_ratio": minimum_grants / maximum_grants if maximum_grants else 1.0,
            "grants_by_transfer": primary_snapshot.grants_by_transfer,
        },
        "accounting": {
            "peak_active_bytes": peak_active_bytes,
            "configured_max_bytes": max_bytes,
            "active_bytes_after": drained_snapshot.active_bytes,
            "queued_bytes_after": drained_snapshot.queued_bytes,
            "queue_wait_seconds_total": sum(queue_wait_seconds),
            "queue_wait_seconds_max": max(queue_wait_seconds, default=0.0),
        },
        "isolation": {
            "different_dc_progressed_while_primary_full": different_dc_progressed,
            "upload_progressed_while_download_full": upload_progressed,
        },
        "cancellation": {
            "queued_waiter_cancelled": queued_waiter_cancelled,
            "leaked_bytes": drained_snapshot.active_bytes + drained_snapshot.queued_bytes,
        },
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the deterministic per-DC media scheduler benchmark")
    parser.add_argument("--transfers", type=int, default=10)
    parser.add_argument("--parts-per-transfer", type=int, default=64)
    parser.add_argument("--part-size", type=int, default=512 * 1024)
    parser.add_argument("--max-bytes", type=int, default=8 * 1024 * 1024)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = asyncio.run(
        run_scheduler_benchmark(
            transfers=args.transfers,
            parts_per_transfer=args.parts_per_transfer,
            part_size=args.part_size,
            max_bytes=args.max_bytes,
        )
    )
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
