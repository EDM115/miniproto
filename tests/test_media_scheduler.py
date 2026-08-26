from __future__ import annotations

import asyncio
from typing import Any, cast

import pytest

from miniproto.config import ClientConfig
from miniproto.media.scheduler import MEDIA_SCHEDULER_UNIT, MediaSchedulerRegistry


def test_scheduler_enforces_byte_cap_and_round_robin_progress() -> None:
    async def run() -> None:
        registry = MediaSchedulerRegistry(
            download_max_bytes=2 * MEDIA_SCHEDULER_UNIT, upload_max_bytes=MEDIA_SCHEDULER_UNIT
        )
        first = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        second = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        first_permit = await first.acquire(2 * MEDIA_SCHEDULER_UNIT)
        first_waiter = asyncio.create_task(first.acquire(2 * MEDIA_SCHEDULER_UNIT))
        second_waiter = asyncio.create_task(second.acquire(2 * MEDIA_SCHEDULER_UNIT))
        await asyncio.sleep(0)

        assert not first_waiter.done()
        assert not second_waiter.done()
        assert first.scheduler_snapshot.active_bytes == 2 * MEDIA_SCHEDULER_UNIT

        first_permit.release()
        second_permit = await asyncio.wait_for(second_waiter, 0.1)
        assert not first_waiter.done()
        assert second.scheduler_snapshot.active_bytes == 2 * MEDIA_SCHEDULER_UNIT

        second_permit.release()
        next_first_permit = await asyncio.wait_for(first_waiter, 0.1)
        next_first_permit.release()
        await first.close()
        await second.close()
        assert registry.scheduler_count == 0

    asyncio.run(run())


def test_scheduler_uses_remaining_byte_capacity_while_another_transfer_is_active() -> None:
    async def run() -> None:
        registry = MediaSchedulerRegistry(
            download_max_bytes=4 * MEDIA_SCHEDULER_UNIT, upload_max_bytes=MEDIA_SCHEDULER_UNIT, download_small_limit=2
        )
        first = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        second = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        first_permit = await first.acquire(2 * MEDIA_SCHEDULER_UNIT)
        second_permit = await asyncio.wait_for(second.acquire(2 * MEDIA_SCHEDULER_UNIT), 0.1)
        assert first.scheduler_snapshot.active_bytes == 4 * MEDIA_SCHEDULER_UNIT
        first_permit.release()
        second_permit.release()
        await first.close()
        await second.close()

    asyncio.run(run())


def test_scheduler_foreground_precedes_background_without_starving_it() -> None:
    async def run() -> None:
        registry = MediaSchedulerRegistry(
            download_max_bytes=MEDIA_SCHEDULER_UNIT, upload_max_bytes=MEDIA_SCHEDULER_UNIT
        )
        blocker = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        foreground = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        background = registry.open_transfer(dc_id=2, direction="download", total_size=1024, priority="background")
        blocker_permit = await blocker.acquire(MEDIA_SCHEDULER_UNIT)
        background_waiter = asyncio.create_task(background.acquire(MEDIA_SCHEDULER_UNIT))
        foreground_waiter = asyncio.create_task(foreground.acquire(MEDIA_SCHEDULER_UNIT))
        await asyncio.sleep(0)

        blocker_permit.release()
        foreground_permit = await asyncio.wait_for(foreground_waiter, 0.1)
        assert not background_waiter.done()

        for _ in range(8):
            next_foreground = asyncio.create_task(foreground.acquire(MEDIA_SCHEDULER_UNIT))
            await asyncio.sleep(0)
            foreground_permit.release()
            await asyncio.sleep(0)
            if background_waiter.done():
                break
            foreground_permit = await asyncio.wait_for(next_foreground, 0.1)
        else:
            pytest.fail("background transfer did not receive a bounded fairness grant")

        if not next_foreground.done():
            next_foreground.cancel()
            await asyncio.gather(next_foreground, return_exceptions=True)
        background_permit = await background_waiter
        background_permit.release()
        if not foreground_permit.released:
            foreground_permit.release()
        await blocker.close()
        await foreground.close()
        await background.close()

    asyncio.run(run())


def test_scheduler_separates_dcs_directions_and_download_size_classes() -> None:
    async def run() -> None:
        registry = MediaSchedulerRegistry(
            download_max_bytes=2 * MEDIA_SCHEDULER_UNIT,
            upload_max_bytes=MEDIA_SCHEDULER_UNIT,
            download_small_limit=1,
            download_large_limit=1,
        )
        small = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        other_small = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        large = registry.open_transfer(dc_id=2, direction="download", total_size=20 * 1024 * 1024)
        other_dc = registry.open_transfer(dc_id=4, direction="download", total_size=1024)
        upload = registry.open_transfer(dc_id=2, direction="upload", total_size=1024)

        small_permit = await small.acquire(MEDIA_SCHEDULER_UNIT)
        other_small_waiter = asyncio.create_task(other_small.acquire(MEDIA_SCHEDULER_UNIT))
        large_waiter = asyncio.create_task(large.acquire(MEDIA_SCHEDULER_UNIT))
        await asyncio.sleep(0)
        assert not other_small_waiter.done()
        large_permit = await asyncio.wait_for(large_waiter, 0.1)

        other_dc_permit, upload_permit = await asyncio.gather(
            other_dc.acquire(MEDIA_SCHEDULER_UNIT), upload.acquire(MEDIA_SCHEDULER_UNIT)
        )
        other_dc_permit.release()
        upload_permit.release()
        small_permit.release()
        other_small_permit = await asyncio.wait_for(other_small_waiter, 0.1)
        large_permit.release()
        other_small_permit.release()
        for transfer in (small, other_small, large, other_dc, upload):
            await transfer.close()

    asyncio.run(run())


def test_scheduler_cancellation_and_rebind_leak_no_permits_or_idle_schedulers() -> None:
    async def run() -> None:
        registry = MediaSchedulerRegistry(
            download_max_bytes=MEDIA_SCHEDULER_UNIT, upload_max_bytes=MEDIA_SCHEDULER_UNIT
        )
        transfer = registry.open_transfer(dc_id=2, direction="download", total_size=None)
        permit = await transfer.acquire(MEDIA_SCHEDULER_UNIT)
        waiter = asyncio.create_task(transfer.acquire(MEDIA_SCHEDULER_UNIT))
        await asyncio.sleep(0)
        waiter.cancel()
        with pytest.raises(asyncio.CancelledError):
            await waiter
        permit.release()
        assert transfer.scheduler_snapshot.active_bytes == 0
        assert transfer.scheduler_snapshot.queued_bytes == 0

        await transfer.rebind(4)
        assert transfer.dc_id == 4
        rebound = await transfer.acquire(MEDIA_SCHEDULER_UNIT)
        rebound.release()
        await transfer.close()
        assert registry.scheduler_count == 0

    asyncio.run(run())


def test_scheduler_releases_a_grant_cancelled_before_the_waiter_resumes() -> None:
    async def run() -> None:
        registry = MediaSchedulerRegistry(
            download_max_bytes=MEDIA_SCHEDULER_UNIT, upload_max_bytes=MEDIA_SCHEDULER_UNIT
        )
        blocker = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        waiting = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        blocker_permit = await blocker.acquire(MEDIA_SCHEDULER_UNIT)
        waiter = asyncio.create_task(waiting.acquire(MEDIA_SCHEDULER_UNIT))
        await asyncio.sleep(0)
        asyncio.get_running_loop().call_soon(waiter.cancel)
        blocker_permit.release()
        with pytest.raises(asyncio.CancelledError):
            await waiter
        snapshot = waiting.scheduler_snapshot
        assert snapshot.active_bytes == 0
        assert snapshot.queued_bytes == 0
        await blocker.close()
        await waiting.close()
        assert registry.scheduler_count == 0

    asyncio.run(run())


def test_scheduler_cancellation_after_rebind_removes_the_destination_waiter() -> None:
    async def run() -> None:
        registry = MediaSchedulerRegistry(
            download_max_bytes=MEDIA_SCHEDULER_UNIT, upload_max_bytes=MEDIA_SCHEDULER_UNIT
        )
        transfer = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        destination_blocker = registry.open_transfer(dc_id=4, direction="download", total_size=1024)
        source_permit = await transfer.acquire(MEDIA_SCHEDULER_UNIT)
        destination_permit = await destination_blocker.acquire(MEDIA_SCHEDULER_UNIT)
        waiter = asyncio.create_task(transfer.acquire(MEDIA_SCHEDULER_UNIT))
        await asyncio.sleep(0)
        source_scheduler = cast(Any, transfer)._scheduler

        await transfer.rebind(4)
        destination_scheduler = cast(Any, transfer)._scheduler
        assert source_scheduler.snapshot().queued_bytes == 0
        assert destination_scheduler.snapshot().queued_bytes == MEDIA_SCHEDULER_UNIT

        waiter.cancel()
        with pytest.raises(asyncio.CancelledError):
            await waiter
        assert source_scheduler.snapshot().queued_bytes == 0
        assert destination_scheduler.snapshot().queued_bytes == 0

        source_permit.release()
        destination_permit.release()
        assert source_scheduler.snapshot().active_bytes == 0
        assert destination_scheduler.snapshot().active_bytes == 0
        await transfer.close()
        await destination_blocker.close()
        assert registry.scheduler_count == 0

    asyncio.run(run())


def test_scheduler_rejects_request_larger_than_configured_hard_cap() -> None:
    async def run() -> None:
        registry = MediaSchedulerRegistry(
            download_max_bytes=MEDIA_SCHEDULER_UNIT, upload_max_bytes=MEDIA_SCHEDULER_UNIT
        )
        transfer = registry.open_transfer(dc_id=2, direction="download", total_size=1024)
        with pytest.raises(ValueError, match="exceeds the per-DC byte limit"):
            await transfer.acquire(2 * MEDIA_SCHEDULER_UNIT)
        await transfer.close()

    asyncio.run(run())


@pytest.mark.parametrize(
    ("option", "value"),
    [
        ("media_download_max_in_flight_bytes_per_dc", MEDIA_SCHEDULER_UNIT - 1),
        ("media_upload_max_in_flight_bytes_per_dc", 0),
        ("media_download_small_queue_limit", 0),
        ("media_download_large_queue_limit", -1),
    ],
)
def test_client_config_rejects_invalid_scheduler_limits(option: str, value: int) -> None:
    with pytest.raises(ValueError, match=option):
        cast(Any, ClientConfig)(api_id=1, api_hash="hash", **{option: value})
