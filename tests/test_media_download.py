from __future__ import annotations

import asyncio
import base64
import hashlib
import io
import json
import logging
import random
import sys
import threading
import time
import weakref
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from types import FrameType
from typing import Any, BinaryIO, cast

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
    iter_download,
)
from miniproto.crypto.mtproto import media_ctr_crypt
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
from miniproto.media.download import iter_download_media
from miniproto.observability import InMemoryMetrics, get_metrics_sink, set_metrics_sink
from miniproto.raw import functions, types

AUTH_KEY = b"m" * 256
BOT_CREDENTIAL = "42:secret"


@dataclass(slots=True)
class FakeInvoker:
    responses: list[object]
    requests: list[Any] = field(default_factory=list)
    cdn_requests: list[Any] = field(default_factory=list)
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

    async def invoke_cdn(self, request: object, *, dc_id: int, **kwargs: object) -> object:
        assert dc_id == 4
        self.cdn_requests.append(request)
        self.kwargs.append(dict(kwargs))
        if not self.responses:
            raise AssertionError("fake CDN invoker has no queued response")
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
class PlainHashInvoker:
    payload: bytes
    hashes: tuple[types.FileHash, ...]
    corrupt_offsets: set[int] = field(default_factory=set)
    requests: list[Any] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        await asyncio.sleep(0)
        if isinstance(request, functions.UploadGetFileHashes):
            return self.hashes
        assert isinstance(request, functions.UploadGetFile)
        payload = self.payload[request.offset : request.offset + request.limit]
        if request.offset in self.corrupt_offsets and payload:
            payload = bytes([payload[0] ^ 0xFF]) + payload[1:]
        return upload_file_part(payload)


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


def test_iter_download_streams_ordered_chunks_before_transfer_completion() -> None:
    async def scenario() -> None:
        invoker = DelayedMapOffsetInvoker(
            responses={0: b"a" * 1024, 1024: b"b" * 1024, 2048: b"c" * 1024}, delays={0: 0.01, 1024: 1.0, 2048: 1.0}
        )
        iterator = media_download.iter_download(
            invoker,
            document_location(),
            limit=3 * 1024,
            total_size=3 * 1024,
            part_size=1024,
            concurrency=3,
            adaptive_concurrency=False,
            adaptive_part_size=False,
        )
        first = await asyncio.wait_for(anext(iterator), 0.5)
        assert first == b"a" * 1024
        assert {request.offset for request in invoker.requests} == {0, 1024, 2048}
        await iterator.aclose()
        assert invoker.cancelled_offsets == {1024, 2048}

    run(scenario())


@pytest.mark.parametrize("interface", ["media", "client"])
def test_public_iter_download_close_joins_owned_part_cancellation(
    interface: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def scenario() -> None:
        invoker = DelayedMapOffsetInvoker(
            responses={0: b"a" * 1024, 1024: b"b" * 1024, 2048: b"c" * 1024}, delays={0: 0.01, 1024: 1.0, 2048: 1.0}
        )
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        options = {
            "limit": 3 * 1024,
            "total_size": 3 * 1024,
            "part_size": 1024,
            "concurrency": 3,
            "adaptive_concurrency": False,
            "adaptive_part_size": False,
            "launch_stagger": False,
        }
        if interface == "client":
            monkeypatch.setattr(client, "invoke", invoker)
            await client.connect()
            iterator = client.iter_download(document_location(), media_lanes=0, **options)
        else:
            iterator = media_download.iter_download_media(invoker, document_location(), **options)
        try:
            assert await asyncio.wait_for(anext(iterator), 0.5) == b"a" * 1024
            assert {request.offset for request in invoker.requests} == {0, 1024, 2048}
            await iterator.aclose()
            assert invoker.cancelled_offsets == {1024, 2048}
        finally:
            await iterator.aclose()
            await client.disconnect()

    run(scenario())


@pytest.mark.parametrize("interface", ["media", "client"])
def test_public_iter_download_close_preserves_borrowed_range_cache(
    interface: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def scenario() -> None:
        invoker = DelayedMapOffsetInvoker(responses={0: b"a" * 1024, 1024: b"b" * 1024}, delays={0: 0.01, 1024: 1.0})
        cache = DownloadRangeCache(max_bytes=4096)
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        options = {
            "limit": 2 * 1024,
            "total_size": 2 * 1024,
            "part_size": 1024,
            "concurrency": 2,
            "adaptive_concurrency": False,
            "adaptive_part_size": False,
            "launch_stagger": False,
            "range_cache": cache,
            "range_cache_key": "shared-file",
        }
        if interface == "client":
            monkeypatch.setattr(client, "invoke", invoker)
            await client.connect()
            iterator = client.iter_download(document_location(), media_lanes=0, **options)
        else:
            iterator = media_download.iter_download_media(invoker, document_location(), **options)

        async def unexpected_fetch() -> bytes:
            raise AssertionError("the cached request must already have a shared producer")

        waiter = None
        try:
            assert await asyncio.wait_for(anext(iterator), 0.5) == b"a" * 1024
            waiter = asyncio.create_task(cache.get_or_fetch("shared-file", 1024, 1024, unexpected_fetch))
            await asyncio.sleep(0)
            await iterator.aclose()
            assert not waiter.done()
            assert invoker.cancelled_offsets == set()
            assert await cache.get("shared-file", 0, 1024) == b"a" * 1024
        finally:
            await iterator.aclose()
            await cache.clear()
            if waiter is not None:
                await asyncio.gather(waiter, return_exceptions=True)
            await client.disconnect()

    run(scenario())


def test_iter_download_close_propagates_cancellation_after_part_finalizers_settle() -> None:
    async def scenario() -> None:
        cleanup_started = asyncio.Event()
        cleanup_release = asyncio.Event()
        cleanup_completed = asyncio.Event()
        part_tasks: list[asyncio.Task[Any]] = []

        async def invoke(request: object, **kwargs: object) -> object:
            del kwargs
            assert isinstance(request, functions.UploadGetFile)
            if request.offset == 0:
                return upload_file_part(b"a" * 1024)
            task = asyncio.current_task()
            assert task is not None
            part_tasks.append(task)
            try:
                await asyncio.Future()
            finally:
                cleanup_started.set()
                await cleanup_release.wait()
                cleanup_completed.set()

        iterator = media_download.iter_download(invoke, document_location(), limit=2048, part_size=1024, concurrency=2, launch_stagger=False, adaptive_part_size=False)  # fmt: skip
        assert await anext(iterator) == b"a" * 1024
        closing = asyncio.create_task(iterator.aclose())
        try:
            await asyncio.wait_for(cleanup_started.wait(), timeout=2.0)
            closing.cancel("cancel iterator close")
            loop = asyncio.get_running_loop()
            barrier = loop.create_future()
            loop.call_soon(barrier.set_result, None)
            await barrier
            assert not closing.done()
            assert not part_tasks[0].done()
            closing.cancel("repeat cancellation")
            cleanup_release.set()
            with pytest.raises(asyncio.CancelledError, match="cancel iterator close"):
                await closing
            assert cleanup_completed.is_set()
            assert part_tasks[0].done()
        finally:
            cleanup_release.set()
            await asyncio.gather(closing, *part_tasks, return_exceptions=True)
            await iterator.aclose()

    run(scenario())


def test_iter_download_reorders_concurrent_parts_and_matches_download_file() -> None:
    async def scenario() -> None:
        payload = b"a" * 1024 + b"b" * 1024 + b"c" * 1024
        streaming = DelayedMapOffsetInvoker(
            responses={0: payload[:1024], 1024: payload[1024:2048], 2048: payload[2048:]},
            delays={0: 0.03, 1024: 0.0, 2048: 0.01},
        )
        chunks = [
            chunk
            async for chunk in media_download.iter_download(
                streaming,
                document_location(),
                limit=len(payload),
                total_size=len(payload),
                part_size=1024,
                concurrency=3,
                adaptive_concurrency=False,
                adaptive_part_size=False,
            )
        ]
        materialized = await download_file(
            OffsetInvoker(payload),
            document_location(),
            limit=len(payload),
            total_size=len(payload),
            part_size=1024,
            concurrency=3,
            adaptive_concurrency=False,
            adaptive_part_size=False,
        )
        assert chunks == [payload[:1024], payload[1024:2048], payload[2048:]]
        assert b"".join(chunks) == materialized.data

    run(scenario())


def test_iter_download_consumer_backpressure_bounds_prefetched_bytes() -> None:
    async def scenario() -> None:
        invoker = SlowOffsetInvoker(b"z" * (8 * 1024))
        iterator = media_download.iter_download(
            invoker,
            document_location(),
            limit=8 * 1024,
            total_size=8 * 1024,
            part_size=1024,
            concurrency=8,
            max_in_flight_bytes=2 * 1024,
            adaptive_concurrency=False,
            adaptive_part_size=False,
        )
        assert await anext(iterator) == b"z" * 1024
        await asyncio.sleep(0.05)
        assert len(invoker.requests) <= 2
        await iterator.aclose()
        assert invoker.active == 0

    run(scenario())


def test_iter_download_can_disable_launch_stagger_for_controlled_benchmarks(monkeypatch: pytest.MonkeyPatch) -> None:
    async def scenario() -> None:
        invoker = OffsetInvoker(b"z" * (2 * 1024))

        async def fail_if_paced(self: object) -> None:
            del self
            raise AssertionError("launch pacer was used")

        monkeypatch.setattr(media_download._DownloadLaunchPacer, "wait", fail_if_paced)
        chunks = [
            chunk
            async for chunk in media_download.iter_download(
                invoker,
                document_location(),
                limit=2 * 1024,
                total_size=2 * 1024,
                part_size=1024,
                concurrency=2,
                adaptive_concurrency=False,
                adaptive_part_size=False,
                launch_stagger=False,
            )
        ]

        assert b"".join(chunks) == b"z" * (2 * 1024)

    run(scenario())


def test_client_download_options_forward_launch_stagger_control() -> None:
    default = client_module._download_media_options({})
    burst = client_module._download_media_options({"launch_stagger": False})

    assert default["launch_stagger"] is True
    assert burst["launch_stagger"] is False


def test_read_ahead_marks_scheduler_requests_as_background_priority() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=4096)
        invoker = FakeInvoker([upload_file_part(b"a" * 1024), upload_file_part(b"b" * 1024)])
        result = await download_file(
            invoker,
            document_location(),
            offset=0,
            limit=1024,
            total_size=4096,
            part_size=1024,
            concurrency=1,
            adaptive_part_size=False,
            range_cache=cache,
            range_cache_key="file",
            read_ahead_bytes=1024,
        )
        assert result.data == b"a" * 1024
        for _ in range(20):
            if len(invoker.requests) == 2:
                break
            await asyncio.sleep(0.01)
        assert len(invoker.requests) == 2
        assert "_media_priority" not in invoker.kwargs[0]
        assert invoker.kwargs[1]["_media_priority"] == "background"
        await cache.clear()

    run(scenario())


def test_plain_integrity_disabled_sends_no_hash_requests() -> None:
    async def scenario() -> None:
        payload = b"a" * 1024
        invoker = PlainHashInvoker(
            payload=payload, hashes=(types.FileHash(offset=0, limit=1024, hash=hashlib.sha256(payload).digest()),)
        )
        result = await download_file(
            invoker, document_location(), limit=len(payload), part_size=1024, concurrency=1, adaptive_part_size=False
        )
        assert result.data == payload
        assert not any(isinstance(request, functions.UploadGetFileHashes) for request in invoker.requests)

    run(scenario())


def test_plain_integrity_verifies_exact_hash_intervals_before_output() -> None:
    async def scenario() -> None:
        payload = b"a" * 1024 + b"b" * 1024
        hashes = tuple(
            types.FileHash(offset=offset, limit=1024, hash=hashlib.sha256(payload[offset : offset + 1024]).digest())
            for offset in (0, 1024)
        )
        invoker = PlainHashInvoker(payload=payload, hashes=hashes)
        chunks = [
            chunk
            async for chunk in media_download.iter_download(
                invoker,
                document_location(),
                limit=len(payload),
                total_size=len(payload),
                part_size=1024,
                concurrency=2,
                adaptive_concurrency=False,
                adaptive_part_size=False,
                verify_plain_hashes=True,
            )
        ]
        assert chunks == [payload[:1024], payload[1024:]]
        assert sum(isinstance(request, functions.UploadGetFileHashes) for request in invoker.requests) == 1

    run(scenario())


def test_plain_integrity_hashes_a_range_cache_miss_once() -> None:
    async def scenario() -> None:
        payload = b"a" * 1024
        invoker = PlainHashInvoker(
            payload=payload, hashes=(types.FileHash(offset=0, limit=1024, hash=hashlib.sha256(payload).digest()),)
        )
        cache = DownloadRangeCache(max_bytes=4096)
        metrics = InMemoryMetrics()
        previous = get_metrics_sink()
        set_metrics_sink(metrics)
        try:
            result = await download_file(
                invoker,
                document_location(),
                limit=len(payload),
                part_size=1024,
                concurrency=1,
                adaptive_part_size=False,
                range_cache=cache,
                range_cache_key="doc:10",
                verify_plain_hashes=True,
            )
        finally:
            set_metrics_sink(previous)
            await cache.clear()
        assert result.data == payload
        verified_bytes = sum(
            event.value for event in metrics.events if event.name == "media.download.plain_hash_verified_bytes"
        )
        assert verified_bytes == len(payload)

    run(scenario())


def test_plain_integrity_rejects_interval_completion_after_location_refresh() -> None:
    async def scenario() -> None:
        old_payload = b"a" * 2048
        new_payload = b"b" * 2048
        old_location = document_location()
        new_location = types.InputDocumentFileLocation(id=old_location.id, access_hash=old_location.access_hash, file_reference=b"new-ref", thumb_size=old_location.thumb_size)  # fmt: skip
        interval_started = asyncio.Event()
        release_interval = asyncio.Event()

        @dataclass(slots=True)
        class RefreshingHashInvoker:
            async def __call__(self, request: object, **kwargs: object) -> object:
                del kwargs
                if isinstance(request, functions.UploadGetFileHashes):
                    payload = old_payload if request.location.file_reference == old_location.file_reference else new_payload  # fmt: skip
                    return (types.FileHash(offset=0, limit=2048, hash=hashlib.sha256(payload).digest()),)
                assert isinstance(request, functions.UploadGetFile)
                payload = old_payload if request.location.file_reference == old_location.file_reference else new_payload
                if request.location.file_reference == old_location.file_reference:
                    interval_started.set()
                    await release_interval.wait()
                return upload_file_part(payload[request.offset : request.offset + request.limit])

        invoker = RefreshingHashInvoker()
        deduper = media_download._FileReferenceRefreshDeduper()
        location_state = media_download._DownloadLocationState(old_location)
        verifier = media_download._PlainFileHashVerifier(
            invoker,
            location_state=location_state,
            precise=False,
            cdn_supported=False,
            request_timeout=None,
            max_retries=0,
            flood_sleep_threshold=None,
            reference_deduper=deduper,
            file_reference_refresher=None,
            max_cached_bytes=4096,
        )
        old_verification = asyncio.create_task(verifier.verify(old_location, offset=1024, payload=old_payload[1024:]))
        await interval_started.wait()
        await location_state.refresh(reference_deduper=deduper, refresher=lambda _location: new_location)
        await verifier.verify(new_location, offset=0, payload=new_payload)
        release_interval.set()
        with pytest.raises(media_download.MediaIntegrityError, match="location changed"):
            await old_verification

    run(scenario())


def test_plain_integrity_refreshes_an_expired_hash_request_location() -> None:
    async def scenario() -> None:
        payload = b"a" * 1024
        old_location = document_location()
        new_location = types.InputDocumentFileLocation(
            id=old_location.id, access_hash=old_location.access_hash, file_reference=b"new-ref", thumb_size=""
        )
        refreshes: list[object] = []

        @dataclass(slots=True)
        class ExpiringHashInvoker:
            requests: list[object] = field(default_factory=list)

            async def __call__(self, request: object, **kwargs: object) -> object:
                del kwargs
                self.requests.append(request)
                if isinstance(request, functions.UploadGetFileHashes):
                    if request.location.file_reference == old_location.file_reference:
                        raise BadRequest("FILE_REFERENCE_EXPIRED")
                    return (types.FileHash(offset=0, limit=1024, hash=hashlib.sha256(payload).digest()),)
                assert isinstance(request, functions.UploadGetFile)
                return upload_file_part(payload[request.offset : request.offset + request.limit])

        async def refresh(location: object) -> object:
            refreshes.append(location)
            return new_location

        invoker = ExpiringHashInvoker()
        cache = DownloadRangeCache(max_bytes=4096)
        try:
            result = await download_file(
                invoker,
                old_location,
                limit=len(payload),
                part_size=1024,
                concurrency=1,
                adaptive_part_size=False,
                range_cache=cache,
                range_cache_key="expired-reference",
                verify_plain_hashes=True,
                file_reference_refresher=refresh,
            )
        finally:
            await cache.clear()
        assert result.data == payload
        assert refreshes == [old_location]
        hash_requests = [request for request in invoker.requests if isinstance(request, functions.UploadGetFileHashes)]
        assert [request.location.file_reference for request in hash_requests] == [b"ref", b"new-ref"]

    run(scenario())


def test_plain_integrity_overfetches_full_cross_part_interval_and_trims_partial_range() -> None:
    async def scenario() -> None:
        payload = b"a" * 1024 + b"b" * 1024
        invoker = PlainHashInvoker(
            payload=payload,
            hashes=(types.FileHash(offset=0, limit=len(payload), hash=hashlib.sha256(payload).digest()),),
        )
        result = await download_file(
            invoker,
            document_location(),
            offset=1024,
            limit=1024,
            total_size=len(payload),
            part_size=1024,
            concurrency=1,
            adaptive_part_size=False,
            verify_plain_hashes=True,
        )
        assert result.data == payload[1024:]
        data_requests = [request for request in invoker.requests if isinstance(request, functions.UploadGetFile)]
        assert {(request.offset, request.limit) for request in data_requests} == {(1024, 1024), (0, 2048)}

    run(scenario())


def test_plain_integrity_corruption_raises_before_iterator_yields_or_destination_writes(tmp_path) -> None:
    async def scenario() -> None:
        payload = b"a" * 1024
        invoker = PlainHashInvoker(
            payload=payload,
            hashes=(types.FileHash(offset=0, limit=1024, hash=hashlib.sha256(payload).digest()),),
            corrupt_offsets={0},
        )
        iterator = media_download.iter_download(
            invoker,
            document_location(),
            limit=1024,
            part_size=1024,
            concurrency=1,
            adaptive_part_size=False,
            verify_plain_hashes=True,
        )
        with pytest.raises(media_download.MediaIntegrityError, match="offset 0"):
            await anext(iterator)
        await iterator.aclose()

        target = tmp_path / "corrupt.bin"
        second = PlainHashInvoker(payload=payload, hashes=invoker.hashes, corrupt_offsets={0})
        with pytest.raises(media_download.MediaIntegrityError):
            await download_file(
                second,
                document_location(),
                target,
                limit=1024,
                part_size=1024,
                concurrency=1,
                adaptive_part_size=False,
                verify_plain_hashes=True,
            )
        assert not target.exists()

    run(scenario())


@pytest.mark.parametrize(
    ("hashes", "reason"),
    [
        ((types.FileHash(offset=0, limit=0, hash=b"x" * 32),), "invalid hash metadata"),
        (
            (
                types.FileHash(offset=0, limit=1024, hash=hashlib.sha256(b"a" * 1024).digest()),
                types.FileHash(offset=512, limit=1024, hash=hashlib.sha256(b"a" * 1024).digest()),
            ),
            "contradictory overlapping hash metadata",
        ),
        ((types.FileHash(offset=0, limit=1024, hash=b"short"),), "invalid hash metadata"),
    ],
)
def test_plain_integrity_rejects_invalid_or_contradictory_hash_metadata(hashes: tuple[types.FileHash, ...], reason: str) -> None:  # fmt: skip
    async def scenario() -> None:
        invoker = PlainHashInvoker(payload=b"a" * 2048, hashes=hashes)
        with pytest.raises(media_download.MediaIntegrityError, match=reason):
            await download_file(
                invoker,
                document_location(),
                limit=1024,
                part_size=1024,
                concurrency=1,
                adaptive_part_size=False,
                verify_plain_hashes=True,
            )

    run(scenario())


def test_root_and_client_iter_download_stream_the_same_public_media_shape() -> None:
    async def scenario() -> None:
        payload = b"a" * 1024 + b"b" * 1024
        root_chunks = [
            chunk
            async for chunk in iter_download(
                OffsetInvoker(payload),
                document_location(),
                limit=len(payload),
                total_size=len(payload),
                part_size=1024,
                concurrency=2,
                adaptive_concurrency=False,
                adaptive_part_size=False,
            )
        ]
        sender = FakeSender([upload_file_part(payload[:1024]), upload_file_part(payload[1024:])])
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth()))
        client._sender = sender
        await client.connect()
        client_chunks = [
            chunk
            async for chunk in client.iter_download(
                Media(id=10, size=len(payload), location=document_location()),
                part_size=1024,
                concurrency=2,
                adaptive_concurrency=False,
                adaptive_part_size=False,
                media_lanes=0,
            )
        ]
        assert root_chunks == client_chunks == [payload[:1024], payload[1024:]]
        await client.disconnect()

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
        chunks = (b"a" * 1024, b"b" * 1024, b"c" * 1024, b"d" * 1024, b"e" * 1024)
        payload = b"".join(chunks)
        target = tmp_path / "concurrent.bin"
        progress: list[tuple[int, int | None]] = []
        invoker = DelayedMapOffsetInvoker(
            {index * 1024: chunk for index, chunk in enumerate(chunks)}, delays={0: 0.03, 1024: 0.01}
        )
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=1024,
            adaptive_part_size=False,
            adaptive_concurrency=False,
            concurrency=3,
            launch_stagger=False,
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


@pytest.mark.parametrize("destination_kind", ["new_path", "resume", "bytesio", "internal", "borrowed_file"])
@pytest.mark.parametrize("secondary_failure", ["acknowledgement", "progress"])
@pytest.mark.parametrize("cancel", [False, True])
def test_download_file_unwind_preserves_failure_and_destination(tmp_path, monkeypatch, destination_kind, secondary_failure, cancel) -> None:  # fmt: skip
    async def scenario() -> None:
        target = tmp_path / "unwind.bin"
        original = b"retained-prefix!" * 73 + b"unaligned-tail"
        retained = original[:1024]
        destination: Any
        if destination_kind == "resume":
            target.write_bytes(original)
            destination = target
        elif destination_kind == "new_path":
            destination = target
        elif destination_kind == "bytesio":
            destination = io.BytesIO(original)
            destination.seek(7)
        elif destination_kind == "borrowed_file":
            destination = target.open("w+b")
            destination.write(original)
            destination.seek(7)
        else:
            destination = None
        opened: list[media_download._DestinationHandle] = []
        writers: list[media_download._ConcurrentDestinationWriter] = []
        acknowledgements: list[asyncio.Future[None]] = []
        part_tasks: set[asyncio.Task[Any]] = set()
        acknowledgement_done = asyncio.Event()
        next_request_ready = asyncio.Event()
        fail_request = asyncio.Event()
        original_open = media_download._open_destination
        original_submit = media_download._ConcurrentDestinationWriter.submit
        original_write = media_download._ConcurrentDestinationWriter._write
        primary = RuntimeError("original request failure")
        secondary = OSError("secondary destination failure")
        progress: list[tuple[int, int | None]] = []

        def capture_destination(destination, *, resume):
            handle = original_open(destination, resume=resume)
            opened.append(handle)
            return handle

        async def capture_submit(writer, offset, payload, *, wait_for_completion=True):
            acknowledgement = await original_submit(writer, offset, payload, wait_for_completion=wait_for_completion)
            writers.append(writer)
            acknowledgements.append(acknowledgement)
            acknowledgement.add_done_callback(lambda _future: acknowledgement_done.set())
            return acknowledgement

        def write_then_fail(writer, offset, payload):
            original_write(writer, offset, payload)
            raise secondary

        def fail_progress(current, total):
            progress.append((current, total))
            if secondary_failure == "progress":
                raise secondary

        async def invoke(request: object, **kwargs: object) -> object:
            del kwargs
            assert isinstance(request, functions.UploadGetFile)
            task = asyncio.current_task()
            assert task is not None
            part_tasks.add(task)
            if request.offset == (1024 if destination_kind == "resume" else 0):
                return upload_file_part(b"n" * 1024)
            await acknowledgement_done.wait()
            next_request_ready.set()
            await fail_request.wait()
            raise primary

        monkeypatch.setattr(media_download, "_open_destination", capture_destination)
        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "submit", capture_submit)
        if secondary_failure == "acknowledgement":
            monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_write", write_then_fail)
        download = asyncio.create_task(download_file(invoke, document_location(), destination, limit=3072, part_size=1024, concurrency=1, launch_stagger=False, adaptive_part_size=False, resume=destination_kind == "resume", progress=fail_progress))  # fmt: skip
        try:
            await asyncio.wait_for(next_request_ready.wait(), timeout=2.0)
            if cancel:
                download.cancel("original cancellation")
            else:
                fail_request.set()
            outcome = (await asyncio.gather(download, return_exceptions=True))[0]
            if cancel:
                assert download.cancelled(), outcome
                with pytest.raises(asyncio.CancelledError, match="original cancellation"):
                    download.result()
            else:
                assert outcome is primary
            assert all(task.done() for task in part_tasks)
            assert all(writer._worker.done() for writer in writers)
            assert all(acknowledgement.done() for acknowledgement in acknowledgements)
            if secondary_failure == "progress":
                assert progress == [(2048 if destination_kind == "resume" else 1024, 3072)]
            else:
                assert progress == []
            if destination_kind == "new_path":
                assert opened[0].handle.closed
                assert not target.exists()
            elif destination_kind == "resume":
                assert opened[0].handle.closed
                assert target.read_bytes() == retained
            elif destination_kind == "bytesio":
                assert isinstance(destination, io.BytesIO)
                assert not destination.closed
                assert destination.getvalue() == original
                assert destination.tell() == 7
            elif destination_kind == "internal":
                assert opened[0].get_data() == b""
            else:
                assert destination is not None
                assert not destination.closed
                destination.seek(0)
                assert destination.read() == original[:7] + b"n" * 1024 + original[1031:]
        finally:
            fail_request.set()
            if not download.done():
                download.cancel()
            await asyncio.gather(download, return_exceptions=True)
            for writer in writers:
                await writer.abort()
            for handle in opened:
                handle.handle.close()

    run(scenario())


@pytest.mark.parametrize("cancel", [False, True])
def test_download_file_unwind_progress_remains_cancellable(tmp_path, monkeypatch, cancel) -> None:
    async def scenario() -> None:
        target = tmp_path / "blocked-unwind-progress.bin"
        acknowledgement_done = asyncio.Event()
        next_request_ready = asyncio.Event()
        fail_request = asyncio.Event()
        progress_started = asyncio.Event()
        progress_release = asyncio.Event()
        progress_settled = asyncio.Event()
        download_finished = asyncio.Event()
        original_submit = media_download._ConcurrentDestinationWriter.submit
        writers: list[media_download._ConcurrentDestinationWriter] = []
        primary = RuntimeError("original request failure")

        async def capture_submit(writer, offset, payload, *, wait_for_completion=True):
            acknowledgement = await original_submit(writer, offset, payload, wait_for_completion=wait_for_completion)
            writers.append(writer)
            acknowledgement.add_done_callback(lambda _future: acknowledgement_done.set())
            return acknowledgement

        async def blocking_progress(current, total):
            assert (current, total) == (1024, 2048)
            progress_started.set()
            try:
                await progress_release.wait()
            finally:
                progress_settled.set()

        async def invoke(request: object, **kwargs: object) -> object:
            del kwargs
            assert isinstance(request, functions.UploadGetFile)
            if request.offset == 0:
                return upload_file_part(b"a" * 1024)
            await acknowledgement_done.wait()
            next_request_ready.set()
            await fail_request.wait()
            raise primary

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "submit", capture_submit)
        download = asyncio.create_task(download_file(invoke, document_location(), target, limit=2048, part_size=1024, concurrency=1, launch_stagger=False, adaptive_part_size=False, progress=blocking_progress))  # fmt: skip
        download.add_done_callback(lambda _task: download_finished.set())
        try:
            await asyncio.wait_for(next_request_ready.wait(), timeout=2.0)
            if cancel:
                download.cancel("original cancellation")
            else:
                fail_request.set()
            await asyncio.wait_for(progress_started.wait(), timeout=2.0)
            download.cancel("interrupt progress callback")
            await asyncio.wait_for(download_finished.wait(), timeout=2.0)
            outcome = (await asyncio.gather(download, return_exceptions=True))[0]
            if cancel:
                assert download.cancelled(), outcome
                with pytest.raises(asyncio.CancelledError, match="original cancellation"):
                    download.result()
            else:
                assert outcome is primary
            assert progress_settled.is_set()
            assert writers[0]._worker.done()
            assert writers[0]._destination.handle.closed
            assert not target.exists()
        finally:
            progress_release.set()
            fail_request.set()
            if not download.done():
                download.cancel()
            await asyncio.gather(download, return_exceptions=True)
            for writer in writers:
                await writer.abort()
                writer._destination.handle.close()

    run(scenario())


def test_download_file_cleanup_error_closes_owned_file_and_preserves_failure(tmp_path, monkeypatch, caplog) -> None:
    async def scenario() -> None:
        target = tmp_path / "rollback-error.bin"
        target.write_bytes(b"r" * 1024)
        original_open = media_download._open_destination
        opened: list[Any] = []
        primary = RuntimeError("original request failure")

        class FailingRollback:
            def __init__(self, handle):
                self.handle = handle

            def __getattr__(self, name):
                return getattr(self.handle, name)

            def truncate(self, size):
                if size == 1024:
                    raise OSError("rollback truncate failed")
                return self.handle.truncate(size)

        def capture_destination(destination, *, resume):
            destination_handle = original_open(destination, resume=resume)
            opened.append(destination_handle.handle)
            destination_handle.handle = cast(Any, FailingRollback(destination_handle.handle))
            return destination_handle

        async def invoke(request: object, **kwargs: object) -> object:
            del request, kwargs
            raise primary

        monkeypatch.setattr(media_download, "_open_destination", capture_destination)
        try:
            with pytest.raises(RuntimeError) as raised:
                await download_file(invoke, document_location(), target, limit=3072, part_size=1024, concurrency=2, launch_stagger=False, adaptive_part_size=False, resume=True)  # fmt: skip
            assert raised.value is primary
            assert opened[0].closed
            assert target.read_bytes() == b"r" * 1024
            assert any(record.getMessage() == "media.download.cleanup_failed" for record in caplog.records)
        finally:
            for handle in opened:
                handle.close()

    run(scenario())


@pytest.mark.parametrize("cancel", [False, True])
def test_download_file_cancelled_rollback_failure_has_no_unhandled_loop_error(tmp_path, monkeypatch, caplog, cancel) -> None:  # fmt: skip
    async def scenario() -> None:
        target = tmp_path / "cancelled-rollback-error.bin"
        target.write_bytes(b"r" * 1024)
        original_open = media_download._open_destination
        opened: list[Any] = []
        primary = RuntimeError("original request failure")
        request_started = asyncio.Event()
        rollback_started = asyncio.Event()
        rollback_release = threading.Event()
        loop = asyncio.get_running_loop()
        previous_handler = loop.get_exception_handler()
        loop_errors: list[dict[str, Any]] = []

        class FailingRollback:
            def __init__(self, handle):
                self.handle = handle

            def __getattr__(self, name):
                return getattr(self.handle, name)

            def truncate(self, size):
                if size == 1024:
                    loop.call_soon_threadsafe(rollback_started.set)
                    assert rollback_release.wait(3.0)
                    raise OSError("rollback failed after cancellation")
                return self.handle.truncate(size)

        def capture_destination(destination, *, resume):
            destination_handle = original_open(destination, resume=resume)
            opened.append(destination_handle.handle)
            destination_handle.handle = cast(Any, FailingRollback(destination_handle.handle))
            return destination_handle

        async def invoke(request: object, **kwargs: object) -> object:
            del request, kwargs
            request_started.set()
            if cancel:
                await asyncio.Future()
            raise primary

        monkeypatch.setattr(media_download, "_open_destination", capture_destination)
        loop.set_exception_handler(lambda _loop, context: loop_errors.append(context))
        download = asyncio.create_task(download_file(invoke, document_location(), target, limit=3072, part_size=1024, concurrency=2, launch_stagger=False, adaptive_part_size=False, resume=True))  # fmt: skip
        try:
            if cancel:
                await asyncio.wait_for(request_started.wait(), timeout=2.0)
                download.cancel("original cancellation")
            await asyncio.wait_for(rollback_started.wait(), timeout=2.0)
            for message in ("second cancellation", "third cancellation"):
                download.cancel(message)
                barrier = loop.create_future()
                loop.call_soon(barrier.set_result, None)
                await barrier
                assert not download.done()
            rollback_release.set()
            outcome = (await asyncio.gather(download, return_exceptions=True))[0]
            if cancel:
                assert download.cancelled(), outcome
                with pytest.raises(asyncio.CancelledError, match="original cancellation"):
                    download.result()
            else:
                assert outcome is primary
            assert opened[0].closed
            assert target.read_bytes() == b"r" * 1024
            assert any(record.getMessage() == "media.download.cleanup_failed" for record in caplog.records)
            barrier = loop.create_future()
            loop.call_soon(barrier.set_result, None)
            await barrier
            assert loop_errors == []
        finally:
            rollback_release.set()
            await asyncio.gather(download, return_exceptions=True)
            loop.set_exception_handler(previous_handler)
            for handle in opened:
                handle.close()

    run(scenario())


def test_download_file_close_error_still_removes_new_path_and_preserves_failure(tmp_path, monkeypatch, caplog) -> None:
    async def scenario() -> None:
        target = tmp_path / "close-error.bin"
        original_open = media_download._open_destination
        opened: list[Any] = []
        primary = RuntimeError("original request failure")

        class FailingClose:
            def __init__(self, handle):
                self.handle = handle

            def __getattr__(self, name):
                return getattr(self.handle, name)

            def close(self):
                self.handle.close()
                raise OSError("buffer flush failed during close")

        def capture_destination(destination, *, resume):
            destination_handle = original_open(destination, resume=resume)
            opened.append(destination_handle.handle)
            destination_handle.handle = cast(Any, FailingClose(destination_handle.handle))
            return destination_handle

        async def invoke(request: object, **kwargs: object) -> object:
            del request, kwargs
            raise primary

        monkeypatch.setattr(media_download, "_open_destination", capture_destination)
        try:
            with pytest.raises(RuntimeError) as raised:
                await download_file(invoke, document_location(), target, limit=1024, part_size=1024, concurrency=1, launch_stagger=False, adaptive_part_size=False)  # fmt: skip
            assert raised.value is primary
            assert opened[0].closed
            assert not target.exists()
            assert any(record.getMessage() == "media.download.cleanup_failed" for record in caplog.records)
        finally:
            for handle in opened:
                handle.close()

    run(scenario())


def test_download_file_failed_write_acknowledgement_still_removes_owned_path(tmp_path, monkeypatch) -> None:
    async def scenario() -> None:
        target = tmp_path / "failed-write.bin"
        opened: list[media_download._DestinationHandle] = []
        original_open = media_download._open_destination
        failure = OSError("disk full")

        def capture_destination(destination, *, resume):
            handle = original_open(destination, resume=resume)
            opened.append(handle)
            return handle

        def fail_write(writer, offset, payload):
            del writer, offset, payload
            raise failure

        monkeypatch.setattr(media_download, "_open_destination", capture_destination)
        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_write", fail_write)
        try:
            with pytest.raises(OSError) as raised:
                await download_file(OffsetInvoker(b"a" * 4096), document_location(), target, limit=4096, part_size=1024, concurrency=4, launch_stagger=False, adaptive_part_size=False)  # fmt: skip
            assert raised.value is failure
            assert opened[0].handle.closed
            assert not target.exists()
        finally:
            for handle in opened:
                handle.handle.close()

    run(scenario())


@pytest.mark.parametrize("failure_kind", ["request", "progress", "cancellation"])
def test_download_file_unwind_joins_part_cleanup_under_repeated_cancellation(tmp_path, monkeypatch, failure_kind) -> None:  # fmt: skip
    async def scenario() -> None:
        target = tmp_path / "cancelled-parts.bin"
        failure_ready = asyncio.Event()
        part_ready = asyncio.Event()
        cleanup_started = asyncio.Event()
        cleanup_release = asyncio.Event()
        cleanup_completed = asyncio.Event()
        fail_request = asyncio.Event()
        part_tasks: list[asyncio.Task[Any]] = []
        primary = RuntimeError("original request failure")
        original_submit = media_download._ConcurrentDestinationWriter.submit

        async def completed_submit(writer, offset, payload, *, wait_for_completion=True):
            acknowledgement = await original_submit(writer, offset, payload, wait_for_completion=wait_for_completion)
            await acknowledgement
            return acknowledgement

        def fail_progress(current, total):
            assert (current, total) == (1024, 3072)
            raise primary

        async def invoke(request: object, **kwargs: object) -> object:
            del kwargs
            assert isinstance(request, functions.UploadGetFile)
            if request.offset == 0:
                return upload_file_part(b"a" * 1024)
            if request.offset == 1024:
                failure_ready.set()
                await fail_request.wait()
                raise primary
            task = asyncio.current_task()
            assert task is not None
            part_tasks.append(task)
            part_ready.set()
            try:
                await asyncio.Future()
            finally:
                cleanup_started.set()
                await cleanup_release.wait()
                cleanup_completed.set()

        if failure_kind == "progress":
            monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "submit", completed_submit)
        download = asyncio.create_task(download_file(invoke, document_location(), target, limit=3072, part_size=1024, concurrency=3, launch_stagger=False, adaptive_part_size=False, progress=fail_progress if failure_kind == "progress" else None))  # fmt: skip
        try:
            await asyncio.wait_for(failure_ready.wait(), timeout=2.0)
            await asyncio.wait_for(part_ready.wait(), timeout=2.0)
            if failure_kind == "cancellation":
                download.cancel("original cancellation")
            elif failure_kind == "request":
                fail_request.set()
            await asyncio.wait_for(cleanup_started.wait(), timeout=2.0)
            download.cancel("second cancellation")
            loop = asyncio.get_running_loop()
            barrier = loop.create_future()
            loop.call_soon(barrier.set_result, None)
            await barrier
            assert not part_tasks[0].done()
            assert not download.done()
            download.cancel("third cancellation")
            cleanup_release.set()
            outcome = (await asyncio.gather(download, return_exceptions=True))[0]
            if failure_kind == "cancellation":
                assert download.cancelled(), outcome
                with pytest.raises(asyncio.CancelledError, match="original cancellation"):
                    download.result()
            else:
                assert outcome is primary
            assert cleanup_completed.is_set()
            assert part_tasks[0].done()
            assert not target.exists()
        finally:
            cleanup_release.set()
            fail_request.set()
            if not download.done():
                download.cancel()
            await asyncio.gather(download, *part_tasks, return_exceptions=True)

    run(scenario())


@pytest.mark.parametrize("cancel", [False, True])
def test_download_file_unwind_joins_active_write_under_repeated_cancellation(tmp_path, monkeypatch, cancel) -> None:
    async def scenario() -> None:
        target = tmp_path / "cancelled-writer.bin"
        write_started = asyncio.Event()
        cleanup_started = asyncio.Event()
        release_write = threading.Event()
        write_finished = threading.Event()
        next_request_ready = asyncio.Event()
        fail_request = asyncio.Event()
        loop = asyncio.get_running_loop()
        original_write = media_download._ConcurrentDestinationWriter._write
        original_abort = media_download._ConcurrentDestinationWriter.abort
        writers: list[media_download._ConcurrentDestinationWriter] = []
        primary = RuntimeError("original request failure")

        def blocked_write(writer, offset, payload):
            writers.append(writer)
            loop.call_soon_threadsafe(write_started.set)
            assert release_write.wait(3.0)
            original_write(writer, offset, payload)
            write_finished.set()

        async def observed_abort(writer):
            cleanup_started.set()
            await original_abort(writer)

        async def invoke(request: object, **kwargs: object) -> object:
            del kwargs
            assert isinstance(request, functions.UploadGetFile)
            if request.offset == 0:
                return upload_file_part(b"a" * 1024)
            next_request_ready.set()
            await fail_request.wait()
            raise primary

        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "_write", blocked_write)
        monkeypatch.setattr(media_download._ConcurrentDestinationWriter, "abort", observed_abort)
        download = asyncio.create_task(download_file(invoke, document_location(), target, limit=2048, part_size=1024, concurrency=1, launch_stagger=False, adaptive_part_size=False))  # fmt: skip
        try:
            await asyncio.wait_for(write_started.wait(), timeout=2.0)
            await asyncio.wait_for(next_request_ready.wait(), timeout=2.0)
            if cancel:
                download.cancel("original cancellation")
            else:
                fail_request.set()
            await asyncio.wait_for(cleanup_started.wait(), timeout=2.0)
            download.cancel("second cancellation")
            # The event-loop barrier delivers cancellation while the disk operation remains blocked
            barrier = loop.create_future()
            loop.call_soon(barrier.set_result, None)
            await barrier
            assert not download.done()
            download.cancel("third cancellation")
            release_write.set()
            outcome = (await asyncio.gather(download, return_exceptions=True))[0]
            if cancel:
                assert download.cancelled(), outcome
                with pytest.raises(asyncio.CancelledError, match="original cancellation"):
                    download.result()
            else:
                assert outcome is primary
            assert write_finished.is_set()
            assert writers[0]._worker.done()
            assert writers[0]._destination.handle.closed
            assert not target.exists()
        finally:
            release_write.set()
            fail_request.set()
            if not download.done():
                download.cancel()
            await asyncio.gather(download, return_exceptions=True)
            for writer in writers:
                await original_abort(writer)
                writer._destination.handle.close()

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
        writer = media_download._ConcurrentDestinationWriter(destination, queue_size=1)
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
        writer = media_download._ConcurrentDestinationWriter(destination, queue_size=1)
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
        writer = media_download._ConcurrentDestinationWriter(destination, queue_size=1)
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


def test_download_file_concurrent_writes_path_without_preallocation(tmp_path, monkeypatch) -> None:
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
        target = tmp_path / "no-preallocation.bin"
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
        result = await download_file(
            OffsetInvoker(b"x" * 1024),
            document_location(),
            target,
            limit=1024,
            part_size=1024,
            adaptive_part_size=False,
            concurrency=2,
        )
        assert result.bytes_downloaded == 1024
        assert failing_handle.closed
        assert target.read_bytes() == b"x" * 1024

    run(scenario())


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


def test_range_cache_waiter_cancellation_does_not_cancel_shared_fetch() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=4096)
        started = asyncio.Event()
        release = asyncio.Event()
        fetch_calls = 0

        async def fetch() -> bytes:
            nonlocal fetch_calls
            fetch_calls += 1
            started.set()
            await release.wait()
            return b"shared"

        cancelled_waiter = asyncio.create_task(cache.get_or_fetch("file", 0, 6, fetch))
        surviving_waiter = asyncio.create_task(cache.get_or_fetch("file", 0, 6, fetch))
        await started.wait()
        await asyncio.sleep(0)
        cancelled_waiter.cancel()
        with pytest.raises(asyncio.CancelledError):
            await cancelled_waiter

        release.set()
        assert await surviving_waiter == b"shared"
        assert await cache.get("file", 0, 6) == b"shared"
        assert fetch_calls == 1
        await cache.clear()

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
        # An ordinary FLOOD_WAIT sleeps and retries this request while keeping the concurrency limit unchanged
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
        # Four ordinary flood waits on one part must not exhaust a non-flood retry budget of max_retries=1
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
        # The active window starts fully open, the delay gate staggers initial launches
        assert throttle.limit == 4
        # Ordinary flood waits leave the window unchanged and pause growth
        await throttle.on_retry(FloodWait(1), 1)
        assert throttle.limit == 4
        # Connection failures reduce the window by one and delay regrowth until cooldown ends
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
        for index in range(30):
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
            if index == 0:
                total = mib + 8193
                payload = b"a" * (mib - 1024) + b"b" * 1024 + b"c" * 8193
                offset = mib - 1024
                limit = 8193
                part_size = 65536
                concurrency = 4
                window = None
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
        # Keep both flooded requests' slots reserved during their sleeps so a new range cannot start before they retry
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
            "upload.reuploadCdnFile",
        ]
        assert [getattr(type(request), "QUALNAME", "") for request in invoker.cdn_requests] == [
            "upload.getCdnFile",
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
                (cdn_file_hash(plaintext),),
                types.UploadCdnFile(bytes=ciphertext),
            ]
        )
        result = await download_file(invoker, document_location(), part_size=1024)
        assert result.data == plaintext
        assert [getattr(type(request), "QUALNAME", "") for request in invoker.requests] == [
            "upload.getFile",
            "upload.getCdnFileHashes",
        ]
        assert [getattr(type(request), "QUALNAME", "") for request in invoker.cdn_requests] == ["upload.getCdnFile"]

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
        invoker = FakeInvoker(
            [
                types.UploadFileCdnRedirect(
                    dc_id=4, file_token=b"token", encryption_key=key, encryption_iv=iv, file_hashes=()
                ),
                (),
            ]
        )
        with pytest.raises(CdnIntegrityError, match="no CDN file hash"):
            await download_file(invoker, document_location(), part_size=1024)

    run(scenario())


def test_cdn_partial_download_fetches_and_verifies_complete_hash_interval() -> None:
    async def scenario() -> None:
        key = bytes(range(32))
        iv = bytes(range(16))
        plaintext = bytes(index % 251 for index in range(4096))
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
                types.UploadCdnFile(bytes=ciphertext),
            ]
        )

        result = await download_file(invoker, document_location(), limit=1024, part_size=1024, precise=True)

        assert result.data == plaintext[:1024]
        assert [(request.offset, request.limit) for request in invoker.cdn_requests] == [(0, 4096)]

    run(scenario())


def test_cdn_redirect_repr_hides_bearer_and_encryption_material() -> None:
    redirect = media_download.cdn_redirect_from_raw(
        types.UploadFileCdnRedirect(
            dc_id=4, file_token=b"sensitive-token", encryption_key=b"k" * 32, encryption_iv=b"i" * 16, file_hashes=()
        )
    )

    assert redirect is not None
    rendered = repr(redirect)
    assert "sensitive-token" not in rendered
    assert "kkkk" not in rendered
    assert "iiii" not in rendered


def test_cdn_counter_replaces_iv_tail_instead_of_adding_to_full_iv() -> None:
    key = bytes(range(32))
    iv = bytes.fromhex("00112233445566778899aabb01020304")
    offset = 32
    ciphertext = b"\x00" * 32
    expected = media_ctr_crypt(ciphertext, key, iv[:12] + (offset // 16).to_bytes(4, "big"))

    assert decrypt_cdn_chunk(ciphertext, key=key, iv=iv, offset=offset) == expected


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


def test_client_recreates_auxiliary_bot_sessions_after_disconnect_closes_storage(monkeypatch) -> None:
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
        assert auxiliaries[0] is not first[0]
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
            del worker
            offset = cast(int, options["offset"])
            limit = cast(int, options["limit"])
            payload = bytes([offset // (1024 * 1024)]) * limit
            assert isinstance(destination, Path)
            destination.write_bytes(payload)
            return MediaDownloadResult(bytes_downloaded=limit, offset=offset, destination=destination, raw_location=media_download.download_location_from_media(media))  # fmt: skip

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


def _refresh_document_location(*, document_id: int = 100, access_hash: int = 200, reference: bytes = b"expired", thumb_size: str = "") -> types.InputDocumentFileLocation:  # fmt: skip
    return types.InputDocumentFileLocation(id=document_id, access_hash=access_hash, file_reference=reference, thumb_size=thumb_size)  # fmt: skip


def _refresh_message(*, document_id: int = 100, reference: bytes = b"expired", size: int = 2048) -> types.Message:
    document = types.Document(id=document_id, access_hash=200, file_reference=reference, date=1700000000, mime_type="application/octet-stream", size=size, dc_id=2, attributes=())  # fmt: skip
    return types.Message(id=55, peer_id=types.PeerUser(user_id=7), date=1700000000, message="file", media=types.MessageMediaDocument(document=document))  # fmt: skip


def _refresh_file_part(payload: bytes) -> types.UploadFile:
    return types.UploadFile(type=types.StorageFileUnknown(), mtime=0, bytes=payload)


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("failure_offset", [0, 1024])
@pytest.mark.parametrize("verify", [False, True])
@pytest.mark.parametrize("wrapped", [False, True])
def test_edited_same_size_message_cannot_replace_selected_file(monkeypatch: pytest.MonkeyPatch, streaming: bool, failure_offset: int, verify: bool, wrapped: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
        client._connected = True
        selected = _refresh_message()
        source = Media(id=100, size=2048, raw=selected) if wrapped else selected
        original = b"a" * 1024 + b"c" * 1024
        replacement = b"b" * 1024 + b"d" * 1024
        requests: list[Any] = []
        refreshes: list[object] = []
        cache = DownloadRangeCache(max_bytes=4096)

        async def invoke(request: Any, **_kwargs: object) -> object:
            if isinstance(request, functions.MessagesGetMessages):
                refreshes.append(request)
                return types.MessagesMessages(messages=(_refresh_message(document_id=101, reference=b"renewed"),), topics=(), chats=(), users=())  # fmt: skip
            requests.append(request)
            payload = original if request.location.id == 100 else replacement
            if isinstance(request, functions.UploadGetFileHashes):
                return tuple(types.FileHash(offset=offset, limit=1024, hash=hashlib.sha256(payload[offset : offset + 1024]).digest()) for offset in (0, 1024))  # fmt: skip
            assert isinstance(request, functions.UploadGetFile)
            if request.location.file_reference == b"expired" and request.offset == failure_offset:
                raise BadRequest("FILE_REFERENCE_EXPIRED")
            return _refresh_file_part(payload[request.offset : request.offset + request.limit])

        monkeypatch.setattr(client, "invoke", invoke)
        options: dict[str, Any] = {"part_size": 1024, "concurrency": 1, "adaptive_part_size": False, "media_lanes": 0, "verify_plain_hashes": verify, "range_cache": cache, "range_cache_key": "selected-A"}  # fmt: skip
        yielded: list[bytes] = []
        destination = io.BytesIO(b"retained")
        try:
            with pytest.raises(MediaDownloadError, match="file identity changed"):
                if streaming:
                    async for part in client.iter_download(source, **options):
                        yielded.append(part)
                else:
                    await client.download_media(source, destination, **options)
            assert len(refreshes) == 1
            assert all(request.location.id == 100 for request in requests)
            assert yielded == ([original[:1024]] if streaming and failure_offset else [])
            assert destination.getvalue() == b"retained"
            assert await cache.get("selected-A", failure_offset, 1024) is None
            if failure_offset:
                assert await cache.get("selected-A", 0, 1024) == original[:1024]
        finally:
            await cache.clear()

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "replacement",
    [
        _refresh_document_location(document_id=101),
        _refresh_document_location(access_hash=201),
        _refresh_document_location(thumb_size="m"),
        types.InputPhotoFileLocation(id=100, access_hash=200, file_reference=b"renewed", thumb_size=""),
    ],
)
def test_raw_refresh_rejects_changed_resource_fields(replacement: object) -> None:
    async def scenario() -> None:
        requests: list[object] = []

        async def invoke(request: object, **_kwargs: object) -> object:
            requests.append(request)
            raise BadRequest("FILE_REFERENCE_EXPIRED")

        with pytest.raises(MediaDownloadError, match="file identity changed"):
            await download_file(invoke, _refresh_document_location(), total_size=1024, part_size=1024, concurrency=1, file_reference_refresher=lambda _old: replacement)  # fmt: skip
        assert len(requests) == 1

    asyncio.run(scenario())


@pytest.mark.parametrize(
    ("original", "replacement"),
    [
        (
            types.InputPhotoFileLocation(id=100, access_hash=200, file_reference=b"expired", thumb_size="m"),
            types.InputPhotoFileLocation(id=100, access_hash=200, file_reference=b"renewed", thumb_size="x"),
        ),
        (
            types.InputFileLocation(volume_id=1, local_id=2, secret=3, file_reference=b"expired"),
            types.InputFileLocation(volume_id=1, local_id=4, secret=3, file_reference=b"renewed"),
        ),
        (
            types.InputPeerPhotoFileLocation(peer=types.InputPeerSelf(), photo_id=100),
            types.InputPeerPhotoFileLocation(peer=types.InputPeerSelf(), photo_id=101),
        ),
        (
            types.InputStickerSetThumb(stickerset=types.InputStickerSetID(id=1, access_hash=2), thumb_version=3),
            types.InputStickerSetThumb(stickerset=types.InputStickerSetID(id=1, access_hash=2), thumb_version=4),
        ),
    ],
)
def test_refresh_pins_non_document_location_fields(original: object, replacement: object) -> None:
    async def scenario() -> None:
        state = media_download._DownloadLocationState(original)
        with pytest.raises(MediaDownloadError, match="file identity changed"):
            await state.refresh(reference_deduper=media_download._FileReferenceRefreshDeduper(), refresher=lambda _old: replacement)  # fmt: skip
        assert state.current is original

    asyncio.run(scenario())


@pytest.mark.parametrize("replace_id", [False, True])
def test_hash_request_refresh_preserves_selected_identity(replace_id: bool) -> None:
    async def scenario() -> None:
        original = _refresh_document_location()
        renewed = _refresh_document_location(document_id=101 if replace_id else 100, reference=b"renewed")
        payload = b"a" * 1024
        requests: list[Any] = []

        async def invoke(request: Any, **_kwargs: object) -> object:
            requests.append(request)
            if isinstance(request, functions.UploadGetFileHashes):
                if request.location.file_reference == b"expired":
                    raise BadRequest("FILE_REFERENCE_EXPIRED")
                return (types.FileHash(offset=0, limit=1024, hash=hashlib.sha256(payload).digest()),)
            return _refresh_file_part(payload[request.offset : request.offset + request.limit])

        operation = download_file(invoke, original, total_size=1024, part_size=1024, concurrency=1, verify_plain_hashes=True, file_reference_refresher=lambda _old: renewed)  # fmt: skip
        if replace_id:
            with pytest.raises(MediaDownloadError, match="file identity changed"):
                await operation
            assert len(requests) == 2
        else:
            result = await operation
            assert result.data == payload
            assert result.raw_location == renewed
        assert all(request.location.id == 100 for request in requests)

    asyncio.run(scenario())


def test_concurrent_ranges_cannot_publish_replacement() -> None:
    async def scenario() -> None:
        requested: list[Any] = []
        both_started = asyncio.Event()
        refreshes = 0

        async def invoke(request: Any, **_kwargs: object) -> object:
            requested.append(request)
            if len(requested) == 2:
                both_started.set()
            await both_started.wait()
            raise BadRequest("FILE_REFERENCE_EXPIRED")

        async def refresh(_old: object) -> object:
            nonlocal refreshes
            refreshes += 1
            await asyncio.sleep(0)
            return _refresh_document_location(document_id=101, reference=b"renewed")

        with pytest.raises(MediaDownloadError, match="file identity changed"):
            await download_file(invoke, _refresh_document_location(), total_size=2048, part_size=1024, concurrency=2, launch_stagger=False, file_reference_refresher=refresh)  # fmt: skip
        assert refreshes == 1
        assert {request.offset for request in requested} == {0, 1024}
        assert all(request.location.id == 100 for request in requested)

    asyncio.run(scenario())


def test_read_ahead_cannot_cache_replacement_bytes() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=4096)
        requests: list[Any] = []

        async def invoke(request: Any, **_kwargs: object) -> object:
            requests.append(request)
            if request.offset:
                raise BadRequest("FILE_REFERENCE_EXPIRED")
            return _refresh_file_part(b"a" * 1024)

        try:
            parts = [part async for part in iter_download(invoke, _refresh_document_location(), limit=1024, total_size=3072, part_size=1024, concurrency=1, range_cache=cache, range_cache_key="selected-A", read_ahead_bytes=2048, file_reference_refresher=lambda _old: _refresh_document_location(document_id=101))]  # fmt: skip
            await asyncio.gather(*tuple(cache._background))
            assert parts == [b"a" * 1024]
            assert {request.offset for request in requests} == {0, 1024, 2048}
            assert all(request.location.id == 100 for request in requests)
            assert await cache.get("selected-A", 1024, 1024) is None
            assert await cache.get("selected-A", 2048, 1024) is None
        finally:
            await cache.clear()

    asyncio.run(scenario())


_LARGE_SIZE = (1 << 63) - 1


class GuardedPathFile:
    def __init__(self, handle: BinaryIO, size: int) -> None:
        self.handle = handle
        self.size = size
        self.writes: list[tuple[int, bytes]] = []
        self.truncations: list[int] = []

    def write(self, payload: bytes) -> int:
        offset = self.handle.tell()
        written = self.handle.write(payload)
        self.writes.append((offset, payload))
        self.size = max(self.size, offset + written)
        return written

    def truncate(self, size: int | None = None) -> int:
        size = self.handle.tell() if size is None else size
        self.truncations.append(size)
        # Intercept growth before it can allocate disk space, including when this regression fails
        assert size <= self.size, "destination grew before receiving the corresponding bytes"
        result = self.handle.truncate(size)
        self.size = size
        return result

    def __getattr__(self, name: str) -> Any:
        return getattr(self.handle, name)


def guard_path_files(monkeypatch: pytest.MonkeyPatch) -> list[GuardedPathFile]:
    opened: list[GuardedPathFile] = []
    original_open = media_download._open_destination

    def open_destination(destination: Any, *, resume: bool) -> media_download._DestinationHandle:
        resolved = original_open(destination, resume=resume)
        assert resolved.path is not None
        guarded = GuardedPathFile(resolved.handle, resolved.path.stat().st_size)
        opened.append(guarded)
        resolved.handle = cast(BinaryIO, guarded)
        return resolved

    monkeypatch.setattr(media_download, "_open_destination", open_destination)
    return opened


def _large_download_file_id(size: int) -> str:
    return encode_file_id(
        types.Document(
            id=11,
            access_hash=22,
            file_reference=b"reference",
            date=1_700_000_000,
            mime_type="application/octet-stream",
            size=size,
            dc_id=2,
            attributes=(),
        )
    )


def download_client() -> Client:
    client = Client(ClientConfig(api_id=1, api_hash="hash", session_storage=InMemorySessionStorage()))
    client._connected = True
    return client


@pytest.mark.parametrize("size_source", ["file_id", "total_size", "limit"])
def test_large_download_size_does_not_allocate_before_rpc_rejection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, size_source: str) -> None:  # fmt: skip
    async def scenario() -> None:
        target = tmp_path / "rejected.bin"
        opened = guard_path_files(monkeypatch)
        client = download_client()
        rejection = MediaDownloadError("media was rejected")
        requests: list[functions.UploadGetFile] = []

        async def invoke(request: object, **_kwargs: Any) -> object:
            assert isinstance(request, functions.UploadGetFile)
            requests.append(request)
            assert target.stat().st_size == 0
            raise rejection

        monkeypatch.setattr(client, "invoke", invoke)
        options = {} if size_source == "file_id" else {size_source: _LARGE_SIZE}
        media = _large_download_file_id(_LARGE_SIZE if size_source == "file_id" else 2048)
        with pytest.raises(MediaDownloadError) as failure:
            await client.download_media(
                media,
                target,
                media_lanes=0,
                concurrency=2,
                part_size=1024,
                adaptive_part_size=False,
                launch_stagger=False,
                **options,
            )
        assert failure.value is rejection
        assert requests
        assert len(opened) == 1
        assert opened[0].writes == []
        assert opened[0].truncations == []
        assert opened[0].closed
        assert not target.exists()

    asyncio.run(scenario())


@pytest.mark.parametrize("resume", [False, True])
def test_large_file_id_waits_without_growing_destination_and_cancels_cleanly(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, resume: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        target = tmp_path / "cancelled.bin"
        prefix = b"p" * 1024 if resume else b""
        if resume:
            target.write_bytes(prefix)
        opened = guard_path_files(monkeypatch)
        client = download_client()
        entered = asyncio.Event()
        release = asyncio.Event()

        async def invoke(request: object, **_kwargs: Any) -> object:
            assert isinstance(request, functions.UploadGetFile)
            assert request.offset >= len(prefix)
            entered.set()
            await release.wait()
            raise AssertionError("the pending request should be cancelled")

        monkeypatch.setattr(client, "invoke", invoke)
        operation = asyncio.create_task(
            client.download_media(
                _large_download_file_id(_LARGE_SIZE),
                target,
                media_lanes=0,
                concurrency=2,
                part_size=1024,
                adaptive_part_size=False,
                launch_stagger=False,
                resume=resume,
            )
        )
        entry = asyncio.create_task(entered.wait())
        try:
            async with asyncio.timeout(5):
                await asyncio.wait((operation, entry), return_when=asyncio.FIRST_COMPLETED)
                if operation.done():
                    await operation
                assert entered.is_set()
                assert target.read_bytes() == prefix
                assert opened[0].writes == []
                assert opened[0].truncations == []
                operation.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await operation
            assert opened[0].closed
            if resume:
                assert target.read_bytes() == prefix
                assert opened[0].truncations == [len(prefix)]
            else:
                assert not target.exists()
        finally:
            operation.cancel()
            entry.cancel()
            await asyncio.gather(operation, entry, return_exceptions=True)

    asyncio.run(scenario())


@pytest.mark.parametrize("size_override", ["limit", "total_size"])
@pytest.mark.parametrize("resume", [False, True])
def test_small_override_of_large_file_id_grows_only_by_written_bytes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, size_override: str, resume: bool) -> None:  # fmt: skip
    async def scenario() -> None:
        target = tmp_path / "accepted.bin"
        payload = b"a" * 1024 + b"b" * 513
        if resume:
            target.write_bytes(payload[:1024])
        opened = guard_path_files(monkeypatch)
        client = download_client()

        async def invoke(request: object, **_kwargs: Any) -> object:
            assert isinstance(request, functions.UploadGetFile)
            return types.UploadFile(
                type=types.StorageFileUnknown(),
                mtime=1_700_000_000,
                bytes=payload[request.offset : request.offset + request.limit],
            )

        monkeypatch.setattr(client, "invoke", invoke)
        result = await client.download_media(
            _large_download_file_id(_LARGE_SIZE),
            target,
            media_lanes=0,
            concurrency=2,
            part_size=1024,
            adaptive_part_size=False,
            launch_stagger=False,
            resume=resume,
            **{size_override: len(payload)},
        )
        assert result.bytes_downloaded == len(payload)
        assert target.read_bytes() == payload
        assert len(opened) == 1
        expected_writes = [(1024, b"b" * 513)] if resume else [(0, b"a" * 1024), (1024, b"b" * 513)]
        assert opened[0].writes == expected_writes
        assert opened[0].truncations == []
        assert opened[0].closed

    asyncio.run(scenario())


class TrackedKey(str):
    pass


def test_range_cache_large_keys_preserve_identity_and_range_boundaries() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=32)
        first = "x" * 65535 + "a"
        second = "x" * 65535 + "b"
        digest_text = hashlib.sha256(first.encode()).hexdigest()
        cases = (
            (first, 0, 1024, b"a"),
            (second, 0, 1024, b"b"),
            (digest_text, 0, 1024, b"c"),
            (first, 1024, 1024, b"d"),
            (first, 0, 2048, b"e"),
            ("\ud800", 0, 1024, b"f"),
        )
        for key, offset, limit, payload in cases:
            await cache.put(key, offset, limit, payload)
        for key, offset, limit, payload in cases:
            assert await cache.get(key, offset, limit) == payload
        assert len(cache._entries) == len(cases)
        assert all(isinstance(identity, bytes) and len(identity) == 32 for identity, _, _ in cache._entries)
        assert cache._size == 6

    asyncio.run(scenario())


def test_range_cache_entry_cap_evicts_lru_without_charging_key_bytes_to_payloads() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=6, max_entries=3)
        keys = ["k" * 65536 + str(index) for index in range(4)]
        for key, payload in zip(keys[:3], (b"a", b"b", b"c"), strict=True):
            await cache.put(key, 0, 1024, payload)
        assert len(cache._entries) == 3
        assert await cache.get(keys[0], 0, 1024) == b"a"
        await cache.put(keys[3], 0, 1024, b"d")
        assert len(cache._entries) == 3
        assert cache._size == 3
        assert await cache.get(keys[1], 0, 1024) is None
        assert await cache.get(keys[2], 0, 1024) == b"c"
        await cache.put(keys[0], 0, 1024, b"AAA")
        assert len(cache._entries) == 3
        assert cache._size == 5
        await cache.put(keys[2], 0, 1024, b"CCC")
        assert len(cache._entries) == 2
        assert cache._size == 6
        assert await cache.get(keys[3], 0, 1024) is None
        assert await cache.get(keys[0], 0, 1024) == b"AAA"
        assert await cache.get(keys[2], 0, 1024) == b"CCC"
        await cache.put(keys[3], 0, 1024, b"")
        await cache.put(keys[3], 0, 1024, b"oversize")
        assert len(cache._entries) == 2
        await cache.clear()
        assert cache._size == 0
        assert not cache._entries

    asyncio.run(scenario())


def test_range_cache_default_entry_cap_bounds_tiny_ranges() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache()
        for index in range(4097):
            await cache.put("shared", index, 1, b"x")
        assert len(cache._entries) == 4096
        assert cache._size == 4096
        assert await cache.get("shared", 0, 1) is None
        assert await cache.get("shared", 1, 1) == b"x"
        assert await cache.get("shared", 4096, 1) == b"x"

    asyncio.run(scenario())


@pytest.mark.parametrize("max_entries", [0, -1])
def test_range_cache_rejects_nonpositive_entry_cap(max_entries: int) -> None:
    with pytest.raises(ValueError, match="max_entries must be positive"):
        DownloadRangeCache(max_entries=max_entries)


def test_range_cache_pending_fetch_releases_original_key_and_deduplicates() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=8)
        key = TrackedKey("pending" * 10000)
        key_ref = weakref.ref(key)
        started = asyncio.Event()
        release = asyncio.Event()
        calls = 0

        async def fetch() -> bytes:
            nonlocal calls
            calls += 1
            started.set()
            await release.wait()
            return b"result"

        waiter = asyncio.create_task(cache.get_or_fetch(key, 0, 1024, fetch))
        del key
        await started.wait()
        waiter.cancel()
        with pytest.raises(asyncio.CancelledError):
            await waiter
        assert key_ref() is None
        assert len(cache._pending) == 1
        assert all(isinstance(identity, bytes) and len(identity) == 32 for identity, _, _ in cache._pending)
        survivor = asyncio.create_task(cache.get_or_fetch("pending" * 10000, 0, 1024, fetch))
        await asyncio.sleep(0)
        release.set()
        assert await survivor == b"result"
        assert calls == 1
        assert not cache._pending
        assert await cache.get("pending" * 10000, 0, 1024) == b"result"

    asyncio.run(scenario())


def test_range_cache_prefetch_releases_original_key_and_clear_joins_fetch() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=8)
        key = TrackedKey("prefetch" * 10000)
        key_ref = weakref.ref(key)
        started = asyncio.Event()
        cancelled = asyncio.Event()

        async def fetch() -> bytes:
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.set()
            return b"unreachable"

        cache.prefetch(key, 0, 1024, fetch)
        del key
        assert key_ref() is None
        await started.wait()
        assert all(isinstance(identity, bytes) and len(identity) == 32 for identity, _, _ in cache._pending)
        await cache.clear()
        assert cancelled.is_set()
        assert not cache._pending
        assert not cache._background

    asyncio.run(scenario())


@pytest.mark.parametrize("streaming", [False, True])
def test_noncanonical_file_ids_keep_cache_identity_bounded(streaming: bool) -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=2, max_entries=2)
        requests = []

        async def invoke(request: object, **_kwargs: object) -> object:
            assert isinstance(request, functions.UploadGetFile)
            assert request.location == types.InputDocumentFileLocation(
                id=17, access_hash=29, file_reference=b"ref", thumb_size=""
            )
            requests.append(request)
            return types.UploadFile(type=types.StorageFileUnknown(), mtime=0, bytes=b"z")

        file_ids = []
        for index in range(4):
            payload = {"k": "d", "id": 17, "ah": 29, "fr": "cmVm", "n": str(index), "unused": "x" * 48000}
            encoded = base64.urlsafe_b64encode(json.dumps(payload, indent=index).encode()).decode().rstrip("=")
            file_id = "mpf1_" + encoded
            assert 64000 < len(file_id) <= 65536
            file_ids.append(file_id)
            if streaming:
                chunks = iter_download_media(invoke, file_id, limit=1, part_size=1024, range_cache=cache)
                assert b"".join([part async for part in chunks]) == b"z"
            else:
                assert (await download_media(invoke, file_id, limit=1, part_size=1024, range_cache=cache)).data == b"z"
            assert len(cache._entries) <= 2
            assert all(isinstance(identity, bytes) and len(identity) == 32 for identity, _, _ in cache._entries)
        prior_requests = len(requests)
        assert (await download_media(invoke, file_ids[-1], limit=1, part_size=1024, range_cache=cache)).data == b"z"
        assert len(requests) == prior_requests

    asyncio.run(scenario())


def _unknown_dc_file_id(dc_id: int, size: int) -> str:
    return encode_file_id(Media(id=17, size=size, dc_id=dc_id, location=types.InputDocumentFileLocation(id=17, access_hash=23, file_reference=b"synthetic", thumb_size="")))  # fmt: skip


def client_with_options(*, idle_close: float | None = 120.0) -> Client:
    storage = InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=b"s" * 256),
            dc_options=(
                DCOption(id=2, ip_address="127.0.0.2", port=443),
                DCOption(id=5, ip_address="127.0.0.5", port=443, media_only=True),
            ),
        )
    )
    return Client(ClientConfig(api_id=1, api_hash="synthetic", session_storage=storage, media_idle_close=idle_close))


async def _download_unknown_dc_file(client: Client, source: str, api: str) -> bytes:
    if api == "stream":
        return b"".join([chunk async for chunk in client.iter_download(source)])
    result = await client.download_media(source)
    assert result.data is not None
    return result.data


@pytest.mark.parametrize("api", ["materialized", "stream"])
@pytest.mark.parametrize("size", [0, 1024])
@pytest.mark.parametrize("idle_close", [120.0, None])
def test_unknown_file_id_dcs_do_not_create_pools_or_tasks(monkeypatch: pytest.MonkeyPatch, api: str, size: int, idle_close: float | None) -> None:  # fmt: skip
    async def scenario() -> None:
        client = client_with_options(idle_close=idle_close)
        builds: list[int] = []

        async def build_sender(dc_id: int) -> None:
            builds.append(dc_id)
            raise AssertionError("unknown DC reached sender construction")

        monkeypatch.setattr(client, "_build_media_sender", build_sender)
        await client.connect()
        baseline_tasks = asyncio.all_tasks()
        try:
            for dc_id in (*range(100, 116), (1 << 31) - 1):
                with pytest.raises(ValueError, match=f"no DC option for dc_id={dc_id}"):
                    await _download_unknown_dc_file(client, _unknown_dc_file_id(dc_id, size), api)
                assert not client._media_pools
                assert asyncio.all_tasks() == baseline_tasks
            assert not builds
        finally:
            await client.disconnect()

    asyncio.run(scenario())


@dataclass
class MediaSender:
    payload: bytes = bytes(range(251)) * 5
    requests: list[object] = field(default_factory=list)
    is_connected: bool = True

    async def request(self, body: object, *, content_related: bool = True, retry_safe: bool, request_timeout: float | None = None) -> object:  # fmt: skip
        del content_related, retry_safe, request_timeout
        while isinstance(body, functions.InvokeWithoutUpdates | functions.InvokeWithLayer | functions.InitConnection):
            body = body.query
        self.requests.append(body)
        if isinstance(body, functions.AuthExportAuthorization):
            return types.AuthExportedAuthorization(id=29, bytes=b"synthetic")
        if isinstance(body, functions.AuthImportAuthorization):
            return types.AuthAuthorization(user=types.UserEmpty(id=31))
        assert isinstance(body, functions.UploadGetFile)
        return types.UploadFile(type=types.StorageFileUnknown(), mtime=0, bytes=self.payload[body.offset : body.offset + body.limit])  # fmt: skip

    async def disconnect(self) -> None:
        self.is_connected = False


@pytest.mark.parametrize("dc_id", [2, 5], ids=["home", "foreign-media-only"])
def test_configured_file_id_dc_reuses_pool_after_unknown_dc_rejection(dc_id: int) -> None:
    async def scenario() -> None:
        client = client_with_options()
        senders: list[MediaSender] = []

        def sender_factory(record: SessionRecord) -> MediaSender:
            assert record.dc_id in {2, 5}
            sender = MediaSender()
            senders.append(sender)
            return sender

        client._sender_factory = sender_factory
        await client.connect()
        try:
            expected = bytes(range(251)) * 5
            source = _unknown_dc_file_id(dc_id, len(expected))
            assert await _download_unknown_dc_file(client, source, "materialized") == expected
            pool = client._media_pools[("download", dc_id)]
            reaper = pool._idle_reaper
            assert reaper is not None and not reaper.done()
            built = tuple(senders)
            for size in (0, 1024):
                for api in ("materialized", "stream"):
                    with pytest.raises(ValueError, match="no DC option for dc_id=999"):
                        await _download_unknown_dc_file(client, _unknown_dc_file_id(999, size), api)
            assert await _download_unknown_dc_file(client, source, "stream") == expected
            assert client._media_pools == {("download", dc_id): pool}
            assert pool._idle_reaper is reaper and not reaper.done()
            assert tuple(senders) == built
            assert all(sender.is_connected for sender in senders)
        finally:
            await client.disconnect()
        assert reaper.done()
        assert not any(sender.is_connected for sender in senders)

    asyncio.run(scenario())


type TraceFunction = Callable[[FrameType, str, object], TraceFunction | None]


def _location() -> types.InputDocumentFileLocation:
    return types.InputDocumentFileLocation(id=35, access_hash=71, file_reference=b"test-reference", thumb_size="")


def _hash(offset: int, limit: int, digest: bytes = b"h" * 32) -> types.FileHash:
    return types.FileHash(offset=offset, limit=limit, hash=digest)


def _verifier(invoke: Callable[..., Awaitable[object]]) -> media_download._PlainFileHashVerifier:
    return media_download._PlainFileHashVerifier(
        invoke,
        location_state=media_download._DownloadLocationState(_location()),
        precise=True,
        cdn_supported=False,
        request_timeout=None,
        max_retries=0,
        flood_sleep_threshold=None,
        reference_deduper=media_download._FileReferenceRefreshDeduper(),
        file_reference_refresher=None,
        max_cached_bytes=1024,
    )


async def _unused_invoke(*args: object, **kwargs: object) -> object:
    raise AssertionError("Unexpected network request")


def _count_verifier_lines(action: Callable[[], None]) -> int:
    events = 0

    def trace(frame: FrameType, event: str, arg: object) -> TraceFunction | None:
        nonlocal events
        if frame.f_code.co_filename != media_download.__file__ or not frame.f_code.co_qualname.startswith(
            "_PlainFileHashVerifier."
        ):
            return None
        if event == "line":
            events += 1
        return trace

    previous = sys.gettrace()
    try:
        sys.settrace(trace)
        action()
    finally:
        sys.settrace(previous)
    return events


def test_plain_hash_response_limit_rejects_before_iterating(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(media_download._PlainFileHashVerifier, "_MAX_HASH_RESPONSE_ITEMS", 4)

    class UnreadableBatch(tuple):
        def __iter__(self):
            raise AssertionError("Oversized response must be rejected before item validation")

    requests = []

    async def invoke(request: object, **kwargs: object) -> object:
        requests.append(request)
        return UnreadableBatch(_hash(offset, 1) for offset in range(5))

    verifier = _verifier(invoke)
    with pytest.raises(media_download.MediaIntegrityError, match="hash response item limit exceeded"):
        asyncio.run(verifier._ensure_hash_coverage(_location(), 0, 1))
    assert len(requests) == 1
    assert not verifier._hashes
    assert not verifier._hash_keys


def test_plain_hash_retention_budget_counts_unique_intervals_across_responses(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(media_download._PlainFileHashVerifier, "_MAX_HASH_RESPONSE_ITEMS", 3)
    monkeypatch.setattr(media_download._PlainFileHashVerifier, "_MAX_RETAINED_HASHES", 3)
    batches = iter(((_hash(2, 2), _hash(0, 2), _hash(0, 2)), (_hash(2, 2), _hash(4, 2)), (_hash(4, 2), _hash(6, 2))))
    offsets = []

    async def invoke(request: object, **kwargs: object) -> object:
        assert isinstance(request, functions.UploadGetFileHashes)
        offsets.append(request.offset)
        return next(batches)

    verifier = _verifier(invoke)

    async def scenario() -> None:
        assert await verifier._ensure_hash_coverage(_location(), 0, 4) == ((0, 2, b"h" * 32), (2, 2, b"h" * 32))
        assert await verifier._ensure_hash_coverage(_location(), 4, 6) == ((4, 2, b"h" * 32),)
        before = verifier._hashes.copy()
        with pytest.raises(media_download.MediaIntegrityError, match="hash metadata limit exceeded"):
            await verifier._ensure_hash_coverage(_location(), 6, 8)
        assert verifier._hashes == before
        assert verifier._hash_keys == [(0, 2), (2, 2), (4, 2)]
        assert not verifier._validated

    asyncio.run(scenario())
    assert offsets == [0, 4, 6]


@pytest.mark.parametrize(
    ("batch", "reason", "offset", "limit"),
    [
        ((_hash(13, 3), _hash(0, 2)), "contradictory overlapping hash metadata", 13, 1),
        ((_hash(0, 2), _hash(8, 3)), "contradictory overlapping hash metadata", 10, 1),
        ((_hash(10, 2),), "contradictory overlapping hash metadata", 10, 2),
        ((_hash(10, 4, b"z" * 32),), "contradictory hash metadata", 10, 4),
        ((_hash(3, 4), _hash(0, 4)), "contradictory overlapping hash metadata", 3, 1),
        ((_hash(0, 2), _hash(0, 2, b"z" * 32)), "contradictory hash metadata", 0, 2),
        ((_hash(0, 2), _hash(5, 1, b"short")), "invalid hash metadata", 5, 1),
        ((_hash(0, 2), _hash(5, 0)), "invalid hash metadata", 5, 0),
    ],
)
def test_plain_hash_batch_rejection_keeps_previous_metadata(
    batch: tuple[types.FileHash, ...], reason: str, offset: int, limit: int
) -> None:
    verifier = _verifier(_unused_invoke)
    verifier._remember_hashes((_hash(10, 4),), offset=10, limit=4)
    with pytest.raises(media_download.MediaIntegrityError) as failure:
        verifier._remember_hashes(batch, offset=0, limit=20)
    assert (failure.value.reason, failure.value.offset, failure.value.limit) == (reason, offset, limit)
    assert verifier._hashes == {(10, 4): b"h" * 32}
    assert verifier._hash_keys == [(10, 4)]


def test_plain_hash_unordered_batches_preserve_adjacency_partial_coverage_and_refresh() -> None:
    verifier = _verifier(_unused_invoke)

    async def scenario() -> None:
        await verifier._ensure_identity(("old",))
        verifier._remember_hashes((_hash(10, 4), _hash(0, 3)), offset=0, limit=14)
        verifier._remember_hashes((_hash(14, 2), _hash(3, 7), _hash(0, 3)), offset=3, limit=13)
        assert verifier._covering_intervals(2, 15) == (
            (0, 3, b"h" * 32),
            (3, 7, b"h" * 32),
            (10, 4, b"h" * 32),
            (14, 2, b"h" * 32),
        )
        assert verifier._covering_intervals(10, 14) == ((10, 4, b"h" * 32),)
        assert verifier._first_uncovered_offset(2, 17) == 16
        assert verifier._covering_intervals(16, 17) is None
        await verifier._ensure_identity(("new",))
        assert not verifier._hashes
        assert not verifier._hash_keys
        assert verifier._covering_intervals(0, 1) is None

    asyncio.run(scenario())


@pytest.mark.parametrize("repeat", [False, True])
def test_plain_hash_gap_and_no_progress_fail_at_first_missing_byte(repeat: bool) -> None:
    batch = (_hash(3, 3), _hash(0, 2))
    offsets = []

    async def invoke(request: object, **kwargs: object) -> object:
        assert isinstance(request, functions.UploadGetFileHashes)
        offsets.append(request.offset)
        return batch if len(offsets) == 1 or repeat else ()

    verifier = _verifier(invoke)
    with pytest.raises(media_download.MediaIntegrityError) as failure:
        asyncio.run(verifier._ensure_hash_coverage(_location(), 0, 6))
    assert failure.value.reason == ("hash response loop" if repeat else "hash coverage gap")
    assert (failure.value.offset, failure.value.limit) == (2, 4)
    assert offsets == [0, 2]


@pytest.mark.parametrize("reverse", [False, True])
def test_plain_hash_large_batch_validation_has_bounded_work(reverse: bool) -> None:
    count = 512
    batch = tuple(_hash(offset, 1) for offset in sorted(range(count), reverse=reverse))

    async def invoke(request: object, **kwargs: object) -> object:
        return batch

    verifier = _verifier(invoke)

    def action() -> None:
        intervals = asyncio.run(verifier._ensure_hash_coverage(_location(), 0, count))
        assert intervals == tuple((offset, 1, b"h" * 32) for offset in range(count))

    # Counting executed validator lines catches all-prior scans without wall-clock thresholds
    assert _count_verifier_lines(action) < 80 * count


def test_plain_hash_successive_requests_do_not_rescan_retained_prefix() -> None:
    count = 4096

    async def invoke(request: object, **kwargs: object) -> object:
        assert isinstance(request, functions.UploadGetFileHashes)
        return (_hash(request.offset, 1),)

    verifier = _verifier(invoke)
    verifier._remember_hashes(tuple(_hash(offset, 1) for offset in range(count)), offset=0, limit=count)

    async def scenario() -> None:
        for offset in range(count, count + 4):
            assert await verifier._ensure_hash_coverage(_location(), offset, offset + 1) == ((offset, 1, b"h" * 32),)

    assert _count_verifier_lines(lambda: asyncio.run(scenario())) < 1000
    assert len(verifier._hashes) == count + 4


@pytest.mark.parametrize("corrupt_unrequested_byte", [False, True])
def test_plain_hash_unordered_metadata_verifies_whole_interval_before_partial_output(
    corrupt_unrequested_byte: bool,
) -> None:
    payload = b"a" * 1024 + b"b" * 1024 + b"c" * 1024 + b"d" * 1024
    intervals = ((3072, 1024), (0, 1024), (1024, 2048))
    hashes = tuple(
        _hash(offset, limit, hashlib.sha256(payload[offset : offset + limit]).digest()) for offset, limit in intervals
    )
    fetched = []

    async def invoke(request: object, **kwargs: object) -> object:
        if isinstance(request, functions.UploadGetFileHashes):
            return hashes
        assert isinstance(request, functions.UploadGetFile)
        fetched.append((request.offset, request.limit))
        part = payload[request.offset : request.offset + request.limit]
        if corrupt_unrequested_byte and request.offset == 1024 and request.limit == 2048:
            part = part[:-1] + b"z"
        return types.UploadFile(type=types.StorageFileUnknown(), mtime=0, bytes=part)

    verifier = _verifier(invoke)
    verification = verifier.verify(_location(), offset=1024, payload=payload[1024:2048])
    if corrupt_unrequested_byte:
        with pytest.raises(media_download.MediaIntegrityError, match="hash mismatch"):
            asyncio.run(verification)
    else:
        asyncio.run(verification)
    assert fetched == [(1024, 2048)]


def _cache_document(*, document_id: int = 11, size: int = 1024) -> types.Document:
    return types.Document(id=document_id, access_hash=22, file_reference=b"reference", date=1700000000, mime_type="application/octet-stream", size=size, dc_id=2, attributes=())  # fmt: skip


def _cache_wrapper(*, raw: object | None = None, size: int = 1024) -> Media:
    return Media(id=11, access_hash=22, file_reference=b"reference", mime_type="application/octet-stream", size=size, dc_id=2, raw=raw)  # fmt: skip


def _cached_file_part(payload: bytes) -> types.UploadFile:
    return types.UploadFile(type=types.StorageFileUnknown(), mtime=0, bytes=payload)


async def _download_cached_media(streaming: bool, invoke: Any, media: object, **options: Any) -> bytes:
    if streaming:
        return b"".join([part async for part in iter_download_media(invoke, media, **options)])
    result = await download_media(invoke, media, **options)
    assert result.data is not None
    return result.data


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize(
    "raw",
    [
        _cache_document(document_id=12),
        types.Photo(
            id=11,
            access_hash=22,
            file_reference=b"reference",
            date=1700000000,
            sizes=(types.PhotoSize(type="x", w=100, h=100, size=1024),),
            dc_id=2,
        ),
        types.InputDocumentFileLocation(id=11, access_hash=22, file_reference=b"reference", thumb_size="m"),
    ],
)
def test_conflicting_wrapper_caches_only_effective_raw_location(streaming: bool, raw: object) -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=4096)
        requests: list[Any] = []
        target = encode_file_id(_cache_wrapper())
        conflicting = _cache_wrapper(raw=raw)
        assert conflicting.file_id == target

        async def invoke(request: Any, **_kwargs: object) -> object:
            assert isinstance(request, functions.UploadGetFile)
            requests.append(request)
            is_target = (
                isinstance(request.location, types.InputDocumentFileLocation)
                and request.location.id == 11
                and request.location.thumb_size == ""
            )
            return _cached_file_part((b"a" if is_target else b"b") * 1024)

        options = {"limit": 1024, "part_size": 1024, "range_cache": cache}
        try:
            assert await _download_cached_media(streaming, invoke, conflicting, **options) == b"b" * 1024
            assert await _download_cached_media(streaming, invoke, target, **options) == b"a" * 1024
            assert len(requests) == 2
            assert await _download_cached_media(streaming, invoke, encode_file_id(raw), **options) == b"b" * 1024
            assert await _download_cached_media(streaming, invoke, target, **options) == b"a" * 1024
            assert len(requests) == 2
        finally:
            await cache.clear()

    asyncio.run(scenario())


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("location_type", [types.InputDocumentFileLocation, types.InputPhotoFileLocation])
def test_effective_location_preserves_thumbnail_identity(streaming: bool, location_type: Any) -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=4096)
        requests: list[Any] = []
        small = location_type(id=11, access_hash=22, file_reference=b"reference", thumb_size="m")
        large = replace(small, thumb_size="x")

        async def invoke(request: Any, **_kwargs: object) -> object:
            assert isinstance(request, functions.UploadGetFile)
            requests.append(request)
            return _cached_file_part((b"s" if request.location.thumb_size == "m" else b"l") * 1024)

        options = {"limit": 1024, "part_size": 1024, "range_cache": cache}
        try:
            assert await _download_cached_media(streaming, invoke, _cache_wrapper(raw=small), **options) == b"s" * 1024
            assert await _download_cached_media(streaming, invoke, _cache_wrapper(raw=large), **options) == b"l" * 1024
            assert await _download_cached_media(streaming, invoke, encode_file_id(small), **options) == b"s" * 1024
            assert await _download_cached_media(streaming, invoke, encode_file_id(large), **options) == b"l" * 1024
            assert [request.location.thumb_size for request in requests] == ["m", "x"]
        finally:
            await cache.clear()

    asyncio.run(scenario())


@pytest.mark.parametrize("streaming", [False, True])
def test_read_ahead_uses_effective_location_key(streaming: bool) -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=8192)
        requests: list[Any] = []
        raw = _cache_document(document_id=12, size=3072)
        target = encode_file_id(_cache_wrapper(size=3072))
        payloads = {11: b"a" * 1024 + b"c" * 1024 + b"e" * 1024, 12: b"b" * 1024 + b"d" * 1024 + b"f" * 1024}

        async def invoke(request: Any, **_kwargs: object) -> object:
            assert isinstance(request, functions.UploadGetFile)
            requests.append(request)
            return _cached_file_part(payloads[request.location.id][request.offset : request.offset + request.limit])

        options = {"limit": 1024, "part_size": 1024, "concurrency": 1, "range_cache": cache}
        try:
            assert (
                await _download_cached_media(
                    streaming, invoke, _cache_wrapper(raw=raw, size=3072), read_ahead_bytes=1024, **options
                )
                == b"b" * 1024
            )
            await asyncio.gather(*tuple(cache._background))
            assert [(request.location.id, request.offset) for request in requests] == [(12, 0), (12, 1024)]
            assert await _download_cached_media(streaming, invoke, target, offset=1024, **options) == b"c" * 1024
            assert (
                await _download_cached_media(streaming, invoke, encode_file_id(raw), offset=1024, **options)
                == b"d" * 1024
            )
            assert [(request.location.id, request.offset) for request in requests] == [(12, 0), (12, 1024), (11, 1024)]
        finally:
            await cache.clear()

    asyncio.run(scenario())


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("replace_resource", [False, True])
def test_automatic_cache_key_remains_bound_during_reference_refresh(streaming: bool, replace_resource: bool) -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=4096)
        requests: list[Any] = []
        target = encode_file_id(_cache_document())

        async def invoke(request: Any, **_kwargs: object) -> object:
            assert isinstance(request, functions.UploadGetFile)
            requests.append(request)
            if len(requests) == 1:
                raise BadRequest("FILE_REFERENCE_EXPIRED")
            return _cached_file_part((b"a" if request.location.id == 11 else b"b") * 1024)

        def refresh(location: object) -> object:
            assert isinstance(location, types.InputDocumentFileLocation)
            return types.InputDocumentFileLocation(
                id=12 if replace_resource else 11,
                access_hash=location.access_hash,
                file_reference=b"renewed",
                thumb_size=location.thumb_size,
            )

        options = {"limit": 1024, "part_size": 1024, "range_cache": cache}
        try:
            operation = _download_cached_media(streaming, invoke, target, file_reference_refresher=refresh, **options)
            if replace_resource:
                with pytest.raises(MediaDownloadError, match="file identity changed"):
                    await operation
                assert len(requests) == 1
            else:
                assert await operation == b"a" * 1024
                assert requests[-1].location.file_reference == b"renewed"
            assert await _download_cached_media(streaming, invoke, target, **options) == b"a" * 1024
            assert len(requests) == 2
            assert all(request.location.id == 11 for request in requests)
        finally:
            await cache.clear()

    asyncio.run(scenario())


@pytest.mark.parametrize("streaming", [False, True])
def test_legacy_location_has_no_automatic_file_id_cache_key(streaming: bool) -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=4096)
        requests: list[object] = []
        raw = types.InputFileLocation(volume_id=1, local_id=2, secret=3, file_reference=b"reference")

        async def invoke(request: object, **_kwargs: object) -> object:
            requests.append(request)
            return _cached_file_part(b"legacy")

        try:
            for _ in range(2):
                assert (
                    await _download_cached_media(
                        streaming, invoke, _cache_wrapper(raw=raw), limit=6, part_size=1024, range_cache=cache
                    )
                    == b"legacy"
                )
            assert len(requests) == 2
            assert not cache._entries
        finally:
            await cache.clear()

    asyncio.run(scenario())
