from __future__ import annotations

import asyncio
import hashlib
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any, cast

import pytest

import miniproto.client as client_module
from miniproto import Client, InMemorySessionStorage
from miniproto.client import _MediaInvokeContext
from miniproto.config import ClientConfig
from miniproto.crypto.mtproto import media_ctr_crypt
from miniproto.errors import BadRequest
from miniproto.invoke import MethodFloodWaitCache
from miniproto.media import download_file
from miniproto.media.scheduler import MEDIA_SCHEDULER_UNIT, MediaSchedulerRegistry, MediaTransfer
from miniproto.raw import functions, types


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


UNIT = MEDIA_SCHEDULER_UNIT


class Sender:
    is_connected = True
    connection_initialized = True

    def __init__(self, respond: Callable[[Any], object] | None = None) -> None:
        self.respond = respond
        self.calls: asyncio.Queue[tuple[Any, asyncio.Future[object]]] = asyncio.Queue()

    async def request(self, request: object, **kwargs: object) -> object:
        del kwargs
        if self.respond is not None:
            return self.respond(request)
        result = asyncio.get_running_loop().create_future()
        self.calls.put_nowait((request, result))
        return await result


def make_client(*, budget: int = 2 * UNIT, small_limit: int = 5, large_limit: int = 2) -> Client:
    client = Client(
        ClientConfig(
            api_id=1,
            api_hash="synthetic",
            session_storage=InMemorySessionStorage(),
            media_download_max_in_flight_bytes_per_dc=budget,
            media_download_small_queue_limit=small_limit,
            media_download_large_queue_limit=large_limit,
            media_idle_close=None,
        )
    )
    client._connected = True
    return client


def cdn_request(offset: int = 0, *, limit: int = UNIT) -> object:
    return functions.UploadGetCdnFile(file_token=b"synthetic", offset=offset, limit=limit)


def watch_cdn_acquires(monkeypatch: pytest.MonkeyPatch) -> asyncio.Queue[int]:
    attempts: asyncio.Queue[int] = asyncio.Queue()
    acquire = MediaTransfer.acquire

    async def observed(transfer: MediaTransfer, requested_bytes: int, **kwargs: Any) -> Any:
        if transfer.dc_id == 4:
            attempts.put_nowait(requested_bytes)
        return await acquire(transfer, requested_bytes, **kwargs)

    monkeypatch.setattr(MediaTransfer, "acquire", observed)
    return attempts


def snapshot(client: Client, dc_id: int = 4) -> Any:
    return client._media_schedulers._schedulers[(dc_id, "download")].snapshot()


def test_redirected_downloads_charge_complete_wire_ranges_and_separate_dcs(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        attempts = watch_cdn_acquires(monkeypatch)
        client = make_client()
        plaintext = bytes(range(256)) * 512
        key, iv = bytes(range(32)), bytes(range(12)) + b"\0" * 4
        ciphertext = media_ctr_crypt(plaintext, key, iv)
        redirect = types.UploadFileCdnRedirect(
            dc_id=4,
            file_token=b"synthetic",
            encryption_key=key,
            encryption_iv=iv,
            file_hashes=(types.FileHash(offset=0, limit=len(plaintext), hash=hashlib.sha256(plaintext).digest()),),
        )
        client._sender = cast(Any, Sender(lambda request: redirect))
        cdn, other_cdn = Sender(), Sender()
        client._cdn_senders = {4: cast(Any, cdn), 5: cast(Any, other_cdn)}
        location = types.InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"synthetic", thumb_size="")
        async with AsyncExitStack() as stack:
            contexts = [
                await stack.enter_async_context(_MediaInvokeContext(client, 0, kind="download", dc_id=2, total_size=len(plaintext)))
                for _ in range(3)
            ]  # fmt: skip

            async def fetch(context: _MediaInvokeContext) -> bytes | None:
                result = await download_file(context, location, offset=1024, limit=1024, part_size=1024)
                return result.data

            first = asyncio.create_task(fetch(contexts[0]))
            request, first_reply = await asyncio.wait_for(cdn.calls.get(), 2)
            assert (request.offset, request.limit) == (0, 2 * UNIT)
            assert await attempts.get() == 2 * UNIT
            second = asyncio.create_task(fetch(contexts[1]))
            assert await asyncio.wait_for(attempts.get(), 2) == 2 * UNIT
            assert cdn.calls.empty()
            assert snapshot(client).active_bytes == 2 * UNIT
            assert snapshot(client).queued_bytes == 2 * UNIT
            assert snapshot(client, 2).active_bytes == 0
            separate = asyncio.create_task(contexts[2].invoke_cdn(cdn_request(limit=2 * UNIT), dc_id=5))
            _, separate_reply = await asyncio.wait_for(other_cdn.calls.get(), 2)
            assert snapshot(client, 5).active_bytes == 2 * UNIT
            separate_reply.set_result(types.UploadCdnFile(bytes=b"other DC"))
            await separate
            first_reply.set_result(types.UploadCdnFile(bytes=ciphertext))
            assert await first == plaintext[1024:2048]
            _, second_reply = await asyncio.wait_for(cdn.calls.get(), 2)
            second_reply.set_result(types.UploadCdnFile(bytes=ciphertext))
            assert await second == plaintext[1024:2048]
            assert snapshot(client).active_bytes == 0
        assert client._media_schedulers.scheduler_count == 0

    asyncio.run(scenario())


@pytest.mark.parametrize("total_size", [1024, None, 20 * 1024 * 1024])
def test_cdn_operation_limits_count_transfers_and_preserve_size_class(monkeypatch: pytest.MonkeyPatch, total_size: int | None) -> None:  # fmt: skip
    async def scenario() -> None:
        attempts = watch_cdn_acquires(monkeypatch)
        client = make_client(budget=6 * UNIT, small_limit=1, large_limit=1)
        sender = Sender()
        client._cdn_senders[4] = cast(Any, sender)
        other_size = None if total_size == 1024 else 1024
        async with AsyncExitStack() as stack:
            first, competing, other_class = [
                await stack.enter_async_context(_MediaInvokeContext(client, 0, kind="download", dc_id=2, total_size=size))
                for size in (total_size, total_size, other_size)
            ]  # fmt: skip
            tasks = [asyncio.create_task(first.invoke_cdn(cdn_request(offset), dc_id=4)) for offset in (0, 4096)]
            replies = [(await asyncio.wait_for(sender.calls.get(), 2))[1] for _ in tasks]
            assert [await attempts.get() for _ in tasks] == [UNIT, UNIT]
            waiting = asyncio.create_task(competing.invoke_cdn(cdn_request(8192), dc_id=4))
            await asyncio.wait_for(attempts.get(), 2)
            assert sender.calls.empty()
            assert snapshot(client).active_transfers == 1
            assert snapshot(client).active_bytes == 2 * UNIT
            independent = asyncio.create_task(other_class.invoke_cdn(cdn_request(12288), dc_id=4))
            _, independent_reply = await asyncio.wait_for(sender.calls.get(), 2)
            assert snapshot(client).active_transfers == 2
            replies[0].set_result(types.UploadCdnFile(bytes=b"first part"))
            await tasks[0]
            assert sender.calls.empty()
            replies[1].set_result(types.UploadCdnFile(bytes=b"second part"))
            await tasks[1]
            request, waiting_reply = await asyncio.wait_for(sender.calls.get(), 2)
            assert request.offset == 8192
            waiting_reply.set_result(types.UploadCdnFile(bytes=b"next transfer"))
            independent_reply.set_result(types.UploadCdnFile(bytes=b"other size"))
            await asyncio.gather(waiting, independent)
        assert client._media_schedulers.scheduler_count == 0

    asyncio.run(scenario())


@pytest.mark.parametrize("outcome", ["cancel", "rpc_error", "decode_error"])
def test_cdn_live_permits_release_on_cancellation_and_errors(outcome: str) -> None:
    async def scenario() -> None:
        client = make_client(budget=UNIT)
        sender = Sender()
        client._cdn_senders[4] = cast(Any, sender)
        async with _MediaInvokeContext(client, 0, kind="download", dc_id=2) as context:
            task = asyncio.create_task(context.invoke_cdn(cdn_request(), dc_id=4, retry=False))
            _, reply = await asyncio.wait_for(sender.calls.get(), 2)
            assert snapshot(client).active_bytes == UNIT
            if outcome == "cancel":
                task.cancel()
                expected = asyncio.CancelledError
            elif outcome == "rpc_error":
                reply.set_result(types.Error(code=400, text="SYNTHETIC_FAILURE"))
                expected = BadRequest
            else:
                reply.set_result(b"bad")
                expected = ValueError
            with pytest.raises(expected):
                await task
            assert snapshot(client).active_bytes == 0
            assert snapshot(client).active_transfers == 0
            next_task = asyncio.create_task(context.invoke_cdn(cdn_request(), dc_id=4))
            _, next_reply = await asyncio.wait_for(sender.calls.get(), 2)
            next_reply.set_result(types.UploadCdnFile(bytes=b"capacity reused"))
            await next_task
        assert client._media_schedulers.scheduler_count == 0
        with pytest.raises(RuntimeError, match="closed"):
            await context.invoke_cdn(cdn_request(), dc_id=4)

    asyncio.run(scenario())


@pytest.mark.parametrize("close_context", [False, True])
def test_cdn_queued_requests_cancel_without_dispatch_or_retained_capacity(monkeypatch: pytest.MonkeyPatch, close_context: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        attempts = watch_cdn_acquires(monkeypatch)
        client = make_client(budget=UNIT)
        sender = Sender()
        client._cdn_senders[4] = cast(Any, sender)
        async with (
            _MediaInvokeContext(client, 0, kind="download", dc_id=2) as active,
            _MediaInvokeContext(client, 0, kind="download", dc_id=2) as queued,
        ):
            first = asyncio.create_task(active.invoke_cdn(cdn_request(), dc_id=4))
            _, reply = await asyncio.wait_for(sender.calls.get(), 2)
            await attempts.get()
            waiting = asyncio.create_task(queued.invoke_cdn(cdn_request(), dc_id=4))
            await asyncio.wait_for(attempts.get(), 2)
            assert snapshot(client).queued_bytes == UNIT
            if close_context:
                await queued.__aexit__(None, None, None)
            else:
                waiting.cancel()
            with pytest.raises(asyncio.CancelledError):
                await waiting
            assert snapshot(client).queued_bytes == 0
            assert sender.calls.empty()
            assert snapshot(client).active_bytes == UNIT
            reply.set_result(types.UploadCdnFile(bytes=b"active request"))
            await first
        assert client._media_schedulers.scheduler_count == 0

    asyncio.run(scenario())


def test_cdn_flood_sleep_releases_capacity_and_retry_reacquires(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        attempts = watch_cdn_acquires(monkeypatch)
        client = make_client(budget=UNIT)
        now = [0.0]
        client._method_flood_wait_cache = MethodFloodWaitCache(8, clock=lambda: now[0])
        sleeping, wake = asyncio.Event(), asyncio.Event()

        async def sleep(seconds: float) -> None:
            assert seconds == 1
            assert snapshot(client).active_bytes == 0
            sleeping.set()
            await wake.wait()
            now[0] += seconds

        monkeypatch.setattr(client_module.asyncio, "sleep", sleep)
        sender = Sender()
        client._cdn_senders[4] = cast(Any, sender)
        async with _MediaInvokeContext(client, 0, kind="download", dc_id=2) as context:
            task = asyncio.create_task(context.invoke_cdn(cdn_request(), dc_id=4, flood_sleep_threshold=1))
            _, first_reply = await asyncio.wait_for(sender.calls.get(), 2)
            await attempts.get()
            first_reply.set_result(types.Error(code=420, text="FLOOD_WAIT_1"))
            await asyncio.wait_for(sleeping.wait(), 2)
            competing = client._media_schedulers.open_transfer(dc_id=4, direction="download", total_size=1024)
            permit = await asyncio.wait_for(competing.acquire(UNIT), 2)
            await attempts.get()
            wake.set()
            await asyncio.wait_for(attempts.get(), 2)
            assert sender.calls.empty()
            assert snapshot(client).queued_bytes == UNIT
            permit.release()
            _, second_reply = await asyncio.wait_for(sender.calls.get(), 2)
            assert snapshot(client).active_bytes == UNIT
            second_reply.set_result(types.UploadCdnFile(bytes=b"retry"))
            await task
            await competing.close()
        assert client._media_schedulers.scheduler_count == 0

    asyncio.run(scenario())


def test_cdn_inherits_registered_transfer_priority(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        attempts = watch_cdn_acquires(monkeypatch)
        client = make_client(budget=UNIT)
        sender = Sender()
        client._cdn_senders[4] = cast(Any, sender)
        blocker = client._media_schedulers.open_transfer(dc_id=4, direction="download", total_size=1024)
        permit = await blocker.acquire(UNIT)
        await attempts.get()
        async with AsyncExitStack() as stack:
            background = await stack.enter_async_context(_MediaInvokeContext(client, 0, kind="download", dc_id=2, defer_transfer=True))  # fmt: skip
            foreground = await stack.enter_async_context(_MediaInvokeContext(client, 0, kind="download", dc_id=2, total_size=1024))  # fmt: skip
            await background.register_transfer(1024, priority="background")
            background_task = asyncio.create_task(background.invoke_cdn(cdn_request(4096), dc_id=4))
            await asyncio.wait_for(attempts.get(), 2)
            foreground_task = asyncio.create_task(foreground.invoke_cdn(cdn_request(8192), dc_id=4))
            await asyncio.wait_for(attempts.get(), 2)
            assert snapshot(client).queued_bytes == 2 * UNIT
            permit.release()
            request, reply = await asyncio.wait_for(sender.calls.get(), 2)
            assert request.offset == 8192
            reply.set_result(types.UploadCdnFile(bytes=b"foreground"))
            await foreground_task
            request, reply = await asyncio.wait_for(sender.calls.get(), 2)
            assert request.offset == 4096
            reply.set_result(types.UploadCdnFile(bytes=b"background"))
            await background_task
            await blocker.close()
        assert client._media_schedulers.scheduler_count == 0

    asyncio.run(scenario())


def test_cdn_hash_and_reupload_requests_keep_origin_route_with_same_dc_budget() -> None:
    async def scenario() -> None:
        client = make_client(budget=UNIT)
        plaintext = b"synthetic CDN file"
        key, iv = bytes(range(32)), bytes(range(12)) + b"\0" * 4
        file_hash = types.FileHash(offset=0, limit=len(plaintext), hash=hashlib.sha256(plaintext).digest())
        origin_requests: list[str] = []
        cdn_requests: list[str] = []

        def origin(request: Any) -> object:
            origin_requests.append(type(request).QUALNAME)
            assert snapshot(client).active_bytes == UNIT
            assert snapshot(client).active_transfers == 1
            if isinstance(request, functions.UploadGetFile):
                return types.UploadFileCdnRedirect(dc_id=4, file_token=b"synthetic", encryption_key=key, encryption_iv=iv, file_hashes=())  # fmt: skip
            assert isinstance(request, functions.UploadGetCdnFileHashes | functions.UploadReuploadCdnFile)
            return (file_hash,)

        def cdn(request: Any) -> object:
            cdn_requests.append(type(request).QUALNAME)
            assert isinstance(request, functions.UploadGetCdnFile)
            assert snapshot(client).active_bytes == UNIT
            assert snapshot(client).active_transfers == 1
            if len(cdn_requests) == 1:
                return types.UploadCdnFileReuploadNeeded(request_token=b"synthetic reupload")
            return types.UploadCdnFile(bytes=media_ctr_crypt(plaintext, key, iv))

        client._sender = cast(Any, Sender(origin))
        client._cdn_senders[4] = cast(Any, Sender(cdn))
        async with _MediaInvokeContext(client, 0, kind="download", dc_id=4, total_size=len(plaintext)) as context:
            location = types.InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"synthetic", thumb_size="")
            result = await asyncio.wait_for(download_file(context, location, part_size=1024), 2)
            assert result.data == plaintext
            assert origin_requests == ["upload.getFile", "upload.getCdnFileHashes", "upload.reuploadCdnFile"]
            assert cdn_requests == ["upload.getCdnFile", "upload.getCdnFile"]
        assert client._media_schedulers.scheduler_count == 0

    asyncio.run(scenario())
