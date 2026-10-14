from __future__ import annotations

import asyncio
import io
import logging
import tempfile
import threading
from collections.abc import Mapping
from itertools import pairwise
from pathlib import Path
from typing import Any, BinaryIO, cast

import pytest

import miniproto.client as client_module
from miniproto import Client, ClientConfig, InMemorySessionStorage
from miniproto.media import MediaDownloadResult
from miniproto.media import download as media_download
from miniproto.media.multi_session import MIB, assemble_download_parts, download_session_count, plan_download_ranges
from miniproto.raw import functions, types


def multi_session_clients(monkeypatch: pytest.MonkeyPatch) -> tuple[Client, Client]:
    primary = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
    auxiliary = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()), _updates_enabled=False)  # fmt: skip
    auxiliary._connected = True
    primary._auxiliary_download_clients[1] = auxiliary

    async def available_clients(session_count: int) -> tuple[Client, ...]:
        assert session_count == 2
        return (auxiliary,)

    monkeypatch.setattr(primary, "_ensure_auxiliary_download_clients", available_clients)
    return primary, auxiliary


def download_location() -> object:
    return types.InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"reference", thumb_size="")


@pytest.mark.parametrize(
    ("size", "expected"),
    [(1, 1), (50 * MIB, 1), (50 * MIB + 1, 2), (250 * MIB, 2), (250 * MIB + 1, 4), (2_000 * MIB, 4)],
)
def test_download_session_count_uses_benchmarked_thresholds(size: int, expected: int) -> None:
    assert download_session_count(size) == expected


def test_plan_download_ranges_is_contiguous_aligned_and_complete() -> None:
    total = 503 * MIB + 123
    ranges = plan_download_ranges(total, session_count=4)
    assert len(ranges) == 4
    assert ranges[0].offset == 0
    assert all(item.offset % MIB == 0 for item in ranges)
    assert all(item.limit % MIB == 0 for item in ranges[:-1])
    assert all(left.offset + left.limit == right.offset for left, right in pairwise(ranges))
    assert ranges[-1].offset + ranges[-1].limit == total


@pytest.mark.parametrize(("total", "sessions"), [(0, 1), (1, 0)])
def test_plan_download_ranges_rejects_invalid_values(total: int, sessions: int) -> None:
    with pytest.raises(ValueError):
        plan_download_ranges(total, session_count=sessions)


def test_assemble_download_parts_returns_bytes_in_range_order(tmp_path) -> None:
    parts = (tmp_path / "part-0", tmp_path / "part-1")
    parts[0].write_bytes(b"abc")
    parts[1].write_bytes(b"def")
    destination, data = assemble_download_parts(parts, None, expected_size=6)
    assert destination is None
    assert data == b"abcdef"


def test_assemble_download_parts_writes_destination_path(tmp_path) -> None:
    parts = (tmp_path / "part-0", tmp_path / "part-1")
    parts[0].write_bytes(b"abc")
    parts[1].write_bytes(b"def")
    target = tmp_path / "result.bin"
    destination, data = assemble_download_parts(parts, target, expected_size=6)
    assert destination == target
    assert data is None
    assert target.read_bytes() == b"abcdef"


def test_assemble_download_parts_preserves_existing_path_on_size_mismatch(tmp_path) -> None:
    first = tmp_path / "part-0.bin"
    second = tmp_path / "part-1.bin"
    first.write_bytes(b"abc")
    second.write_bytes(b"def")
    target = tmp_path / "result.bin"
    target.write_bytes(b"previous-good-result")

    with pytest.raises(RuntimeError, match="size mismatch"):
        assemble_download_parts((first, second), target, expected_size=7)

    assert target.read_bytes() == b"previous-good-result"


@pytest.mark.parametrize("accepted_bytes", [0, 2, None])
def test_assemble_download_parts_rejects_incomplete_destination_writes(tmp_path, accepted_bytes: int | None) -> None:
    class IncompleteWriter:
        def __init__(self) -> None:
            self.buffer = io.BytesIO()

        def write(self, payload: bytes) -> int | None:
            if accepted_bytes is None:
                return None
            return self.buffer.write(payload[:accepted_bytes])

    part = tmp_path / "part.bin"
    part.write_bytes(b"abcdefgh")
    destination = IncompleteWriter()
    with pytest.raises(RuntimeError, match="destination write"):
        assemble_download_parts((part,), cast(BinaryIO, destination), expected_size=8)
    assert not destination.buffer.closed
    expected = b"ab" if accepted_bytes == 2 else b""
    assert destination.buffer.getvalue() == expected


@pytest.mark.parametrize("failure_source", ["worker", "progress", "caller_cancel", "worker_cancel"])
@pytest.mark.parametrize("secondary_failure", [False, True])
def test_multi_session_failure_settles_workers_before_releasing_resources(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure_source: str, secondary_failure: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        primary, auxiliary = multi_session_clients(monkeypatch)
        auxiliary_started = asyncio.Event()
        cleanup_started = asyncio.Event()
        allow_cleanup = asyncio.Event()
        workers: list[asyncio.Task[Any]] = []
        paths: list[Path] = []
        cleanup_observations: list[tuple[bool, bool]] = []
        disconnect_observations: list[bool] = []
        primary_failure = RuntimeError("first download failure")
        original_disconnect = auxiliary.disconnect
        target = tmp_path / "result.bin"
        target.write_bytes(b"previous completed download")

        async def disconnect() -> None:
            disconnect_observations.append(all(worker.done() for worker in workers))
            await original_disconnect()
            raise OSError("secondary disconnect failure")

        def progress(_current: int, _total: int | None) -> None:
            raise primary_failure

        async def single(worker: Client, _media: object, destination: object, options: Mapping[str, Any]) -> MediaDownloadResult:  # fmt: skip
            task = asyncio.current_task()
            assert task is not None
            workers.append(task)
            assert isinstance(destination, Path)
            paths.append(destination)
            destination.write_bytes(b"partial")
            if worker is auxiliary:
                auxiliary_started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cleanup_started.set()
                    await allow_cleanup.wait()
                    cleanup_observations.append((destination.exists(), auxiliary.is_connected))
                    if secondary_failure:
                        raise ValueError("secondary worker cleanup failure")
            await auxiliary_started.wait()
            if failure_source == "progress":
                await options["progress"](7, options["limit"])
            if failure_source == "worker":
                raise primary_failure
            if failure_source == "worker_cancel":
                raise asyncio.CancelledError("worker cancelled first")
            await asyncio.Event().wait()
            raise AssertionError("a cancelled worker must not finish normally")

        monkeypatch.setattr(Client, "_download_media_single", single)
        monkeypatch.setattr(auxiliary, "disconnect", disconnect)
        operation = asyncio.create_task(primary._download_media_multi_session(download_location(), target, {"progress": progress}, total_size=2 * MIB, session_count=2))  # fmt: skip
        cleanup_waiter = asyncio.create_task(cleanup_started.wait())
        try:
            async with asyncio.timeout(5):
                await auxiliary_started.wait()
                if failure_source == "caller_cancel":
                    operation.cancel("caller cancelled first")
                await asyncio.wait((operation, cleanup_waiter), return_when=asyncio.FIRST_COMPLETED)
                assert cleanup_started.is_set(), "the sibling must be cancelled and joined before failure escapes"
                assert not operation.done(), "the caller must wait for sibling cleanup"
                assert all(path.parent.exists() for path in paths)
                assert auxiliary.is_connected
                operation.cancel("later cancellation during worker cleanup")
                await asyncio.sleep(0)
                allow_cleanup.set()
                if failure_source in {"worker", "progress"}:
                    with pytest.raises(RuntimeError) as caught:
                        await operation
                    assert caught.value is primary_failure
                else:
                    with pytest.raises(asyncio.CancelledError) as cancelled:
                        await operation
                    expected = "caller cancelled first" if failure_source == "caller_cancel" else "worker cancelled first"  # fmt: skip
                    assert cancelled.value.args == (expected,)
                assert cleanup_observations == [(True, True)]
                assert disconnect_observations == [True]
                assert all(worker.done() for worker in workers)
                assert all(not path.parent.exists() for path in paths)
                assert not auxiliary.is_connected
                assert primary._auxiliary_download_clients == {}
                assert target.read_bytes() == b"previous completed download"
        finally:
            allow_cleanup.set()
            for pending in (operation, cleanup_waiter, *workers):
                if not pending.done():
                    pending.cancel()
            await asyncio.gather(operation, cleanup_waiter, *workers, return_exceptions=True)
            await primary.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("failure_source", ["worker", "caller_cancel"])
def test_multi_session_failure_skips_progress_from_real_worker_cleanup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure_source: str) -> None:  # fmt: skip
    async def scenario() -> None:
        primary, auxiliary = multi_session_clients(monkeypatch)
        first_write_committed = asyncio.Event()
        second_request = asyncio.Event()
        callback_started = asyncio.Event()
        release_callback = asyncio.Event()
        first_error = RuntimeError("primary worker failed after the auxiliary write")
        worker_paths: list[Path] = []
        workers: list[asyncio.Task[Any]] = []
        writer_tasks: list[asyncio.Task[Any]] = []
        original_submit = media_download._ConcurrentDestinationWriter.submit
        target = tmp_path / "result.bin"
        target.write_bytes(b"previous completed download")

        def write_committed(acknowledgement: asyncio.Future[None]) -> None:
            acknowledgement.result()
            first_write_committed.set()

        async def submit(writer: media_download._ConcurrentDestinationWriter, offset: int, payload: bytes, *, wait_for_completion: bool = True) -> asyncio.Future[None]:  # fmt: skip
            acknowledgement = await original_submit(writer, offset, payload, wait_for_completion=wait_for_completion)
            writer_tasks.append(writer._worker)
            acknowledgement.add_done_callback(write_committed)
            return acknowledgement

        async def progress(_current: int, _total: int | None) -> None:
            callback_started.set()
            await release_callback.wait()

        async def invoke(request: object, **_kwargs: object) -> object:
            assert isinstance(request, functions.UploadGetFile)
            if request.offset == 2 * MIB:
                return types.upload.File(type=types.storage.FileUnknown(), mtime=0, bytes=b"a" * MIB)
            assert request.offset == 3 * MIB
            await first_write_committed.wait()
            second_request.set()
            await asyncio.Future()
            raise AssertionError("the pending request must be cancelled")

        async def single(worker: Client, media: object, destination: object, options: Mapping[str, Any]) -> MediaDownloadResult:  # fmt: skip
            task = asyncio.current_task()
            assert task is not None
            workers.append(task)
            assert isinstance(destination, Path)
            worker_paths.append(destination)
            if worker is primary:
                await second_request.wait()
                if failure_source == "worker":
                    raise first_error
                await asyncio.Future()
                raise AssertionError("the primary worker must be cancelled")
            return await media_download.download_file(invoke, media, destination, offset=options["offset"], limit=options["limit"], part_size=MIB, concurrency=1, launch_stagger=False, adaptive_part_size=False, progress=options["progress"])  # fmt: skip

        monkeypatch.setattr(Client, "_download_media_single", single)
        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "submit", submit)
        operation = asyncio.create_task(primary._download_media_multi_session(download_location(), target, {"progress": progress}, total_size=4 * MIB, session_count=2))  # fmt: skip
        callback_waiter = asyncio.create_task(callback_started.wait())
        try:
            async with asyncio.timeout(5):
                await second_request.wait()
                assert not callback_started.is_set()
                if failure_source == "caller_cancel":
                    operation.cancel("caller cancelled after the auxiliary write")
                await asyncio.wait((operation, callback_waiter), return_when=asyncio.FIRST_COMPLETED)
                assert not callback_started.is_set(), "worker cleanup must not start a new user progress callback"
                if failure_source == "worker":
                    with pytest.raises(RuntimeError) as caught:
                        await operation
                    assert caught.value is first_error
                else:
                    with pytest.raises(asyncio.CancelledError) as cancelled:
                        await operation
                    assert cancelled.value.args == ("caller cancelled after the auxiliary write",)
                assert all(task.done() for task in (*workers, *writer_tasks))
                assert all(not path.parent.exists() for path in worker_paths)
                assert not auxiliary.is_connected
                assert target.read_bytes() == b"previous completed download"
        finally:
            release_callback.set()
            callback_waiter.cancel()
            await asyncio.gather(operation, callback_waiter, return_exceptions=True)
            await primary.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("worker_cleanup_failure", [False, True])
def test_multi_session_cancellation_consumes_worker_group_errors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, worker_cleanup_failure: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        primary, auxiliary = multi_session_clients(monkeypatch)
        started = {primary: asyncio.Event(), auxiliary: asyncio.Event()}
        cleanup_started = asyncio.Event()
        release_cleanup = asyncio.Event()
        workers: list[asyncio.Task[Any]] = []
        loop_errors: list[dict[str, Any]] = []
        loop = asyncio.get_running_loop()
        previous_handler = loop.get_exception_handler()
        loop.set_exception_handler(lambda _loop, context: loop_errors.append(context))

        async def single(worker: Client, _media: object, destination: object, _options: Mapping[str, Any]) -> MediaDownloadResult:  # fmt: skip
            task = asyncio.current_task()
            assert task is not None
            workers.append(task)
            assert isinstance(destination, Path)
            destination.write_bytes(b"partial")
            started[worker].set()
            try:
                await asyncio.Future()
                raise AssertionError("workers must be cancelled")
            finally:
                if worker is auxiliary:
                    cleanup_started.set()
                    await release_cleanup.wait()
                elif worker_cleanup_failure:
                    raise RuntimeError("worker failed while cancellation was settling")

        monkeypatch.setattr(Client, "_download_media_single", single)
        operation = asyncio.create_task(primary._download_media_multi_session(download_location(), tmp_path / "result.bin", {}, total_size=2 * MIB, session_count=2))  # fmt: skip
        try:
            async with asyncio.timeout(5):
                await asyncio.gather(*(event.wait() for event in started.values()))
                operation.cancel("original caller cancellation")
                await cleanup_started.wait()
                operation.cancel("later cancellation during settlement")
                await asyncio.sleep(0)
                release_cleanup.set()
                with pytest.raises(asyncio.CancelledError) as cancelled:
                    await operation
                assert cancelled.value.args == ("original caller cancellation",)
                assert all(task.done() for task in workers)
                assert not auxiliary.is_connected
                assert loop_errors == []
        finally:
            release_cleanup.set()
            await asyncio.gather(operation, return_exceptions=True)
            await primary.disconnect()
            loop.set_exception_handler(previous_handler)

    asyncio.run(scenario())


@pytest.mark.parametrize("cleanup_logging_failure", [False, True])
def test_multi_session_cancellation_waits_for_auxiliary_disconnect(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cleanup_logging_failure: bool) -> None:  # fmt: skip
    class FailingDisconnectLog(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            if cleanup_logging_failure and record.msg == "client.download_media.auxiliary_disconnect_failed":
                raise RuntimeError("caller logging handler failed during cleanup")

    async def scenario() -> None:
        primary, auxiliary = multi_session_clients(monkeypatch)
        disconnect_started = asyncio.Event()
        allow_disconnect = asyncio.Event()
        disconnected = asyncio.Event()
        original_disconnect = auxiliary.disconnect
        loop = asyncio.get_running_loop()
        loop_errors: list[dict[str, Any]] = []
        previous_handler = loop.get_exception_handler()
        loop.set_exception_handler(lambda _loop, context: loop_errors.append(context))
        failing_log = FailingDisconnectLog()
        client_module._LOGGER.addHandler(failing_log)

        async def single(_worker: Client, _media: object, destination: object, options: Mapping[str, Any]) -> MediaDownloadResult:  # fmt: skip
            assert isinstance(destination, Path)
            destination.write_bytes(b"x" * options["limit"])
            return MediaDownloadResult(bytes_downloaded=options["limit"], offset=options["offset"], destination=destination)  # fmt: skip

        async def disconnect() -> None:
            disconnect_started.set()
            await allow_disconnect.wait()
            await original_disconnect()
            disconnected.set()
            raise OSError("disconnect failed after closing")

        monkeypatch.setattr(Client, "_download_media_single", single)
        monkeypatch.setattr(auxiliary, "disconnect", disconnect)
        operation = asyncio.create_task(primary._download_media_multi_session(download_location(), tmp_path / "result.bin", {}, total_size=2 * MIB, session_count=2))  # fmt: skip
        try:
            async with asyncio.timeout(5):
                await disconnect_started.wait()
                operation.cancel("first cancellation during disconnect")
                await asyncio.sleep(0)
                operation.cancel("second cancellation during disconnect")
                await asyncio.sleep(0)
                allow_disconnect.set()
                with pytest.raises(asyncio.CancelledError) as cancelled:
                    await operation
                assert cancelled.value.args == ("first cancellation during disconnect",)
                assert disconnected.is_set()
                assert not auxiliary.is_connected
                assert loop_errors == []
        finally:
            allow_disconnect.set()
            await asyncio.gather(operation, return_exceptions=True)
            await primary.disconnect()
            client_module._LOGGER.removeHandler(failing_log)
            loop.set_exception_handler(previous_handler)

    asyncio.run(scenario())


@pytest.mark.parametrize("disconnect_failure", [False, True])
def test_multi_session_success_assembles_range_order_after_reverse_completion(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, disconnect_failure: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        primary, auxiliary = multi_session_clients(monkeypatch)
        auxiliary_finished = asyncio.Event()
        completion_order: list[int] = []
        progress_updates: list[tuple[int, int]] = []
        paths: list[Path] = []
        original_disconnect = auxiliary.disconnect

        async def single(worker: Client, _media: object, destination: object, options: Mapping[str, Any]) -> MediaDownloadResult:  # fmt: skip
            assert isinstance(destination, Path)
            if worker is primary:
                await auxiliary_finished.wait()
            offset = options["offset"]
            size = options["limit"]
            destination.write_bytes((b"a" if worker is primary else b"z") * size)
            await options["progress"](size, size)
            paths.append(destination)
            completion_order.append(offset)
            if worker is auxiliary:
                auxiliary_finished.set()
            return MediaDownloadResult(bytes_downloaded=size, offset=offset, destination=destination)

        async def disconnect() -> None:
            assert completion_order == [MIB, 0]
            await original_disconnect()
            if disconnect_failure:
                raise OSError("disconnect failed after successful transfer")

        monkeypatch.setattr(Client, "_download_media_single", single)
        monkeypatch.setattr(auxiliary, "disconnect", disconnect)
        target = tmp_path / "result.bin"

        def progress(current: int, total: int) -> None:
            progress_updates.append((current, total))

        try:
            result = await primary._download_media_multi_session(download_location(), target, {"progress": progress}, total_size=2 * MIB + 3, session_count=2)  # fmt: skip
            assert result.destination == target
            assert result.bytes_downloaded == 2 * MIB + 3
            assert target.read_bytes() == b"a" * MIB + b"z" * (MIB + 3)
            assert progress_updates == [(MIB + 3, 2 * MIB + 3), (2 * MIB + 3, 2 * MIB + 3)]
            assert all(not path.parent.exists() for path in paths)
            assert not auxiliary.is_connected
        finally:
            await primary.disconnect()

    asyncio.run(scenario())


@pytest.mark.parametrize("worker_failure", [False, True])
@pytest.mark.parametrize("cleanup_logging_failure", [False, True])
def test_multi_session_temporary_cleanup_preserves_the_first_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, worker_failure: bool, cleanup_logging_failure: bool) -> None:  # fmt: skip
    primary_error = RuntimeError("worker failed before cleanup")
    cleanup_error = OSError("temporary cleanup failed")

    class FailingCleanup(tempfile.TemporaryDirectory):
        def cleanup(self) -> None:
            super().cleanup()
            raise cleanup_error

    class FailingTemporaryCleanupLog(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            if cleanup_logging_failure and record.msg == "client.download_media.temporary_cleanup_failed":
                raise RuntimeError("caller logging handler failed during temporary cleanup")

    async def scenario() -> None:
        primary, auxiliary = multi_session_clients(monkeypatch)
        failing_log = FailingTemporaryCleanupLog()
        client_module._LOGGER.addHandler(failing_log)

        async def single(_worker: Client, _media: object, destination: object, options: Mapping[str, Any]) -> MediaDownloadResult:  # fmt: skip
            assert isinstance(destination, Path)
            destination.write_bytes(b"x" * options["limit"])
            if worker_failure:
                raise primary_error
            return MediaDownloadResult(bytes_downloaded=options["limit"], offset=options["offset"], destination=destination)  # fmt: skip

        monkeypatch.setattr(Client, "_download_media_single", single)
        monkeypatch.setattr(client_module.tempfile, "TemporaryDirectory", FailingCleanup)
        expected = primary_error if worker_failure else cleanup_error
        try:
            with pytest.raises(type(expected)) as caught:
                await primary._download_media_multi_session(download_location(), tmp_path / "result.bin", {}, total_size=2 * MIB, session_count=2)  # fmt: skip
            assert caught.value is expected
            assert not auxiliary.is_connected
        finally:
            await primary.disconnect()
            client_module._LOGGER.removeHandler(failing_log)

    asyncio.run(scenario())


@pytest.mark.parametrize("assembly_failure", [False, True])
def test_multi_session_cancellation_joins_assembly_before_removing_parts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, assembly_failure: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        primary, auxiliary = multi_session_clients(monkeypatch)
        assembly_started = asyncio.Event()
        allow_assembly = threading.Event()
        assembly_finished = asyncio.Event()
        loop = asyncio.get_running_loop()
        loop_errors: list[dict[str, Any]] = []
        previous_handler = loop.get_exception_handler()
        loop.set_exception_handler(lambda _loop, context: loop_errors.append(context))
        source_observations: list[bool] = []
        disconnect_observations: list[bool] = []
        original_disconnect = auxiliary.disconnect

        async def single(_worker: Client, _media: object, destination: object, options: Mapping[str, Any]) -> MediaDownloadResult:  # fmt: skip
            assert isinstance(destination, Path)
            destination.write_bytes(b"x" * options["limit"])
            return MediaDownloadResult(bytes_downloaded=options["limit"], offset=options["offset"], destination=destination)  # fmt: skip

        def assemble(parts: tuple[Path, ...], destination: Path, *, expected_size: int) -> tuple[Path | BinaryIO | None, bytes | None]:  # fmt: skip
            loop.call_soon_threadsafe(assembly_started.set)
            try:
                assert allow_assembly.wait(timeout=5)
                source_observations.append(all(part.exists() for part in parts))
                if assembly_failure:
                    raise OSError("assembly failed after caller cancellation")
                return assemble_download_parts(parts, destination, expected_size=expected_size)
            finally:
                loop.call_soon_threadsafe(assembly_finished.set)

        async def disconnect() -> None:
            disconnect_observations.append(assembly_finished.is_set())
            await original_disconnect()

        monkeypatch.setattr(Client, "_download_media_single", single)
        monkeypatch.setattr(client_module, "assemble_download_parts", assemble)
        monkeypatch.setattr(auxiliary, "disconnect", disconnect)
        operation = asyncio.create_task(primary._download_media_multi_session(download_location(), tmp_path / "result.bin", {}, total_size=2 * MIB, session_count=2))  # fmt: skip
        try:
            async with asyncio.timeout(5):
                await assembly_started.wait()
                operation.cancel("cancel during assembly")
                await asyncio.sleep(0)
                operation.cancel("cancel again during assembly")
                await asyncio.sleep(0)
                allow_assembly.set()
                with pytest.raises(asyncio.CancelledError) as cancelled:
                    await operation
                assert cancelled.value.args == ("cancel during assembly",)
                await assembly_finished.wait()
                assert source_observations == [True]
                assert disconnect_observations == [True]
                assert loop_errors == []
        finally:
            allow_assembly.set()
            await asyncio.gather(operation, return_exceptions=True)
            await assembly_finished.wait()
            await primary.disconnect()
            loop.set_exception_handler(previous_handler)

    asyncio.run(scenario())
