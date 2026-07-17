from __future__ import annotations

import asyncio
import hashlib
import io
import logging
import random
import threading
import time
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, cast

import pytest

import miniproto.client as client_module
import miniproto.media.download as media_download
from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    Media,
    SessionRecord,
    UserIdentity,
    encode_file_id,
    event_loop,
)
from miniproto.errors import (
    BadRequest,
    ClientDisconnected,
    FloodPremiumWait,
    FloodWait,
    RpcError,
    TransportFlood,
    classify_rpc_error,
)
from miniproto.media import (
    CdnIntegrityError,
    DownloadRangeCache,
    MediaDownloadError,
    MediaDownloadResult,
    decrypt_cdn_chunk,
    download_file,
    download_media,
)
from miniproto.observability import InMemoryMetrics, get_metrics_sink, set_metrics_sink
from miniproto.raw import functions, types

AUTH_KEY = b"m" * 256
BOT_CREDENTIAL = "42:secret"


@dataclass(slots=True)
class FakeInvoker:
    responses: list[object]
    requests: list[Any] = field(default_factory=list)
    kwargs: list[dict[str, object]] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        self.requests.append(request)
        self.kwargs.append(dict(kwargs))
        if not self.responses:
            raise AssertionError("fake invoker has no queued response")
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


@dataclass(slots=True)
class OffsetInvoker:
    payload: bytes
    requests: list[Any] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        assert isinstance(request, functions.UploadGetFile)
        await asyncio.sleep(0)
        return upload_file_part(self.payload[request.offset : request.offset + request.limit])


@dataclass(slots=True)
class FlakyOffsetInvoker:
    payload: bytes
    fail_offsets: set[int]
    requests: list[Any] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        assert isinstance(request, functions.UploadGetFile)
        await asyncio.sleep(0)
        if request.offset in self.fail_offsets:
            self.fail_offsets.remove(request.offset)
            raise ClientDisconnected("sender disconnected")
        return upload_file_part(self.payload[request.offset : request.offset + request.limit])


@dataclass(slots=True)
class FloodingOffsetInvoker:
    payload: bytes
    flood_offsets: set[int]
    seconds: int = 0
    requests: list[Any] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        assert isinstance(request, functions.UploadGetFile)
        await asyncio.sleep(0)
        if request.offset in self.flood_offsets:
            self.flood_offsets.remove(request.offset)
            raise TransportFlood(self.seconds)
        return upload_file_part(self.payload[request.offset : request.offset + request.limit])


@dataclass(slots=True)
class SlowOffsetInvoker:
    payload: bytes
    requests: list[Any] = field(default_factory=list)
    active: int = 0
    max_active: int = 0

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        assert isinstance(request, functions.UploadGetFile)
        self.active += 1
        self.max_active = max(self.max_active, self.active)
        try:
            await asyncio.sleep(0.01)
            return upload_file_part(self.payload[request.offset : request.offset + request.limit])
        finally:
            self.active -= 1


@dataclass(slots=True)
class DelayedMapOffsetInvoker:
    responses: Mapping[int, bytes | BaseException]
    delays: dict[int, float] = field(default_factory=dict)
    requests: list[Any] = field(default_factory=list)
    cancelled_offsets: set[int] = field(default_factory=set)

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        assert isinstance(request, functions.UploadGetFile)
        try:
            await asyncio.sleep(self.delays.get(request.offset, 0.0))
        except asyncio.CancelledError:
            self.cancelled_offsets.add(request.offset)
            raise
        response = self.responses[request.offset]
        if isinstance(response, BaseException):
            raise response
        return upload_file_part(response)


@dataclass(slots=True)
class RefreshingOffsetInvoker:
    payload: bytes
    old_reference: bytes
    delay: float = 0.01
    requests: list[Any] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        assert isinstance(request, functions.UploadGetFile)
        await asyncio.sleep(self.delay)
        if getattr(request.location, "file_reference", b"") == self.old_reference:
            raise BadRequest("FILE_REFERENCE_EXPIRED")
        return upload_file_part(self.payload[request.offset : request.offset + request.limit])


@dataclass(slots=True)
class FakeSender:
    responses: list[object]
    requests: list[Any] = field(default_factory=list)
    is_connected: bool = True

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, retry_safe, request_timeout
        await asyncio.sleep(0)
        self.requests.append(body)
        if not self.responses:
            raise AssertionError("fake sender has no queued response")
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response

    async def disconnect(self) -> None:
        self.is_connected = False


class LifecycleTrackingSender:
    is_connected = True

    def __init__(self) -> None:
        self.disconnect_calls = 0

    async def disconnect(self) -> None:
        self.disconnect_calls += 1
        self.is_connected = False


def run(coro):
    return event_loop.run(coro)


def storage_with_auth() -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
        )
    )


def storage_with_identity(*, is_bot: bool) -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
            user=UserIdentity(id=42, is_bot=is_bot),
        )
    )


def inner_request(wrapped: object) -> object:
    if isinstance(wrapped, functions.InvokeWithoutUpdates):
        wrapped = wrapped.query
    if isinstance(wrapped, functions.InvokeWithLayer):
        assert isinstance(wrapped.query, functions.InitConnection)
        return wrapped.query.query
    return wrapped


def cdn_file_hash(payload: bytes, offset: int = 0) -> types.FileHash:
    return types.FileHash(offset=offset, limit=len(payload), hash=hashlib.sha256(payload).digest())


def document_location() -> types.InputDocumentFileLocation:
    return types.InputDocumentFileLocation(id=10, access_hash=20, file_reference=b"ref", thumb_size="")


def upload_file_part(payload: bytes) -> types.UploadFile:
    return types.UploadFile(type=types.StorageFileUnknown(), mtime=1_700_000_000, bytes=payload)


def test_download_file_returns_bytes_for_location() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([upload_file_part(b"abc")])
        result = await download_file(invoker, document_location(), part_size=1024)
        assert result.data == b"abc"
        assert result.bytes_downloaded == 3
        assert isinstance(invoker.requests[0], functions.UploadGetFile)
        assert invoker.requests[0].location == document_location()
        assert invoker.requests[0].offset == 0
        assert invoker.requests[0].limit == 1024

    run(scenario())


def test_download_file_writes_path_and_resumes(tmp_path) -> None:
    async def scenario() -> None:
        target = tmp_path / "download.bin"
        target.write_bytes(b"o" * 1024)
        progress: list[tuple[int, int | None]] = []
        invoker = FakeInvoker([upload_file_part(b"n" * 1024)])
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=2048,
            part_size=1024,
            resume=True,
            progress=lambda current, total: progress.append((current, total)),
        )
        assert target.read_bytes() == b"o" * 1024 + b"n" * 1024
        assert result.destination == target
        assert result.bytes_downloaded == 2048
        assert invoker.requests[0].offset == 1024
        assert invoker.requests[0].limit == 1024
        # 1 KiB granularity requires precise mode; it is switched on automatically.
        assert invoker.requests[0].precise is True
        assert progress == [(2048, 2048)]

    run(scenario())


def test_download_file_resume_realigns_unaligned_tail(tmp_path) -> None:
    async def scenario() -> None:
        target = tmp_path / "download.bin"
        target.write_bytes(b"x" * 1500)
        invoker = FakeInvoker([upload_file_part(b"n" * 1000)])
        result = await download_file(invoker, document_location(), target, part_size=1024, resume=True)
        # 1500 is not a legal Telegram offset; the partial tail past the last
        # 1 KiB boundary is dropped and re-downloaded instead of failing.
        assert invoker.requests[0].offset == 1024
        assert invoker.requests[0].limit == 1024
        assert target.read_bytes() == b"x" * 1024 + b"n" * 1000
        assert result.bytes_downloaded == 2024

    run(scenario())


def test_download_file_concurrent_writes_ordered_payload(tmp_path) -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 20  # 5 KiB
        target = tmp_path / "concurrent.bin"
        progress: list[tuple[int, int | None]] = []
        invoker = OffsetInvoker(payload)
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            concurrency=3,
            progress=lambda current, total: progress.append((current, total)),
        )
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        assert sorted(request.offset for request in invoker.requests) == [0, 1024, 2048, 3072, 4096]
        assert progress[-1] == (len(payload), len(payload))

    run(scenario())


@pytest.mark.parametrize("empty_offset", [0, 1024, 2048])
def test_download_file_concurrent_rejects_empty_expected_chunk(tmp_path, empty_offset) -> None:
    async def scenario() -> None:
        target = tmp_path / f"empty-{empty_offset}.bin"
        responses = {offset: bytes([offset // 1024 + 1]) * 1024 for offset in range(0, 3072, 1024)}
        responses[empty_offset] = b""
        invoker = DelayedMapOffsetInvoker(responses)
        with pytest.raises(MediaDownloadError, match=rf"offset {empty_offset}.*expected 1024.*received 0"):
            await download_file(
                invoker,
                document_location(),
                target,
                limit=3072,
                part_size=1024,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=3,
            )
        assert not target.exists()

    run(scenario())


@pytest.mark.parametrize(
    ("short_offset", "limit", "expected", "received"),
    [(0, 3072, 1024, 1000), (1024, 3072, 1024, 1000), (2048, 2500, 452, 451)],
)
def test_download_file_concurrent_rejects_short_expected_chunk(
    tmp_path, short_offset, limit, expected, received
) -> None:
    async def scenario() -> None:
        target = tmp_path / f"short-{short_offset}.bin"
        responses = {0: b"a" * 1024, 1024: b"b" * 1024, 2048: b"c" * 1024}
        responses[short_offset] = b"x" * received
        invoker = DelayedMapOffsetInvoker(responses)
        with pytest.raises(
            MediaDownloadError, match=rf"offset {short_offset}.*expected {expected}.*received {received}"
        ):
            await download_file(
                invoker,
                document_location(),
                target,
                limit=limit,
                part_size=1024,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=3,
            )
        assert not target.exists()

    run(scenario())


def test_download_file_concurrent_preserves_legal_aligned_tail_overread() -> None:
    async def scenario() -> None:
        expected = b"a" * 1024 + b"b" * 1024 + b"c" * 452
        invoker = DelayedMapOffsetInvoker({0: b"a" * 1024, 1024: b"b" * 1024, 2048: b"c" * 1024})
        result = await download_file(
            invoker,
            document_location(),
            limit=len(expected),
            part_size=1024,
            adaptive_part_size=False,
            adaptive_concurrency=False,
            concurrency=3,
        )
        assert result.data == expected
        assert result.bytes_downloaded == len(expected)

    run(scenario())


def test_download_file_concurrent_cancels_delayed_later_chunks_after_middle_hole(tmp_path) -> None:
    async def scenario() -> None:
        target = tmp_path / "middle-hole.bin"
        invoker = DelayedMapOffsetInvoker(
            {0: b"a" * 1024, 1024: b"", 2048: b"c" * 1024}, delays={0: 0.4, 1024: 0.2, 2048: 5.0}
        )
        with pytest.raises(MediaDownloadError, match=r"offset 1024.*received 0"):
            await download_file(
                invoker,
                document_location(),
                target,
                limit=3072,
                part_size=1024,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=3,
            )
        assert 2048 in invoker.cancelled_offsets
        assert not target.exists()

    run(scenario())


def test_download_file_concurrent_failure_restores_resumed_prefix(tmp_path) -> None:
    async def scenario() -> None:
        target = tmp_path / "resume-partial.bin"
        prefix = b"v" * 1024
        target.write_bytes(prefix)
        invoker = DelayedMapOffsetInvoker({1024: b"n" * 1024, 2048: b"x" * 1000}, delays={1024: 0.0, 2048: 0.15})
        with pytest.raises(MediaDownloadError, match=r"offset 2048.*expected 1024.*received 1000"):
            await download_file(
                invoker,
                document_location(),
                target,
                limit=3072,
                part_size=1024,
                resume=True,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=2,
            )
        assert target.read_bytes() == prefix

    run(scenario())


def test_download_file_concurrent_failure_discards_internal_memory_buffer(monkeypatch) -> None:
    async def scenario() -> None:
        opened: list[media_download._DestinationHandle] = []
        original_open_destination = media_download._open_destination

        def capture_destination(destination, *, resume):
            handle = original_open_destination(destination, resume=resume)
            opened.append(handle)
            return handle

        monkeypatch.setattr(media_download, "_open_destination", capture_destination)
        invoker = DelayedMapOffsetInvoker(
            {0: b"a" * 1024, 1024: b"", 2048: b"c" * 1024}, delays={0: 0.0, 1024: 0.15, 2048: 0.3}
        )
        with pytest.raises(MediaDownloadError, match=r"offset 1024.*received 0"):
            await download_file(
                invoker,
                document_location(),
                limit=3072,
                part_size=1024,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=3,
            )
        assert len(opened) == 1
        assert opened[0].get_data() == b""

    run(scenario())


def test_download_file_concurrent_failure_restores_caller_bytesio() -> None:
    async def scenario() -> None:
        original = b"caller-owned-memory"
        destination = io.BytesIO(original)
        destination.seek(7)
        invoker = DelayedMapOffsetInvoker(
            {0: b"a" * 1024, 1024: b"", 2048: b"c" * 1024}, delays={0: 0.0, 1024: 0.15, 2048: 0.3}
        )
        with pytest.raises(MediaDownloadError, match=r"offset 1024.*received 0"):
            await download_file(
                invoker,
                document_location(),
                destination,
                limit=3072,
                part_size=1024,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=3,
            )
        assert destination.getvalue() == original
        assert destination.tell() == 7

    run(scenario())


def test_download_file_concurrent_progress_waits_for_committed_writes(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        target = tmp_path / "committed-progress.bin"
        payload = b"a" * 1024 + b"b" * 1024
        original_write = media_download._ConcurrentDestinationWriter._write
        completed_writes: list[tuple[int, int]] = []

        def delayed_write(writer, offset, chunk):
            time.sleep(0.05)
            original_write(writer, offset, chunk)
            completed_writes.append((offset, len(chunk)))

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_write", delayed_write)
        observed: list[tuple[int, int]] = []

        def on_progress(current: int, total: int | None) -> None:
            del total
            observed.append((current, sum(length for _offset, length in completed_writes)))

        result = await download_file(
            DelayedMapOffsetInvoker({0: payload[:1024], 1024: payload[1024:]}, delays={0: 0.0, 1024: 0.2}),
            document_location(),
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            adaptive_concurrency=False,
            concurrency=2,
            progress=on_progress,
        )
        assert result.bytes_downloaded == len(payload)
        assert observed
        assert all(committed >= current for current, committed in observed)
        assert [current for current, _committed in observed].count(len(payload)) == 1

    run(scenario())


def test_download_file_concurrent_refills_network_while_disk_write_is_active(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        target = tmp_path / "network-write-overlap.bin"
        payload = b"a" * 1024 + b"b" * 1024 + b"c" * 1024
        third_requested = asyncio.Event()
        initial_requests_ready = asyncio.Event()
        release_initial_requests = asyncio.Event()
        initial_request_count = 0

        async def invoke(request: object, **kwargs: object) -> object:
            nonlocal initial_request_count
            del kwargs
            assert isinstance(request, functions.UploadGetFile)
            if request.offset == 2048:
                third_requested.set()
            else:
                initial_request_count += 1
                if initial_request_count == 2:
                    initial_requests_ready.set()
                await release_initial_requests.wait()
                if request.offset == 1024:
                    await asyncio.sleep(0.2)
            await asyncio.sleep(0)
            return upload_file_part(payload[request.offset : request.offset + request.limit])

        original_write = media_download._ConcurrentDestinationWriter._write
        write_started = threading.Event()
        release_write = threading.Event()

        def blocked_first_write(writer, offset, chunk):
            if offset == 0:
                write_started.set()
                assert release_write.wait(1.0)
            original_write(writer, offset, chunk)

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_write", blocked_first_write)
        download = asyncio.create_task(
            download_file(
                invoke,
                document_location(),
                target,
                limit=len(payload),
                part_size=1024,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=2,
            )
        )
        await asyncio.wait_for(initial_requests_ready.wait(), timeout=1.0)
        release_initial_requests.set()
        assert await asyncio.to_thread(write_started.wait, 1.0)
        try:
            try:
                await asyncio.wait_for(third_requested.wait(), timeout=0.5)
                overlapped = True
            except TimeoutError:
                overlapped = False
        finally:
            release_write.set()
        result = await asyncio.wait_for(download, timeout=1.0)
        assert overlapped
        assert result.bytes_downloaded == len(payload)
        assert target.read_bytes() == payload

    run(scenario())


def test_download_file_concurrent_progress_never_reports_target_on_failure(tmp_path) -> None:
    async def scenario() -> None:
        target = tmp_path / "failed-progress.bin"
        progress: list[tuple[int, int | None]] = []
        invoker = DelayedMapOffsetInvoker(
            {0: b"a" * 1024, 1024: b"x" * 1000, 2048: b"c" * 1024}, delays={0: 0.0, 1024: 0.15, 2048: 0.3}
        )
        with pytest.raises(MediaDownloadError):
            await download_file(
                invoker,
                document_location(),
                target,
                limit=3072,
                part_size=1024,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=3,
                progress=lambda current, total: progress.append((current, total)),
            )
        assert progress
        assert all(current < 3072 for current, _total in progress)
        assert (3072, 3072) not in progress

    run(scenario())


def test_download_file_concurrent_truncates_resume_already_beyond_limit(tmp_path) -> None:
    async def scenario() -> None:
        target = tmp_path / "resume-beyond-limit.bin"
        target.write_bytes(b"x" * 3072)
        invoker = OffsetInvoker(b"")
        progress: list[tuple[int, int | None]] = []
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=2048,
            part_size=1024,
            resume=True,
            adaptive_part_size=False,
            concurrency=2,
            progress=lambda current, total: progress.append((current, total)),
        )
        assert invoker.requests == []
        assert target.read_bytes() == b"x" * 2048
        assert result.bytes_downloaded == 2048
        assert progress == [(2048, 2048)]

    run(scenario())


def test_download_file_concurrent_preserves_exact_limit_prefix_if_flush_fails(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        target = tmp_path / "resume-beyond-limit-flush-error.bin"
        original = b"a" * 1024 + b"b" * 1024 + b"c" * 1024
        target.write_bytes(original)
        progress: list[tuple[int, int | None]] = []

        async def fail_flush(writer) -> None:
            del writer
            raise OSError("flush failed")

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_flush", fail_flush)
        with pytest.raises(OSError, match="flush failed"):
            await download_file(
                OffsetInvoker(b""),
                document_location(),
                target,
                limit=2048,
                part_size=1024,
                resume=True,
                adaptive_part_size=False,
                concurrency=2,
                progress=lambda current, total: progress.append((current, total)),
            )
        assert target.read_bytes() == original[:2048]
        assert all(current < 2048 for current, _total in progress)

    run(scenario())


def test_download_file_concurrent_does_not_report_target_if_flush_fails(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        part_size = 1024
        part_count = 9
        limit = part_size * part_count
        target = tmp_path / "flush-progress-error.bin"
        progress: list[tuple[int, int | None]] = []
        responses = {offset: bytes([offset // part_size]) * part_size for offset in range(0, limit, part_size)}

        async def fail_flush(writer) -> None:
            del writer
            raise OSError("flush failed")

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_flush", fail_flush)
        with pytest.raises(OSError, match="flush failed"):
            await download_file(
                DelayedMapOffsetInvoker(responses),
                document_location(),
                target,
                limit=limit,
                part_size=part_size,
                adaptive_part_size=False,
                adaptive_concurrency=False,
                concurrency=part_count,
                progress=lambda current, total: progress.append((current, total)),
            )
        assert progress
        assert all(current < limit for current, _total in progress)

    run(scenario())


def test_concurrent_destination_writer_fails_all_queued_acknowledgements(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        destination = media_download._open_destination(tmp_path / "writer-error.bin", resume=False)
        original_write = media_download._ConcurrentDestinationWriter._write

        def fail_first_write(writer, offset, payload):
            if offset == 0:
                time.sleep(0.05)
                raise OSError("disk full")
            original_write(writer, offset, payload)

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_write", fail_first_write)
        writer = media_download._ConcurrentDestinationWriter(destination, queue_size=1, preallocate_size=3072)
        submissions = [
            asyncio.create_task(writer.submit(offset, bytes([offset // 1024 + 1]) * 1024)) for offset in (0, 1024, 2048)
        ]
        results = await asyncio.wait_for(asyncio.gather(*submissions, return_exceptions=True), timeout=1.0)
        assert all(isinstance(result, OSError) for result in results)
        with pytest.raises(OSError, match="disk full"):
            await asyncio.wait_for(writer.close(), timeout=1.0)
        destination.handle.close()

    run(scenario())


def test_concurrent_destination_writer_abort_waits_for_active_threaded_write(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        destination = media_download._open_destination(tmp_path / "writer-abort.bin", resume=False)
        original_write = media_download._ConcurrentDestinationWriter._write
        started = threading.Event()
        finished = threading.Event()

        def delayed_write(writer, offset, payload):
            started.set()
            time.sleep(0.1)
            original_write(writer, offset, payload)
            finished.set()

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_write", delayed_write)
        writer = media_download._ConcurrentDestinationWriter(destination, queue_size=1, preallocate_size=1024)
        submission = asyncio.create_task(writer.submit(0, b"x" * 1024))
        assert await asyncio.to_thread(started.wait, 1.0)
        await asyncio.wait_for(writer.abort(), timeout=1.0)
        assert finished.is_set()
        await asyncio.gather(submission, return_exceptions=True)
        destination.handle.close()

    run(scenario())


def test_concurrent_destination_writer_preserves_bounded_queue_backpressure(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        destination = media_download._open_destination(tmp_path / "writer-bounded.bin", resume=False)
        original_write = media_download._ConcurrentDestinationWriter._write
        started = threading.Event()
        release = threading.Event()

        def blocked_write(writer, offset, payload):
            if offset == 0:
                started.set()
                assert release.wait(1.0)
            original_write(writer, offset, payload)

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_write", blocked_write)
        writer = media_download._ConcurrentDestinationWriter(destination, queue_size=1, preallocate_size=3072)
        await writer.submit(0, b"a" * 1024, wait_for_completion=False)
        assert await asyncio.to_thread(started.wait, 1.0)
        await writer.submit(1024, b"b" * 1024, wait_for_completion=False)
        third = asyncio.create_task(writer.submit(2048, b"c" * 1024, wait_for_completion=False))
        await asyncio.sleep(0)
        assert not third.done()
        release.set()
        await asyncio.wait_for(third, timeout=1.0)
        await asyncio.wait_for(writer.close(), timeout=1.0)
        destination.handle.close()

    run(scenario())


def test_download_file_concurrent_rejects_short_destination_write() -> None:
    class ShortWriteBuffer:
        def __init__(self) -> None:
            self.buffer = io.BytesIO()

        def seek(self, offset: int, whence: int = 0) -> int:
            return self.buffer.seek(offset, whence)

        def write(self, payload: bytes) -> int:
            return self.buffer.write(payload[:-1])

        def flush(self) -> None:
            self.buffer.flush()

    async def scenario() -> None:
        destination = ShortWriteBuffer()
        with pytest.raises(
            MediaDownloadError, match=r"destination write at offset 0 expected 1024 bytes but wrote 1023"
        ):
            await download_file(
                OffsetInvoker(b"x" * 1024),
                document_location(),
                cast(Any, destination),
                limit=1024,
                part_size=1024,
                adaptive_part_size=False,
                concurrency=2,
            )

    run(scenario())


def test_download_file_concurrent_cleans_new_path_when_preallocation_fails(tmp_path, monkeypatch) -> None:
    class FailingTruncate:
        def __init__(self, handle) -> None:
            self.handle = handle

        @property
        def closed(self) -> bool:
            return self.handle.closed

        def close(self) -> None:
            self.handle.close()

        def truncate(self, size: int | None = None) -> int:
            del size
            raise OSError("preallocation failed")

        def __getattr__(self, name: str):
            return getattr(self.handle, name)

    async def scenario() -> None:
        target = tmp_path / "preallocation-error.bin"
        raw_handle = target.open("w+b")
        failing_handle = FailingTruncate(raw_handle)

        def failing_destination(destination, *, resume):
            del destination, resume
            return media_download._DestinationHandle(
                handle=cast(Any, failing_handle),
                path=target,
                should_close=True,
                remove_on_cancel=True,
                discard_on_failure=False,
                existing_bytes=0,
                get_data=lambda: None,
            )

        monkeypatch.setattr(media_download, "_open_destination", failing_destination)
        with pytest.raises(OSError, match="preallocation failed"):
            await download_file(
                OffsetInvoker(b"x" * 1024),
                document_location(),
                target,
                limit=1024,
                part_size=1024,
                adaptive_part_size=False,
                concurrency=2,
            )
        assert failing_handle.closed
        assert not target.exists()

    run(scenario())


def test_interval_coverage_accepts_exact_target() -> None:
    coverage = media_download._IntervalCoverage(1024, 2048)
    assert coverage.add(1024, 2048) == 1024
    assert coverage.covered_bytes == 1024
    assert coverage.complete


def test_interval_coverage_merges_out_of_order_adjacency() -> None:
    coverage = media_download._IntervalCoverage(0, 3072)
    assert coverage.add(2048, 3072) == 1024
    assert coverage.add(0, 1024) == 1024
    assert not coverage.complete
    assert coverage.add(1024, 2048) == 1024
    assert coverage.complete


def test_interval_coverage_overlap_and_duplicate_do_not_inflate_coverage() -> None:
    coverage = media_download._IntervalCoverage(0, 3072)
    assert coverage.add(0, 2048) == 2048
    assert coverage.add(1024, 3072) == 1024
    assert coverage.add(0, 3072) == 0
    assert coverage.covered_bytes == 3072
    assert coverage.complete


def test_interval_coverage_detects_gap() -> None:
    coverage = media_download._IntervalCoverage(0, 3072)
    coverage.add(0, 1024)
    coverage.add(2048, 3072)
    assert coverage.covered_bytes == 2048
    assert coverage.contiguous_end == 1024
    assert not coverage.complete


def test_interval_coverage_rejects_overrun() -> None:
    coverage = media_download._IntervalCoverage(1024, 2048)
    with pytest.raises(ValueError, match="outside target"):
        coverage.add(1024, 3072)


def test_download_file_concurrent_respects_byte_window(tmp_path) -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 16  # 4 KiB
        target = tmp_path / "byte-window.bin"
        invoker = SlowOffsetInvoker(payload)
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            concurrency=4,
            max_in_flight_bytes=1024,
        )
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        assert invoker.max_active == 1
        assert [request.offset for request in invoker.requests] == [0, 1024, 2048, 3072]

    run(scenario())


def test_download_media_range_cache_reuses_miniproto_file_id() -> None:
    async def scenario() -> None:
        document = types.Document(
            id=11,
            access_hash=22,
            file_reference=b"ref",
            date=1_700_000_000,
            mime_type="application/octet-stream",
            size=3,
            dc_id=2,
            attributes=(types.DocumentAttributeFilename(file_name="remote.bin"),),
        )
        file_id = encode_file_id(document)
        cache = DownloadRangeCache(max_bytes=4096)
        first = FakeInvoker([upload_file_part(b"abc")])
        first_result = await download_media(first, file_id, limit=3, part_size=1024, range_cache=cache)
        assert first_result.data == b"abc"
        second = FakeInvoker([])
        second_result = await download_media(second, file_id, limit=3, part_size=1024, range_cache=cache)
        assert second_result.data == b"abc"
        assert len(first.requests) == 1
        assert second.requests == []

    run(scenario())


def test_download_file_read_ahead_prefetches_into_range_cache() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=8192)
        payload = b"a" * 1024 + b"d" * 1024
        invoker = OffsetInvoker(payload)
        result = await download_file(
            invoker,
            document_location(),
            limit=1024,
            part_size=1024,
            total_size=len(payload),
            range_cache=cache,
            range_cache_key="doc:10",
            read_ahead_bytes=1024,
        )
        assert result.data == b"a" * 1024
        cached = None
        for _ in range(50):
            cached = await cache.get("doc:10", 1024, 1024)
            if cached is not None:
                break
            await asyncio.sleep(0.01)
        assert [request.offset for request in invoker.requests] == [0, 1024]
        assert cached == b"d" * 1024

    run(scenario())


def test_download_file_deduplicates_file_reference_refresh(tmp_path) -> None:
    async def scenario() -> None:
        old_location = document_location()
        new_location = types.InputDocumentFileLocation(id=10, access_hash=20, file_reference=b"new-ref", thumb_size="")
        refresh_calls = 0

        async def refresher(location: object) -> object:
            nonlocal refresh_calls
            assert location == old_location
            refresh_calls += 1
            await asyncio.sleep(0.25)
            return new_location

        payload = bytes(range(256)) * 8  # 2 KiB
        target = tmp_path / "refreshed.bin"
        # The delay keeps both staggered launches in flight together so their
        # FILE_REFERENCE_EXPIRED failures overlap one shared refresh.
        invoker = RefreshingOffsetInvoker(payload, old_reference=b"ref", delay=0.25)
        result = await download_file(
            invoker,
            old_location,
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            concurrency=2,
            adaptive_concurrency=False,
            max_retries=0,
            file_reference_refresher=refresher,
        )
        assert target.read_bytes() == payload
        assert result.raw_location == new_location
        assert refresh_calls == 1
        assert [request.location.file_reference for request in invoker.requests].count(b"ref") == 2
        assert [request.location.file_reference for request in invoker.requests].count(b"new-ref") == 2

    run(scenario())


def test_download_file_retries_transient_get_file_failure() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([ClientDisconnected("sender disconnected"), upload_file_part(b"abc")])
        result = await download_file(invoker, document_location(), part_size=1024, request_timeout=3, max_retries=1)
        assert result.data == b"abc"
        assert len(invoker.requests) == 2
        assert invoker.kwargs == [
            {"request_timeout": 3, "retry": False, "flood_sleep_threshold": 0},
            {"request_timeout": 3, "retry": False, "flood_sleep_threshold": 0},
        ]

    run(scenario())


def test_download_file_retries_short_flood_wait_at_media_layer() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([TransportFlood(0), upload_file_part(b"abc")])
        result = await download_file(
            invoker, document_location(), part_size=1024, max_retries=1, flood_sleep_threshold=1
        )
        assert result.data == b"abc"
        assert len(invoker.requests) == 2
        assert invoker.kwargs == [
            {"request_timeout": None, "retry": False, "flood_sleep_threshold": 0},
            {"request_timeout": None, "retry": False, "flood_sleep_threshold": 0},
        ]

    run(scenario())


def test_download_file_does_not_retry_long_flood_wait() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([TransportFlood(2)])
        with pytest.raises(TransportFlood):
            await download_file(invoker, document_location(), part_size=1024, max_retries=2, flood_sleep_threshold=1)
        assert len(invoker.requests) == 1

    run(scenario())


def test_download_file_does_not_retry_non_transient_get_file_failure() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([BadRequest("FILE_REFERENCE_EXPIRED")])
        with pytest.raises(BadRequest):
            await download_file(invoker, document_location(), part_size=1024, max_retries=2)
        assert len(invoker.requests) == 1

    run(scenario())


def test_download_file_raises_on_empty_payload_before_explicit_limit_is_satisfied() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([upload_file_part(b"")])
        with pytest.raises(MediaDownloadError, match="empty payload"):
            await download_file(invoker, document_location(), part_size=1024, limit=1024, concurrency=1)

    run(scenario())


def test_download_file_concurrent_retries_transient_chunk_failure(tmp_path) -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 20  # 5 KiB
        target = tmp_path / "retry.bin"
        invoker = FlakyOffsetInvoker(payload, fail_offsets={2048})
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            concurrency=3,
            max_retries=1,
        )
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        offsets = [request.offset for request in invoker.requests]
        assert offsets.count(2048) == 2

    run(scenario())


def test_download_file_flood_wait_does_not_reduce_concurrency(tmp_path) -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 32  # 8 KiB
        target = tmp_path / "adaptive.bin"
        invoker = FloodingOffsetInvoker(payload, flood_offsets={0})
        metrics = InMemoryMetrics()
        set_metrics_sink(metrics)
        try:
            result = await download_file(
                invoker,
                document_location(),
                target,
                limit=len(payload),
                part_size=1024,
                adaptive_part_size=False,
                concurrency=4,
                max_retries=1,
                flood_sleep_threshold=1,
            )
        finally:
            set_metrics_sink(None)
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        # FLOOD_WAIT is per-request pacing: the flooded request just sleeps and
        # retries while the concurrency limit stays untouched.
        throttle_events = [event for event in metrics.events if event.name == "media.download.adaptive_throttle"]
        assert all(event.value >= 4 for event in throttle_events)

    run(scenario())


def test_download_file_floods_do_not_consume_the_transient_retry_budget(tmp_path) -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 8  # 2 KiB
        target = tmp_path / "flood-budget.bin"
        floods_remaining = [4]

        @dataclass(slots=True)
        class RepeatFloodInvoker:
            requests: list[Any] = field(default_factory=list)

            async def __call__(self, request: object, **kwargs: object) -> object:
                del kwargs
                self.requests.append(request)
                assert isinstance(request, functions.UploadGetFile)
                if request.offset == 0 and floods_remaining[0] > 0:
                    floods_remaining[0] -= 1
                    raise FloodWait(0)
                return upload_file_part(payload[request.offset : request.offset + request.limit])

        invoker = RepeatFloodInvoker()
        # 4 consecutive floods on one part with max_retries=1: floods are server
        # pacing and must not abort the transfer (they used to burn the retry
        # budget and kill 2000 MiB downloads mid-flight).
        await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            concurrency=2,
            adaptive_concurrency=False,
            max_retries=1,
            flood_sleep_threshold=30,
        )
        assert target.read_bytes() == payload
        assert floods_remaining[0] == 0
        assert [r.offset for r in invoker.requests].count(0) == 5

    run(scenario())


def test_adaptive_download_throttle_reduces_only_on_disconnects() -> None:
    async def scenario() -> None:
        clock_value = [0.0]

        def clock() -> float:
            return clock_value[0]

        throttle = media_download._AdaptiveDownloadThrottle(4, clock=clock)
        # No slow start: the delay-gate stagger handles burst protection.
        assert throttle.limit == 4
        # Floods never reduce the window (they only pause growth).
        await throttle.on_retry(FloodWait(1), 1)
        assert throttle.limit == 4
        # Disconnect-ish errors reduce by one with a cooldown.
        await throttle.on_retry(ClientDisconnected("sender disconnected"), 1)
        assert throttle.limit == 3
        for _ in range(20):
            throttle.on_success()
        assert throttle.limit == 3  # still cooling down
        clock_value[0] = 2.1
        for _ in range(7):
            throttle.on_success()
        assert throttle.limit == 3
        throttle.on_success()
        assert throttle.limit == 4

    run(scenario())


def test_adaptive_download_throttle_falls_back_to_single_slot_on_premium_flood() -> None:
    async def scenario() -> None:
        throttle = media_download._AdaptiveDownloadThrottle(4, clock=lambda: 100.0)
        assert throttle.limit == 4
        await throttle.on_retry(FloodPremiumWait(3), 1)
        assert throttle.limit == 1
        for _ in range(20):
            throttle.on_success()
        assert throttle.limit == 1

    run(scenario())


def test_download_requests_always_satisfy_telegram_alignment_rules() -> None:
    # Seeded property test: every emitted upload.getFile request must satisfy
    # the documented constraints regardless of offsets/limits/windows.
    async def scenario() -> None:
        rng = random.Random(20260707)  # noqa: S311 - deterministic property-test seed
        mib = 1024 * 1024
        for _ in range(30):
            total = rng.randrange(1, 192 * 1024)
            payload = bytes(rng.getrandbits(8) for _ in range(64)) * ((total // 64) + 1)
            payload = payload[:total]
            offset = rng.choice([0, 1024, 2048, 4096, 8192, 1024 * rng.randrange(0, 32)])
            if offset >= total:
                offset = 0
            limit = rng.choice([None, rng.randrange(1, total - offset + 1)])
            part_size = rng.choice([1024, 4096, 16384, 65536])
            concurrency = rng.choice([1, 2, 4, 6])
            window = rng.choice([None, part_size, part_size * 4])
            invoker = OffsetInvoker(payload)
            result = await download_file(
                invoker,
                document_location(),
                offset=offset,
                limit=limit,
                total_size=total,
                part_size=part_size,
                adaptive_part_size=False,
                concurrency=concurrency,
                max_in_flight_bytes=window,
            )
            expected = payload[offset : offset + limit if limit is not None else total]
            assert result.data == expected, (total, offset, limit, part_size, concurrency)
            for request in invoker.requests:
                alignment = 1024 if request.precise else 4096
                assert request.offset % alignment == 0, request
                assert request.limit % alignment == 0, request
                assert 0 < request.limit <= mib, request
                if not request.precise:
                    assert mib % request.limit == 0, request
                assert request.offset // mib == (request.offset + request.limit - 1) // mib, request

    run(scenario())


def test_download_file_flood_sleeps_hold_their_slot_without_backfill(tmp_path) -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 24  # 6 KiB -> 6 parts
        target = tmp_path / "flood-hold.bin"
        invoker = FloodingOffsetInvoker(payload, flood_offsets={0, 1024}, seconds=1)
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            adaptive_concurrency=False,
            concurrency=2,
            max_retries=1,
        )
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        # Both initial requests flooded together. Their slots stay HELD during
        # the sleeps -- backfilling them with new offsets would sustain the
        # request rate the server just objected to (observed live as a
        # FLOOD_WAIT_2 -> FLOOD_WAIT_15 escalation). The next request after the
        # floods must therefore be one of the retries, never a new offset (with
        # backfill it would have been offset 2048, issued ~1 s before any retry).
        assert [request.offset for request in invoker.requests[:2]] == [0, 1024]
        assert invoker.requests[2].offset in {0, 1024}
        assert len(invoker.requests) == 8

    run(scenario())


def test_download_launch_pacer_rate_limits_after_flood() -> None:
    async def scenario() -> None:
        now = [0.0]
        sleeps: list[float] = []

        async def sleep(delay: float) -> None:
            sleeps.append(delay)
            now[0] += delay

        pacer = media_download._DownloadLaunchPacer(concurrency=6, clock=lambda: now[0], sleep=sleep)
        for _ in range(10):
            pacer.on_success()
            now[0] += 0.1
        pacer.on_flood(FloodWait(1))
        await pacer.wait()
        await pacer.wait()
        assert sleeps
        assert max(sleeps) >= 1 / 9

    run(scenario())


def test_download_launch_pacer_keeps_flood_pacing_from_dominating_runtime() -> None:
    now = [0.0]

    async def sleep(delay: float) -> None:
        now[0] += delay

    pacer = media_download._DownloadLaunchPacer(concurrency=6, clock=lambda: now[0], sleep=sleep)
    for _ in range(10):
        pacer.on_success()
        now[0] += 0.1
    for _ in range(10):
        pacer.on_flood(FloodPremiumWait(3))
    assert pacer.current_rate_per_s >= 4.0


def test_download_launch_pacer_reset_clears_wait_state_after_single_slot_fallback() -> None:
    pacer = media_download._DownloadLaunchPacer(concurrency=6)
    pacer.on_flood(FloodWait(1))
    assert pacer.current_rate_per_s > 0
    pacer.reset()
    assert pacer.current_rate_per_s == 0


def test_download_flood_retry_sleep_only_uses_large_floor_for_zero_wait(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        sleeps: list[float] = []

        async def sleep(delay: float) -> None:
            sleeps.append(delay)

        jitter_args: list[tuple[float, float]] = []

        def uniform(low: float, high: float) -> float:
            jitter_args.append((low, high))
            return high

        monkeypatch.setattr("miniproto.media.download.asyncio.sleep", sleep)
        monkeypatch.setattr("miniproto.media.download.random.uniform", uniform)
        await media_download._sleep_before_retry(FloodWait(2))
        await media_download._sleep_before_retry(FloodWait(0))
        assert jitter_args == [(0.0, 0.3), (0.0, 0.3)]
        assert sleeps[0] == pytest.approx(2.3)
        assert sleeps[1] == pytest.approx(1.3)

    run(scenario())


def test_download_file_disables_read_ahead_for_full_file_downloads() -> None:
    async def scenario() -> None:
        payload = b"a" * 2048
        cache = DownloadRangeCache(max_bytes=8192)
        invoker = OffsetInvoker(payload)
        metrics = InMemoryMetrics()
        set_metrics_sink(metrics)
        try:
            result = await download_file(
                invoker,
                document_location(),
                limit=len(payload),
                total_size=len(payload),
                part_size=1024,
                adaptive_part_size=False,
                range_cache=cache,
                range_cache_key="doc:10",
                read_ahead_bytes=4096,
            )
        finally:
            set_metrics_sink(None)
        assert result.data == payload
        disabled = [event for event in metrics.events if event.name == "media.download.read_ahead_disabled"]
        assert disabled
        # No prefetch requests beyond the transfer itself.
        assert sorted(request.offset for request in invoker.requests) == [0, 1024]

    run(scenario())


def test_progress_reporter_coalesces_and_always_finishes() -> None:
    async def scenario() -> None:
        clock_value = [0.0]
        calls: list[tuple[int, int | None]] = []
        reporter = media_download._ProgressReporter(
            lambda current, total: calls.append((current, total)), total=100, clock=lambda: clock_value[0]
        )
        await reporter.report(1)  # first report always fires
        for current in range(2, 9):
            await reporter.report(current)  # coalesced: < 250 ms and < 8 parts
        assert calls == [(1, 100)]
        await reporter.report(9)  # 8th part since last report -> fires
        assert calls == [(1, 100), (9, 100)]
        clock_value[0] = 0.3
        await reporter.report(10)  # interval elapsed -> fires
        assert calls == [(1, 100), (9, 100), (10, 100)]
        await reporter.finish(10)  # already reported -> deduplicated
        assert calls == [(1, 100), (9, 100), (10, 100)]
        await reporter.report(11)
        await reporter.finish(12)  # final call always lands
        assert calls[-1] == (12, 100)

    run(scenario())


def test_transfer_window_tracks_slots_and_bytes() -> None:
    async def scenario() -> None:
        window = media_download._TransferWindow(2048)
        assert window.try_acquire(1024)
        assert window.try_acquire(1024)
        assert not window.try_acquire(1024)
        assert window.active == 2
        window.release(1024)
        assert window.active == 1
        assert window.in_flight_bytes == 1024
        # A release always wakes the scheduler so it can refill the window.
        await asyncio.wait_for(window.wait_refill(), timeout=1.0)
        assert window.try_acquire(1024)

    run(scenario())


def test_adaptive_part_sizer_grows_and_settles_on_regression() -> None:
    sizer = media_download._AdaptivePartSizer(
        initial_size=4, max_size=16, total_bytes=1024, enabled=True, min_total_bytes=0, min_samples=2
    )
    sizer.on_success(requested_size=4, received_size=4, duration_s=1.0)
    assert sizer.current_size == 4
    sizer.on_success(requested_size=4, received_size=4, duration_s=1.0)
    assert sizer.current_size == 8
    sizer.on_success(requested_size=8, received_size=8, duration_s=0.5)
    sizer.on_success(requested_size=8, received_size=8, duration_s=0.5)
    assert sizer.current_size == 16
    sizer.on_success(requested_size=16, received_size=16, duration_s=10.0)
    sizer.on_success(requested_size=16, received_size=16, duration_s=10.0)
    assert sizer.current_size == 8


def test_download_file_sequential_adaptive_part_size_grows(tmp_path) -> None:
    async def scenario() -> None:
        payload = b"a" * (media_download.DEFAULT_ADAPTIVE_PART_SIZE_MIN_BYTES + 4096)
        target = tmp_path / "adaptive-sequential.bin"
        invoker = OffsetInvoker(payload)
        metrics = InMemoryMetrics()
        previous = get_metrics_sink()
        set_metrics_sink(metrics)
        try:
            result = await download_file(
                invoker,
                document_location(),
                target,
                limit=len(payload),
                part_size=1024,
                max_part_size=media_download.MAX_DOWNLOAD_CHUNK_SIZE,
                adaptive_part_size=True,
            )
        finally:
            set_metrics_sink(previous)
        assert result.bytes_downloaded == len(payload)
        assert target.stat().st_size == len(payload)
        assert max(request.limit for request in invoker.requests) > 1024
        assert any(event.name == "media.download.adaptive_part_size" for event in metrics.events)

    run(scenario())


def test_download_file_handles_cdn_redirect_reupload_and_decrypt() -> None:
    async def scenario() -> None:
        key = bytes(range(32))
        iv = bytes(range(16))
        plaintext = b"cdn-data"
        ciphertext = decrypt_cdn_chunk(plaintext, key=key, iv=iv, offset=0)
        invoker = FakeInvoker(
            [
                types.UploadFileCdnRedirect(
                    dc_id=4,
                    file_token=b"token",
                    encryption_key=key,
                    encryption_iv=iv,
                    file_hashes=(cdn_file_hash(plaintext),),
                ),
                types.UploadCdnFileReuploadNeeded(request_token=b"retry"),
                (),
                types.UploadCdnFile(bytes=ciphertext),
            ]
        )
        result = await download_file(invoker, document_location(), part_size=1024)
        assert result.data == plaintext
        assert [getattr(type(request), "QUALNAME", "") for request in invoker.requests] == [
            "upload.getFile",
            "upload.getCdnFile",
            "upload.reuploadCdnFile",
            "upload.getCdnFile",
        ]

    run(scenario())


def test_download_file_fetches_missing_cdn_hashes_before_verifying() -> None:
    async def scenario() -> None:
        key = bytes(range(32))
        iv = bytes(range(16))
        plaintext = b"cdn-data"
        ciphertext = decrypt_cdn_chunk(plaintext, key=key, iv=iv, offset=0)
        invoker = FakeInvoker(
            [
                types.UploadFileCdnRedirect(
                    dc_id=4, file_token=b"token", encryption_key=key, encryption_iv=iv, file_hashes=()
                ),
                types.UploadCdnFile(bytes=ciphertext),
                (cdn_file_hash(plaintext),),
            ]
        )
        result = await download_file(invoker, document_location(), part_size=1024)
        assert result.data == plaintext
        assert [getattr(type(request), "QUALNAME", "") for request in invoker.requests] == [
            "upload.getFile",
            "upload.getCdnFile",
            "upload.getCdnFileHashes",
        ]

    run(scenario())


def test_download_file_raises_cdn_integrity_error_on_corrupted_chunk() -> None:
    async def scenario() -> None:
        key = bytes(range(32))
        iv = bytes(range(16))
        plaintext = b"cdn-data"
        tampered = b"cdn-dAta"
        ciphertext = decrypt_cdn_chunk(tampered, key=key, iv=iv, offset=0)
        invoker = FakeInvoker(
            [
                types.UploadFileCdnRedirect(
                    dc_id=4,
                    file_token=b"token",
                    encryption_key=key,
                    encryption_iv=iv,
                    file_hashes=(cdn_file_hash(plaintext),),
                ),
                types.UploadCdnFile(bytes=ciphertext),
            ]
        )
        with pytest.raises(CdnIntegrityError):
            await download_file(invoker, document_location(), part_size=1024)

    run(scenario())


def test_download_file_raises_cdn_integrity_error_when_no_hash_covers_data() -> None:
    async def scenario() -> None:
        key = bytes(range(32))
        iv = bytes(range(16))
        plaintext = b"cdn-data"
        ciphertext = decrypt_cdn_chunk(plaintext, key=key, iv=iv, offset=0)
        invoker = FakeInvoker(
            [
                types.UploadFileCdnRedirect(
                    dc_id=4, file_token=b"token", encryption_key=key, encryption_iv=iv, file_hashes=()
                ),
                types.UploadCdnFile(bytes=ciphertext),
                (),
            ]
        )
        with pytest.raises(CdnIntegrityError, match="no CDN file hash"):
            await download_file(invoker, document_location(), part_size=1024)

    run(scenario())


def test_download_media_resolves_public_media_location() -> None:
    async def scenario() -> None:
        location = document_location()
        media = Media(id=10, size=3, location=location)
        invoker = FakeInvoker([upload_file_part(b"abc")])
        result = await download_media(invoker, media)
        assert result.data == b"abc"
        assert invoker.requests[0].location == location

    run(scenario())


def test_download_media_uses_known_size_for_concurrent_download() -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 17  # 4352 bytes: 4 full parts + 256-byte tail
        media = Media(id=10, size=len(payload), location=document_location())
        invoker = OffsetInvoker(payload)
        result = await download_media(invoker, media, part_size=1024, adaptive_part_size=False, concurrency=2)
        assert result.data == payload
        assert sorted(request.offset for request in invoker.requests) == [0, 1024, 2048, 3072, 4096]

    run(scenario())


def test_download_media_accepts_miniproto_file_id() -> None:
    async def scenario() -> None:
        document = types.Document(
            id=11,
            access_hash=22,
            file_reference=b"ref",
            date=1_700_000_000,
            mime_type="application/octet-stream",
            size=3,
            dc_id=2,
            attributes=(types.DocumentAttributeFilename(file_name="remote.bin"),),
        )
        file_id = encode_file_id(document)
        invoker = FakeInvoker([upload_file_part(b"abc")])
        result = await download_media(invoker, file_id)
        assert result.data == b"abc"
        assert isinstance(invoker.requests[0].location, types.InputDocumentFileLocation)
        assert invoker.requests[0].location.id == 11
        # A 3-byte file still needs the smallest legal request (4 KiB, truncated).
        assert invoker.requests[0].limit == 4096

    run(scenario())


def test_download_file_cleans_partial_path_on_cancellation(tmp_path) -> None:
    async def scenario() -> None:
        target = tmp_path / "partial.bin"
        invoker = FakeInvoker([upload_file_part(b"x" * 1024), asyncio.CancelledError()])
        with pytest.raises(asyncio.CancelledError):
            await download_file(invoker, document_location(), target, part_size=1024)
        assert not target.exists()

    run(scenario())


def test_download_file_enforces_memory_ceiling() -> None:
    async def scenario() -> None:
        with pytest.raises(ValueError, match="max_in_flight_bytes"):
            await download_file(bad_invoker, document_location(), part_size=1024, max_buffer_size=512)

    async def bad_invoker(request: object, **kwargs: object) -> object:
        raise AssertionError("download should validate before invoking")

    run(scenario())


def test_download_file_rejects_negative_retries() -> None:
    async def scenario() -> None:
        with pytest.raises(ValueError, match="max_retries"):
            await download_file(bad_invoker, document_location(), max_retries=-1)

    async def bad_invoker(request: object, **kwargs: object) -> object:
        raise AssertionError("download should validate before invoking")

    run(scenario())


def test_download_file_rejects_negative_flood_sleep_threshold() -> None:
    async def scenario() -> None:
        with pytest.raises(ValueError, match="flood_sleep_threshold"):
            await download_file(bad_invoker, document_location(), flood_sleep_threshold=-1)

    async def bad_invoker(request: object, **kwargs: object) -> object:
        raise AssertionError("download should validate before invoking")

    run(scenario())


def test_download_file_uses_memory_ceiling_as_byte_window(tmp_path) -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 8  # 2 KiB
        target = tmp_path / "buffer-window.bin"
        invoker = SlowOffsetInvoker(payload)
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            concurrency=2,
            max_buffer_size=1024,
        )
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        assert invoker.max_active == 1

    run(scenario())


def test_download_file_rejects_unknown_media_location() -> None:
    async def scenario() -> None:
        with pytest.raises(MediaDownloadError):
            await download_media(bad_invoker, object())

    async def bad_invoker(request: object, **kwargs: object) -> object:
        raise AssertionError("download should resolve media before invoking")

    run(scenario())


def test_client_download_media_uses_generated_get_file_request() -> None:
    async def scenario() -> None:
        media = Media(id=10, size=3, location=document_location())
        sender = FakeSender([upload_file_part(b"abc")])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender = sender
        await client.connect()
        result = await client.download_media(media, media_lanes=0)
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.UploadGetFile)
        assert request.location == document_location()
        assert request.cdn_supported is True
        assert result.data == b"abc"

    run(scenario())


def test_client_download_media_refreshes_message_backed_file_references() -> None:
    async def scenario() -> None:
        old_document = types.Document(
            id=100,
            access_hash=200,
            file_reference=b"old-ref",
            date=1_700_000_000,
            mime_type="application/octet-stream",
            size=3,
            dc_id=2,
            attributes=(types.DocumentAttributeFilename(file_name="file.bin"),),
        )
        new_document = types.Document(
            id=100,
            access_hash=200,
            file_reference=b"new-ref",
            date=1_700_000_001,
            mime_type="application/octet-stream",
            size=3,
            dc_id=2,
            attributes=(types.DocumentAttributeFilename(file_name="file.bin"),),
        )
        raw_message = types.Message(
            id=55,
            peer_id=types.PeerUser(user_id=7),
            date=1_700_000_000,
            message="file",
            media=types.MessageMediaDocument(document=old_document),
        )
        refreshed_message = types.Message(
            id=55,
            peer_id=types.PeerUser(user_id=7),
            date=1_700_000_001,
            message="file",
            media=types.MessageMediaDocument(document=new_document),
        )
        sender = FakeSender(
            [
                BadRequest("FILE_REFERENCE_EXPIRED"),
                types.MessagesMessages(messages=(refreshed_message,), topics=(), chats=(), users=()),
                upload_file_part(b"abc"),
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender = sender
        await client.connect()
        result = await client.download_media(raw_message, media_lanes=0)
        assert result.data == b"abc"
        first = inner_request(sender.requests[0])
        refresh = inner_request(sender.requests[1])
        second = inner_request(sender.requests[2])
        assert isinstance(first, functions.UploadGetFile)
        assert first.location.file_reference == b"old-ref"
        assert isinstance(refresh, functions.MessagesGetMessages)
        assert refresh.id == (types.InputMessageID(id=55),)
        assert isinstance(second, functions.UploadGetFile)
        assert second.location.file_reference == b"new-ref"

    run(scenario())


def test_client_download_media_uses_dedicated_media_lanes() -> None:
    async def scenario() -> None:
        media = Media(id=10, size=2048, location=document_location())
        lane_senders = [FakeSender([upload_file_part(b"a" * 1024)]), FakeSender([upload_file_part(b"b" * 1024)])]
        built_senders: list[FakeSender] = []

        def sender_factory(record: SessionRecord) -> FakeSender:
            del record
            sender = lane_senders[len(built_senders)]
            built_senders.append(sender)
            return sender

        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender_factory = sender_factory
        await client.connect()
        result = await client.download_media(
            media, part_size=1024, concurrency=2, media_lanes=2, adaptive_concurrency=False
        )
        assert result.data == b"a" * 1024 + b"b" * 1024
        assert built_senders == lane_senders
        assert client._sender is None
        assert [len(sender.requests) for sender in lane_senders] == [1, 1]
        requests: list[functions.UploadGetFile] = []
        for request in (inner_request(sender.requests[0]) for sender in lane_senders):
            assert isinstance(request, functions.UploadGetFile)
            requests.append(request)
        assert {request.offset for request in requests} == {0, 1024}

    run(scenario())


def test_client_download_media_reuses_warm_media_lanes_until_disconnect() -> None:
    async def scenario() -> None:
        media = Media(id=10, size=2048, location=document_location())
        lane_senders = [
            FakeSender([upload_file_part(b"a" * 1024), upload_file_part(b"c" * 1024)]),
            FakeSender([upload_file_part(b"b" * 1024), upload_file_part(b"d" * 1024)]),
        ]
        built_senders: list[FakeSender] = []

        def sender_factory(record: SessionRecord) -> FakeSender:
            del record
            sender = lane_senders[len(built_senders)]
            built_senders.append(sender)
            return sender

        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender_factory = sender_factory
        await client.connect()
        first = await client.download_media(
            media, part_size=1024, concurrency=2, media_lanes=2, adaptive_concurrency=False
        )
        second = await client.download_media(
            media, part_size=1024, concurrency=2, media_lanes=2, adaptive_concurrency=False
        )
        assert first.data == b"a" * 1024 + b"b" * 1024
        assert second.data == b"c" * 1024 + b"d" * 1024
        assert built_senders == lane_senders
        assert [len(sender.requests) for sender in lane_senders] == [2, 2]
        await client.disconnect()
        assert not any(sender.is_connected for sender in lane_senders)

    run(scenario())


@dataclass(slots=True)
class OffsetFakeSender:
    payload: bytes
    requests: list[Any] = field(default_factory=list)
    is_connected: bool = True

    async def request(
        self,
        body: bytes | object,
        *,
        content_related: bool = True,
        retry_safe: bool,
        request_timeout: float | None = None,
    ) -> object:
        del content_related, retry_safe, request_timeout
        await asyncio.sleep(0)
        self.requests.append(body)
        inner = inner_request(body)
        if isinstance(inner, functions.AuthImportAuthorization):
            return types.AuthAuthorization(user=types.UserEmpty(id=1))
        assert isinstance(inner, functions.UploadGetFile)
        return upload_file_part(self.payload[inner.offset : inner.offset + inner.limit])

    async def disconnect(self) -> None:
        self.is_connected = False


def test_client_media_pool_is_reused_and_resized_across_lane_counts() -> None:
    async def scenario() -> None:
        payload = bytes(range(256)) * 8  # 2 KiB
        media_one = Media(id=10, size=1024, location=document_location())
        media_two = Media(id=11, size=2048, location=document_location())
        lane_senders = [OffsetFakeSender(payload), OffsetFakeSender(payload)]
        built_senders: list[OffsetFakeSender] = []

        def sender_factory(record: SessionRecord) -> OffsetFakeSender:
            del record
            sender = lane_senders[len(built_senders)]
            built_senders.append(sender)
            return sender

        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender_factory = sender_factory
        await client.connect()
        first = await client.download_media(media_one, part_size=1024, limit=1024, concurrency=1, media_lanes=1)
        # Asking for more lanes must resize the SAME pool (one warm socket kept),
        # not build a disjoint pool keyed by lane count.
        second = await client.download_media(
            media_two, part_size=1024, concurrency=2, media_lanes=2, adaptive_concurrency=False
        )
        assert first.data == payload[:1024]
        assert second.data == payload
        assert built_senders == lane_senders  # exactly 2 senders ever built
        assert len(client._media_pools) == 1
        await client.disconnect()

    run(scenario())


def test_client_media_lanes_close_after_idle_timeout() -> None:
    async def scenario() -> None:
        media = Media(id=10, size=1024, location=document_location())
        lane_senders = [OffsetFakeSender(b"a" * 1024), OffsetFakeSender(b"b" * 1024)]
        built_senders: list[OffsetFakeSender] = []

        def sender_factory(record: SessionRecord) -> OffsetFakeSender:
            del record
            sender = lane_senders[len(built_senders)]
            built_senders.append(sender)
            return sender

        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth(), media_idle_close=0.1)
        )
        client._sender_factory = sender_factory
        await client.connect()
        first = await client.download_media(media, part_size=1024, limit=1024, concurrency=1, media_lanes=1)
        assert first.data == b"a" * 1024
        assert lane_senders[0].is_connected
        for _ in range(50):
            if not lane_senders[0].is_connected:
                break
            await asyncio.sleep(0.05)
        # The idle reaper closed the lane; the pool transparently rebuilds on
        # the next transfer.
        assert not lane_senders[0].is_connected
        second = await client.download_media(media, part_size=1024, limit=1024, concurrency=1, media_lanes=1)
        assert second.data == b"b" * 1024
        assert built_senders == lane_senders
        await client.disconnect()

    run(scenario())


def _multi_dc_storage() -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(
                DCOption(id=2, ip_address="127.0.0.1", port=443),
                DCOption(id=5, ip_address="127.0.0.5", port=443),
            ),
        )
    )


def test_client_download_media_follows_file_migrate_without_touching_session() -> None:
    async def scenario() -> None:
        media = Media(id=10, size=1024, location=document_location())
        payload = upload_file_part(b"m" * 1024)
        file_migrate = classify_rpc_error(RpcError("FILE_MIGRATE_5", code=303))
        home_lane = FakeSender([file_migrate])
        main_sender = FakeSender([types.AuthExportedAuthorization(id=7, bytes=b"exported")])
        foreign_lane = FakeSender([types.AuthAuthorization(user=types.UserEmpty(id=1)), payload])
        built: list[tuple[int, FakeSender]] = []

        def sender_factory(record: SessionRecord) -> FakeSender:
            if record.dc_id == 5:
                sender = foreign_lane
            elif not built:
                sender = home_lane
            else:
                sender = main_sender
            built.append((record.dc_id or 0, sender))
            return sender

        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=_multi_dc_storage()))
        client._sender_factory = sender_factory
        await client.connect()
        result = await client.download_media(
            media, part_size=1024, limit=1024, concurrency=1, media_lanes=1, max_retries=0
        )
        assert result.data == b"m" * 1024
        # The main session stays on its DC; only the media pool moved.
        record = await client._storage.load()
        assert record is not None and record["dc_id"] == 2
        # The foreign lane imported the exported authorization before getFile.
        first_foreign = inner_request(foreign_lane.requests[0])
        assert isinstance(first_foreign, functions.AuthImportAuthorization)
        assert first_foreign.id == 7
        assert first_foreign.bytes == b"exported"
        second_foreign = inner_request(foreign_lane.requests[1])
        assert isinstance(second_foreign, functions.UploadGetFile)
        # The main sender served exactly the exportAuthorization call.
        exported_request = inner_request(main_sender.requests[0])
        assert isinstance(exported_request, functions.AuthExportAuthorization)
        assert exported_request.dc_id == 5
        await client.disconnect()

    run(scenario())


def test_client_download_media_targets_the_media_dc_directly() -> None:
    async def scenario() -> None:
        media = Media(id=10, size=1024, dc_id=5, location=document_location())
        main_sender = FakeSender([types.AuthExportedAuthorization(id=9, bytes=b"exp5")])
        foreign_lane = FakeSender([types.AuthAuthorization(user=types.UserEmpty(id=1)), upload_file_part(b"z" * 1024)])
        built: list[int] = []

        def sender_factory(record: SessionRecord) -> FakeSender:
            built.append(record.dc_id or 0)
            return foreign_lane if record.dc_id == 5 else main_sender

        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=_multi_dc_storage()))
        client._sender_factory = sender_factory
        await client.connect()
        result = await client.download_media(media, part_size=1024, limit=1024, concurrency=1, media_lanes=1)
        assert result.data == b"z" * 1024
        # Media whose DC is known goes straight to a (kind, dc=5) pool; no
        # FILE_MIGRATE round trip on the session DC.
        assert 5 in built
        assert isinstance(inner_request(foreign_lane.requests[1]), functions.UploadGetFile)
        await client.disconnect()

    run(scenario())


def test_client_download_media_rejects_unknown_options() -> None:
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        with pytest.raises(TypeError, match="unsupported download_media options"):
            await client.download_media(Media(id=1, location=document_location()), unsupported=True)

    run(scenario())


@pytest.mark.parametrize(("size", "expected_sessions"), [(50 * 1024 * 1024 + 1, 2), (250 * 1024 * 1024 + 1, 4)])
def test_client_download_media_routes_bot_multi_session_by_size(size: int, expected_sessions: int, monkeypatch) -> None:
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_identity(is_bot=True)))
        calls: list[tuple[int, int]] = []

        async def fake_multi(media, destination, options, *, total_size, session_count):
            del media, destination, options
            calls.append((total_size, session_count))
            return MediaDownloadResult(bytes_downloaded=total_size, offset=0, data=b"multi")

        monkeypatch.setattr(client, "_download_media_multi_session", fake_multi)
        result = await client.download_media(Media(id=10, size=size, location=document_location()), multi_session=True)
        assert result.data == b"multi"
        assert calls == [(size, expected_sessions)]

    run(scenario())


def test_client_download_media_ignores_multi_session_for_user_with_error_log(monkeypatch) -> None:
    async def scenario() -> None:
        sender = FakeSender([upload_file_part(b"abc")])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_identity(is_bot=False)))
        client._sender = sender
        events: list[tuple[int, str, dict[str, object]]] = []

        def capture_event(logger, level, event, **fields):
            del logger
            events.append((level, event, fields))

        monkeypatch.setattr("miniproto.client.emit_event", capture_event)
        await client.connect()
        result = await client.download_media(
            Media(id=10, size=75 * 1024 * 1024, location=document_location()),
            multi_session=True,
            concurrency=1,
            media_lanes=0,
        )
        assert result.data == b"abc"
        ignored = [item for item in events if item[1] == "client.download_media.multi_session_ignored"]
        assert len(ignored) == 1
        assert ignored[0][0] == logging.ERROR
        assert ignored[0][2]["reason"] == "account_is_not_bot"
        await client.disconnect()

    run(scenario())


def test_client_small_bot_download_does_not_create_auxiliary_session() -> None:
    async def scenario() -> None:
        sender = FakeSender([upload_file_part(b"abc")])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_identity(is_bot=True)))
        client._sender = sender
        await client.connect()
        result = await client.download_media(
            Media(id=10, size=5 * 1024 * 1024, location=document_location()),
            multi_session=True,
            concurrency=1,
            media_lanes=0,
        )
        assert result.data == b"abc"
        assert client._auxiliary_download_clients == {}
        await client.disconnect()

    run(scenario())


def test_client_lazily_creates_reuses_and_disconnects_auxiliary_bot_sessions(monkeypatch) -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, bot_token=BOT_CREDENTIAL))
        sign_ins: list[Client] = []

        async def fake_sign_in_bot(auxiliary: Client, token: str) -> object:
            assert token == BOT_CREDENTIAL
            assert not auxiliary._updates_enabled
            await auxiliary.connect()
            assert auxiliary._update_manager._task is None
            index = len(sign_ins) + 1
            await auxiliary._storage.save(
                SessionRecord(
                    dc_id=2,
                    auth_key=AuthKey(dc_id=2, key=bytes([index]) * 256, key_id=index),
                    dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
                    user=UserIdentity(id=42, is_bot=True),
                )
            )
            sign_ins.append(auxiliary)
            return object()

        monkeypatch.setattr(Client, "sign_in_bot", fake_sign_in_bot)
        first = await client._ensure_auxiliary_download_clients(2)
        assert len(first) == 1
        assert len(sign_ins) == 1
        await client._disconnect_auxiliary_download_clients(first)
        assert not first[0].is_connected
        auxiliaries = await client._ensure_auxiliary_download_clients(4)
        assert len(auxiliaries) == 3
        assert auxiliaries[0] is first[0]
        assert len(sign_ins) == 3
        assert all(auxiliary.is_connected for auxiliary in auxiliaries)
        await client._disconnect_auxiliary_download_clients(auxiliaries)
        assert all(not auxiliary.is_connected for auxiliary in auxiliaries)

    run(scenario())


def test_auxiliary_bot_authorization_cancellation_cleans_local_client(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        class TrackingSender:
            is_connected = True

            def __init__(self) -> None:
                self.disconnect_calls = 0

            async def disconnect(self) -> None:
                self.disconnect_calls += 1
                self.is_connected = False

        storage = storage_with_identity(is_bot=True)
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, bot_token=BOT_CREDENTIAL))
        authorization_started = asyncio.Event()
        authorization_release = asyncio.Event()
        captured: list[tuple[Client, TrackingSender, asyncio.Task[None]]] = []

        async def blocking_sign_in(auxiliary: Client, token: str) -> object:
            assert token == BOT_CREDENTIAL
            await auxiliary.connect()
            sender = TrackingSender()

            async def wait_forever() -> None:
                await asyncio.Event().wait()

            background = asyncio.create_task(wait_forever(), name="plan009-auxiliary-background")
            auxiliary._sender = cast(Any, sender)
            auxiliary._receive_dispatch_task = background
            auxiliary._dispatch_sender = cast(Any, sender)
            captured.append((auxiliary, sender, background))
            authorization_started.set()
            await authorization_release.wait()
            raise AssertionError("authorization cancellation did not interrupt wait")

        monkeypatch.setattr(Client, "sign_in_bot", blocking_sign_in)
        setup = asyncio.create_task(client._ensure_auxiliary_download_clients(2))
        await authorization_started.wait()
        setup.cancel()
        with pytest.raises(asyncio.CancelledError):
            await setup

        assert len(captured) == 1
        auxiliary, sender, background = captured[0]
        assert client._auxiliary_download_clients == {}
        assert not auxiliary.is_connected
        assert sender.disconnect_calls == 1
        assert background.done()
        assert cast(Any, auxiliary._session_storage_backend)._closed is True
        assert not [
            task
            for task in asyncio.all_tasks()
            if task is not asyncio.current_task()
            and task.get_name() == "plan009-auxiliary-background"
            and not task.done()
        ]

    run(scenario())


def test_auxiliary_cleanup_joins_disconnect_under_repeated_cancellation() -> None:
    async def scenario() -> None:
        disconnect_started = asyncio.Event()
        disconnect_release = asyncio.Event()
        disconnect_calls = 0

        class FakeAuxiliary:
            async def disconnect(self) -> None:
                nonlocal disconnect_calls
                disconnect_calls += 1
                disconnect_started.set()
                await disconnect_release.wait()

        cleanup = asyncio.create_task(
            client_module._cleanup_auxiliary_download_client(cast(Any, FakeAuxiliary()), auxiliary_index=1)
        )
        await disconnect_started.wait()
        cleanup.cancel()
        await asyncio.sleep(0)
        cleanup.cancel()
        disconnect_release.set()
        with pytest.raises(asyncio.CancelledError):
            await cleanup
        assert disconnect_calls == 1

    run(scenario())


def test_recovered_auxiliary_connect_cancellation_before_open_cleans_local_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        sibling = storage.sibling("download-1")
        await sibling.save(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=b"a" * 256, key_id=1),
                dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
                user=UserIdentity(id=42, is_bot=True),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        connect_started = asyncio.Event()
        captured: list[Client] = []

        async def blocking_connect(auxiliary: Client) -> None:
            captured.append(auxiliary)
            connect_started.set()
            await asyncio.Event().wait()

        monkeypatch.setattr(Client, "connect", blocking_connect)
        setup = asyncio.create_task(client._ensure_auxiliary_download_clients(2))
        await connect_started.wait()
        setup.cancel()
        with pytest.raises(asyncio.CancelledError):
            await setup

        assert len(captured) == 1
        assert client._auxiliary_download_clients == {}
        assert not captured[0].is_connected
        assert sibling._closed is True

    run(scenario())


def test_recovered_auxiliary_connect_cancellation_cleans_before_registration(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        sibling = storage.sibling("download-1")
        await sibling.save(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=b"a" * 256, key_id=1),
                dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
                user=UserIdentity(id=42, is_bot=True),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        connect_started = asyncio.Event()
        connect_release = asyncio.Event()
        captured: list[tuple[Client, LifecycleTrackingSender]] = []

        async def blocking_connect(auxiliary: Client) -> None:
            sender = LifecycleTrackingSender()
            auxiliary._connected = True
            auxiliary._sender = cast(Any, sender)
            captured.append((auxiliary, sender))
            connect_started.set()
            await connect_release.wait()

        monkeypatch.setattr(Client, "connect", blocking_connect)
        setup = asyncio.create_task(client._ensure_auxiliary_download_clients(2))
        await connect_started.wait()
        setup.cancel()
        with pytest.raises(asyncio.CancelledError):
            await setup

        assert len(captured) == 1
        auxiliary, sender = captured[0]
        assert client._auxiliary_download_clients == {}
        assert not auxiliary.is_connected
        assert sender.disconnect_calls == 1
        assert sibling._closed is True

    run(scenario())


def test_recovered_auxiliary_connect_failure_is_ignored_after_cleanup(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        sibling = storage.sibling("download-1")
        await sibling.save(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=b"a" * 256, key_id=1),
                dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
                user=UserIdentity(id=42, is_bot=True),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        captured: list[tuple[Client, LifecycleTrackingSender]] = []
        ignored: list[tuple[str, dict[str, object]]] = []

        async def failing_connect(auxiliary: Client) -> None:
            sender = LifecycleTrackingSender()
            auxiliary._connected = True
            auxiliary._sender = cast(Any, sender)
            captured.append((auxiliary, sender))
            raise RuntimeError("connect failed")

        monkeypatch.setattr(Client, "connect", failing_connect)
        monkeypatch.setattr(
            "miniproto.client._emit_multi_session_ignored", lambda reason, **fields: ignored.append((reason, fields))
        )
        auxiliaries = await client._ensure_auxiliary_download_clients(2)

        assert len(captured) == 1
        auxiliary, sender = captured[0]
        assert auxiliaries == ()
        assert client._auxiliary_download_clients == {}
        assert not auxiliary.is_connected
        assert sender.disconnect_calls == 1
        assert sibling._closed is True
        assert ignored == [("auxiliary_session_setup_failed", {"auxiliary_index": 1, "error_type": "RuntimeError"})]

    run(scenario())


def test_auxiliary_identity_mismatch_closes_local_storage() -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        sibling = storage.sibling("download-1")
        await sibling.save(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=b"a" * 256, key_id=1),
                dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
                user=UserIdentity(id=99, is_bot=True),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))

        auxiliaries = await client._ensure_auxiliary_download_clients(2)

        assert auxiliaries == ()
        assert client._auxiliary_download_clients == {}
        assert sibling._closed is True

    run(scenario())


def test_auxiliary_identity_mismatch_cancellation_during_cleanup_disconnects_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        sibling = storage.sibling("download-1")
        await sibling.save(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=b"a" * 256, key_id=1),
                dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
                user=UserIdentity(id=99, is_bot=True),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        disconnect_started = asyncio.Event()
        disconnect_release = asyncio.Event()
        disconnect_calls = 0
        original_disconnect = Client.disconnect

        async def blocking_disconnect(auxiliary: Client) -> None:
            nonlocal disconnect_calls
            disconnect_calls += 1
            disconnect_started.set()
            await disconnect_release.wait()
            await original_disconnect(auxiliary)

        monkeypatch.setattr(Client, "disconnect", blocking_disconnect)
        setup = asyncio.create_task(client._ensure_auxiliary_download_clients(2))
        await disconnect_started.wait()
        setup.cancel()
        await asyncio.sleep(0)
        disconnect_release.set()
        with pytest.raises(asyncio.CancelledError):
            await setup

        assert disconnect_calls == 1
        assert client._auxiliary_download_clients == {}
        assert sibling._closed is True

    run(scenario())


def test_auxiliary_missing_bot_token_closes_local_storage() -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        sibling = storage.sibling("download-1")
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))

        auxiliaries = await client._ensure_auxiliary_download_clients(2)

        assert auxiliaries == ()
        assert client._auxiliary_download_clients == {}
        assert sibling._closed is True

    run(scenario())


def test_auxiliary_post_auth_load_cancellation_cleans_local_client(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, bot_token=BOT_CREDENTIAL))
        load_started = asyncio.Event()
        load_release = asyncio.Event()
        captured: list[Client] = []

        async def sign_in_then_block_load(auxiliary: Client, token: str) -> object:
            assert token == BOT_CREDENTIAL
            await auxiliary.connect()
            await auxiliary._storage.save(
                SessionRecord(
                    dc_id=2,
                    auth_key=AuthKey(dc_id=2, key=b"a" * 256, key_id=1),
                    dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
                    user=UserIdentity(id=42, is_bot=True),
                )
            )
            original_load = auxiliary._storage.load

            async def blocking_load():
                load_started.set()
                await load_release.wait()
                return await original_load()

            cast(Any, auxiliary._storage).load = blocking_load
            captured.append(auxiliary)
            return object()

        monkeypatch.setattr(Client, "sign_in_bot", sign_in_then_block_load)
        setup = asyncio.create_task(client._ensure_auxiliary_download_clients(2))
        await load_started.wait()
        setup.cancel()
        with pytest.raises(asyncio.CancelledError):
            await setup

        assert len(captured) == 1
        auxiliary = captured[0]
        assert client._auxiliary_download_clients == {}
        assert not auxiliary.is_connected
        assert cast(Any, auxiliary._session_storage_backend)._closed is True

    run(scenario())


def test_auxiliary_registration_failure_is_ignored_after_cleanup(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        class FailingRegistration(dict[int, Client]):
            def __init__(self) -> None:
                super().__init__()
                self.attempted: list[Client] = []

            def __setitem__(self, key: int, value: Client) -> None:
                del key
                self.attempted.append(value)
                raise RuntimeError("registration failed")

        storage = storage_with_identity(is_bot=True)
        sibling = storage.sibling("download-1")
        await sibling.save(
            SessionRecord(
                dc_id=2,
                auth_key=AuthKey(dc_id=2, key=b"a" * 256, key_id=1),
                dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
                user=UserIdentity(id=42, is_bot=True),
            )
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage))
        registrations = FailingRegistration()
        client._auxiliary_download_clients = registrations
        ignored: list[tuple[str, dict[str, object]]] = []

        monkeypatch.setattr(
            "miniproto.client._emit_multi_session_ignored", lambda reason, **fields: ignored.append((reason, fields))
        )
        auxiliaries = await client._ensure_auxiliary_download_clients(2)

        assert len(registrations.attempted) == 1
        auxiliary = registrations.attempted[0]
        assert auxiliaries == ()
        assert not auxiliary.is_connected
        assert sibling._closed is True
        assert ignored == [("auxiliary_session_setup_failed", {"auxiliary_index": 1, "error_type": "RuntimeError"})]

    run(scenario())


def test_auxiliary_cleanup_error_does_not_replace_authorization_cancellation(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, bot_token=BOT_CREDENTIAL))
        authorization_started = asyncio.Event()
        authorization_release = asyncio.Event()
        captured: list[Client] = []
        events: list[tuple[str, dict[str, object]]] = []

        def capture_event(logger, level, event, **fields):
            del logger, level
            events.append((event, fields))

        async def blocking_sign_in(auxiliary: Client, token: str) -> object:
            assert token == BOT_CREDENTIAL
            await auxiliary.connect()

            async def failing_disconnect() -> None:
                await auxiliary._storage.close()
                raise RuntimeError("cleanup failed")

            cast(Any, auxiliary).disconnect = failing_disconnect
            captured.append(auxiliary)
            authorization_started.set()
            await authorization_release.wait()
            raise AssertionError("authorization cancellation did not interrupt wait")

        monkeypatch.setattr("miniproto.client.emit_event", capture_event)
        monkeypatch.setattr(Client, "sign_in_bot", blocking_sign_in)
        setup = asyncio.create_task(client._ensure_auxiliary_download_clients(2))
        await authorization_started.wait()
        setup.cancel()
        with pytest.raises(asyncio.CancelledError):
            await setup

        assert len(captured) == 1
        assert cast(Any, captured[0]._session_storage_backend)._closed is True
        cleanup_events = [
            fields for event, fields in events if event == "client.download_media.auxiliary_cleanup_failed"
        ]
        assert cleanup_events == [{"outcome": "error", "auxiliary_index": 1, "error_type": "RuntimeError"}]
        assert BOT_CREDENTIAL not in repr(events)

    run(scenario())


def test_auxiliary_setup_cancellation_does_not_disconnect_cached_client(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        storage = storage_with_identity(is_bot=True)
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage, bot_token=BOT_CREDENTIAL))
        healthy = Client(replace(client.config, session_storage=storage.sibling("download-1")), _updates_enabled=False)
        await healthy.connect()
        client._auxiliary_download_clients[1] = healthy
        authorization_started = asyncio.Event()
        authorization_release = asyncio.Event()

        async def blocking_sign_in(auxiliary: Client, token: str) -> object:
            assert auxiliary is not healthy
            assert token == BOT_CREDENTIAL
            await auxiliary.connect()
            authorization_started.set()
            await authorization_release.wait()
            raise AssertionError("authorization cancellation did not interrupt wait")

        monkeypatch.setattr(Client, "sign_in_bot", blocking_sign_in)
        setup = asyncio.create_task(client._ensure_auxiliary_download_clients(3))
        await authorization_started.wait()
        setup.cancel()
        with pytest.raises(asyncio.CancelledError):
            await setup

        assert client._auxiliary_download_clients == {1: healthy}
        assert healthy.is_connected
        await healthy.disconnect()

    run(scenario())


def test_auxiliary_client_initializes_sender_without_updates() -> None:
    async def scenario() -> None:
        sender = FakeSender([upload_file_part(b"abc")])
        auxiliary = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_identity(is_bot=True)),
            _updates_enabled=False,
        )
        auxiliary._sender = sender
        await auxiliary.connect()
        result = await auxiliary.invoke(
            functions.UploadGetFile(
                location=document_location(), offset=0, limit=1024, precise=False, cdn_supported=True
            )
        )
        assert isinstance(result, types.UploadFile)
        assert isinstance(sender.requests[0], functions.InvokeWithoutUpdates)
        assert auxiliary._update_manager._task is None
        assert auxiliary._receive_dispatch_task is None
        await auxiliary.disconnect()

    run(scenario())


def test_client_multi_session_download_splits_and_assembles_ranges(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        primary = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_identity(is_bot=True)))
        auxiliary = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_identity(is_bot=True)),
            _updates_enabled=False,
        )
        auxiliary._connected = True

        async def fake_auxiliaries(session_count: int) -> tuple[Client, ...]:
            assert session_count == 2
            return (auxiliary,)

        async def fake_single(
            worker: Client, media: object, destination: object, options: dict[str, object]
        ) -> MediaDownloadResult:
            del worker, media
            offset = cast(int, options["offset"])
            limit = cast(int, options["limit"])
            payload = bytes([offset // (1024 * 1024)]) * limit
            assert isinstance(destination, Path)
            destination.write_bytes(payload)
            return MediaDownloadResult(bytes_downloaded=limit, offset=offset, destination=destination)

        monkeypatch.setattr(primary, "_ensure_auxiliary_download_clients", fake_auxiliaries)
        monkeypatch.setattr(Client, "_download_media_single", fake_single)
        target = tmp_path / "assembled.bin"
        result = await primary._download_media_multi_session(
            Media(id=10, size=2 * 1024 * 1024, location=document_location()),
            target,
            client_module._download_media_options({}),
            total_size=2 * 1024 * 1024,
            session_count=2,
        )
        assert result.destination == target
        assert result.bytes_downloaded == 2 * 1024 * 1024
        payload = target.read_bytes()
        assert payload[: 1024 * 1024] == b"\0" * (1024 * 1024)
        assert payload[1024 * 1024 :] == b"\1" * (1024 * 1024)
        assert not auxiliary.is_connected

    run(scenario())
