from __future__ import annotations

import asyncio
import json

from tools.bench.benchmark_media_scheduler import run_scheduler_benchmark


def test_scheduler_benchmark_json_proves_cap_fairness_cancellation_and_isolation() -> None:
    report = asyncio.run(
        run_scheduler_benchmark(transfers=4, parts_per_transfer=8, part_size=128 * 1024, max_bytes=256 * 1024)
    )

    assert report["schema"] == "miniproto.media-scheduler-benchmark.v1"
    assert report["workload"]["transfers"] == 4
    assert report["accounting"]["peak_active_bytes"] <= 256 * 1024
    assert report["accounting"]["active_bytes_after"] == 0
    assert report["accounting"]["queued_bytes_after"] == 0
    assert report["fairness"]["minimum_grants"] == 8
    assert report["fairness"]["maximum_grants"] == 8
    assert report["fairness"]["grant_ratio"] == 1.0
    assert report["isolation"]["different_dc_progressed_while_primary_full"] is True
    assert report["isolation"]["upload_progressed_while_download_full"] is True
    assert report["cancellation"]["queued_waiter_cancelled"] is True
    assert report["cancellation"]["leaked_bytes"] == 0
    assert report["aggregate"]["bytes"] == 4 * 8 * 128 * 1024
    assert report["aggregate"]["throughput_bytes_per_second"] > 0
    assert len(report["transfers"]) == 4

    encoded = json.dumps(report, sort_keys=True)
    assert "transfer_id" in encoded
