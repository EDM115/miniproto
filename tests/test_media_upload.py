from __future__ import annotations

import asyncio
import hashlib
from dataclasses import dataclass, field
from typing import Any

import pytest

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    Peer,
    SessionRecord,
)
from miniproto.media import BIG_FILE_THRESHOLD, DEFAULT_CHUNK_SIZE, MediaUploadError, upload_file
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry

AUTH_KEY = b"m" * 256


@dataclass(slots=True)
class FakeInvoker:
    responses: list[object]
    requests: list[Any] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        self.requests.append(request)
        if not self.responses:
            raise AssertionError("fake invoker has no queued response")
        return self.responses.pop(0)


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
    return asyncio.run(coro)


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
    assert isinstance(wrapped, functions.InvokeWithLayer)
    assert isinstance(wrapped.query, functions.InitConnection)
    return wrapped.query.query


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


def test_client_send_file_rejects_unknown_options() -> None:
    async def scenario() -> None:
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
        with pytest.raises(TypeError, match="unsupported send_file options"):
            await client.send_file("@alice", b"hello", unsupported=True)

    run(scenario())
