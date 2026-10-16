from __future__ import annotations

import asyncio
import hashlib
import io
from collections.abc import AsyncIterator, Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, cast

import pytest

import miniproto.media.upload as media_upload
from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    ClientDisconnected,
    DCOption,
    FloodWait,
    InMemorySessionStorage,
    Peer,
    RpcError,
    SessionRecord,
    encode_file_id,
    event_loop,
)
from miniproto.errors import classify_rpc_error
from miniproto.media import BIG_FILE_THRESHOLD, DEFAULT_CHUNK_SIZE, MediaUploadError, upload_file
from miniproto.media.retry import backoff_delay
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry

AUTH_KEY = b"m" * 256


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
        self.requests.append(body)
        if not self.responses:
            raise AssertionError("fake sender has no queued response")
        return self.responses.pop(0)

    async def disconnect(self) -> None:
        self.is_connected = False


def run(coro):
    return event_loop.run(coro)


def storage_with_auth() -> InMemorySessionStorage:
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address="127.0.0.1", port=443),),
            peers=(PeerCacheEntry(id=7, kind="user", access_hash=77, username="alice"),),
        )
    )


def inner_request(wrapped: object) -> object:
    if isinstance(wrapped, functions.InvokeWithoutUpdates):
        wrapped = wrapped.query
    if isinstance(wrapped, functions.InvokeWithLayer):
        assert isinstance(wrapped.query, functions.InitConnection)
        return wrapped.query.query
    return wrapped


@pytest.fixture
def upload_spools(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[BinaryIO]]:
    original_temporary_file = media_upload.tempfile.TemporaryFile
    spools: list[BinaryIO] = []

    def retain_spool(*args: Any, **kwargs: Any) -> BinaryIO:
        spool = cast(BinaryIO, original_temporary_file(*args, **kwargs))
        spools.append(spool)
        return spool

    monkeypatch.setattr(media_upload.tempfile, "TemporaryFile", retain_spool)
    try:
        yield spools
    finally:
        for spool in spools:
            spool.close()


def test_upload_file_closes_spool_when_part_cap_cannot_be_met(upload_spools: list[BinaryIO]) -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([])
        with pytest.raises(MediaUploadError):
            await upload_file(invoker, iter((b"x" * (512 * 1024 + 1),)), part_size=1024, max_file_parts=1)
        assert invoker.requests == []
        assert len(upload_spools) == 1
        assert upload_spools[0].closed

    run(scenario())


@pytest.mark.parametrize("await_registration", [False, True])
def test_upload_file_closes_spool_when_registration_fails(upload_spools: list[BinaryIO], await_registration: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        failure = OSError("registration failed")

        async def fail_registration() -> None:
            raise failure

        class RegistrationInvoker:
            def register_transfer(self, size: int) -> object:
                assert size == 7
                if await_registration:
                    return fail_registration()
                raise failure

            async def __call__(self, request: object, **kwargs: object) -> object:
                raise AssertionError("registration failure must prevent part requests")

        with pytest.raises(OSError) as error:
            await upload_file(RegistrationInvoker(), iter((b"payload",)))
        assert error.value is failure
        assert len(upload_spools) == 1
        assert upload_spools[0].closed

    run(scenario())


def test_upload_file_closes_spool_when_registration_is_cancelled(upload_spools: list[BinaryIO]) -> None:
    async def scenario() -> None:
        started = asyncio.Event()

        class RegistrationInvoker:
            async def register_transfer(self, size: int) -> None:
                assert size == 7
                started.set()
                await asyncio.Future()

            async def __call__(self, request: object, **kwargs: object) -> object:
                raise AssertionError("registration cancellation must prevent part requests")

        task = asyncio.create_task(upload_file(RegistrationInvoker(), iter((b"payload",))))
        await asyncio.wait_for(started.wait(), timeout=1.0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert len(upload_spools) == 1
        assert upload_spools[0].closed

    run(scenario())


def test_upload_file_closes_spool_when_file_id_conversion_fails(upload_spools: list[BinaryIO]) -> None:
    class InvalidFileId:
        def __int__(self) -> int:
            raise ValueError("invalid file ID")

    async def scenario() -> None:
        invoker = FakeInvoker([])
        with pytest.raises(ValueError, match="invalid file ID"):
            await upload_file(invoker, iter((b"payload",)), file_id=cast(Any, InvalidFileId()))
        assert invoker.requests == []
        assert len(upload_spools) == 1
        assert upload_spools[0].closed

    run(scenario())


@pytest.mark.parametrize("failure_stage", ["preparation", "setup", "transfer", "cancellation"])
def test_upload_file_preserves_original_failure_when_spool_close_fails(monkeypatch: pytest.MonkeyPatch, failure_stage: str) -> None:  # fmt: skip
    class CloseFailingSpool(io.BytesIO):
        def close(self) -> None:
            super().close()
            raise OSError("spool close failed")

    async def scenario() -> None:
        spool = CloseFailingSpool()
        monkeypatch.setattr(media_upload.tempfile, "TemporaryFile", lambda *args, **kwargs: spool)
        failure = asyncio.CancelledError("registration cancelled") if failure_stage == "cancellation" else RuntimeError("upload failed")  # fmt: skip

        class FailingInvoker:
            def register_transfer(self, size: int) -> None:
                if failure_stage in {"setup", "cancellation"}:
                    raise failure

            async def __call__(self, request: object, **kwargs: object) -> object:
                raise failure

        def source() -> Iterator[bytes]:
            yield b"payload"
            if failure_stage == "preparation":
                raise failure

        try:
            with pytest.raises(type(failure)) as error:
                await upload_file(FailingInvoker(), source())
            assert error.value is failure
            assert spool.closed
        finally:
            io.BytesIO.close(spool)

    run(scenario())


def test_upload_file_does_not_report_success_when_spool_close_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    class CloseFailingSpool(io.BytesIO):
        def close(self) -> None:
            super().close()
            raise OSError("spool close failed")

    async def scenario() -> None:
        spool = CloseFailingSpool()
        events: list[dict[str, object]] = []
        monkeypatch.setattr(media_upload.tempfile, "TemporaryFile", lambda *args, **kwargs: spool)
        monkeypatch.setattr(media_upload, "emit_event", lambda *args, **fields: events.append(fields))
        try:
            with pytest.raises(OSError, match="spool close failed"):
                await upload_file(FakeInvoker([types.BoolTrue()]), iter((b"payload",)))
            assert spool.closed
            assert not any(event.get("outcome") == "success" for event in events)
        finally:
            io.BytesIO.close(spool)

    run(scenario())


@pytest.mark.parametrize("failure_stage", ["setup", "transfer", "cancellation"])
def test_upload_file_leaves_borrowed_reader_open_on_failure(failure_stage: str) -> None:
    async def scenario() -> None:
        failure = asyncio.CancelledError("upload cancelled") if failure_stage == "cancellation" else RuntimeError("upload failed")  # fmt: skip

        class FailingInvoker:
            def register_transfer(self, size: int) -> None:
                if failure_stage == "setup":
                    raise failure

            async def __call__(self, request: object, **kwargs: object) -> object:
                raise failure

        with io.BytesIO(b"payload") as reader:
            with pytest.raises(type(failure)) as error:
                await upload_file(FailingInvoker(), reader)
            assert error.value is failure
            assert not reader.closed

    run(scenario())


@pytest.mark.parametrize("available", [0, 1024, 1025, 2048])
@pytest.mark.parametrize("big", [False, True])
def test_upload_file_rejects_premature_eof(monkeypatch: pytest.MonkeyPatch, available: int, big: bool) -> None:
    class TruncatedReader(io.BytesIO):
        def read(self, size: int | None = -1, /) -> bytes:
            remaining = available - self.tell()
            requested = remaining if size is None or size < 0 else min(size, remaining)
            return super().read(max(0, requested))

    async def scenario() -> None:
        if big:
            monkeypatch.setattr(media_upload, "BIG_FILE_THRESHOLD", 2048)
        invoker = FakeInvoker([types.BoolTrue()] * 3)
        with TruncatedReader(b"a" * 1024 + b"b" * 1024 + b"z") as reader:
            with pytest.raises(MediaUploadError):
                await asyncio.wait_for(upload_file(invoker, reader, part_size=1024, concurrency=1), timeout=1.0)
            assert not reader.closed

    run(scenario())


@pytest.mark.parametrize("async_reader", [False, True])
@pytest.mark.parametrize("big", [False, True])
def test_upload_file_fills_parts_across_nonuniform_short_reads(monkeypatch: pytest.MonkeyPatch, async_reader: bool, big: bool) -> None:  # fmt: skip
    class ShortReader(io.BytesIO):
        def __init__(self, payload: bytes) -> None:
            super().__init__(payload)
            self.read_sizes = iter((3, 509, 700, 17, 900, 2, 111, 1))

        def read(self, size: int | None = -1, /) -> bytes:
            if size is None or size < 0:
                return super().read(next(self.read_sizes, -1))
            return super().read(min(size, next(self.read_sizes, size)))

    class AsyncShortReader(ShortReader):
        # upload_file explicitly supports awaited read methods on seekable readers
        async def read(self, size: int | None = -1, /) -> bytes:  # ty: ignore[invalid-method-override]
            return ShortReader.read(self, size)

    async def scenario() -> None:
        if big:
            monkeypatch.setattr(media_upload, "BIG_FILE_THRESHOLD", 2048)
        prefix = b"skipped-prefix"
        payload = b"a" * 1024 + b"bc" * 512 + b"tail"
        invoker = FakeInvoker([types.BoolTrue()] * 3)
        progress: list[tuple[int, int | None]] = []
        reader_type = AsyncShortReader if async_reader else ShortReader
        with reader_type(prefix + payload) as reader:
            reader.seek(len(prefix))
            result = await upload_file(invoker, reader, part_size=1024, concurrency=2, file_id=11, progress=lambda current, total: progress.append((current, total)))  # fmt: skip
            assert not reader.closed
            assert reader.tell() == len(prefix) + len(payload)
        assert {request.file_part: request.bytes for request in invoker.requests} == {0: b"a" * 1024, 1: b"bc" * 512, 2: b"tail"}  # fmt: skip
        assert result.size == 2052
        assert result.parts == result.input_file.parts == len(invoker.requests) == 3
        assert progress[-1] == (2052, 2052)
        if big:
            assert isinstance(result.input_file, types.InputFileBig)
            assert result.md5_checksum is None
            assert all(isinstance(request, functions.UploadSaveBigFilePart) and request.file_total_parts == 3 for request in invoker.requests)  # fmt: skip
        else:
            assert isinstance(result.input_file, types.InputFile)
            checksum = hashlib.md5(payload, usedforsecurity=False).hexdigest()
            assert result.md5_checksum == result.input_file.md5_checksum == checksum

    run(scenario())


def test_upload_file_defaults_to_45s_part_timeout() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([types.BoolTrue()])
        await upload_file(invoker, b"payload", file_name="t.bin")
        assert invoker.kwargs[0]["request_timeout"] == 45.0
        # An explicit timeout still wins.
        explicit = FakeInvoker([types.BoolTrue()])
        await upload_file(explicit, b"payload", file_name="t.bin", request_timeout=10.0)
        assert explicit.kwargs[0]["request_timeout"] == 10.0

    run(scenario())


def test_upload_file_rejects_part_size_that_does_not_divide_512_kib() -> None:
    async def scenario() -> None:
        with pytest.raises(ValueError, match="divide 512 KiB"):
            await upload_file(FakeInvoker([]), b"payload", part_size=3 * 1024)

    run(scenario())


def test_upload_file_propagates_reader_errors_without_hanging() -> None:
    class ExplodingReader:
        # Reports a two-part file; the second read explodes.
        def __init__(self) -> None:
            self.calls = 0
            self.position = 0

        def read(self, size: int) -> bytes:
            self.calls += 1
            if self.calls > 1:
                raise OSError("disk detached")
            return b"x" * size

        def seek(self, offset: int, whence: int = 0) -> int:
            self.position = DEFAULT_CHUNK_SIZE * 2 if whence == 2 else offset
            return self.position

        def tell(self) -> int:
            return self.position

        def seekable(self) -> bool:
            return True

    async def scenario() -> None:
        invoker = FakeInvoker([types.BoolTrue(), types.BoolTrue()])
        with pytest.raises(OSError, match="disk detached"):
            await upload_file(invoker, cast(Any, ExplodingReader()), file_name="boom.bin")

    run(scenario())


def test_upload_file_cancels_pending_part_tasks_when_outer_upload_is_cancelled(upload_spools: list[BinaryIO]) -> None:
    async def scenario() -> None:
        started = asyncio.Event()
        active = 0
        cancelled = 0

        async def invoke(request: object, **kwargs: object) -> object:
            nonlocal active, cancelled
            del request, kwargs
            active += 1
            if active >= 2:
                started.set()
            try:
                await asyncio.sleep(60)
            finally:
                cancelled += 1

        task = asyncio.create_task(upload_file(invoke, iter((b"x" * (4 * 1024),)), part_size=1024, concurrency=2))
        await asyncio.wait_for(started.wait(), timeout=1.0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert cancelled >= 2
        assert len(upload_spools) == 1
        assert upload_spools[0].closed

    run(scenario())


def test_upload_file_uses_small_file_parts_and_md5() -> None:
    async def scenario() -> None:
        payload = b"a" * DEFAULT_CHUNK_SIZE + b"xyz"
        progress: list[tuple[int, int | None]] = []
        invoker = FakeInvoker([types.BoolTrue(), types.BoolTrue()])
        result = await upload_file(
            invoker,
            payload,
            file_name="small.bin",
            progress=lambda current, total: progress.append((current, total)),
            file_id=5,
        )
        assert isinstance(result.input_file, types.InputFile)
        assert result.input_file.id == 5
        assert result.input_file.parts == 2
        assert result.input_file.name == "small.bin"
        assert result.input_file.md5_checksum == hashlib.md5(payload, usedforsecurity=False).hexdigest()
        assert [type(request) for request in invoker.requests] == [
            functions.UploadSaveFilePart,
            functions.UploadSaveFilePart,
        ]
        assert invoker.requests[0].file_part == 0
        assert invoker.requests[0].bytes == payload[:DEFAULT_CHUNK_SIZE]
        assert invoker.requests[1].file_part == 1
        assert invoker.requests[1].bytes == b"xyz"
        assert progress == [(DEFAULT_CHUNK_SIZE, len(payload)), (len(payload), len(payload))]

    run(scenario())


def test_upload_file_uses_big_file_branch() -> None:
    async def scenario() -> None:
        payload = b"b" * (BIG_FILE_THRESHOLD + 1)
        parts = (len(payload) + DEFAULT_CHUNK_SIZE - 1) // DEFAULT_CHUNK_SIZE
        invoker = FakeInvoker([types.BoolTrue()] * parts)
        result = await upload_file(invoker, payload, file_name="big.bin", file_id=6)
        assert isinstance(result.input_file, types.InputFileBig)
        assert result.big is True
        assert result.md5_checksum is None
        assert result.parts == parts
        assert all(isinstance(request, functions.UploadSaveBigFilePart) for request in invoker.requests)
        assert invoker.requests[0].file_total_parts == parts
        assert invoker.requests[-1].file_part == parts - 1

    run(scenario())


def test_upload_file_grows_part_size_to_respect_max_file_parts() -> None:
    async def scenario() -> None:
        payload = b"c" * (5 * 1024)
        invoker = FakeInvoker([types.BoolTrue(), types.BoolTrue(), types.BoolTrue()])
        result = await upload_file(
            invoker, payload, file_name="capped.bin", part_size=1024, max_file_parts=4, file_id=12
        )
        assert result.part_size == 2048
        assert result.parts == 3
        assert [len(request.bytes) for request in invoker.requests] == [2048, 2048, 1024]

    run(scenario())


def test_client_reads_upload_limit_parts_from_app_config() -> None:
    async def scenario() -> None:
        config = types.HelpAppConfig(
            hash=123,
            config=types.JsonObject(
                value=(
                    types.JsonObjectValue(key="upload_max_fileparts", value=types.JsonNumber(value=4096.0)),
                    types.JsonObjectValue(
                        key="small_queue_max_active_operations_count", value=types.JsonNumber(value=7.0)
                    ),
                    types.JsonObjectValue(
                        key="large_queue_max_active_operations_count", value=types.JsonNumber(value=3.0)
                    ),
                )
            ),
        )
        sender = FakeSender([config])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender = sender
        await client.connect()
        assert await client._upload_limit_parts_from_app_config() == 4096
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.HelpGetAppConfig)
        assert request.hash == 0
        assert client._media_schedulers.download_small_limit == 7
        assert client._media_schedulers.download_large_limit == 3

    run(scenario())


def test_upload_file_spools_unknown_size_iterables_and_retries_false_parts(upload_spools: list[BinaryIO]) -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([types.BoolFalse(), types.BoolTrue()])
        source = (chunk for chunk in (b"ab", b"cd"))
        result = await upload_file(invoker, source, file_name="stream.bin", part_size=1024, file_id=7)
        assert isinstance(result.input_file, types.InputFile)
        assert result.size == 4
        assert [request.file_part for request in invoker.requests] == [0, 0]
        assert invoker.requests[0].bytes == b"abcd"
        assert len(upload_spools) == 1
        assert upload_spools[0].closed

    run(scenario())


def test_upload_file_retries_transient_part_exceptions_at_media_layer() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([ClientDisconnected("sender disconnected"), types.BoolTrue()])
        result = await upload_file(invoker, b"abc", part_size=1024, max_retries=1, file_id=8)
        assert result.size == 3
        assert [request.file_part for request in invoker.requests] == [0, 0]

    run(scenario())


def test_upload_file_does_not_retry_non_transient_rpc_errors() -> None:
    async def scenario() -> None:
        requests: list[object] = []

        async def invoke(request: object, **kwargs: object) -> object:
            del kwargs
            requests.append(request)
            raise RpcError("FILE_PART_INVALID", code=400)

        with pytest.raises(RpcError, match="FILE_PART_INVALID"):
            await upload_file(invoke, b"abc", part_size=1024, max_retries=3)
        assert len(requests) == 1

    run(scenario())


def test_upload_file_sleeps_and_retries_flood_waits_within_threshold() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([classify_rpc_error(RpcError("FLOOD_PREMIUM_WAIT_0", code=420)), types.BoolTrue()])
        result = await upload_file(invoker, b"abc", part_size=1024, max_retries=1, file_id=9)
        assert result.size == 3
        assert [request.file_part for request in invoker.requests] == [0, 0]
        # The media layer owns flood sleeping: client-level sleeping must be disabled.
        assert all(kwargs["flood_sleep_threshold"] == 0 for kwargs in invoker.kwargs)

    run(scenario())


def test_upload_file_floods_do_not_consume_the_transient_retry_budget() -> None:
    async def scenario() -> None:
        # Four flood waits on one part must not exhaust a non-flood retry budget of max_retries=1
        invoker = FakeInvoker([FloodWait(0), FloodWait(0), FloodWait(0), FloodWait(0), types.BoolTrue()])
        result = await upload_file(invoker, b"abc", part_size=1024, max_retries=1, file_id=9)
        assert result.size == 3
        assert [request.file_part for request in invoker.requests] == [0, 0, 0, 0, 0]

    run(scenario())


def test_upload_flood_retry_sleep_only_uses_large_floor_for_zero_wait(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        sleeps: list[float] = []

        async def sleep(delay: float) -> None:
            sleeps.append(delay)

        jitter_args: list[tuple[float, float]] = []

        def uniform(low: float, high: float) -> float:
            jitter_args.append((low, high))
            return high

        monkeypatch.setattr("miniproto.media.upload.asyncio.sleep", sleep)
        monkeypatch.setattr("miniproto.media.upload.random.uniform", uniform)
        await media_upload._sleep_before_retry(FloodWait(2), 0, big=True)
        await media_upload._sleep_before_retry(FloodWait(0), 0, big=True)
        assert jitter_args == [(0.0, 0.3), (0.0, 0.3)]
        assert sleeps[0] == pytest.approx(2.3)
        assert sleeps[1] == pytest.approx(1.3)

    run(scenario())


def test_upload_file_aborts_on_flood_wait_beyond_threshold() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([FloodWait(60)])
        with pytest.raises(FloodWait):
            await upload_file(invoker, b"abc", part_size=1024, max_retries=3)
        assert len(invoker.requests) == 1

    run(scenario())


def test_upload_file_flood_threshold_is_a_hard_cap_override() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([FloodWait(0)])
        with pytest.raises(FloodWait):
            await upload_file(invoker, b"abc", part_size=1024, max_retries=3, flood_sleep_threshold=None)
        assert len(invoker.requests) == 1

    run(scenario())


def test_backoff_delay_grows_exponentially_with_jitter_and_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    for endpoint, expected in ((0, (0.4, 0.8, 1.6, 8.0)), (1, (0.6, 1.2, 2.4, 12.0))):
        monkeypatch.setattr("miniproto.media.retry.random.uniform", lambda low, high, endpoint=endpoint: (low, high)[endpoint])  # fmt: skip
        assert [backoff_delay(attempt) for attempt in (0, 1, 2, 30)] == pytest.approx(expected)


def test_upload_retry_backoff_sleeps_nonzero_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        sleeps: list[float] = []

        original_sleep = asyncio.sleep

        async def recording_sleep(delay: float) -> None:
            sleeps.append(delay)
            await original_sleep(0)

        monkeypatch.setattr("miniproto.media.upload.asyncio.sleep", recording_sleep)
        invoker = FakeInvoker(
            [ClientDisconnected("sender disconnected"), ClientDisconnected("sender disconnected"), types.BoolTrue()]
        )
        result = await upload_file(invoker, b"abc", part_size=1024, max_retries=2, file_id=10)
        assert result.size == 3
        retry_sleeps = [delay for delay in sleeps if delay > 0]
        assert len(retry_sleeps) == 2
        # Second retry must back off further than the first (0.5s * 2^attempt +/- 20%).
        assert retry_sleeps[1] > retry_sleeps[0]

    run(scenario())


def test_upload_file_raises_after_missing_part_retries_are_exhausted() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([types.BoolFalse(), types.BoolFalse()])
        with pytest.raises(MediaUploadError):
            await upload_file(invoker, b"abc", part_size=1024, max_retries=1)

    run(scenario())


def test_upload_file_enforces_memory_ceiling() -> None:
    async def scenario() -> None:
        with pytest.raises(ValueError, match="max_buffer_size"):
            await upload_file(bad_invoker, b"abc", part_size=1024, concurrency=2, max_buffer_size=1024)

    async def bad_invoker(request: object, **kwargs: object) -> object:
        raise AssertionError("upload should validate before invoking")

    run(scenario())


def test_client_send_file_uploads_and_sends_generated_media_request() -> None:
    async def scenario() -> None:
        document = types.Document(
            id=100,
            access_hash=200,
            file_reference=b"ref",
            date=1_700_000_000,
            mime_type="text/plain",
            size=5,
            dc_id=2,
            attributes=(types.DocumentAttributeFilename(file_name="note.txt"),),
        )
        raw_media = types.MessageMediaDocument(document=document)
        sender = FakeSender(
            [
                types.BoolTrue(),
                types.UpdateShortSentMessage(id=300, pts=1, pts_count=1, date=1_700_000_001, media=raw_media),
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender = sender
        await client.connect()
        message = await client.send_file(
            "@alice",
            b"hello",
            file_name="note.txt",
            caption="see **file**",
            parse_mode="markdown-lite",
            random_id=9,
            media_lanes=0,
        )
        upload_request = inner_request(sender.requests[0])
        send_request = inner_request(sender.requests[1])
        assert isinstance(upload_request, functions.UploadSaveFilePart)
        assert upload_request.bytes == b"hello"
        assert isinstance(send_request, functions.MessagesSendMedia)
        assert isinstance(send_request.peer, types.InputPeerUser)
        assert isinstance(send_request.media, types.InputMediaUploadedDocument)
        assert isinstance(send_request.media.file, types.InputFile)
        assert send_request.media.file.name == "note.txt"
        assert send_request.media.mime_type == "text/plain"
        assert send_request.media.attributes == (types.DocumentAttributeFilename(file_name="note.txt"),)
        assert send_request.message == "see file"
        assert send_request.entities == (types.MessageEntityBold(offset=4, length=4),)
        assert send_request.random_id == 9
        assert message.id == 300
        assert message.peer == Peer(id=7, kind="user", access_hash=77)
        assert message.media is not None
        assert message.media.file_name == "note.txt"
        assert message.media.location == types.InputDocumentFileLocation(
            id=100, access_hash=200, file_reference=b"ref", thumb_size=""
        )

    run(scenario())


def test_client_send_file_uses_dedicated_media_lanes() -> None:
    async def scenario() -> None:
        document = types.Document(
            id=101,
            access_hash=201,
            file_reference=b"ref",
            date=1_700_000_000,
            mime_type="application/octet-stream",
            size=2048,
            dc_id=2,
            attributes=(types.DocumentAttributeFilename(file_name="lanes.bin"),),
        )
        raw_media = types.MessageMediaDocument(document=document)
        main_sender = FakeSender(
            [types.UpdateShortSentMessage(id=301, pts=1, pts_count=1, date=1_700_000_001, media=raw_media)]
        )
        lane_senders = [FakeSender([types.BoolTrue()]), FakeSender([types.BoolTrue()])]
        built_senders: list[FakeSender] = []

        def sender_factory(record: SessionRecord) -> FakeSender:
            del record
            sender = lane_senders[len(built_senders)]
            built_senders.append(sender)
            return sender

        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender = main_sender
        client._sender_factory = sender_factory
        await client.connect()
        message = await client.send_file(
            "@alice", b"a" * 1024 + b"b" * 1024, file_name="lanes.bin", part_size=1024, concurrency=2, random_id=10
        )
        assert message.id == 301
        assert built_senders == lane_senders
        assert [len(sender.requests) for sender in lane_senders] == [1, 1]
        assert len(main_sender.requests) == 1
        upload_requests: list[functions.UploadSaveFilePart] = []
        for request in (inner_request(sender.requests[0]) for sender in lane_senders):
            assert isinstance(request, functions.UploadSaveFilePart)
            upload_requests.append(request)
        assert {request.file_part: request.bytes for request in upload_requests} == {0: b"a" * 1024, 1: b"b" * 1024}
        assert isinstance(inner_request(main_sender.requests[0]), functions.MessagesSendMedia)

    run(scenario())


def test_client_send_file_reuses_miniproto_file_id_without_upload() -> None:
    async def scenario() -> None:
        document = types.Document(
            id=102,
            access_hash=202,
            file_reference=b"existing-ref",
            date=1_700_000_000,
            mime_type="application/octet-stream",
            size=4096,
            dc_id=2,
            attributes=(types.DocumentAttributeFilename(file_name="existing.bin"),),
        )
        file_id = encode_file_id(document)
        raw_media = types.MessageMediaDocument(document=document)
        sender = FakeSender(
            [types.UpdateShortSentMessage(id=302, pts=1, pts_count=1, date=1_700_000_001, media=raw_media)]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender = sender
        await client.connect()
        message = await client.send_file("@alice", file_id, caption="reuse", random_id=11)
        assert message.id == 302
        assert len(sender.requests) == 1
        send_request = inner_request(sender.requests[0])
        assert isinstance(send_request, functions.MessagesSendMedia)
        assert isinstance(send_request.media, types.InputMediaDocument)
        assert isinstance(send_request.media.id, types.InputDocument)
        assert send_request.media.id.id == document.id
        assert send_request.media.id.access_hash == document.access_hash
        assert send_request.media.id.file_reference == document.file_reference

    run(scenario())


def test_client_send_file_rejects_unknown_options() -> None:
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        with pytest.raises(TypeError, match="unsupported send_file options"):
            await client.send_file("@alice", b"hello", unsupported=True)

    run(scenario())


MAX_PART_BYTES = 512 * 1024


SOURCE_KINDS = ("reader", "async_reader", "iterable", "async_iterable")


class RecordingSpool(io.BytesIO):
    def __init__(self) -> None:
        super().__init__()
        self.written = 0
        self.writes = 0

    def write(self, buffer: Any, /) -> int:
        self.written += len(buffer)
        self.writes += 1
        return super().write(buffer)


@pytest.fixture
def spool(monkeypatch: pytest.MonkeyPatch) -> Iterator[RecordingSpool]:
    temporary = RecordingSpool()
    monkeypatch.setattr(media_upload.tempfile, "TemporaryFile", lambda *args, **kwargs: temporary)
    try:
        yield temporary
    finally:
        io.BytesIO.close(temporary)


@dataclass
class SourceProbe:
    chunks: Iterator[bytes]
    consumed: int = 0
    calls: int = 0
    closed: bool = False
    pending: bytes = b""
    on_chunk: Callable[[], None] | None = None
    read_sizes: list[int] = field(default_factory=list)

    def observe(self, payload: bytes) -> bytes:
        self.consumed += len(payload)
        self.calls += 1
        if self.on_chunk is not None:
            self.on_chunk()
        return payload

    def read(self, size: int) -> bytes:
        self.read_sizes.append(size)
        if not self.pending:
            self.pending = next(self.chunks, b"")
        payload, self.pending = self.pending[:size], self.pending[size:]
        return self.observe(payload)

    def iterate(self) -> Iterator[bytes]:
        for chunk in self.chunks:
            yield self.observe(chunk)

    def close(self) -> None:
        self.closed = True

    def source(self, kind: str) -> Any:
        if kind == "reader":
            return self
        if kind == "async_reader":
            probe = self

            class AsyncReader:
                async def read(self, size: int) -> bytes:
                    return probe.read(size)

                def close(self) -> None:
                    probe.close()

            return AsyncReader()
        if kind == "async_iterable":

            async def chunks() -> AsyncIterator[bytes]:
                for chunk in self.iterate():
                    yield chunk

            return chunks()
        return self.iterate()


@dataclass
class InvokerProbe:
    registered: list[int] = field(default_factory=list)
    parts: dict[int, bytes] = field(default_factory=dict)

    def register_transfer(self, size: int) -> None:
        self.registered.append(size)

    async def __call__(self, request: object, **kwargs: object) -> bool:
        assert isinstance(request, functions.UploadSaveFilePart)
        self.parts[request.file_part] = request.bytes
        return True


@pytest.mark.parametrize("kind", SOURCE_KINDS)
@pytest.mark.parametrize("max_parts", (1, 2))
def test_unknown_upload_stops_before_crossing_write(spool: RecordingSpool, kind: str, max_parts: int) -> None:
    async def scenario() -> None:
        limit = max_parts * MAX_PART_BYTES
        probe = SourceProbe(iter([b"a" * (64 * 1024)] * (8 * max_parts) + [b"!", b"unconsumed-tail"]))
        invoker = InvokerProbe()
        with pytest.raises(MediaUploadError):
            await upload_file(invoker, probe.source(kind), part_size=64 * 1024, max_file_parts=max_parts)
        assert probe.consumed == limit + 1
        assert spool.written == limit
        assert spool.closed
        assert not probe.closed
        assert invoker.registered == []
        assert invoker.parts == {}
        if kind in {"reader", "async_reader"}:
            assert probe.read_sizes[-1] == 1

    event_loop.run(scenario())


@pytest.mark.parametrize("kind", SOURCE_KINDS)
@pytest.mark.parametrize("size", (MAX_PART_BYTES - 1, MAX_PART_BYTES))
def test_unknown_upload_accepts_boundary_after_part_growth(spool: RecordingSpool, kind: str, size: int) -> None:
    async def scenario() -> None:
        payload = b"a" * 1023 + b"b" * (size - 1024) + b"z"
        probe = SourceProbe(iter((payload[:1023], payload[1023:-1], payload[-1:])))
        invoker = InvokerProbe()
        result = await upload_file(invoker, probe.source(kind), part_size=1024, max_file_parts=1)
        assert result.size == size
        assert result.part_size == MAX_PART_BYTES
        assert result.parts == 1
        assert invoker.parts == {0: payload}
        assert invoker.registered == [size]
        assert spool.written == size
        assert spool.closed
        assert not probe.closed

    event_loop.run(scenario())


@pytest.mark.parametrize("kind", ("iterable", "async_iterable"))
def test_unknown_upload_rejects_oversized_first_chunk_without_writing(spool: RecordingSpool, kind: str) -> None:
    async def scenario() -> None:
        probe = SourceProbe(iter((b"x" * (MAX_PART_BYTES + 1), b"unconsumed")))
        invoker = InvokerProbe()
        with pytest.raises(MediaUploadError):
            await upload_file(invoker, probe.source(kind), max_file_parts=1)
        assert probe.calls == 1
        assert spool.writes == 0
        assert spool.closed
        assert invoker.registered == []
        assert invoker.parts == {}

    event_loop.run(scenario())


@pytest.mark.parametrize("kind", SOURCE_KINDS)
def test_unknown_upload_preserves_explicit_unlimited_parts(spool: RecordingSpool, kind: str) -> None:
    async def scenario() -> None:
        payload = b"a" * MAX_PART_BYTES + b"z"
        probe = SourceProbe(iter((payload[:MAX_PART_BYTES], payload[-1:])))
        invoker = InvokerProbe()
        result = await upload_file(invoker, probe.source(kind), max_file_parts=None)
        assert result.size == MAX_PART_BYTES + 1
        assert result.parts == 2
        assert invoker.parts == {0: payload[:-1], 1: b"z"}
        assert spool.written == len(payload)
        assert spool.closed

    event_loop.run(scenario())


@pytest.mark.parametrize("kind,payload", [(kind, b"x") for kind in SOURCE_KINDS] + [("iterable", b""), ("async_iterable", b"")])  # fmt: skip
def test_immediate_upload_producers_allow_preparation_cancellation(spool: RecordingSpool, kind: str, payload: bytes) -> None:  # fmt: skip
    async def scenario() -> None:
        probe = SourceProbe(iter([payload] * 256))
        invoker = InvokerProbe()

        def cancel_after_first_chunk() -> None:
            if probe.calls == 1:
                asyncio.get_running_loop().call_soon(task.cancel)

        probe.on_chunk = cancel_after_first_chunk
        task = asyncio.create_task(upload_file(invoker, probe.source(kind), max_file_parts=None))
        with pytest.raises(asyncio.CancelledError):
            await task
        assert 0 < probe.calls < 256
        assert spool.written == probe.consumed
        assert spool.closed
        assert not probe.closed
        assert invoker.registered == []
        assert invoker.parts == {}

    event_loop.run(scenario())


def test_early_limit_failure_survives_spool_close_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    class CloseFailingSpool(RecordingSpool):
        def close(self) -> None:
            super().close()
            raise OSError("spool close failed")

    async def scenario() -> None:
        temporary = CloseFailingSpool()
        monkeypatch.setattr(media_upload.tempfile, "TemporaryFile", lambda *args, **kwargs: temporary)
        try:
            with pytest.raises(MediaUploadError):
                await upload_file(InvokerProbe(), iter((b"x" * (MAX_PART_BYTES + 1),)), max_file_parts=1)
            assert temporary.closed
            assert temporary.writes == 0
        finally:
            io.BytesIO.close(temporary)

    event_loop.run(scenario())


@pytest.mark.parametrize("kind", ("bytes", "seekable", "path"))
@pytest.mark.parametrize("size", (MAX_PART_BYTES, MAX_PART_BYTES + 1))
def test_known_length_uploads_keep_part_ceiling_without_spooling(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, kind: str, size: int) -> None:  # fmt: skip
    def reject_spool(*args: object, **kwargs: object) -> None:
        raise AssertionError("known-size sources must not be spooled")

    monkeypatch.setattr(media_upload.tempfile, "TemporaryFile", reject_spool)

    async def scenario() -> None:
        payload = b"x" * size
        source: Any = payload
        reader = io.BytesIO(b"prefix" + payload)
        reader.seek(6)
        if kind == "seekable":
            source = reader
        elif kind == "path":
            source = tmp_path / "known-size.bin"
            source.write_bytes(payload)
        invoker = InvokerProbe()
        try:
            if size > MAX_PART_BYTES:
                with pytest.raises(MediaUploadError):
                    await upload_file(invoker, source, part_size=1024, max_file_parts=1)
                assert invoker.registered == []
                assert invoker.parts == {}
            else:
                result = await upload_file(invoker, source, part_size=1024, max_file_parts=1)
                assert result.parts == 1
                assert result.part_size == MAX_PART_BYTES
                assert invoker.parts == {0: payload}
            assert not reader.closed
        finally:
            reader.close()

    event_loop.run(scenario())
