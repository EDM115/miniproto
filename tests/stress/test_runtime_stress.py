from __future__ import annotations

import os
from dataclasses import dataclass, field

import pytest

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    PeerCacheEntry,
    SessionRecord,
    event_loop,
)
from miniproto.media import DEFAULT_CHUNK_SIZE, download_file, upload_file
from miniproto.raw import functions, types
from miniproto.types import Update
from miniproto.updates.manager import UpdateManager

pytestmark = pytest.mark.skipif(
    os.environ.get("MINIPROTO_STRESS") != "1", reason="set MINIPROTO_STRESS=1 to run stress tests"
)

AUTH_KEY = b"s" * 256


@dataclass(slots=True)
class FakeSender:
    responses: list[object]
    requests: list[object] = field(default_factory=list)
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


@dataclass(slots=True)
class UploadInvoker:
    requests: list[object] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        self.requests.append(request)
        return types.BoolTrue()


@dataclass(slots=True)
class DownloadInvoker:
    payload: bytes
    requests: list[object] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        self.requests.append(request)
        if not isinstance(request, functions.UploadGetFile):
            raise TypeError(f"unexpected request: {type(request).__name__}")
        offset = int(request.offset)
        limit = int(request.limit)
        return types.UploadFile(
            type=types.StorageFileUnknown(), mtime=1_700_000_000, bytes=self.payload[offset : offset + limit]
        )


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


def test_stress_large_upload_and_download_roundtrip_buffers() -> None:
    async def scenario() -> None:
        payload = bytes((index * 29) % 256 for index in range(16 * 1024 * 1024))
        upload_invoker = UploadInvoker()
        upload = await upload_file(
            upload_invoker, payload, file_name="stress.bin", part_size=DEFAULT_CHUNK_SIZE, concurrency=8, file_id=55
        )
        assert upload.size == len(payload)
        assert len(upload_invoker.requests) == len(payload) // DEFAULT_CHUNK_SIZE

        download_invoker = DownloadInvoker(payload)
        location = types.InputDocumentFileLocation(id=10, access_hash=20, file_reference=b"ref", thumb_size="")
        download = await download_file(
            download_invoker, location, limit=len(payload), part_size=DEFAULT_CHUNK_SIZE, total_size=len(payload)
        )
        assert download.data == payload
        assert download.bytes_downloaded == len(payload)

    run(scenario())


def test_stress_dispatches_many_updates_without_loss() -> None:
    async def scenario() -> None:
        count = 50_000
        manager = UpdateManager(
            ClientConfig(api_id=1, api_hash="hash", update_queue_size=count + 1),
            InMemorySessionStorage(),
            _unexpected_invoke,
        )
        for index in range(count):
            await manager.emit_update(Update(raw=index))
        received = [await anext(manager.iter_updates()) for _ in range(count)]
        assert len(received) == count
        assert received[0].raw == 0
        assert received[-1].raw == count - 1

    run(scenario())


def test_stress_sends_many_messages_through_cached_peer() -> None:
    async def scenario() -> None:
        count = 1_000
        sender = FakeSender(
            [
                types.UpdateShortSentMessage(id=index, pts=index, pts_count=1, date=1_700_000_000 + index)
                for index in range(count)
            ]
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender = sender
        await client.connect()
        for index in range(count):
            message = await client.send_message("@alice", f"message {index}", random_id=index + 1)
            assert message.id == index
        assert len(sender.requests) == count

    run(scenario())


def test_stress_repeated_client_lifecycle_does_not_leak_tasks() -> None:
    async def scenario() -> None:
        for _ in range(500):
            client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
            await client.connect()
            await client.disconnect()
            assert not client.is_connected

    run(scenario())


async def _unexpected_invoke(request: object) -> object:
    raise AssertionError(f"unexpected invoke: {type(request).__name__}")
