from __future__ import annotations

import asyncio
import inspect
import io
import logging
import os
import random
import time
from collections import OrderedDict, deque
from collections.abc import Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, cast

from miniproto.errors import (
    ClientDisconnected,
    FloodWait,
    InternalServerError,
    RequestTimeout,
    RpcError,
    RpcTimeout,
)
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
_PREMIUM_FLOOD_LAUNCH_RATE_MULTIPLIER = 0.15
_PREMIUM_FLOOD_MAX_LAUNCH_RATE_PER_S = 1.5
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
    existing_bytes: int
    get_data: Callable[[], bytes | None]


@dataclass(slots=True)
class _DownloadWriterStats:
    queued_seconds: float = 0.0
    write_seconds: float = 0.0
    writes: int = 0


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

    async def get_or_fetch(
        self, key: str, offset: int, limit: int, fetch: Callable[[], Awaitable[bytes]]
    ) -> bytes:
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

    def prefetch(
        self, key: str, offset: int, limit: int, fetch: Callable[[], Awaitable[bytes]]
    ) -> None:
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
        self,
        *,
        initial: float = _STAGGER_INITIAL_DELAY,
        decay: float = _STAGGER_DECAY,
        floor: float = _STAGGER_FLOOR,
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

    def __init__(
        self, *, concurrency: int, clock: Clock = time.monotonic, sleep: SleepFunc = asyncio.sleep
    ) -> None:
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
        if type(exc).__name__ == "FloodPremiumWait":
            target_rate = min(
                target_rate * _PREMIUM_FLOOD_LAUNCH_RATE_MULTIPLIER,
                _PREMIUM_FLOOD_MAX_LAUNCH_RATE_PER_S,
            )
            target_rate = max(1.0, target_rate)
        interval = 1.0 / target_rate
        if self._min_interval > 0:
            interval = max(interval, self._min_interval * 1.25)
        self._min_interval = min(1.0, interval)
        self._next_launch_at = max(self._next_launch_at, self._clock() + self._min_interval)
        record_metric(
            "media.download.launch_pace_rate",
            1.0 / self._min_interval,
            attributes={"reason": type(exc).__name__},
        )

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
        if (
            now - self._last_time < self._min_interval
            and self._parts_since_report < self._max_parts
        ):
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
    effective_max_in_flight_bytes = (
        max_in_flight_bytes if max_in_flight_bytes is not None else max_buffer_size
    )
    if read_ahead_bytes > 0 and _is_full_file_download(offset, limit, total_size):
        # Read-ahead is a streaming/repeated-range feature; racing it against a
        # full-file transfer's own scheduler was 3x slower on live benches.
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
    location_state = _DownloadLocationState(location)
    reference_deduper = _FileReferenceRefreshDeduper()
    if limit is None and concurrency > 1 and total_size is not None:
        limit = max(0, total_size - offset)
    started = time.perf_counter()
    try:
        if concurrency > 1 and limit is not None:
            result = await _download_file_concurrent(
                invoke,
                destination,
                offset=offset,
                limit=limit,
                part_size=part_size,
                resume=resume,
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
                location_state=location_state,
                reference_deduper=reference_deduper,
                file_reference_refresher=file_reference_refresher,
            )
        else:
            result = await _download_file_sequential(
                invoke,
                location_state,
                destination,
                offset=offset,
                limit=limit,
                part_size=part_size,
                resume=resume,
                progress=progress,
                precise=precise,
                cdn_supported=cdn_supported,
                total_size=total_size,
                request_timeout=request_timeout,
                max_retries=max_retries,
                flood_sleep_threshold=flood_sleep_threshold,
                adaptive_part_size=adaptive_part_size,
                max_part_size=max_part_size,
                range_cache=resolved_range_cache,
                range_cache_key=range_cache_key,
                read_ahead_bytes=read_ahead_bytes,
                reference_deduper=reference_deduper,
                file_reference_refresher=file_reference_refresher,
            )
    except BaseException:
        duration_ms = (time.perf_counter() - started) * 1000
        record_metric(
            "media.download.errors", 1, attributes={"concurrency": concurrency, "limit": limit}
        )
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
        "media.download.duration",
        duration_ms,
        unit="ms",
        attributes={"concurrency": concurrency, "limit": limit},
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


async def _download_file_sequential(
    invoke: RawInvoker,
    location_state: _DownloadLocationState,
    destination: Destination = None,
    *,
    offset: int,
    limit: int | None,
    part_size: int,
    resume: bool,
    progress: ProgressCallback | None,
    precise: bool,
    cdn_supported: bool,
    total_size: int | None,
    request_timeout: float | None,
    max_retries: int,
    flood_sleep_threshold: int | None,
    adaptive_part_size: bool,
    max_part_size: int,
    range_cache: DownloadRangeCache | None,
    range_cache_key: str | None,
    read_ahead_bytes: int,
    reference_deduper: _FileReferenceRefreshDeduper,
    file_reference_refresher: FileReferenceRefresher | None,
) -> MediaDownloadResult:
    destination_handle = _open_destination(destination, resume=resume)
    current_offset = offset + destination_handle.existing_bytes
    downloaded = destination_handle.existing_bytes
    remaining = None if limit is None else max(0, limit - destination_handle.existing_bytes)
    effective_precise = _resolve_precise_mode(current_offset, precise, part_size)
    reporter = _ProgressReporter(progress, limit)
    part_sizer = _AdaptivePartSizer(
        initial_size=part_size,
        max_size=max_part_size,
        total_bytes=limit if limit is not None else total_size,
        enabled=adaptive_part_size,
    )
    # Disk writes ride the same threaded writer pipeline as the concurrent path
    # (sequential mode: in-order appends, no seeks) so they never block the loop.
    writer = _ConcurrentDestinationWriter(
        destination_handle, queue_size=4, preallocate_size=None, sequential=True
    )
    try:
        while remaining is None or remaining > 0:
            target = (
                part_sizer.current_size
                if remaining is None
                else min(part_sizer.current_size, remaining)
            )
            wire_limit = _legal_request_limit(current_offset, target, precise=effective_precise)
            if wire_limit is None:
                # Tail smaller than the smallest legal request: over-request one
                # minimal chunk and truncate (the server clamps reads at EOF).
                wire_limit = _PRECISE_ALIGNMENT if effective_precise else _ALIGNMENT
            started = time.perf_counter()
            payload = await _download_part_cached(
                invoke,
                location_state=location_state,
                offset=current_offset,
                limit=wire_limit,
                precise=effective_precise,
                cdn_supported=cdn_supported,
                request_timeout=request_timeout,
                max_retries=max_retries,
                flood_sleep_threshold=flood_sleep_threshold,
                range_cache=range_cache,
                range_cache_key=range_cache_key,
                reference_deduper=reference_deduper,
                file_reference_refresher=file_reference_refresher,
            )
            short_read = len(payload) < wire_limit
            if remaining is not None and len(payload) > remaining:
                payload = payload[:remaining]
            if not payload:
                break
            part_sizer.on_success(
                requested_size=wire_limit,
                received_size=len(payload),
                duration_s=max(time.perf_counter() - started, 1e-9),
            )
            await writer.submit(downloaded, payload)
            downloaded += len(payload)
            current_offset += len(payload)
            if remaining is not None:
                remaining -= len(payload)
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
                start_offset=current_offset,
                part_size=part_sizer.current_size,
                read_ahead_bytes=read_ahead_bytes,
                hard_end=None,
                reference_deduper=reference_deduper,
                file_reference_refresher=file_reference_refresher,
            )
            if short_read:
                break
        stats = await writer.close()
        _record_writer_stats(stats)
        await reporter.finish(downloaded)
        if destination_handle.should_close:
            destination_handle.handle.close()
        data = destination_handle.get_data()
        return MediaDownloadResult(
            bytes_downloaded=downloaded,
            offset=offset,
            destination=destination_handle.path or destination_handle.handle,
            data=data,
            raw_location=location_state.current,
        )
    except asyncio.CancelledError:
        await writer.abort()
        if destination_handle.should_close:
            destination_handle.handle.close()
        if destination_handle.remove_on_cancel and destination_handle.path is not None:
            destination_handle.path.unlink(missing_ok=True)
        raise
    except BaseException:
        await writer.abort()
        if destination_handle.should_close:
            destination_handle.handle.close()
        raise


async def _download_file_concurrent(
    invoke: RawInvoker,
    destination: Destination = None,
    *,
    offset: int,
    limit: int,
    part_size: int,
    resume: bool,
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
    location_state: _DownloadLocationState,
    reference_deduper: _FileReferenceRefreshDeduper,
    file_reference_refresher: FileReferenceRefresher | None,
) -> MediaDownloadResult:
    destination_handle = _open_destination(destination, resume=resume)
    downloaded = destination_handle.existing_bytes
    remaining = max(0, limit - destination_handle.existing_bytes)
    callback_total = limit if limit is not None else total_size
    start_offset = offset + destination_handle.existing_bytes
    next_offset = start_offset
    end_offset = start_offset + remaining
    effective_precise = _resolve_precise_mode(start_offset, precise, part_size)
    pending: set[asyncio.Task[tuple[int, bytes, int, int]]] = set()
    byte_window = max_in_flight_bytes or max(
        DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES, part_size * concurrency
    )
    window = _TransferWindow(byte_window)
    launch_pacer = _DownloadLaunchPacer(concurrency=concurrency) if concurrency > 1 else None
    reporter = _ProgressReporter(progress, callback_total)
    stopped = False
    throttle = (
        _AdaptiveDownloadThrottle(concurrency) if adaptive_concurrency and concurrency > 1 else None
    )
    part_sizer = _AdaptivePartSizer(
        initial_size=part_size,
        max_size=max_part_size,
        total_bytes=limit,
        enabled=adaptive_part_size,
    )
    writer = _ConcurrentDestinationWriter(
        destination_handle, queue_size=max(1, concurrency), preallocate_size=limit
    )

    async def on_part_retry(exc: Exception, attempt: int) -> None:
        if launch_pacer is not None and isinstance(exc, FloodWait):
            launch_pacer.on_flood(exc)
        if throttle is not None:
            await throttle.on_retry(exc, attempt)

    async def fetch(
        request_offset: int, wire_limit: int, expect_limit: int
    ) -> tuple[int, bytes, int, int]:
        started = time.perf_counter()
        try:
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
            )
        finally:
            window.release(wire_limit)
        if throttle is not None:
            throttle.on_success()
        if launch_pacer is not None:
            launch_pacer.on_success()
        received = len(payload)
        if received > expect_limit:
            payload = payload[:expect_limit]
        part_sizer.on_success(
            requested_size=wire_limit,
            received_size=received,
            duration_s=max(time.perf_counter() - started, 1e-9),
        )
        return request_offset, payload, expect_limit, wire_limit

    async def fill_window() -> None:
        nonlocal next_offset
        while not stopped and next_offset < end_offset:
            allowed = concurrency if throttle is None else min(concurrency, throttle.limit)
            if window.active >= allowed:
                break
            target = min(part_sizer.current_size, window.max_bytes, end_offset - next_offset)
            wire_limit = _legal_request_limit(next_offset, target, precise=effective_precise)
            if wire_limit is None:
                # Tail smaller than the smallest legal request: over-request one
                # minimal chunk and truncate (the server clamps reads at EOF).
                wire_limit = _PRECISE_ALIGNMENT if effective_precise else _ALIGNMENT
            expect_limit = min(wire_limit, end_offset - next_offset)
            if not window.try_acquire(wire_limit):
                record_metric("media.download.byte_window_waits", 1)
                break
            if launch_pacer is not None:
                await launch_pacer.wait()
            task = asyncio.create_task(fetch(next_offset, wire_limit, expect_limit))
            pending.add(task)
            record_metric("media.download.in_flight_bytes", window.in_flight_bytes, unit="bytes")
            next_offset += expect_limit

    try:
        await fill_window()
        while pending:
            refill_wait = asyncio.ensure_future(window.wait_refill())
            try:
                done, _ = await asyncio.wait(
                    {*pending, refill_wait}, return_when=asyncio.FIRST_COMPLETED
                )
            finally:
                refill_wait.cancel()
                with suppress(asyncio.CancelledError):
                    await refill_wait
            for task in done:
                if task is refill_wait:
                    continue
                fetch_task = cast(asyncio.Task[tuple[int, bytes, int, int]], task)
                pending.discard(fetch_task)
                request_offset, payload, expect_limit, _wire_limit = await fetch_task
                if not payload:
                    stopped = True
                    continue
                output_offset = request_offset - offset
                await writer.submit(output_offset, payload)
                downloaded += len(payload)
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
                    start_offset=request_offset + len(payload),
                    part_size=part_sizer.current_size,
                    read_ahead_bytes=read_ahead_bytes,
                    # Read-ahead exists to prime the NEXT range read, so it may
                    # run past this call's end_offset -- only EOF caps it.
                    hard_end=total_size if total_size is not None else None,
                    reference_deduper=reference_deduper,
                    file_reference_refresher=file_reference_refresher,
                )
                if len(payload) < expect_limit:
                    stopped = True
            await fill_window()
        stats = await writer.close()
        _record_writer_stats(stats)
        await reporter.finish(downloaded)
        if destination_handle.should_close:
            destination_handle.handle.close()
        data = destination_handle.get_data()
        return MediaDownloadResult(
            bytes_downloaded=downloaded,
            offset=offset,
            destination=destination_handle.path or destination_handle.handle,
            data=data,
            raw_location=location_state.current,
        )
    except asyncio.CancelledError:
        await _cancel_tasks(pending)
        await writer.abort()
        if destination_handle.should_close:
            destination_handle.handle.close()
        if destination_handle.remove_on_cancel and destination_handle.path is not None:
            destination_handle.path.unlink(missing_ok=True)
        raise
    except BaseException:
        await _cancel_tasks(pending)
        await writer.abort()
        if destination_handle.should_close:
            destination_handle.handle.close()
        raise


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
            id=media.id,
            access_hash=media.access_hash,
            file_reference=media.file_reference,
            thumb_size="",
        )
    if isinstance(media, types.MessageMediaPhoto) and media.photo is not None:
        return download_location_from_media(media.photo)
    if isinstance(media, types.Photo):
        thumb_size = _largest_photo_thumb_size(media.sizes)
        return types.InputPhotoFileLocation(
            id=media.id,
            access_hash=media.access_hash,
            file_reference=media.file_reference,
            thumb_size=thumb_size,
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


async def _call_file_reference_refresher(
    refresher: FileReferenceRefresher, location: object
) -> object:
    refreshed = refresher(location)
    return await refreshed if inspect.isawaitable(refreshed) else refreshed


async def _payload_from_get_file_result(
    invoke: RawInvoker, result: object, *, offset: int, limit: int, request_timeout: float | None
) -> bytes:
    redirect = cdn_redirect_from_raw(result)
    if redirect is not None:
        return await get_cdn_file_part(
            invoke, redirect, offset=offset, limit=limit, request_timeout=request_timeout
        )
    if isinstance(result, types.UploadFile):
        return result.bytes
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
) -> bytes:
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
        )

    if range_cache is None or range_cache_key is None:
        return await fetch()
    return await range_cache.get_or_fetch(range_cache_key, offset, limit, fetch)


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
            )
        except Exception as exc:
            if (
                file_reference_refresher is None
                or refresh_attempt > 0
                or not _is_file_reference_error(exc)
            ):
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
            await location_state.refresh(
                reference_deduper=reference_deduper, refresher=file_reference_refresher
            )
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
) -> bytes:
    request = functions.UploadGetFile(
        precise=precise, cdn_supported=cdn_supported, location=location, offset=offset, limit=limit
    )
    failures = 0
    flood_retries = 0
    while True:
        try:
            record_metric("media.download.part_requests", 1)
            result = await invoke(
                request, request_timeout=request_timeout, retry=False, flood_sleep_threshold=0
            )
            return await _payload_from_get_file_result(
                invoke, result, offset=offset, limit=limit, request_timeout=request_timeout
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
        id=document.id,
        access_hash=document.access_hash,
        file_reference=document.file_reference,
        thumb_size="",
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
        id=photo.id,
        access_hash=photo.access_hash,
        file_reference=photo.file_reference,
        thumb_size=thumb_size,
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
    sized = [size for size in sizes if isinstance(getattr(size, "size", None), int)]
    if sized:
        selected = max(sized, key=lambda item: cast(int, item.size))
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
        request_limit = _legal_request_limit(
            current_offset, min(part_size, remaining), precise=precise
        )
        if request_limit is None:
            break
        if hard_end is not None and current_offset + request_limit > hard_end:
            reduced = _legal_request_limit(
                current_offset, hard_end - current_offset, precise=precise
            )
            request_limit = reduced if reduced is not None else request_limit
        if request_limit <= 0:
            break
        offset_for_task = current_offset
        limit_for_task = request_limit

        async def fetch(offset: int = offset_for_task, limit: int = limit_for_task) -> bytes:
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
        self._queue: asyncio.Queue[tuple[int, bytes, float] | None] = asyncio.Queue(
            maxsize=max(1, queue_size)
        )
        self._stats = _DownloadWriterStats()
        self._threaded = destination.path is not None
        # Sequential transfers write strictly in order, so the writer appends at
        # the handle's current position instead of seeking (user-supplied
        # handles may be positioned intentionally or not be seekable at all).
        self._sequential = sequential
        if destination.path is not None and preallocate_size is not None:
            destination.handle.truncate(preallocate_size)
        self._worker = asyncio.create_task(self._run())

    async def submit(self, offset: int, payload: bytes) -> None:
        await self._queue.put((offset, payload, time.perf_counter()))

    async def close(self) -> _DownloadWriterStats:
        await self._queue.join()
        await self._queue.put(None)
        await self._worker
        return self._stats

    async def abort(self) -> None:
        self._worker.cancel()
        await asyncio.gather(self._worker, return_exceptions=True)

    async def _run(self) -> None:
        while True:
            item = await self._queue.get()
            try:
                if item is None:
                    return
                offset, payload, queued_at = item
                self._stats.queued_seconds += max(time.perf_counter() - queued_at, 0.0)
                started = time.perf_counter()
                if self._threaded:
                    await asyncio.to_thread(self._write, offset, payload)
                else:
                    self._write(offset, payload)
                self._stats.write_seconds += max(time.perf_counter() - started, 0.0)
                self._stats.writes += 1
            finally:
                self._queue.task_done()

    def _write(self, offset: int, payload: bytes) -> None:
        if not self._sequential:
            self._destination.handle.seek(offset)
        self._destination.handle.write(payload)


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
            enabled
            and initial_size < self._max_size
            and (total_bytes is None or total_bytes >= min_total_bytes)
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
            existing_bytes=0,
            get_data=buffer.getvalue,
        )
    if isinstance(destination, str | os.PathLike):
        path = Path(cast(str | os.PathLike[str], destination))
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.stat().st_size if resume and path.exists() else 0
        handle = path.open("r+b" if resume and path.exists() else "w+b")
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
            remove_on_cancel=not resume,
            existing_bytes=existing,
            get_data=lambda: None,
        )
    return _DestinationHandle(
        handle=destination,
        path=None,
        should_close=False,
        remove_on_cancel=False,
        existing_bytes=0,
        get_data=lambda: None,
    )


async def _cancel_tasks(pending: set[asyncio.Task[Any]]) -> None:
    if not pending:
        return
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)


async def _call_progress(
    progress: ProgressCallback | None, current: int, total: int | None
) -> None:
    if progress is None:
        return
    result = progress(current, total)
    if inspect.isawaitable(result):
        await result


def _is_transient_download_error(exc: Exception, *, flood_sleep_threshold: int | None = 30) -> bool:
    if isinstance(exc, FloodWait):
        return flood_sleep_threshold is not None and exc.seconds <= flood_sleep_threshold
    if isinstance(
        exc,
        ClientDisconnected
        | RequestTimeout
        | RpcTimeout
        | InternalServerError
        | TimeoutError
        | ConnectionError,
    ):
        return True
    if not isinstance(exc, RpcError):
        return False
    if exc.code == -503 or (exc.code is not None and exc.code >= 500):
        return True
    if exc.code is not None:
        return False
    message = exc.message.casefold()
    return any(
        token in message
        for token in ("sender disconnected", "transport", "connection", "timed out", "timeout")
    )


def _emit_part_retry(
    *,
    offset: int,
    limit: int,
    attempt: int,
    max_retries: int,
    error_type: str,
    flood_wait_seconds: int | None = None,
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
        record_metric(
            "media.download.flood_wait_seconds", flood_wait_seconds, unit="s", attributes=attrs
        )
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

    async def on_retry(self, exc: Exception, attempt: int) -> None:
        previous = self.limit
        if isinstance(exc, FloodWait):
            self._successes_since_change = 0
            self._cooldown_until = max(
                self._cooldown_until, self._clock() + max(float(exc.seconds), 2.0)
            )
            return
        if isinstance(
            exc, ClientDisconnected | RequestTimeout | RpcTimeout | TimeoutError | ConnectionError
        ):
            self.limit = max(1, self.limit - 1)
            self._successes_since_change = 0
            self._cooldown_until = max(self._cooldown_until, self._clock() + 2.0)
        if self.limit == previous:
            return
        record_metric(
            "media.download.adaptive_throttle",
            self.limit,
            attributes={
                "reason": type(exc).__name__,
                "attempt": attempt,
                "previous_limit": previous,
            },
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
            "media.download.adaptive_throttle",
            self.limit,
            attributes={"reason": "success", "previous_limit": previous},
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
    "download_file",
    "download_location_from_media",
    "download_media",
    "media_from_raw",
]
