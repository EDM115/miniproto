from __future__ import annotations

import asyncio
import json
from collections import Counter
from typing import Any

import pytest
import tools.bench.benchmark_media_scheduler as benchmark
from tools.bench.benchmark_media_scheduler import run_scheduler_benchmark


def test_scheduler_benchmark_json_proves_cap_fairness_cancellation_and_isolation() -> None:
    async def scenario() -> tuple[dict[str, Any], str]:
        loop = asyncio.get_running_loop()
        actual_backend = f"{type(loop).__module__}.{type(loop).__name__}"
        report = await run_scheduler_benchmark(
            transfers=4, parts_per_transfer=8, part_size=128 * 1024, max_bytes=256 * 1024
        )
        return report, actual_backend

    measured, actual_backend = asyncio.run(scenario())
    report = json.loads(json.dumps(measured, sort_keys=True))

    assert report["schema"] == "miniproto.media-scheduler-benchmark.v1"
    assert report["workload"]["transfers"] == 4
    assert report["accounting"]["peak_active_bytes"] <= 256 * 1024
    assert report["accounting"]["active_bytes_after"] == 0
    assert report["accounting"]["queued_bytes_after"] == 0
    assert report["accounting"]["minimum_grants"] == 8
    assert report["accounting"]["maximum_grants"] == 8
    assert report["accounting"]["grant_ratio"] == 1.0
    assert (
        report["fairness"]["max_competing_grant_imbalance"] <= report["fairness"]["allowed_competing_grant_imbalance"]
    )
    assert report["fairness"]["completed_transfers_excluded"] is True
    assert len(report["fairness"]["grant_order"]) == 32
    assert report["failures"] == []
    assert report["event_loop"]["running_backend"] == actual_backend
    assert report["isolation"]["different_dc_progressed_while_primary_full"] is True
    assert report["isolation"]["upload_progressed_while_download_full"] is True
    assert report["cancellation"]["queued_waiter_cancelled"] is True
    assert report["cancellation"]["leaked_bytes"] == 0
    assert report["aggregate"]["bytes"] == 4 * 8 * 128 * 1024
    assert report["aggregate"]["throughput_bytes_per_second"] > 0
    assert len(report["transfers"]) == 4

    transfer_ids = {transfer["transfer_id"] for transfer in report["transfers"]}
    assert len(transfer_ids) == 4
    assert all(isinstance(transfer_id, str) and transfer_id for transfer_id in transfer_ids)
    assert Counter(report["fairness"]["grant_order"]) == dict.fromkeys(transfer_ids, 8)
    for transfer in report["transfers"]:
        assert transfer["parts"] == 8
        assert transfer["bytes"] == 8 * 128 * 1024


def test_scheduler_fairness_rejects_monopolization_despite_equal_completed_counts(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    gather = asyncio.gather
    primary = True

    async def serialize_primary(*coroutines, **kwargs):
        nonlocal primary
        if primary:
            primary = False
            return [await coroutine for coroutine in coroutines]
        return await gather(*coroutines, **kwargs)

    monkeypatch.setattr(benchmark.asyncio, "gather", serialize_primary)
    report = asyncio.run(
        run_scheduler_benchmark(transfers=4, parts_per_transfer=8, part_size=128 * 1024, max_bytes=256 * 1024)
    )

    assert report["fairness"]["max_competing_grant_imbalance"] == 7
    assert report["fairness"]["allowed_competing_grant_imbalance"] == 2
    assert report["accounting"]["minimum_grants"] == report["accounting"]["maximum_grants"] == 8
    assert report["failures"][0]["type"] == "SchedulerFairnessError"
    primary = True
    assert (
        benchmark.main(
            ["--transfers", "4", "--parts-per-transfer", "8", "--part-size", "131072", "--max-bytes", "262144"]
        )
        == 1
    )
    assert json.loads(capsys.readouterr().out)["failures"][0]["type"] == "SchedulerFairnessError"
