from __future__ import annotations

import asyncio
import hashlib
from dataclasses import dataclass, field
from typing import Any, cast

import pytest

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
        request_timeout: float | None = None,
    ) -> object:
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


def test_upload_file_uses_small_file_parts_and_md5() -> None:
    async def scenario() -> None:
        payload = b"a" * (DEFAULT_CHUNK_SIZE + 3)
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
        assert (
            result.input_file.md5_checksum
            == hashlib.md5(payload, usedforsecurity=False).hexdigest()
        )
        assert [type(request) for request in invoker.requests] == [
            functions.UploadSaveFilePart,
            functions.UploadSaveFilePart,
        ]
        assert invoker.requests[0].file_part == 0
        assert len(invoker.requests[0].bytes) == DEFAULT_CHUNK_SIZE
        assert invoker.requests[1].file_part == 1
        assert invoker.requests[1].bytes == b"aaa"
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
        assert all(
            isinstance(request, functions.UploadSaveBigFilePart) for request in invoker.requests
        )
        assert invoker.requests[0].file_total_parts == parts
        assert invoker.requests[-1].file_part == parts - 1

    run(scenario())


def test_upload_file_spools_unknown_size_iterables_and_retries_false_parts() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([types.BoolFalse(), types.BoolTrue()])
        source = (chunk for chunk in (b"ab", b"cd"))
        result = await upload_file(
            invoker, source, file_name="stream.bin", part_size=1024, file_id=7
        )
        assert isinstance(result.input_file, types.InputFile)
        assert result.size == 4
        assert [request.file_part for request in invoker.requests] == [0, 0]
        assert invoker.requests[0].bytes == b"abcd"

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
        invoker = FakeInvoker(
            [classify_rpc_error(RpcError("FLOOD_PREMIUM_WAIT_0", code=420)), types.BoolTrue()]
        )
        result = await upload_file(invoker, b"abc", part_size=1024, max_retries=1, file_id=9)
        assert result.size == 3
        assert [request.file_part for request in invoker.requests] == [0, 0]
        # The media layer owns flood sleeping: client-level sleeping must be disabled.
        assert all(kwargs["flood_sleep_threshold"] == 0 for kwargs in invoker.kwargs)

    run(scenario())


def test_upload_file_floods_do_not_consume_the_transient_retry_budget() -> None:
    async def scenario() -> None:
        # 4 consecutive floods on one part with max_retries=1: server pacing
        # must not abort the upload (one flood used to kill uploads at 99%).
        invoker = FakeInvoker(
            [FloodWait(0), FloodWait(0), FloodWait(0), FloodWait(0), types.BoolTrue()]
        )
        result = await upload_file(invoker, b"abc", part_size=1024, max_retries=1, file_id=9)
        assert result.size == 3
        assert [request.file_part for request in invoker.requests] == [0, 0, 0, 0, 0]

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
            await upload_file(
                invoker, b"abc", part_size=1024, max_retries=3, flood_sleep_threshold=None
            )
        assert len(invoker.requests) == 1

    run(scenario())


def test_backoff_delay_grows_exponentially_with_jitter_and_cap() -> None:
    for _ in range(50):
        first = backoff_delay(0)
        second = backoff_delay(1)
        third = backoff_delay(2)
        capped = backoff_delay(30)
        assert 0.4 <= first <= 0.6
        assert 0.8 <= second <= 1.2
        assert 1.6 <= third <= 2.4
        assert capped <= 12.0


def test_upload_retry_backoff_sleeps_nonzero_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        sleeps: list[float] = []

        original_sleep = asyncio.sleep

        async def recording_sleep(delay: float) -> None:
            sleeps.append(delay)
            await original_sleep(0)

        monkeypatch.setattr("miniproto.media.upload.asyncio.sleep", recording_sleep)
        invoker = FakeInvoker(
            [
                ClientDisconnected("sender disconnected"),
                ClientDisconnected("sender disconnected"),
                types.BoolTrue(),
            ]
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
            await upload_file(
                bad_invoker, b"abc", part_size=1024, concurrency=2, max_buffer_size=1024
            )

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
                types.UpdateShortSentMessage(
                    id=300, pts=1, pts_count=1, date=1_700_000_001, media=raw_media
                ),
            ]
        )
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
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
        assert send_request.media.attributes == (
            types.DocumentAttributeFilename(file_name="note.txt"),
        )
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
            [
                types.UpdateShortSentMessage(
                    id=301, pts=1, pts_count=1, date=1_700_000_001, media=raw_media
                )
            ]
        )
        lane_senders = [FakeSender([types.BoolTrue()]), FakeSender([types.BoolTrue()])]
        built_senders: list[FakeSender] = []

        def sender_factory(record: SessionRecord) -> FakeSender:
            del record
            sender = lane_senders[len(built_senders)]
            built_senders.append(sender)
            return sender

        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
        client._sender = main_sender
        client._sender_factory = sender_factory
        await client.connect()
        message = await client.send_file(
            "@alice",
            b"a" * 2048,
            file_name="lanes.bin",
            part_size=1024,
            concurrency=2,
            random_id=10,
        )
        assert message.id == 301
        assert built_senders == lane_senders
        assert [len(sender.requests) for sender in lane_senders] == [1, 1]
        assert len(main_sender.requests) == 1
        upload_requests: list[functions.UploadSaveFilePart] = []
        for request in (inner_request(sender.requests[0]) for sender in lane_senders):
            assert isinstance(request, functions.UploadSaveFilePart)
            upload_requests.append(request)
        assert {request.file_part for request in upload_requests} == {0, 1}
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
            [
                types.UpdateShortSentMessage(
                    id=302, pts=1, pts_count=1, date=1_700_000_001, media=raw_media
                )
            ]
        )
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
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
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
        with pytest.raises(TypeError, match="unsupported send_file options"):
            await client.send_file("@alice", b"hello", unsupported=True)

    run(scenario())
