from __future__ import annotations

import asyncio
import hashlib
from dataclasses import dataclass, field
from typing import Any

import pytest

import miniproto.media.download as media_download
from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    Media,
    SessionRecord,
    encode_file_id,
    event_loop,
)
from miniproto.errors import BadRequest, ClientDisconnected, TransportFlood
from miniproto.media import (
    CdnIntegrityError,
    DownloadRangeCache,
    MediaDownloadError,
    decrypt_cdn_chunk,
    download_file,
    download_media,
)
from miniproto.observability import InMemoryMetrics, get_metrics_sink, set_metrics_sink
from miniproto.raw import functions, types

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
    requests: list[Any] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        assert isinstance(request, functions.UploadGetFile)
        await asyncio.sleep(0)
        if request.offset in self.flood_offsets:
            self.flood_offsets.remove(request.offset)
            raise TransportFlood(0)
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
class RefreshingOffsetInvoker:
    payload: bytes
    old_reference: bytes
    requests: list[Any] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        self.requests.append(request)
        assert isinstance(request, functions.UploadGetFile)
        await asyncio.sleep(0.01)
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
        request_timeout: float | None = None,
    ) -> object:
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
    return types.InputDocumentFileLocation(
        id=10, access_hash=20, file_reference=b"ref", thumb_size=""
    )


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
        target.write_bytes(b"old")
        progress: list[tuple[int, int | None]] = []
        invoker = FakeInvoker([upload_file_part(b"new")])
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=6,
            part_size=1024,
            resume=True,
            progress=lambda current, total: progress.append((current, total)),
        )
        assert target.read_bytes() == b"oldnew"
        assert result.destination == target
        assert result.bytes_downloaded == 6
        assert invoker.requests[0].offset == 3
        assert invoker.requests[0].limit == 3
        assert progress == [(6, 6)]

    run(scenario())


def test_download_file_concurrent_writes_ordered_payload(tmp_path) -> None:
    async def scenario() -> None:
        payload = b"abcdefghijklmnopqrstuvwxyz"
        target = tmp_path / "concurrent.bin"
        progress: list[tuple[int, int | None]] = []
        invoker = OffsetInvoker(payload)
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=5,
            concurrency=3,
            progress=lambda current, total: progress.append((current, total)),
        )
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        assert sorted(request.offset for request in invoker.requests) == [0, 5, 10, 15, 20, 25]
        assert progress[-1] == (len(payload), len(payload))

    run(scenario())


def test_download_file_concurrent_respects_byte_window(tmp_path) -> None:
    async def scenario() -> None:
        payload = b"abcdefghijklmnop"
        target = tmp_path / "byte-window.bin"
        invoker = SlowOffsetInvoker(payload)
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=4,
            concurrency=4,
            max_in_flight_bytes=4,
        )
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        assert invoker.max_active == 1
        assert [request.offset for request in invoker.requests] == [0, 4, 8, 12]

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
        cache = DownloadRangeCache(max_bytes=1024)
        first = FakeInvoker([upload_file_part(b"abc")])
        first_result = await download_media(first, file_id, limit=3, part_size=3, range_cache=cache)
        assert first_result.data == b"abc"
        second = FakeInvoker([])
        second_result = await download_media(
            second, file_id, limit=3, part_size=3, range_cache=cache
        )
        assert second_result.data == b"abc"
        assert len(first.requests) == 1
        assert second.requests == []

    run(scenario())


def test_download_file_read_ahead_prefetches_into_range_cache() -> None:
    async def scenario() -> None:
        cache = DownloadRangeCache(max_bytes=1024)
        invoker = OffsetInvoker(b"abcdef")
        result = await download_file(
            invoker,
            document_location(),
            limit=3,
            part_size=3,
            range_cache=cache,
            range_cache_key="doc:10",
            read_ahead_bytes=3,
        )
        assert result.data == b"abc"
        for _ in range(10):
            if len(invoker.requests) >= 2:
                break
            await asyncio.sleep(0.01)
        assert [request.offset for request in invoker.requests] == [0, 3]
        cached = await cache.get("doc:10", 3, 3)
        assert cached == b"def"

    run(scenario())


def test_download_file_deduplicates_file_reference_refresh(tmp_path) -> None:
    async def scenario() -> None:
        old_location = document_location()
        new_location = types.InputDocumentFileLocation(
            id=10, access_hash=20, file_reference=b"new-ref", thumb_size=""
        )
        refresh_calls = 0

        async def refresher(location: object) -> object:
            nonlocal refresh_calls
            assert location == old_location
            refresh_calls += 1
            await asyncio.sleep(0.01)
            return new_location

        payload = b"abcdefgh"
        target = tmp_path / "refreshed.bin"
        invoker = RefreshingOffsetInvoker(payload, old_reference=b"ref")
        result = await download_file(
            invoker,
            old_location,
            target,
            limit=len(payload),
            part_size=4,
            concurrency=2,
            adaptive_concurrency=False,
            max_retries=0,
            file_reference_refresher=refresher,
        )
        assert target.read_bytes() == payload
        assert result.raw_location == new_location
        assert refresh_calls == 1
        assert [request.location.file_reference for request in invoker.requests].count(b"ref") == 2
        assert [request.location.file_reference for request in invoker.requests].count(
            b"new-ref"
        ) == 2

    run(scenario())


def test_download_file_retries_transient_get_file_failure() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([ClientDisconnected("sender disconnected"), upload_file_part(b"abc")])
        result = await download_file(
            invoker, document_location(), part_size=1024, request_timeout=3, max_retries=1
        )
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
            await download_file(
                invoker, document_location(), part_size=1024, max_retries=2, flood_sleep_threshold=1
            )
        assert len(invoker.requests) == 1

    run(scenario())


def test_download_file_does_not_retry_non_transient_get_file_failure() -> None:
    async def scenario() -> None:
        invoker = FakeInvoker([BadRequest("FILE_REFERENCE_EXPIRED")])
        with pytest.raises(BadRequest):
            await download_file(invoker, document_location(), part_size=1024, max_retries=2)
        assert len(invoker.requests) == 1

    run(scenario())


def test_download_file_concurrent_retries_transient_chunk_failure(tmp_path) -> None:
    async def scenario() -> None:
        payload = b"abcdefghijklmnopqrstuvwxyz"
        target = tmp_path / "retry.bin"
        invoker = FlakyOffsetInvoker(payload, fail_offsets={10})
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=5,
            concurrency=3,
            max_retries=1,
        )
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        offsets = [request.offset for request in invoker.requests]
        assert offsets.count(10) == 2

    run(scenario())


def test_download_file_adaptive_concurrency_records_throttle(tmp_path) -> None:
    async def scenario() -> None:
        payload = b"abcdefgh"
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
                part_size=1,
                concurrency=4,
                max_retries=1,
                flood_sleep_threshold=1,
            )
        finally:
            set_metrics_sink(None)
        assert target.read_bytes() == payload
        assert result.bytes_downloaded == len(payload)
        throttle_events = [
            event for event in metrics.events if event.name == "media.download.adaptive_throttle"
        ]
        assert throttle_events
        assert min(event.value for event in throttle_events) < 4

    run(scenario())


def test_adaptive_download_throttle_slow_starts_and_ramps_after_cooldown() -> None:
    async def scenario() -> None:
        clock_value = [0.0]

        def clock() -> float:
            return clock_value[0]

        throttle = media_download._AdaptiveDownloadThrottle(4, clock=clock)
        assert throttle.limit == 1
        for _ in range(7):
            throttle.on_success()
        assert throttle.limit == 1
        throttle.on_success()
        assert throttle.limit == 2
        await throttle.on_retry(TransportFlood(0), 1)
        assert throttle.limit == 1
        for _ in range(20):
            throttle.on_success()
        assert throttle.limit == 1
        clock_value[0] = 2.1
        for _ in range(7):
            throttle.on_success()
        assert throttle.limit == 1
        throttle.on_success()
        assert throttle.limit == 2

    run(scenario())


def test_adaptive_part_sizer_grows_and_settles_on_regression() -> None:
    sizer = media_download._AdaptivePartSizer(
        initial_size=4,
        max_size=16,
        total_bytes=1024,
        enabled=True,
        min_total_bytes=0,
        min_samples=2,
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
                    dc_id=4,
                    file_token=b"token",
                    encryption_key=key,
                    encryption_iv=iv,
                    file_hashes=(),
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
                    dc_id=4,
                    file_token=b"token",
                    encryption_key=key,
                    encryption_iv=iv,
                    file_hashes=(),
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
        payload = b"known-size-download"
        media = Media(id=10, size=len(payload), location=document_location())
        invoker = OffsetInvoker(payload)
        result = await download_media(invoker, media, part_size=4, concurrency=2)
        assert result.data == payload
        assert sorted(request.offset for request in invoker.requests) == [0, 4, 8, 12, 16]

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
        assert invoker.requests[0].limit == 1024 * 1024

    run(scenario())


def test_download_file_cleans_partial_path_on_cancellation(tmp_path) -> None:
    async def scenario() -> None:
        target = tmp_path / "partial.bin"
        invoker = FakeInvoker([upload_file_part(b"partial"), asyncio.CancelledError()])
        with pytest.raises(asyncio.CancelledError):
            await download_file(invoker, document_location(), target, part_size=7)
        assert not target.exists()

    run(scenario())


def test_download_file_enforces_memory_ceiling() -> None:
    async def scenario() -> None:
        with pytest.raises(ValueError, match="max_in_flight_bytes"):
            await download_file(
                bad_invoker, document_location(), part_size=1024, max_buffer_size=512
            )

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
        payload = b"abcdefghijklmnop"
        target = tmp_path / "buffer-window.bin"
        invoker = SlowOffsetInvoker(payload)
        result = await download_file(
            invoker,
            document_location(),
            target,
            limit=len(payload),
            part_size=8,
            concurrency=2,
            max_buffer_size=8,
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
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
        client._sender = sender
        await client.connect()
        result = await client.download_media(media, media_lanes=0)
        request = inner_request(sender.requests[0])
        assert isinstance(request, functions.UploadGetFile)
        assert request.location == document_location()
        assert request.cdn_supported is True
        assert result.data == b"abc"

    run(scenario())


def test_client_download_media_uses_dedicated_media_lanes() -> None:
    async def scenario() -> None:
        media = Media(id=10, size=2048, location=document_location())
        lane_senders = [
            FakeSender([upload_file_part(b"a" * 1024)]),
            FakeSender([upload_file_part(b"b" * 1024)]),
        ]
        built_senders: list[FakeSender] = []

        def sender_factory(record: SessionRecord) -> FakeSender:
            del record
            sender = lane_senders[len(built_senders)]
            built_senders.append(sender)
            return sender

        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
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

        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
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


def test_client_download_media_rejects_unknown_options() -> None:
    async def scenario() -> None:
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
        with pytest.raises(TypeError, match="unsupported download_media options"):
            await client.download_media(Media(id=1, location=document_location()), unsupported=True)

    run(scenario())
