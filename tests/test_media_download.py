from __future__ import annotations

import asyncio
import hashlib
import random
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
from miniproto.errors import (
    BadRequest,
    ClientDisconnected,
    FloodWait,
    RpcError,
    TransportFlood,
    classify_rpc_error,
)
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
        result = await download_file(
            invoker, document_location(), target, part_size=1024, resume=True
        )
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
        first_result = await download_media(
            first, file_id, limit=3, part_size=1024, range_cache=cache
        )
        assert first_result.data == b"abc"
        second = FakeInvoker([])
        second_result = await download_media(
            second, file_id, limit=3, part_size=1024, range_cache=cache
        )
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
        new_location = types.InputDocumentFileLocation(
            id=10, access_hash=20, file_reference=b"new-ref", thumb_size=""
        )
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
        throttle_events = [
            event for event in metrics.events if event.name == "media.download.adaptive_throttle"
        ]
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

        pacer = media_download._DownloadLaunchPacer(
            concurrency=6, clock=lambda: now[0], sleep=sleep
        )
        for _ in range(10):
            pacer.on_success()
            now[0] += 0.1
        pacer.on_flood(FloodWait(1))
        await pacer.wait()
        await pacer.wait()
        assert sleeps
        assert max(sleeps) >= 1 / 9

    run(scenario())


def test_download_flood_retry_sleep_only_uses_large_floor_for_zero_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
        disabled = [
            event for event in metrics.events if event.name == "media.download.read_ahead_disabled"
        ]
        assert disabled
        # No prefetch requests beyond the transfer itself.
        assert sorted(request.offset for request in invoker.requests) == [0, 1024]

    run(scenario())


def test_progress_reporter_coalesces_and_always_finishes() -> None:
    async def scenario() -> None:
        clock_value = [0.0]
        calls: list[tuple[int, int | None]] = []
        reporter = media_download._ProgressReporter(
            lambda current, total: calls.append((current, total)),
            total=100,
            clock=lambda: clock_value[0],
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
        payload = bytes(range(256)) * 17  # 4352 bytes: 4 full parts + 256-byte tail
        media = Media(id=10, size=len(payload), location=document_location())
        invoker = OffsetInvoker(payload)
        result = await download_media(
            invoker, media, part_size=1024, adaptive_part_size=False, concurrency=2
        )
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
        request_timeout: float | None = None,
    ) -> object:
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

        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
        client._sender_factory = sender_factory
        await client.connect()
        first = await client.download_media(
            media_one, part_size=1024, limit=1024, concurrency=1, media_lanes=1
        )
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
            ClientConfig(
                api_id=1, api_hash="hash", session_storage=storage_with_auth(), media_idle_close=0.1
            )
        )
        client._sender_factory = sender_factory
        await client.connect()
        first = await client.download_media(
            media, part_size=1024, limit=1024, concurrency=1, media_lanes=1
        )
        assert first.data == b"a" * 1024
        assert lane_senders[0].is_connected
        for _ in range(50):
            if not lane_senders[0].is_connected:
                break
            await asyncio.sleep(0.05)
        # The idle reaper closed the lane; the pool transparently rebuilds on
        # the next transfer.
        assert not lane_senders[0].is_connected
        second = await client.download_media(
            media, part_size=1024, limit=1024, concurrency=1, media_lanes=1
        )
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

        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=_multi_dc_storage())
        )
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
        foreign_lane = FakeSender(
            [types.AuthAuthorization(user=types.UserEmpty(id=1)), upload_file_part(b"z" * 1024)]
        )
        built: list[int] = []

        def sender_factory(record: SessionRecord) -> FakeSender:
            built.append(record.dc_id or 0)
            return foreign_lane if record.dc_id == 5 else main_sender

        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=_multi_dc_storage())
        )
        client._sender_factory = sender_factory
        await client.connect()
        result = await client.download_media(
            media, part_size=1024, limit=1024, concurrency=1, media_lanes=1
        )
        assert result.data == b"z" * 1024
        # Media whose DC is known goes straight to a (kind, dc=5) pool; no
        # FILE_MIGRATE round trip on the session DC.
        assert 5 in built
        assert isinstance(inner_request(foreign_lane.requests[1]), functions.UploadGetFile)
        await client.disconnect()

    run(scenario())


def test_client_download_media_rejects_unknown_options() -> None:
    async def scenario() -> None:
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=storage_with_auth())
        )
        with pytest.raises(TypeError, match="unsupported download_media options"):
            await client.download_media(Media(id=1, location=document_location()), unsupported=True)

    run(scenario())
