from __future__ import annotations

import asyncio
import hashlib
import inspect
import io
import logging
import os
import random
import time
from collections import OrderedDict, deque
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, cast

from miniproto.errors import ClientDisconnected, FloodWait, InternalServerError, RequestTimeout, RpcError, RpcTimeout
from miniproto.file_id import is_file_id, media_from_file_id
from miniproto.media.cdn import cdn_redirect_from_raw, get_cdn_file_part
from miniproto.media.retry import backoff_delay
from miniproto.media.upload import ProgressCallback
from miniproto.observability import emit_event, get_logger, record_metric
from miniproto.raw import functions, types
from miniproto.types import Media

type Destination = str | os.PathLike[str] | BinaryIO | None


class MediaDownloadError(RuntimeError):
    pass


class MediaIntegrityError(MediaDownloadError):
    def __init__(self, reason: str, *, offset: int, limit: int) -> None:
        self.offset = offset
        self.limit = limit
        self.reason = reason
        super().__init__(f"media integrity {reason} at offset {offset} for {limit} bytes")


type RawInvoker = Callable[..., Awaitable[object]]
type DownloadRetryObserver = Callable[[Exception, int], Awaitable[None] | None]
type FileReferenceRefresher = Callable[[object], Awaitable[object] | object]
type Clock = Callable[[], float]
type SleepFunc = Callable[[float], Awaitable[None]]
_LOGGER = get_logger("media.download")
MAX_DOWNLOAD_CHUNK_SIZE = 1024 * 1024
# 2 lanes x ~3 pipelined 512 KiB..1 MiB requests with an 8 MiB rolling byte
# window sustains bandwidth x RTT for ~16 MiB/s at WAN latencies (mtcute ships
# 2 conns x 3 in-flight; MTKruto 2 x 2 x 1 MiB).
DEFAULT_DOWNLOAD_PART_SIZE = 512 * 1024
DEFAULT_DOWNLOAD_CONCURRENCY = 6
DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES = 8 * 1024 * 1024
DEFAULT_RANGE_CACHE_BYTES = 64 * 1024 * 1024
DEFAULT_ADAPTIVE_PART_SIZE_MIN_BYTES = 8 * 1024 * 1024
_MIB = 1024 * 1024
_ALIGNMENT = 4096
_PRECISE_ALIGNMENT = 1024
_MAX_BACKGROUND_PREFETCHES = 32
# Floods within the sleep threshold are server pacing and retry without
# consuming the transient-failure budget; this cap only bounds pathological
# storms (16 x <=30 s worst case per part).
MAX_FLOOD_RETRIES_PER_PART = 16
_MIN_FLOOD_SLEEP_S = 1.0
_FLOOD_SLEEP_JITTER_S = 0.3
_MAX_LAUNCH_PACE_INTERVAL_S = 0.25
# mtcute's DownloadDelayGate constants: stagger request launches so opening the
# window does not burst-fire every request in one event-loop tick (burst starts
# reliably attract FLOOD_WAITs).
_STAGGER_INITIAL_DELAY = 0.05
_STAGGER_DECAY = 0.8
_STAGGER_FLOOR = 0.003
_PROGRESS_MIN_INTERVAL = 0.25
_PROGRESS_MAX_PARTS = 8


@dataclass(frozen=True, slots=True)
class MediaDownloadResult:
    bytes_downloaded: int
    offset: int
    destination: Path | BinaryIO | None = None
    data: bytes | None = None
    raw_location: object | None = None


@dataclass(slots=True)
class _DestinationHandle:
    handle: BinaryIO
    path: Path | None
    should_close: bool
    remove_on_cancel: bool
    discard_on_failure: bool
    existing_bytes: int
    get_data: Callable[[], bytes | None]
    restore_on_failure: Callable[[], None] | None = None


@dataclass(slots=True)
class _DownloadWriterStats:
    queued_seconds: float = 0.0
    write_seconds: float = 0.0
    writes: int = 0


@dataclass(slots=True)
class _WriteRequest:
    offset: int
    payload: bytes
    queued_at: float
    acknowledgement: asyncio.Future[None]


def _validate_concurrent_payload(request_offset: int, payload: bytes, *, expect_limit: int, target_end: int) -> bytes:
    if request_offset < 0 or expect_limit < 0 or request_offset + expect_limit > target_end:
        raise ValueError("concurrent download range is outside the target interval")
    received = len(payload)
    if received > expect_limit:
        payload = payload[:expect_limit]
    if len(payload) != expect_limit:
        raise MediaDownloadError(
            f"concurrent download chunk at offset {request_offset} expected "
            f"{expect_limit} bytes but received {received}"
        )
    return payload


class DownloadRangeCache:
    def __init__(self, *, max_bytes: int = DEFAULT_RANGE_CACHE_BYTES) -> None:
        if max_bytes <= 0:
            raise ValueError("range cache max_bytes must be positive")
        self.max_bytes = int(max_bytes)
        self._entries: OrderedDict[tuple[str, int, int], bytes] = OrderedDict()
        self._pending: dict[tuple[str, int, int], asyncio.Task[bytes]] = {}
        self._background: set[asyncio.Task[None]] = set()
        self._size = 0
        self._lock = asyncio.Lock()

    async def get(self, key: str, offset: int, limit: int) -> bytes | None:
        cache_key = (key, offset, limit)
        async with self._lock:
            payload = self._entries.get(cache_key)
            if payload is None:
                record_metric("media.download.range_cache_misses", 1)
                return None
            self._entries.move_to_end(cache_key)
            record_metric("media.download.range_cache_hits", 1)
            return payload

    async def put(self, key: str, offset: int, limit: int, payload: bytes) -> None:
        if not payload or len(payload) > self.max_bytes:
            return
        cache_key = (key, offset, limit)
        async with self._lock:
            previous = self._entries.pop(cache_key, None)
            if previous is not None:
                self._size -= len(previous)
            self._entries[cache_key] = payload
            self._size += len(payload)
            while self._size > self.max_bytes and self._entries:
                _old_key, old_payload = self._entries.popitem(last=False)
                self._size -= len(old_payload)
            record_metric("media.download.range_cache_bytes", self._size, unit="bytes")

    async def get_or_fetch(self, key: str, offset: int, limit: int, fetch: Callable[[], Awaitable[bytes]]) -> bytes:
        async def run_fetch() -> bytes:
            return await fetch()

        cached = await self.get(key, offset, limit)
        if cached is not None:
            return cached
        cache_key = (key, offset, limit)
        async with self._lock:
            task = self._pending.get(cache_key)
            if task is None:
                task = asyncio.create_task(run_fetch())
                self._pending[cache_key] = task
                record_metric("media.download.range_cache_fetches", 1)
            else:
                record_metric("media.download.range_cache_deduped", 1)
        try:
            payload = await task
        finally:
            async with self._lock:
                if self._pending.get(cache_key) is task:
                    del self._pending[cache_key]
        await self.put(key, offset, limit, payload)
        return payload

    def prefetch(self, key: str, offset: int, limit: int, fetch: Callable[[], Awaitable[bytes]]) -> None:
        if len(self._background) >= _MAX_BACKGROUND_PREFETCHES:
            # Unbounded background fetches were 3x slower than no read-ahead at
            # all on live benches; skip instead of queueing ever more work.
            record_metric("media.download.range_cache_prefetch_skipped", 1)
            return

        async def run() -> None:
            try:
                await self.get_or_fetch(key, offset, limit, fetch)
            except Exception:
                record_metric("media.download.range_cache_prefetch_errors", 1)

        task = asyncio.create_task(run())
        self._background.add(task)
        task.add_done_callback(self._background.discard)

    async def clear(self) -> None:
        async with self._lock:
            pending = tuple(self._pending.values())
            background = tuple(self._background)
            self._pending.clear()
            self._background.clear()
            self._entries.clear()
            self._size = 0
        for task in (*pending, *background):
            task.cancel()
        if pending or background:
            await asyncio.gather(*pending, *background, return_exceptions=True)


class _PlainFileHashVerifier:
    _MAX_HASH_REQUESTS = 32
    _MAX_HASH_INTERVAL = MAX_DOWNLOAD_CHUNK_SIZE

    def __init__(
        self,
        invoke: RawInvoker,
        *,
        location_state: _DownloadLocationState,
        precise: bool,
        cdn_supported: bool,
        request_timeout: float | None,
        max_retries: int,
        flood_sleep_threshold: int | None,
        reference_deduper: _FileReferenceRefreshDeduper,
        file_reference_refresher: FileReferenceRefresher | None,
        max_cached_bytes: int,
    ) -> None:
        self._invoke = invoke
        self._location_state = location_state
        self._precise = precise
        self._cdn_supported = cdn_supported
        self._request_timeout = request_timeout
        self._max_retries = max_retries
        self._flood_sleep_threshold = flood_sleep_threshold
        self._reference_deduper = reference_deduper
        self._file_reference_refresher = file_reference_refresher
        self._max_cached_bytes = max(MAX_DOWNLOAD_CHUNK_SIZE, max_cached_bytes)
        self._identity: tuple[object, ...] | None = None
        self._hashes: dict[tuple[int, int], bytes] = {}
        self._validated: OrderedDict[tuple[tuple[object, ...], int, int, bytes], bytes] = OrderedDict()
        self._validated_bytes = 0
        self._validation_tasks: dict[tuple[tuple[object, ...], int, int, bytes], asyncio.Task[bytes]] = {}
        self._metadata_lock = asyncio.Lock()

    async def verify(self, location: object, *, offset: int, payload: bytes) -> None:
        if not payload:
            return
        identity = _plain_location_identity(location)
        await self._ensure_identity(identity)
        end = offset + len(payload)
        intervals = await self._ensure_hash_coverage(location, offset, end)
        self._assert_identity(identity, offset=offset, limit=len(payload))
        for hash_offset, hash_limit, expected_hash in intervals:
            hash_end = hash_offset + hash_limit
            if hash_offset == offset and hash_limit == len(payload):
                verified = self._verify_digest(payload, expected_hash, offset=hash_offset, limit=hash_limit)
                self._assert_identity(identity, offset=hash_offset, limit=hash_limit)
                self._remember_validated((identity, hash_offset, hash_limit, expected_hash), verified)
            else:
                verified = await self._validated_interval(identity, hash_offset, hash_limit, expected_hash)
            self._assert_identity(identity, offset=hash_offset, limit=hash_limit)
            overlap_start = max(offset, hash_offset)
            overlap_end = min(end, hash_end)
            actual_slice = payload[overlap_start - offset : overlap_end - offset]
            verified_slice = verified[overlap_start - hash_offset : overlap_end - hash_offset]
            if actual_slice != verified_slice:
                raise MediaIntegrityError("mismatch", offset=overlap_start, limit=overlap_end - overlap_start)

    async def _ensure_identity(self, identity: tuple[object, ...]) -> None:
        async with self._metadata_lock:
            if self._identity == identity:
                return
            self._identity = identity
            self._hashes.clear()
            self._validated.clear()
            self._validated_bytes = 0
            self._validation_tasks.clear()
            record_metric("media.download.plain_hash_cache_invalidations", 1)

    def _assert_identity(self, identity: tuple[object, ...], *, offset: int, limit: int) -> None:
        if self._identity != identity or _plain_location_identity(self._location_state.current) != identity:
            raise MediaIntegrityError("location changed during verification", offset=offset, limit=limit)

    async def _ensure_hash_coverage(self, location: object, start: int, end: int) -> tuple[tuple[int, int, bytes], ...]:
        async with self._metadata_lock:
            for _attempt in range(self._MAX_HASH_REQUESTS):
                covered = self._covering_intervals(start, end)
                if covered is not None:
                    return covered
                cursor = self._first_uncovered_offset(start, end)
                request = functions.UploadGetFileHashes(location=location, offset=cursor)
                record_metric("media.download.plain_hash_requests", 1)
                result = await self._invoke(
                    request, request_timeout=self._request_timeout, retry=False, flood_sleep_threshold=0
                )
                if not isinstance(result, tuple | list) or not result:
                    raise MediaIntegrityError("hash coverage gap", offset=cursor, limit=end - cursor)
                before = len(self._hashes)
                for item in result:
                    self._remember_hash(item)
                if len(self._hashes) == before:
                    raise MediaIntegrityError("hash response loop", offset=cursor, limit=end - cursor)
            cursor = self._first_uncovered_offset(start, end)
            raise MediaIntegrityError("hash response limit exceeded", offset=cursor, limit=end - cursor)

    def _remember_hash(self, item: object) -> None:
        if not isinstance(item, types.FileHash):
            raise MediaIntegrityError("invalid hash metadata", offset=0, limit=0)
        offset = int(item.offset)
        limit = int(item.limit)
        digest = bytes(item.hash)
        if offset < 0 or limit <= 0 or limit > self._MAX_HASH_INTERVAL or len(digest) != hashlib.sha256().digest_size:
            raise MediaIntegrityError("invalid hash metadata", offset=max(0, offset), limit=max(0, limit))
        key = (offset, limit)
        existing = self._hashes.get(key)
        if existing is not None:
            if existing != digest:
                raise MediaIntegrityError("contradictory hash metadata", offset=offset, limit=limit)
            return
        end = offset + limit
        for (known_offset, known_limit), _known_hash in self._hashes.items():
            known_end = known_offset + known_limit
            if offset < known_end and known_offset < end:
                raise MediaIntegrityError(
                    "contradictory overlapping hash metadata",
                    offset=max(offset, known_offset),
                    limit=min(end, known_end) - max(offset, known_offset),
                )
        self._hashes[key] = digest

    def _covering_intervals(self, start: int, end: int) -> tuple[tuple[int, int, bytes], ...] | None:
        cursor = start
        result: list[tuple[int, int, bytes]] = []
        for (offset, limit), digest in sorted(self._hashes.items()):
            interval_end = offset + limit
            if interval_end <= cursor:
                continue
            if offset > cursor:
                return None
            result.append((offset, limit, digest))
            cursor = interval_end
            if cursor >= end:
                return tuple(result)
        return None

    def _first_uncovered_offset(self, start: int, end: int) -> int:
        cursor = start
        for (offset, limit), _digest in sorted(self._hashes.items()):
            interval_end = offset + limit
            if interval_end <= cursor:
                continue
            if offset > cursor:
                break
            cursor = interval_end
            if cursor >= end:
                break
        return min(cursor, end)

    async def _validated_interval(
        self, identity: tuple[object, ...], offset: int, limit: int, expected_hash: bytes
    ) -> bytes:
        key = (identity, offset, limit, expected_hash)
        cached = self._validated.get(key)
        if cached is not None:
            self._validated.move_to_end(key)
            return cached
        task = self._validation_tasks.get(key)
        if task is None:
            task = asyncio.create_task(self._fetch_and_verify_interval(identity, offset, limit, expected_hash))
            self._validation_tasks[key] = task
        try:
            payload = await task
        finally:
            if self._validation_tasks.get(key) is task:
                self._validation_tasks.pop(key, None)
        self._assert_identity(identity, offset=offset, limit=limit)
        self._remember_validated(key, payload)
        return payload

    async def _fetch_and_verify_interval(
        self, identity: tuple[object, ...], offset: int, limit: int, expected_hash: bytes
    ) -> bytes:
        cursor = offset
        remaining = limit
        chunks: list[bytes] = []
        while remaining > 0:
            self._assert_identity(identity, offset=cursor, limit=remaining)
            target = min(remaining, MAX_DOWNLOAD_CHUNK_SIZE)
            wire_limit = _legal_request_limit(cursor, target, precise=self._precise)
            if wire_limit is None:
                wire_limit = _PRECISE_ALIGNMENT if self._precise else _ALIGNMENT
            payload = await _download_part_with_reference_refresh(
                self._invoke,
                location_state=self._location_state,
                offset=cursor,
                limit=wire_limit,
                precise=self._precise,
                cdn_supported=self._cdn_supported,
                request_timeout=self._request_timeout,
                max_retries=self._max_retries,
                flood_sleep_threshold=self._flood_sleep_threshold,
                retry_observer=None,
                reference_deduper=self._reference_deduper,
                file_reference_refresher=self._file_reference_refresher,
                plain_verifier=None,
            )
            self._assert_identity(identity, offset=cursor, limit=remaining)
            if not payload:
                raise MediaIntegrityError("hash interval coverage gap", offset=cursor, limit=remaining)
            take = min(remaining, len(payload))
            chunks.append(payload[:take])
            cursor += take
            remaining -= take
        return self._verify_digest(b"".join(chunks), expected_hash, offset=offset, limit=limit)

    @staticmethod
    def _verify_digest(payload: bytes, expected_hash: bytes, *, offset: int, limit: int) -> bytes:
        if hashlib.sha256(payload).digest() != expected_hash:
            record_metric("media.download.plain_hash_mismatches", 1)
            raise MediaIntegrityError("hash mismatch", offset=offset, limit=limit)
        record_metric("media.download.plain_hash_verified_bytes", limit, unit="bytes")
        return payload

    def _remember_validated(self, key: tuple[tuple[object, ...], int, int, bytes], payload: bytes) -> None:
        previous = self._validated.pop(key, None)
        if previous is not None:
            self._validated_bytes -= len(previous)
        self._validated[key] = payload
        self._validated_bytes += len(payload)
        while self._validated_bytes > self._max_cached_bytes and self._validated:
            _old_key, old_payload = self._validated.popitem(last=False)
            self._validated_bytes -= len(old_payload)


_DEFAULT_RANGE_CACHE: DownloadRangeCache | None = None


def _legal_request_limit(offset: int, max_bytes: int, *, precise: bool) -> int | None:
    """Largest protocol-legal ``upload.getFile`` limit at ``offset``.

    Telegram rules (core.telegram.org/api/files): without ``precise``, offset and
    limit must be divisible by 4096 and limit must divide 1 MiB; with ``precise``
    they must be divisible by 1024. In both modes a request must never straddle
    a 1 MiB boundary. Returns ``None`` when no legal request fits ``max_bytes``
    (the caller defers or over-requests the tail and truncates).
    """
    alignment = _PRECISE_ALIGNMENT if precise else _ALIGNMENT
    boundary_room = _MIB - (offset % _MIB)
    allowed = min(max_bytes, boundary_room)
    if allowed < alignment:
        return None
    if precise:
        return (allowed // alignment) * alignment
    # Non-precise limits must divide 1 MiB, i.e. be a power of two >= 4096.
    return 1 << (allowed.bit_length() - 1)


def _resolve_precise_mode(start_offset: int, precise: bool, part_size: int) -> bool:
    """Auto-enable precise mode when offsets or part sizes need 1 KiB granularity.

    Non-precise ``upload.getFile`` requires 4 KiB-aligned offsets and limits;
    precise mode relaxes both to 1 KiB. Offsets below 1 KiB alignment cannot be
    expressed at all and are rejected.
    """
    if start_offset % _PRECISE_ALIGNMENT != 0:
        raise ValueError(
            f"download offset {start_offset} must be a multiple of 1024 bytes; "
            "truncate resumed files to a 1 KiB boundary"
        )
    if not precise and (start_offset % _ALIGNMENT != 0 or part_size % _ALIGNMENT != 0):
        record_metric("media.download.precise_auto_enabled", 1)
        return True
    return precise


def _is_full_file_download(offset: int, limit: int | None, total_size: int | None) -> bool:
    if limit is None:
        return True
    return total_size is not None and offset + limit >= total_size


class _TransferWindow:
    """Slot/byte budget for in-flight download requests.

    A part task sleeping out a ``FLOOD_WAIT`` keeps holding its slot: floods
    are the server's pacing signal, and backfilling freed slots with new
    requests sustains the request rate the server just objected to (observed
    live as an escalation from FLOOD_WAIT_2 to FLOOD_WAIT_15 and thousands of
    retries). Holding the slot lets pressure drop naturally while every other
    slot keeps flowing -- mtcute's fixed-slot model.
    """

    def __init__(self, max_bytes: int) -> None:
        self.max_bytes = max(1, max_bytes)
        self.in_flight_bytes = 0
        self.active = 0
        self._refill = asyncio.Event()

    def _has_room(self, nbytes: int) -> bool:
        return self.in_flight_bytes == 0 or self.in_flight_bytes + nbytes <= self.max_bytes

    def try_acquire(self, nbytes: int) -> bool:
        if not self._has_room(nbytes):
            return False
        self.in_flight_bytes += nbytes
        self.active += 1
        return True

    def release(self, nbytes: int) -> None:
        self.in_flight_bytes = max(0, self.in_flight_bytes - nbytes)
        self.active = max(0, self.active - 1)
        self._refill.set()

    async def wait_refill(self) -> None:
        await self._refill.wait()
        self._refill.clear()


class _DownloadDelayGate:
    """Stagger request launches at transfer start (mtcute's DownloadDelayGate)."""

    def __init__(
        self, *, initial: float = _STAGGER_INITIAL_DELAY, decay: float = _STAGGER_DECAY, floor: float = _STAGGER_FLOOR
    ) -> None:
        self._initial = initial
        self._delay = initial
        self._decay = decay
        self._floor = floor

    async def wait(self) -> None:
        delay = self._delay
        self._delay = max(self._floor, delay * self._decay)
        if delay > 0:
            await asyncio.sleep(delay)

    def reset(self) -> None:
        """Re-arm the full stagger after a flood so launches stop bursting."""
        self._delay = self._initial


class _DownloadLaunchPacer:
    """Pace launches after floods without reducing the fixed request slots."""

    def __init__(self, *, concurrency: int, clock: Clock = time.monotonic, sleep: SleepFunc = asyncio.sleep) -> None:
        self._concurrency = max(1, concurrency)
        self._clock = clock
        self._sleep = sleep
        self._stagger = _DownloadDelayGate() if self._concurrency > 1 else None
        self._success_times: deque[float] = deque(maxlen=64)
        self._min_interval = 0.0
        self._next_launch_at = 0.0
        self._clean_successes = 0

    async def wait(self) -> None:
        if self._min_interval > 0:
            now = self._clock()
            wait_s = max(0.0, self._next_launch_at - now)
            if wait_s > 0:
                record_metric("media.download.launch_pace_wait_seconds", wait_s, unit="s")
                await self._sleep(wait_s)
                now = self._clock()
            self._next_launch_at = max(self._next_launch_at, now) + self._min_interval
        if self._stagger is not None:
            await self._stagger.wait()

    def on_success(self) -> None:
        self._success_times.append(self._clock())
        if self._min_interval <= 0:
            return
        self._clean_successes += 1
        if self._clean_successes < max(4, self._concurrency * 2):
            return
        self._clean_successes = 0
        self._min_interval *= 0.9
        if self._min_interval < _STAGGER_FLOOR:
            self._min_interval = 0.0
        if self._min_interval > 0:
            record_metric("media.download.launch_pace_rate", 1.0 / self._min_interval)

    def on_flood(self, exc: FloodWait) -> None:
        if self._stagger is not None:
            self._stagger.reset()
        self._clean_successes = 0
        target_rate = self._target_rate()
        interval = 1.0 / target_rate
        if self._min_interval > 0:
            interval = max(interval, self._min_interval * 1.25)
        self._min_interval = min(_MAX_LAUNCH_PACE_INTERVAL_S, interval)
        self._next_launch_at = max(self._next_launch_at, self._clock() + self._min_interval)
        record_metric(
            "media.download.launch_pace_rate", 1.0 / self._min_interval, attributes={"reason": type(exc).__name__}
        )

    def reset(self) -> None:
        if self._stagger is not None:
            self._stagger.reset()
        self._min_interval = 0.0
        self._next_launch_at = 0.0
        self._clean_successes = 0

    @property
    def current_rate_per_s(self) -> float:
        if self._min_interval <= 0:
            return 0.0
        return 1.0 / self._min_interval

    def _target_rate(self) -> float:
        now = self._clock()
        while self._success_times and now - self._success_times[0] > 10.0:
            self._success_times.popleft()
        if len(self._success_times) >= 2:
            span = max(now - self._success_times[0], 1e-9)
            return max(1.0, len(self._success_times) / span * 0.9)
        return max(1.0, float(self._concurrency))


class _ProgressReporter:
    """Coalesce progress callbacks to >=250 ms apart or every 8 parts.

    Per-part callbacks add measurable latency on 512 KiB parts; the final call
    is always delivered via ``finish()`` so consumers observe completion.
    """

    def __init__(
        self,
        progress: ProgressCallback | None,
        total: int | None,
        *,
        min_interval: float = _PROGRESS_MIN_INTERVAL,
        max_parts: int = _PROGRESS_MAX_PARTS,
        clock: Clock = time.monotonic,
    ) -> None:
        self._progress = progress
        self._total = total
        self._min_interval = min_interval
        self._max_parts = max_parts
        self._clock = clock
        self._last_time = float("-inf")
        self._parts_since_report = 0
        self._last_reported: int | None = None

    async def report(self, current: int) -> None:
        if self._progress is None:
            return
        self._parts_since_report += 1
        now = self._clock()
        if now - self._last_time < self._min_interval and self._parts_since_report < self._max_parts:
            return
        self._last_time = now
        self._parts_since_report = 0
        self._last_reported = current
        await _call_progress(self._progress, current, self._total)

    async def finish(self, current: int) -> None:
        if self._progress is None or self._last_reported == current:
            return
        self._last_reported = current
        await _call_progress(self._progress, current, self._total)


async def iter_download(
    invoke: RawInvoker,
    location: object,
    *,
    offset: int = 0,
    limit: int | None = None,
    part_size: int = DEFAULT_DOWNLOAD_PART_SIZE,
    progress: ProgressCallback | None = None,
    precise: bool = False,
    cdn_supported: bool = True,
    total_size: int | None = None,
    request_timeout: float | None = None,
    max_retries: int = 2,
    flood_sleep_threshold: int | None = 30,
    max_buffer_size: int | None = None,
    concurrency: int = DEFAULT_DOWNLOAD_CONCURRENCY,
    adaptive_concurrency: bool = True,
    max_in_flight_bytes: int | None = None,
    adaptive_part_size: bool = True,
    max_part_size: int = MAX_DOWNLOAD_CHUNK_SIZE,
    range_cache: DownloadRangeCache | bool | None = None,
    range_cache_key: str | None = None,
    range_cache_max_bytes: int = DEFAULT_RANGE_CACHE_BYTES,
    read_ahead_bytes: int = 0,
    verify_plain_hashes: bool = False,
    file_reference_refresher: FileReferenceRefresher | None = None,
) -> AsyncGenerator[bytes]:
    """Yield an exact download range as ordered, bounded byte chunks."""

    _validate_download_options(
        offset,
        limit,
        part_size,
        max_retries,
        flood_sleep_threshold,
        max_buffer_size,
        concurrency,
        max_in_flight_bytes,
        adaptive_part_size,
        max_part_size,
        range_cache_max_bytes,
        read_ahead_bytes,
        precise,
    )
    if not isinstance(verify_plain_hashes, bool):
        raise TypeError("verify_plain_hashes must be a bool")
    if limit is None and total_size is not None:
        limit = max(0, total_size - offset)
    if read_ahead_bytes > 0 and _is_full_file_download(offset, limit, total_size):
        record_metric("media.download.read_ahead_disabled", 1)
        read_ahead_bytes = 0
    resolved_range_cache = _resolve_range_cache(
        range_cache, max_bytes=range_cache_max_bytes, read_ahead_bytes=read_ahead_bytes
    )
    effective_max_in_flight_bytes = max_in_flight_bytes if max_in_flight_bytes is not None else max_buffer_size
    location_state = _DownloadLocationState(location)
    reference_deduper = _FileReferenceRefreshDeduper()
    parts = _iter_download_parts(
        invoke,
        location_state=location_state,
        offset=offset,
        limit=limit,
        part_size=part_size,
        progress=progress,
        precise=precise,
        cdn_supported=cdn_supported,
        total_size=total_size,
        request_timeout=request_timeout,
        max_retries=max_retries,
        flood_sleep_threshold=flood_sleep_threshold,
        concurrency=concurrency,
        adaptive_concurrency=adaptive_concurrency,
        max_in_flight_bytes=effective_max_in_flight_bytes,
        adaptive_part_size=adaptive_part_size,
        max_part_size=max_part_size,
        range_cache=resolved_range_cache,
        range_cache_key=range_cache_key,
        read_ahead_bytes=read_ahead_bytes,
        verify_plain_hashes=verify_plain_hashes,
        reference_deduper=reference_deduper,
        file_reference_refresher=file_reference_refresher,
    )
    try:
        async for payload in parts:
            yield payload
    finally:
        await parts.aclose()


async def _iter_download_parts(
    invoke: RawInvoker,
    *,
    location_state: _DownloadLocationState,
    offset: int,
    limit: int | None,
    part_size: int,
    progress: ProgressCallback | None,
    precise: bool,
    cdn_supported: bool,
    total_size: int | None,
    request_timeout: float | None,
    max_retries: int,
    flood_sleep_threshold: int | None,
    concurrency: int,
    adaptive_concurrency: bool,
    max_in_flight_bytes: int | None,
    adaptive_part_size: bool,
    max_part_size: int,
    range_cache: DownloadRangeCache | None,
    range_cache_key: str | None,
    read_ahead_bytes: int,
    verify_plain_hashes: bool,
    reference_deduper: _FileReferenceRefreshDeduper,
    file_reference_refresher: FileReferenceRefresher | None,
) -> AsyncGenerator[bytes]:
    end_offset = None if limit is None else offset + limit
    next_request_offset = offset
    next_yield_offset = offset
    effective_precise = _resolve_precise_mode(offset, precise, part_size)
    effective_concurrency = concurrency if end_offset is not None else 1
    byte_window = max_in_flight_bytes or max(DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES, part_size * effective_concurrency)
    window = _TransferWindow(byte_window)
    pending: set[asyncio.Task[tuple[int, bytes, int, int, bool]]] = set()
    charges: dict[int, int] = {}
    ready: dict[int, tuple[bytes, int, bool]] = {}
    reporter = _ProgressReporter(progress, limit if limit is not None else total_size)
    launch_pacer = _DownloadLaunchPacer(concurrency=effective_concurrency) if effective_concurrency > 1 else None
    throttle = (
        _AdaptiveDownloadThrottle(effective_concurrency) if adaptive_concurrency and effective_concurrency > 1 else None
    )
    part_sizer = _AdaptivePartSizer(
        initial_size=part_size,
        max_size=max_part_size,
        total_bytes=limit if limit is not None else total_size,
        enabled=adaptive_part_size,
    )
    plain_verifier = (
        _PlainFileHashVerifier(
            invoke,
            location_state=location_state,
            precise=effective_precise,
            cdn_supported=cdn_supported,
            request_timeout=request_timeout,
            max_retries=max_retries,
            flood_sleep_threshold=flood_sleep_threshold,
            reference_deduper=reference_deduper,
            file_reference_refresher=file_reference_refresher,
            max_cached_bytes=byte_window,
        )
        if verify_plain_hashes
        else None
    )
    downloaded = 0
    exhausted = False

    async def on_part_retry(exc: Exception, attempt: int) -> None:
        if throttle is not None:
            await throttle.on_retry(exc, attempt)
            if launch_pacer is not None and throttle.limit <= 1:
                launch_pacer.reset()
        if launch_pacer is not None and isinstance(exc, FloodWait) and (throttle is None or throttle.limit > 1):
            launch_pacer.on_flood(exc)

    async def fetch(request_offset: int, wire_limit: int, expect_limit: int) -> tuple[int, bytes, int, int, bool]:
        started = time.perf_counter()
        payload = await _download_part_cached(
            invoke,
            location_state=location_state,
            offset=request_offset,
            limit=wire_limit,
            precise=effective_precise,
            cdn_supported=cdn_supported,
            request_timeout=request_timeout,
            max_retries=max_retries,
            flood_sleep_threshold=flood_sleep_threshold,
            retry_observer=on_part_retry,
            range_cache=range_cache,
            range_cache_key=range_cache_key,
            reference_deduper=reference_deduper,
            file_reference_refresher=file_reference_refresher,
            plain_verifier=plain_verifier,
        )
        received = len(payload)
        short_read = received < wire_limit
        if end_offset is not None:
            if received == 0 and expect_limit > 0 and effective_concurrency <= 1:
                raise MediaDownloadError(
                    f"download returned empty payload with {end_offset - request_offset} bytes remaining"
                )
            payload = _validate_concurrent_payload(
                request_offset, payload, expect_limit=expect_limit, target_end=end_offset
            )
        elif len(payload) > expect_limit:
            payload = payload[:expect_limit]
        if throttle is not None:
            throttle.on_success()
        if launch_pacer is not None:
            launch_pacer.on_success()
        part_sizer.on_success(
            requested_size=wire_limit, received_size=received, duration_s=max(time.perf_counter() - started, 1e-9)
        )
        return request_offset, payload, expect_limit, wire_limit, short_read

    async def fill_window() -> None:
        nonlocal next_request_offset
        while not exhausted and (end_offset is None or next_request_offset < end_offset):
            allowed = effective_concurrency if throttle is None else min(effective_concurrency, throttle.limit)
            if window.active >= allowed:
                return
            remaining = part_sizer.current_size if end_offset is None else end_offset - next_request_offset
            target = min(part_sizer.current_size, window.max_bytes, remaining)
            wire_limit = _legal_request_limit(next_request_offset, target, precise=effective_precise)
            if wire_limit is None:
                wire_limit = _PRECISE_ALIGNMENT if effective_precise else _ALIGNMENT
            expect_limit = wire_limit if end_offset is None else min(wire_limit, end_offset - next_request_offset)
            if not window.try_acquire(wire_limit):
                record_metric("media.download.byte_window_waits", 1)
                return
            if launch_pacer is not None and allowed > 1:
                await launch_pacer.wait()
            request_offset = next_request_offset
            charges[request_offset] = wire_limit
            pending.add(asyncio.create_task(fetch(request_offset, wire_limit, expect_limit)))
            record_metric("media.download.in_flight_bytes", window.in_flight_bytes, unit="bytes")
            next_request_offset += expect_limit

    try:
        await fill_window()
        while pending or ready:
            current = ready.pop(next_yield_offset, None)
            if current is not None:
                payload, _expect_limit, short_read = current
                charge = charges.pop(next_yield_offset)
                if not payload:
                    window.release(charge)
                    exhausted = True
                    break
                try:
                    yield payload
                finally:
                    window.release(charge)
                downloaded += len(payload)
                next_yield_offset += len(payload)
                await reporter.report(downloaded)
                _prefetch_read_ahead(
                    invoke,
                    location_state=location_state,
                    precise=effective_precise,
                    cdn_supported=cdn_supported,
                    request_timeout=request_timeout,
                    max_retries=max_retries,
                    flood_sleep_threshold=flood_sleep_threshold,
                    range_cache=range_cache,
                    range_cache_key=range_cache_key,
                    start_offset=next_yield_offset,
                    part_size=part_sizer.current_size,
                    read_ahead_bytes=read_ahead_bytes,
                    hard_end=total_size,
                    reference_deduper=reference_deduper,
                    file_reference_refresher=file_reference_refresher,
                )
                if short_read:
                    exhausted = True
                await fill_window()
                continue
            if not pending:
                break
            done, _ = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                pending.discard(task)
                request_offset, payload, expect_limit, _wire_limit, short_read = await task
                ready[request_offset] = (payload, expect_limit, short_read)
        if end_offset is not None and next_yield_offset != end_offset:
            raise MediaDownloadError(
                f"incomplete streamed download coverage for [{offset}, {end_offset}); stopped at {next_yield_offset}"
            )
        await reporter.finish(downloaded)
    finally:
        await _cancel_tasks(pending)
        for charge in charges.values():
            window.release(charge)


async def download_file(
    invoke: RawInvoker,
    location: object,
    destination: Destination = None,
    *,
    offset: int = 0,
    limit: int | None = None,
    part_size: int = DEFAULT_DOWNLOAD_PART_SIZE,
    resume: bool = False,
    progress: ProgressCallback | None = None,
    precise: bool = False,
    cdn_supported: bool = True,
    total_size: int | None = None,
    request_timeout: float | None = None,
    max_retries: int = 2,
    flood_sleep_threshold: int | None = 30,
    max_buffer_size: int | None = None,
    concurrency: int = DEFAULT_DOWNLOAD_CONCURRENCY,
    adaptive_concurrency: bool = True,
    max_in_flight_bytes: int | None = None,
    adaptive_part_size: bool = True,
    max_part_size: int = MAX_DOWNLOAD_CHUNK_SIZE,
    range_cache: DownloadRangeCache | bool | None = None,
    range_cache_key: str | None = None,
    range_cache_max_bytes: int = DEFAULT_RANGE_CACHE_BYTES,
    read_ahead_bytes: int = 0,
    verify_plain_hashes: bool = False,
    file_reference_refresher: FileReferenceRefresher | None = None,
) -> MediaDownloadResult:
    _validate_download_options(
        offset,
        limit,
        part_size,
        max_retries,
        flood_sleep_threshold,
        max_buffer_size,
        concurrency,
        max_in_flight_bytes,
        adaptive_part_size,
        max_part_size,
        range_cache_max_bytes,
        read_ahead_bytes,
        precise,
    )
    if not isinstance(verify_plain_hashes, bool):
        raise TypeError("verify_plain_hashes must be a bool")
    if read_ahead_bytes > 0 and _is_full_file_download(offset, limit, total_size):
        record_metric("media.download.read_ahead_disabled", 1)
        emit_event(
            _LOGGER,
            logging.WARNING,
            "media.download.read_ahead",
            outcome="disabled",
            reason="full_file_download",
            read_ahead_bytes=read_ahead_bytes,
        )
        read_ahead_bytes = 0
    resolved_range_cache = _resolve_range_cache(
        range_cache, max_bytes=range_cache_max_bytes, read_ahead_bytes=read_ahead_bytes
    )
    effective_max_in_flight_bytes = max_in_flight_bytes if max_in_flight_bytes is not None else max_buffer_size
    location_state = _DownloadLocationState(location)
    reference_deduper = _FileReferenceRefreshDeduper()
    if limit is None and concurrency > 1 and total_size is not None:
        limit = max(0, total_size - offset)
    destination_handle = _open_destination(destination, resume=resume)
    original_existing = destination_handle.existing_bytes
    verified_existing = original_existing if limit is None else min(original_existing, limit)
    destination_handle.existing_bytes = verified_existing
    if destination_handle.path is not None and verified_existing != original_existing:
        destination_handle.handle.seek(verified_existing)
    remaining = None if limit is None else max(0, limit - verified_existing)
    current_offset = offset + verified_existing
    downloaded = verified_existing
    reporter = _ProgressReporter(progress, limit if limit is not None else total_size)
    writer: _ConcurrentDestinationWriter | None = None
    write_acks: deque[tuple[asyncio.Future[None], int]] = deque()

    async def report_committed(*, drain_all: bool = False) -> None:
        nonlocal downloaded
        while write_acks and (drain_all or write_acks[0][0].done()):
            acknowledgement, payload_size = write_acks.popleft()
            await acknowledgement
            downloaded += payload_size
            if limit is None or downloaded < limit:
                await reporter.report(downloaded)

    started = time.perf_counter()
    try:
        writer = _ConcurrentDestinationWriter(
            destination_handle,
            queue_size=max(1, concurrency),
            preallocate_size=limit
            if destination_handle.path is not None and limit is not None and concurrency > 1
            else None,
            sequential=True,
        )
        parts = _iter_download_parts(
            invoke,
            location_state=location_state,
            offset=current_offset,
            limit=remaining,
            part_size=part_size,
            progress=None,
            precise=precise,
            cdn_supported=cdn_supported,
            total_size=total_size,
            request_timeout=request_timeout,
            max_retries=max_retries,
            flood_sleep_threshold=flood_sleep_threshold,
            concurrency=concurrency,
            adaptive_concurrency=adaptive_concurrency,
            max_in_flight_bytes=effective_max_in_flight_bytes,
            adaptive_part_size=adaptive_part_size,
            max_part_size=max_part_size,
            range_cache=resolved_range_cache,
            range_cache_key=range_cache_key,
            read_ahead_bytes=read_ahead_bytes,
            verify_plain_hashes=verify_plain_hashes,
            reference_deduper=reference_deduper,
            file_reference_refresher=file_reference_refresher,
        )
        try:
            async for payload in parts:
                acknowledgement = await writer.submit(
                    downloaded - verified_existing, payload, wait_for_completion=False
                )
                write_acks.append((acknowledgement, len(payload)))
                await report_committed()
        finally:
            await parts.aclose()
        stats = await writer.close()
        _record_writer_stats(stats)
        await report_committed(drain_all=True)
        if original_existing > verified_existing and limit is not None:
            await _truncate_destination(destination_handle, limit)
        await reporter.finish(downloaded)
        if destination_handle.should_close:
            destination_handle.handle.close()
        result = MediaDownloadResult(
            bytes_downloaded=downloaded,
            offset=offset,
            destination=destination_handle.path or destination_handle.handle,
            data=destination_handle.get_data(),
            raw_location=location_state.current,
        )
    except asyncio.CancelledError:
        await report_committed()
        if writer is not None:
            await writer.abort()
        if write_acks:
            await asyncio.gather(*(ack for ack, _size in write_acks), return_exceptions=True)
        await _cleanup_failed_destination(destination_handle)
        duration_ms = (time.perf_counter() - started) * 1000
        record_metric("media.download.errors", 1, attributes={"concurrency": concurrency, "limit": limit})
        emit_event(
            _LOGGER,
            40,
            "media.download",
            outcome="error",
            offset=offset,
            limit=limit,
            part_size=part_size,
            concurrency=concurrency,
            duration_ms=duration_ms,
        )
        raise
    except BaseException:
        await report_committed()
        if writer is not None:
            await writer.abort()
        if write_acks:
            await asyncio.gather(*(ack for ack, _size in write_acks), return_exceptions=True)
        await _cleanup_failed_destination(destination_handle)
        duration_ms = (time.perf_counter() - started) * 1000
        record_metric("media.download.errors", 1, attributes={"concurrency": concurrency, "limit": limit})
        emit_event(
            _LOGGER,
            40,
            "media.download",
            outcome="error",
            offset=offset,
            limit=limit,
            part_size=part_size,
            concurrency=concurrency,
            duration_ms=duration_ms,
        )
        raise
    duration_ms = (time.perf_counter() - started) * 1000
    throughput_bytes_s = result.bytes_downloaded / max(duration_ms / 1000, 1e-9)
    record_metric(
        "media.download.bytes",
        result.bytes_downloaded,
        unit="bytes",
        attributes={"concurrency": concurrency, "limit": limit},
    )
    record_metric(
        "media.download.duration", duration_ms, unit="ms", attributes={"concurrency": concurrency, "limit": limit}
    )
    record_metric(
        "media.download.throughput",
        throughput_bytes_s,
        unit="bytes/s",
        attributes={"concurrency": concurrency, "limit": limit},
    )
    emit_event(
        _LOGGER,
        20,
        "media.download",
        outcome="success",
        bytes_downloaded=result.bytes_downloaded,
        offset=offset,
        limit=limit,
        part_size=part_size,
        concurrency=concurrency,
        duration_ms=duration_ms,
        throughput_bytes_s=throughput_bytes_s,
    )
    return result


async def iter_download_media(invoke: RawInvoker, media: object, **kwargs: Any) -> AsyncGenerator[bytes]:
    if "range_cache_key" not in kwargs or kwargs.get("range_cache_key") is None:
        kwargs["range_cache_key"] = _range_cache_key_from_media(media)
    location = download_location_from_media(media)
    total_size = kwargs.pop("total_size", None)
    if total_size is None:
        resolved = (
            media
            if isinstance(media, Media)
            else media_from_file_id(media)
            if is_file_id(media)
            else media_from_raw(media)
        )
        if resolved is not None:
            total_size = resolved.size
    async for payload in iter_download(invoke, location, total_size=total_size, **kwargs):
        yield payload


async def download_media(
    invoke: RawInvoker, media: object, destination: Destination = None, **kwargs: Any
) -> MediaDownloadResult:
    if "range_cache_key" not in kwargs or kwargs.get("range_cache_key") is None:
        kwargs["range_cache_key"] = _range_cache_key_from_media(media)
    location = download_location_from_media(media)
    total_size = kwargs.pop("total_size", None)
    if total_size is None:
        # Resolve the size from any media shape so concurrency never silently
        # degrades to the sequential path when the caller omits limit.
        resolved = (
            media
            if isinstance(media, Media)
            else media_from_file_id(media)
            if is_file_id(media)
            else media_from_raw(media)
        )
        if resolved is not None:
            total_size = resolved.size
    return await download_file(invoke, location, destination, total_size=total_size, **kwargs)


def download_location_from_media(media: object) -> object:
    if is_file_id(media):
        return download_location_from_media(media_from_file_id(media))
    if isinstance(media, Media):
        if media.location is not None:
            return media.location
        if media.raw is not None:
            return download_location_from_media(media.raw)
    if _is_input_file_location(media):
        return media
    if isinstance(media, types.Message):
        return download_location_from_media(media.media)
    if isinstance(media, types.MessageMediaDocument) and media.document is not None:
        return download_location_from_media(media.document)
    if isinstance(media, types.Document):
        return types.InputDocumentFileLocation(
            id=media.id, access_hash=media.access_hash, file_reference=media.file_reference, thumb_size=""
        )
    if isinstance(media, types.MessageMediaPhoto) and media.photo is not None:
        return download_location_from_media(media.photo)
    if isinstance(media, types.Photo):
        thumb_size = _largest_photo_thumb_size(media.sizes)
        return types.InputPhotoFileLocation(
            id=media.id, access_hash=media.access_hash, file_reference=media.file_reference, thumb_size=thumb_size
        )
    raise MediaDownloadError(f"cannot resolve download location from {type(media).__name__}")


def media_from_raw(raw: object) -> Media | None:
    if isinstance(raw, Media):
        return raw
    if raw is None:
        return None
    if isinstance(raw, types.Message):
        return media_from_raw(raw.media)
    if isinstance(raw, types.UpdateShortSentMessage):
        return media_from_raw(raw.media)
    if isinstance(raw, types.MessageMediaDocument) and isinstance(raw.document, types.Document):
        return _media_from_document(raw.document, raw=raw)
    if isinstance(raw, types.Document):
        return _media_from_document(raw, raw=raw)
    if isinstance(raw, types.MessageMediaPhoto) and isinstance(raw.photo, types.Photo):
        return _media_from_photo(raw.photo, raw=raw)
    if isinstance(raw, types.Photo):
        return _media_from_photo(raw, raw=raw)
    if _is_input_file_location(raw):
        return Media(id=0, raw=raw, location=raw)
    return None


class _DownloadLocationState:
    def __init__(self, location: object) -> None:
        self._location = location
        self._lock = asyncio.Lock()

    @property
    def current(self) -> object:
        return self._location

    async def refresh(
        self, *, reference_deduper: _FileReferenceRefreshDeduper, refresher: FileReferenceRefresher
    ) -> object:
        old_location = self._location
        new_location = await reference_deduper.refresh(old_location, refresher)
        async with self._lock:
            if _file_reference_bytes(self._location) == _file_reference_bytes(old_location):
                self._location = new_location
            return self._location


class _FileReferenceRefreshDeduper:
    def __init__(self) -> None:
        self._pending: dict[bytes, asyncio.Task[object]] = {}
        self._lock = asyncio.Lock()

    async def refresh(self, location: object, refresher: FileReferenceRefresher) -> object:
        reference = _file_reference_bytes(location)
        if not reference:
            refreshed = refresher(location)
            return await refreshed if inspect.isawaitable(refreshed) else refreshed
        async with self._lock:
            task = self._pending.get(reference)
            if task is None:
                task = asyncio.create_task(_call_file_reference_refresher(refresher, location))
                self._pending[reference] = task
                record_metric("media.download.file_reference_refreshes", 1)
            else:
                record_metric("media.download.file_reference_refresh_deduped", 1)
        try:
            return await task
        finally:
            async with self._lock:
                if self._pending.get(reference) is task:
                    del self._pending[reference]


async def _call_file_reference_refresher(refresher: FileReferenceRefresher, location: object) -> object:
    refreshed = refresher(location)
    return await refreshed if inspect.isawaitable(refreshed) else refreshed


async def _payload_from_get_file_result(
    invoke: RawInvoker,
    result: object,
    *,
    location: object,
    offset: int,
    limit: int,
    request_timeout: float | None,
    plain_verifier: _PlainFileHashVerifier | None,
) -> bytes:
    redirect = cdn_redirect_from_raw(result)
    if redirect is not None:
        return await get_cdn_file_part(invoke, redirect, offset=offset, limit=limit, request_timeout=request_timeout)
    if isinstance(result, types.UploadFile):
        payload = result.bytes
        if plain_verifier is not None:
            await plain_verifier.verify(location, offset=offset, payload=payload)
        return payload
    raise MediaDownloadError(f"unsupported upload.getFile response: {type(result).__name__}")


async def _download_part_cached(
    invoke: RawInvoker,
    *,
    location_state: _DownloadLocationState,
    offset: int,
    limit: int,
    precise: bool,
    cdn_supported: bool,
    request_timeout: float | None,
    max_retries: int,
    flood_sleep_threshold: int | None,
    range_cache: DownloadRangeCache | None,
    range_cache_key: str | None,
    reference_deduper: _FileReferenceRefreshDeduper,
    file_reference_refresher: FileReferenceRefresher | None,
    retry_observer: DownloadRetryObserver | None = None,
    plain_verifier: _PlainFileHashVerifier | None = None,
) -> bytes:
    use_range_cache = range_cache is not None and range_cache_key is not None

    async def fetch() -> bytes:
        return await _download_part_with_reference_refresh(
            invoke,
            location_state=location_state,
            offset=offset,
            limit=limit,
            precise=precise,
            cdn_supported=cdn_supported,
            request_timeout=request_timeout,
            max_retries=max_retries,
            flood_sleep_threshold=flood_sleep_threshold,
            retry_observer=retry_observer,
            reference_deduper=reference_deduper,
            file_reference_refresher=file_reference_refresher,
            plain_verifier=None if use_range_cache else plain_verifier,
        )

    if not use_range_cache:
        return await fetch()
    assert range_cache is not None and range_cache_key is not None
    payload = await range_cache.get_or_fetch(range_cache_key, offset, limit, fetch)
    if plain_verifier is not None:
        await plain_verifier.verify(location_state.current, offset=offset, payload=payload)
    return payload


async def _download_part_with_reference_refresh(
    invoke: RawInvoker,
    *,
    location_state: _DownloadLocationState,
    offset: int,
    limit: int,
    precise: bool,
    cdn_supported: bool,
    request_timeout: float | None,
    max_retries: int,
    flood_sleep_threshold: int | None,
    retry_observer: DownloadRetryObserver | None,
    reference_deduper: _FileReferenceRefreshDeduper,
    file_reference_refresher: FileReferenceRefresher | None,
    plain_verifier: _PlainFileHashVerifier | None = None,
) -> bytes:
    for refresh_attempt in range(2):
        try:
            return await _download_part(
                invoke,
                location=location_state.current,
                offset=offset,
                limit=limit,
                precise=precise,
                cdn_supported=cdn_supported,
                request_timeout=request_timeout,
                max_retries=max_retries,
                flood_sleep_threshold=flood_sleep_threshold,
                retry_observer=retry_observer,
                plain_verifier=plain_verifier,
            )
        except Exception as exc:
            if file_reference_refresher is None or refresh_attempt > 0 or not _is_file_reference_error(exc):
                raise
            record_metric("media.download.file_reference_refresh_attempts", 1)
            emit_event(
                _LOGGER,
                logging.WARNING,
                "media.download.file_reference_refresh",
                outcome="retry",
                offset=offset,
                limit=limit,
                error_type=type(exc).__name__,
            )
            await location_state.refresh(reference_deduper=reference_deduper, refresher=file_reference_refresher)
    raise MediaDownloadError(f"download part at offset {offset} did not complete")


async def _download_part(
    invoke: RawInvoker,
    *,
    location: object,
    offset: int,
    limit: int,
    precise: bool,
    cdn_supported: bool,
    request_timeout: float | None,
    max_retries: int,
    flood_sleep_threshold: int | None,
    retry_observer: DownloadRetryObserver | None = None,
    plain_verifier: _PlainFileHashVerifier | None = None,
) -> bytes:
    request = functions.UploadGetFile(
        precise=precise, cdn_supported=cdn_supported, location=location, offset=offset, limit=limit
    )
    failures = 0
    flood_retries = 0
    while True:
        try:
            record_metric("media.download.part_requests", 1)
            result = await invoke(request, request_timeout=request_timeout, retry=False, flood_sleep_threshold=0)
            return await _payload_from_get_file_result(
                invoke,
                result,
                location=location,
                offset=offset,
                limit=limit,
                request_timeout=request_timeout,
                plain_verifier=plain_verifier,
            )
        except Exception as exc:
            if not _is_transient_download_error(exc, flood_sleep_threshold=flood_sleep_threshold):
                raise
            if isinstance(exc, FloodWait):
                # Floods within the threshold are server pacing, not failures:
                # they never consume the transient retry budget (a 2 GiB
                # transfer routinely sees several per part). A generous
                # separate cap still bounds pathological storms.
                flood_retries += 1
                if flood_retries > MAX_FLOOD_RETRIES_PER_PART:
                    record_metric("media.download.flood_retry_budget_exhausted", 1)
                    raise
                attempt = flood_retries
            else:
                failures += 1
                if failures > max_retries:
                    raise
                attempt = failures
            _emit_part_retry(
                offset=offset,
                limit=limit,
                attempt=attempt,
                max_retries=max_retries,
                error_type=type(exc).__name__,
                flood_wait_seconds=exc.seconds if isinstance(exc, FloodWait) else None,
            )
            if retry_observer is not None:
                observed = retry_observer(exc, attempt)
                if inspect.isawaitable(observed):
                    await observed
            await _sleep_before_retry(exc, failures)


def _media_from_document(document: types.Document, *, raw: object) -> Media:
    file_name = _document_file_name(document.attributes)
    location = types.InputDocumentFileLocation(
        id=document.id, access_hash=document.access_hash, file_reference=document.file_reference, thumb_size=""
    )
    return Media(
        id=document.id,
        mime_type=document.mime_type,
        size=document.size,
        file_name=file_name,
        raw=raw,
        access_hash=document.access_hash,
        file_reference=document.file_reference,
        dc_id=document.dc_id,
        location=location,
    )


def _media_from_photo(photo: types.Photo, *, raw: object) -> Media:
    size = _largest_photo_size(photo.sizes)
    thumb_size = _largest_photo_thumb_size(photo.sizes)
    location = types.InputPhotoFileLocation(
        id=photo.id, access_hash=photo.access_hash, file_reference=photo.file_reference, thumb_size=thumb_size
    )
    return Media(
        id=photo.id,
        mime_type="image/jpeg",
        size=size,
        raw=raw,
        access_hash=photo.access_hash,
        file_reference=photo.file_reference,
        dc_id=photo.dc_id,
        location=location,
    )


def _document_file_name(attributes: tuple[object, ...]) -> str | None:
    for attribute in attributes:
        if isinstance(attribute, types.DocumentAttributeFilename):
            return attribute.file_name
    return None


def _largest_photo_size(sizes: tuple[object, ...]) -> int | None:
    candidates: list[int] = []
    for size in sizes:
        value = getattr(size, "size", None)
        if isinstance(value, int):
            candidates.append(value)
    return max(candidates) if candidates else None


def _largest_photo_thumb_size(sizes: tuple[object, ...]) -> str:
    sized: list[tuple[object, int]] = []
    for size in sizes:
        value = getattr(size, "size", None)
        if isinstance(value, int):
            sized.append((size, value))
    if sized:
        selected = max(sized, key=lambda item: item[1])[0]
        thumb = getattr(selected, "type", "")
        return thumb if isinstance(thumb, str) else ""
    for size in reversed(sizes):
        thumb = getattr(size, "type", "")
        if isinstance(thumb, str):
            return thumb
    return ""


def _is_input_file_location(value: object) -> bool:
    return getattr(type(value), "RESULT_TYPE", None) == "InputFileLocation"


def _range_cache_key_from_media(media: object) -> str | None:
    if is_file_id(media):
        return str(media)
    if isinstance(media, Media):
        return media.file_id
    resolved = media_from_raw(media)
    return resolved.file_id if resolved is not None else None


def _resolve_range_cache(
    range_cache: DownloadRangeCache | bool | None, *, max_bytes: int, read_ahead_bytes: int
) -> DownloadRangeCache | None:
    if isinstance(range_cache, DownloadRangeCache):
        return range_cache
    if range_cache is False:
        return None
    if range_cache is True or read_ahead_bytes > 0:
        return _default_range_cache(max_bytes)
    return None


def _default_range_cache(max_bytes: int) -> DownloadRangeCache:
    global _DEFAULT_RANGE_CACHE
    if _DEFAULT_RANGE_CACHE is None or _DEFAULT_RANGE_CACHE.max_bytes != max_bytes:
        _DEFAULT_RANGE_CACHE = DownloadRangeCache(max_bytes=max_bytes)
    return _DEFAULT_RANGE_CACHE


def _prefetch_read_ahead(
    invoke: RawInvoker,
    *,
    location_state: _DownloadLocationState,
    precise: bool,
    cdn_supported: bool,
    request_timeout: float | None,
    max_retries: int,
    flood_sleep_threshold: int | None,
    range_cache: DownloadRangeCache | None,
    range_cache_key: str | None,
    start_offset: int,
    part_size: int,
    read_ahead_bytes: int,
    hard_end: int | None,
    reference_deduper: _FileReferenceRefreshDeduper,
    file_reference_refresher: FileReferenceRefresher | None,
) -> None:
    if range_cache is None or range_cache_key is None or read_ahead_bytes <= 0:
        return
    alignment = _PRECISE_ALIGNMENT if precise else _ALIGNMENT
    if start_offset % alignment != 0:
        # A short read left the cursor on an offset Telegram cannot serve;
        # prefetching from here would only produce protocol errors.
        record_metric("media.download.read_ahead_unaligned_skips", 1)
        return
    remaining = read_ahead_bytes
    current_offset = start_offset
    while remaining > 0 and (hard_end is None or current_offset < hard_end):
        request_limit = _legal_request_limit(current_offset, min(part_size, remaining), precise=precise)
        if request_limit is None:
            break
        if hard_end is not None and current_offset + request_limit > hard_end:
            reduced = _legal_request_limit(current_offset, hard_end - current_offset, precise=precise)
            request_limit = reduced if reduced is not None else request_limit
        if request_limit <= 0:
            break
        offset_for_task = current_offset
        limit_for_task = request_limit

        async def fetch(offset: int = offset_for_task, limit: int = limit_for_task) -> bytes:
            async def background_invoke(request: object, **kwargs: Any) -> object:
                kwargs["_media_priority"] = "background"
                return await invoke(request, **kwargs)

            return await _download_part_with_reference_refresh(
                background_invoke,
                location_state=location_state,
                offset=offset,
                limit=limit,
                precise=precise,
                cdn_supported=cdn_supported,
                request_timeout=request_timeout,
                max_retries=max_retries,
                flood_sleep_threshold=flood_sleep_threshold,
                retry_observer=None,
                reference_deduper=reference_deduper,
                file_reference_refresher=file_reference_refresher,
            )

        range_cache.prefetch(range_cache_key, offset_for_task, limit_for_task, fetch)
        current_offset += request_limit
        remaining -= request_limit


def _file_reference_bytes(location: object) -> bytes:
    reference = getattr(location, "file_reference", b"")
    if isinstance(reference, bytes):
        return reference
    if isinstance(reference, bytearray | memoryview):
        return bytes(reference)
    if isinstance(reference, str):
        return reference.encode("utf-8")
    return b""


def _plain_location_identity(location: object) -> tuple[object, ...]:
    return (
        getattr(type(location), "QUALNAME", type(location).__qualname__),
        getattr(location, "id", None),
        getattr(location, "access_hash", None),
        getattr(location, "volume_id", None),
        getattr(location, "local_id", None),
        getattr(location, "secret", None),
        getattr(location, "thumb_size", None),
        _file_reference_bytes(location),
    )


def _is_file_reference_error(exc: Exception) -> bool:
    if not isinstance(exc, RpcError):
        return False
    message = exc.message.upper()
    name = exc.rpc_error_name.upper()
    return "FILE_REFERENCE" in message or "FILE_REFERENCE" in name


def _validate_download_options(
    offset: int,
    limit: int | None,
    part_size: int,
    max_retries: int,
    flood_sleep_threshold: int | None,
    max_buffer_size: int | None,
    concurrency: int,
    max_in_flight_bytes: int | None,
    adaptive_part_size: bool,
    max_part_size: int,
    range_cache_max_bytes: int,
    read_ahead_bytes: int,
    precise: bool = False,
) -> None:
    del precise  # part sizes below 4 KiB auto-enable precise mode instead
    if offset < 0:
        raise ValueError("offset must not be negative")
    if limit is not None and limit < 0:
        raise ValueError("limit must not be negative")
    if part_size < _PRECISE_ALIGNMENT:
        raise ValueError(f"part_size must be at least {_PRECISE_ALIGNMENT} bytes")
    if part_size > MAX_DOWNLOAD_CHUNK_SIZE:
        raise ValueError("part_size must not exceed 1 MiB")
    if part_size & (part_size - 1):
        # Telegram limits must divide 1 MiB; powers of two also keep the
        # adaptive sizer (which doubles) protocol-legal.
        raise ValueError("part_size must be a power of two")
    if max_part_size < _PRECISE_ALIGNMENT:
        raise ValueError(f"max_part_size must be at least {_PRECISE_ALIGNMENT} bytes")
    if max_part_size > MAX_DOWNLOAD_CHUNK_SIZE:
        raise ValueError("max_part_size must not exceed 1 MiB")
    if max_part_size & (max_part_size - 1):
        raise ValueError("max_part_size must be a power of two")
    if max_part_size < part_size:
        raise ValueError("max_part_size must be greater than or equal to part_size")
    if concurrency <= 0:
        raise ValueError("concurrency must be positive")
    if max_retries < 0:
        raise ValueError("max_retries must not be negative")
    if flood_sleep_threshold is not None and flood_sleep_threshold < 0:
        raise ValueError("flood_sleep_threshold must not be negative")
    byte_limit = max_in_flight_bytes if max_in_flight_bytes is not None else max_buffer_size
    if byte_limit is not None and byte_limit < part_size:
        raise ValueError("max_in_flight_bytes must be greater than or equal to part_size")
    if read_ahead_bytes < 0:
        raise ValueError("read_ahead_bytes must not be negative")
    if range_cache_max_bytes <= 0:
        raise ValueError("range_cache_max_bytes must be positive")
    del adaptive_part_size


class _ConcurrentDestinationWriter:
    def __init__(
        self,
        destination: _DestinationHandle,
        *,
        queue_size: int,
        preallocate_size: int | None,
        sequential: bool = False,
    ) -> None:
        self._destination = destination
        self._queue: asyncio.Queue[_WriteRequest | None] = asyncio.Queue()
        self._queue_slots = asyncio.Semaphore(max(1, queue_size))
        self._stats = _DownloadWriterStats()
        self._threaded = destination.path is not None
        self._state_lock = asyncio.Lock()
        self._terminal = asyncio.Event()
        self._failure: BaseException | None = None
        self._closed = False
        self._acknowledgements: set[asyncio.Future[None]] = set()
        # Sequential transfers write strictly in order, so the writer appends at
        # the handle's current position instead of seeking (user-supplied
        # handles may be positioned intentionally or not be seekable at all).
        self._sequential = sequential
        if destination.path is not None and preallocate_size is not None:
            destination.handle.truncate(preallocate_size)
        self._worker = asyncio.create_task(self._run())

    async def submit(self, offset: int, payload: bytes, *, wait_for_completion: bool = True) -> asyncio.Future[None]:
        loop = asyncio.get_running_loop()
        acknowledgement = loop.create_future()
        acknowledgement.add_done_callback(self._consume_acknowledgement)
        async with self._state_lock:
            if self._failure is not None:
                raise self._failure
            if self._closed:
                raise RuntimeError("destination writer is closed")
            self._acknowledgements.add(acknowledgement)
        slot_task = asyncio.create_task(self._queue_slots.acquire())
        terminal_task = asyncio.create_task(self._terminal.wait())
        admitted = False
        queued = False
        try:
            done, _pending = await asyncio.wait({slot_task, terminal_task}, return_when=asyncio.FIRST_COMPLETED)
            admitted = slot_task in done and not slot_task.cancelled()
            if not admitted:
                slot_task.cancel()
            terminal_task.cancel()
            await asyncio.gather(slot_task, terminal_task, return_exceptions=True)
            async with self._state_lock:
                if self._failure is not None or self._closed:
                    if admitted:
                        self._queue_slots.release()
                    exc = self._failure or RuntimeError("destination writer is closed")
                    if not acknowledgement.done():
                        acknowledgement.set_exception(exc)
                else:
                    self._queue.put_nowait(
                        _WriteRequest(
                            offset=offset,
                            payload=payload,
                            queued_at=time.perf_counter(),
                            acknowledgement=acknowledgement,
                        )
                    )
                    queued = True
            if not queued or wait_for_completion:
                await acknowledgement
        except asyncio.CancelledError:
            if not admitted and slot_task.done() and not slot_task.cancelled():
                with suppress(BaseException):
                    admitted = bool(slot_task.result())
            slot_task.cancel()
            terminal_task.cancel()
            await asyncio.gather(slot_task, terminal_task, return_exceptions=True)
            if admitted and not queued:
                self._queue_slots.release()
            if not acknowledgement.done():
                acknowledgement.cancel()
            raise
        return acknowledgement

    async def close(self) -> _DownloadWriterStats:
        async with self._state_lock:
            if not self._closed:
                self._closed = True
                self._terminal.set()
                if self._failure is None:
                    self._queue.put_nowait(None)
        await asyncio.shield(self._worker)
        if self._failure is not None:
            raise self._failure
        return self._stats

    async def abort(self) -> None:
        async with self._state_lock:
            if not self._closed:
                self._closed = True
                self._terminal.set()
                self._fail_all_acknowledgements(asyncio.CancelledError())
                self._drain_queued_requests(asyncio.CancelledError())
                if not self._worker.done():
                    self._queue.put_nowait(None)
        await asyncio.shield(self._worker)

    async def _run(self) -> None:
        while True:
            item = await self._queue.get()
            if item is not None:
                self._queue_slots.release()
            try:
                if item is None:
                    await self._flush()
                    return
                self._stats.queued_seconds += max(time.perf_counter() - item.queued_at, 0.0)
                started = time.perf_counter()
                if self._threaded:
                    await asyncio.to_thread(self._write, item.offset, item.payload)
                else:
                    self._write(item.offset, item.payload)
                self._stats.write_seconds += max(time.perf_counter() - started, 0.0)
                self._stats.writes += 1
            except BaseException as exc:
                self._set_acknowledgement_exception(item, exc)
                await self._record_failure(exc)
                return
            else:
                if item is not None and not item.acknowledgement.done():
                    item.acknowledgement.set_result(None)

    def _write(self, offset: int, payload: bytes) -> None:
        if not self._sequential:
            self._destination.handle.seek(offset)
        written = self._destination.handle.write(payload)
        if written != len(payload):
            raise MediaDownloadError(
                f"destination write at offset {offset} expected {len(payload)} bytes but wrote {written}"
            )

    async def _flush(self) -> None:
        if self._threaded:
            await asyncio.to_thread(self._destination.handle.flush)
        else:
            self._destination.handle.flush()

    async def _record_failure(self, exc: BaseException) -> None:
        async with self._state_lock:
            if self._failure is None:
                self._failure = exc
            self._closed = True
            self._terminal.set()
            self._fail_all_acknowledgements(self._failure)
            self._drain_queued_requests(self._failure)

    def _fail_all_acknowledgements(self, exc: BaseException) -> None:
        for acknowledgement in tuple(self._acknowledgements):
            if not acknowledgement.done():
                acknowledgement.set_exception(exc)

    def _drain_queued_requests(self, exc: BaseException) -> None:
        while True:
            try:
                queued = self._queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            if queued is not None:
                self._queue_slots.release()
                self._set_acknowledgement_exception(queued, exc)

    @staticmethod
    def _set_acknowledgement_exception(item: _WriteRequest | None, exc: BaseException) -> None:
        if item is not None and not item.acknowledgement.done():
            item.acknowledgement.set_exception(exc)

    def _consume_acknowledgement(self, acknowledgement: asyncio.Future[None]) -> None:
        self._acknowledgements.discard(acknowledgement)
        if acknowledgement.cancelled():
            return
        with suppress(BaseException):
            acknowledgement.exception()


def _record_writer_stats(stats: _DownloadWriterStats) -> None:
    if stats.writes <= 0:
        return
    record_metric("media.download.writer_writes", stats.writes)
    record_metric("media.download.writer_queue_seconds", stats.queued_seconds, unit="s")
    record_metric("media.download.writer_write_seconds", stats.write_seconds, unit="s")


class _AdaptivePartSizer:
    def __init__(
        self,
        *,
        initial_size: int,
        max_size: int,
        total_bytes: int | None,
        enabled: bool,
        min_total_bytes: int = DEFAULT_ADAPTIVE_PART_SIZE_MIN_BYTES,
        min_samples: int = 4,
        worse_tolerance: float = 0.03,
    ) -> None:
        self.current_size = initial_size
        self._max_size = max(initial_size, max_size)
        self._enabled = (
            enabled and initial_size < self._max_size and (total_bytes is None or total_bytes >= min_total_bytes)
        )
        self._min_samples = max(1, min_samples)
        self._worse_tolerance = worse_tolerance
        self._sample_count = 0
        self._sample_bytes = 0
        self._sample_seconds = 0.0
        self._best_size = initial_size
        self._best_throughput: float | None = None
        self._settled = not self._enabled

    def on_success(self, *, requested_size: int, received_size: int, duration_s: float) -> None:
        if self._settled or requested_size != self.current_size or received_size < requested_size:
            return
        self._sample_count += 1
        self._sample_bytes += received_size
        self._sample_seconds += max(duration_s, 1e-9)
        if self._sample_count < self._min_samples:
            return
        throughput = self._sample_bytes / max(self._sample_seconds, 1e-9)
        previous = self.current_size
        if self._best_throughput is None:
            self._best_throughput = throughput
            self._best_size = self.current_size
            self._try_grow(previous=previous, reason="initial_sample")
            return
        if throughput >= self._best_throughput * (1.0 - self._worse_tolerance):
            self._best_throughput = throughput
            self._best_size = self.current_size
            self._try_grow(previous=previous, reason="throughput_improved")
            return
        self.current_size = self._best_size
        self._settled = True
        record_metric(
            "media.download.adaptive_part_size",
            self.current_size,
            attributes={"reason": "throughput_regressed", "previous_size": previous},
        )
        emit_event(
            _LOGGER,
            logging.DEBUG,
            "media.download.part_size",
            outcome="settled",
            previous_size=previous,
            current_size=self.current_size,
            reason="throughput_regressed",
        )

    def _try_grow(self, *, previous: int, reason: str) -> None:
        if self.current_size >= self._max_size:
            self._settled = True
            return
        self.current_size = min(self._max_size, self.current_size * 2)
        self._sample_count = 0
        self._sample_bytes = 0
        self._sample_seconds = 0.0
        record_metric(
            "media.download.adaptive_part_size",
            self.current_size,
            attributes={"reason": reason, "previous_size": previous},
        )
        emit_event(
            _LOGGER,
            logging.DEBUG,
            "media.download.part_size",
            outcome="increased",
            previous_size=previous,
            current_size=self.current_size,
            reason=reason,
        )


def _open_destination(destination: Destination, *, resume: bool) -> _DestinationHandle:
    if destination is None:
        buffer = io.BytesIO()
        return _DestinationHandle(
            handle=buffer,
            path=None,
            should_close=False,
            remove_on_cancel=False,
            discard_on_failure=True,
            existing_bytes=0,
            get_data=buffer.getvalue,
        )
    if isinstance(destination, str | os.PathLike):
        path = Path(cast(str | os.PathLike[str], destination))
        path.parent.mkdir(parents=True, exist_ok=True)
        path_existed = path.exists()
        existing = path.stat().st_size if resume and path_existed else 0
        handle = path.open("r+b" if resume and path_existed else "w+b")
        aligned = (existing // _PRECISE_ALIGNMENT) * _PRECISE_ALIGNMENT
        if aligned != existing:
            # Telegram cannot serve sub-1 KiB-aligned offsets; drop the partial
            # tail and re-download it instead of failing the resume.
            handle.truncate(aligned)
            record_metric("media.download.resume_realigned", 1)
            existing = aligned
        handle.seek(existing)
        return _DestinationHandle(
            handle=handle,
            path=path,
            should_close=True,
            remove_on_cancel=not path_existed,
            discard_on_failure=False,
            existing_bytes=existing,
            get_data=lambda: None,
        )
    restore_on_failure: Callable[[], None] | None = None
    if isinstance(destination, io.BytesIO):
        original_data = destination.getvalue()
        original_position = destination.tell()

        def restore_bytesio() -> None:
            destination.seek(0)
            destination.truncate(0)
            destination.write(original_data)
            destination.truncate(len(original_data))
            destination.seek(original_position)

        restore_on_failure = restore_bytesio
    return _DestinationHandle(
        handle=destination,
        path=None,
        should_close=False,
        remove_on_cancel=False,
        discard_on_failure=False,
        existing_bytes=0,
        get_data=lambda: None,
        restore_on_failure=restore_on_failure,
    )


async def _truncate_destination(destination: _DestinationHandle, size: int) -> None:
    def truncate_and_flush() -> None:
        destination.handle.truncate(size)
        destination.handle.flush()

    if destination.path is not None:
        await asyncio.to_thread(truncate_and_flush)
    else:
        truncate_and_flush()


async def _cleanup_failed_destination(destination: _DestinationHandle) -> None:
    if destination.path is not None:
        if destination.remove_on_cancel:
            if destination.should_close and not destination.handle.closed:
                destination.handle.close()
            destination.path.unlink(missing_ok=True)
            return

        def restore_prefix() -> None:
            destination.handle.truncate(destination.existing_bytes)
            destination.handle.flush()
            if destination.should_close:
                destination.handle.close()

        await asyncio.to_thread(restore_prefix)
        return
    if destination.restore_on_failure is not None:
        destination.restore_on_failure()
        return
    if destination.discard_on_failure:
        destination.handle.seek(0)
        destination.handle.truncate(0)
    if destination.should_close and not destination.handle.closed:
        destination.handle.close()


async def _cancel_tasks(pending: set[asyncio.Task[Any]]) -> None:
    if not pending:
        return
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)


async def _call_progress(progress: ProgressCallback | None, current: int, total: int | None) -> None:
    if progress is None:
        return
    result = progress(current, total)
    if inspect.isawaitable(result):
        await result


def _is_premium_flood(exc: Exception) -> bool:
    return isinstance(exc, FloodWait) and type(exc).__name__ == "FloodPremiumWait"


def _is_transient_download_error(exc: Exception, *, flood_sleep_threshold: int | None = 30) -> bool:
    if isinstance(exc, FloodWait):
        return flood_sleep_threshold is not None and exc.seconds <= flood_sleep_threshold
    if isinstance(
        exc, ClientDisconnected | RequestTimeout | RpcTimeout | InternalServerError | TimeoutError | ConnectionError
    ):
        return True
    if not isinstance(exc, RpcError):
        return False
    if exc.code == -503 or (exc.code is not None and exc.code >= 500):
        return True
    if exc.code is not None:
        return False
    message = exc.message.casefold()
    return any(token in message for token in ("sender disconnected", "transport", "connection", "timed out", "timeout"))


def _emit_part_retry(
    *, offset: int, limit: int, attempt: int, max_retries: int, error_type: str, flood_wait_seconds: int | None = None
) -> None:
    record_metric("media.download.part_retries", 1, attributes={"error_type": error_type})
    fields: dict[str, object] = {
        "outcome": "retry",
        "offset": offset,
        "limit": limit,
        "attempt": attempt,
        "max_retries": max_retries,
        "error_type": error_type,
    }
    if flood_wait_seconds is not None:
        fields["flood_wait_seconds"] = flood_wait_seconds
        attrs = {"error_type": error_type}
        record_metric("media.download.flood_waits", 1, attributes=attrs)
        record_metric("media.download.flood_wait_seconds", flood_wait_seconds, unit="s", attributes=attrs)
    emit_event(_LOGGER, logging.WARNING, "media.download.part_retry", **fields)


async def _sleep_before_retry(exc: Exception, attempt: int = 0) -> None:
    if isinstance(exc, FloodWait):
        # FLOOD_WAIT_0 retried instantly just re-triggers the flood. Positive
        # waits already carry server pacing, so only add tight jitter to
        # desynchronize lockstep wakers without over-sleeping at scale.
        base = _MIN_FLOOD_SLEEP_S if exc.seconds <= 0 else float(exc.seconds)
        delay = base + random.uniform(0.0, _FLOOD_SLEEP_JITTER_S)  # noqa: S311
    else:
        delay = backoff_delay(attempt)
    if delay > 0:
        record_metric("media.download.retry_sleep_seconds", delay, unit="s")
    await asyncio.sleep(delay)


class _AdaptiveDownloadThrottle:
    """Reduce the request window only on connection-health signals.

    ``FLOOD_WAIT`` is per-request pacing, not congestion: the affected task
    sleeps while holding its fixed slot, so pressure drops naturally while
    everything else keeps flowing. Floods only pause growth and feed the launch
    pacer. Disconnects/timeouts still shrink the window by one, and the
    start-of-transfer burst is handled by ``_DownloadLaunchPacer``, so there is
    no slow start either.
    """

    def __init__(self, max_limit: int, *, clock: Clock = time.monotonic) -> None:
        self.max_limit = max(1, max_limit)
        self.limit = self.max_limit
        self._clock = clock
        self._successes_since_change = 0
        self._cooldown_until = 0.0
        self._premium_fallback = False

    async def on_retry(self, exc: Exception, attempt: int) -> None:
        previous = self.limit
        if isinstance(exc, FloodWait):
            self._successes_since_change = 0
            self._cooldown_until = max(self._cooldown_until, self._clock() + max(float(exc.seconds), 2.0))
            if _is_premium_flood(exc):
                self._premium_fallback = True
                self.limit = 1
                record_metric(
                    "media.download.premium_flood_fallback",
                    1,
                    attributes={"attempt": attempt, "previous_limit": previous},
                )
            if self.limit != previous:
                record_metric(
                    "media.download.adaptive_throttle",
                    self.limit,
                    attributes={"reason": type(exc).__name__, "attempt": attempt, "previous_limit": previous},
                )
                emit_event(
                    _LOGGER,
                    logging.WARNING,
                    "media.download.throttle",
                    outcome="premium_fallback",
                    previous_limit=previous,
                    current_limit=self.limit,
                    reason=type(exc).__name__,
                    attempt=attempt,
                )
            return
        if isinstance(exc, ClientDisconnected | RequestTimeout | RpcTimeout | TimeoutError | ConnectionError):
            self.limit = max(1, self.limit - 1)
            self._successes_since_change = 0
            self._cooldown_until = max(self._cooldown_until, self._clock() + 2.0)
        if self.limit == previous:
            return
        record_metric(
            "media.download.adaptive_throttle",
            self.limit,
            attributes={"reason": type(exc).__name__, "attempt": attempt, "previous_limit": previous},
        )
        emit_event(
            _LOGGER,
            logging.WARNING,
            "media.download.throttle",
            outcome="reduced",
            previous_limit=previous,
            current_limit=self.limit,
            reason=type(exc).__name__,
            attempt=attempt,
        )

    def on_success(self) -> None:
        if self._premium_fallback:
            return
        if self.limit >= self.max_limit:
            return
        if self._clock() < self._cooldown_until:
            return
        self._successes_since_change += 1
        if self._successes_since_change < 8:
            return
        previous = self.limit
        self.limit = min(self.max_limit, self.limit + 1)
        self._successes_since_change = 0
        record_metric(
            "media.download.adaptive_throttle", self.limit, attributes={"reason": "success", "previous_limit": previous}
        )
        emit_event(
            _LOGGER,
            logging.DEBUG,
            "media.download.throttle",
            outcome="increased",
            previous_limit=previous,
            current_limit=self.limit,
            reason="success",
        )


__all__ = [
    "DEFAULT_DOWNLOAD_CONCURRENCY",
    "DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES",
    "DEFAULT_DOWNLOAD_PART_SIZE",
    "DEFAULT_RANGE_CACHE_BYTES",
    "MAX_DOWNLOAD_CHUNK_SIZE",
    "Destination",
    "DownloadRangeCache",
    "MediaDownloadError",
    "MediaDownloadResult",
    "MediaIntegrityError",
    "download_file",
    "download_location_from_media",
    "download_media",
    "iter_download",
    "iter_download_media",
    "media_from_raw",
]
