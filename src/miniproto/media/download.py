"""Concurrent Telegram media downloading with retry, integrity, cache and destination handling.

The public coroutines support bounded streaming and file materialization while
preserving ordered ranges, cancellable cleanup, optional CDN/plain-file
verification and safe reuse of cached byte ranges.
"""

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
    """Raised when a requested media range cannot be downloaded or materialized."""


class MediaIntegrityError(MediaDownloadError):
    """Raised when declared file hashes or download-range invariants are violated.

    Args:
        reason: Machine-readable explanation of the integrity failure.
        offset: First affected media byte offset.
        limit: Number of affected bytes.
    """

    def __init__(self, reason: str, *, offset: int, limit: int) -> None:
        """Record the corrupted interval and format the transfer error message.

        Args:
            reason: Integrity-failure classification included in the exception message.
            offset: First affected byte offset.
            limit: Number of affected bytes.
        """
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
    """Completed materialized-download metadata and optional in-memory payload.

    Attributes:
        bytes_downloaded: Bytes committed for this operation, including resumed bytes.
        offset: Requested starting byte offset.
        destination: Resolved path or caller-owned stream, if one was used.
        data: Downloaded bytes only when the destination was omitted.
        raw_location: Effective raw location, potentially refreshed after a stale reference.
    """

    bytes_downloaded: int
    offset: int
    destination: Path | BinaryIO | None = None
    data: bytes | None = None
    raw_location: object | None = None


@dataclass(slots=True)
class _DestinationHandle:
    """Internal ownership, rollback and data-extraction policy for an output handle.

    Attributes:
        handle: Open binary output receiving downloaded bytes.
        path: Owned filesystem path or ``None`` for caller-owned/in-memory streams.
        should_close: Whether transfer cleanup closes ``handle``.
        remove_on_cancel: Whether failure removes a newly created path.
        discard_on_failure: Whether an owned in-memory buffer is emptied on failure.
        existing_bytes: Aligned pre-transfer bytes retained by a resumed destination.
        get_data: Callback returning bytes only for an internally owned memory buffer.
        restore_on_failure: Optional rollback callback for a caller-provided ``BytesIO``.
    """

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
    """Internal aggregate queueing and write timing emitted as download metrics.

    Attributes:
        queued_seconds: Cumulative seconds writes spent awaiting the writer worker.
        write_seconds: Cumulative seconds spent performing writes and flushes.
        writes: Number of successfully committed write requests.
    """

    queued_seconds: float = 0.0
    write_seconds: float = 0.0
    writes: int = 0


@dataclass(slots=True)
class _WriteRequest:
    """Internal asynchronous destination-write request with its completion future.

    Attributes:
        offset: Byte seek offset for a non-sequential destination.
        payload: Downloaded bytes to write; the buffer is not zeroized after use.
        queued_at: Monotonic timestamp used to accumulate queue delay in seconds.
        acknowledgement: Future completed when the payload is committed or fails.
    """

    offset: int
    payload: bytes
    queued_at: float
    acknowledgement: asyncio.Future[None]


def _validate_concurrent_payload(request_offset: int, payload: bytes, *, expect_limit: int, target_end: int) -> bytes:
    """Trim allowed overreads and reject gaps in a concurrently requested target range.

    Args:
        request_offset: Start byte of the request that produced ``payload``.
        payload: Raw response bytes, retained by the caller after any allowed trim.
        expect_limit: Exact bytes needed from this request within the target range.
        target_end: Exclusive end byte of the caller's requested interval.
    """
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
    """Async LRU cache that deduplicates exact media-range requests and bounded prefetches.

    Args:
        max_bytes: Maximum payload bytes retained by the LRU; defaults to
            :data:`DEFAULT_RANGE_CACHE_BYTES`.

    Resource Semantics:
        Cache entries are shared by ``(key, offset, limit)``. ``clear()`` cancels
        in-progress owner and background prefetch tasks; callers awaiting them
        receive their normal task outcome or cancellation.
    """

    def __init__(self, *, max_bytes: int = DEFAULT_RANGE_CACHE_BYTES) -> None:
        """Initialize an empty bounded cache.

        Args:
            max_bytes: Positive aggregate byte capacity for cached payloads.

        Raises:
            ValueError: ``max_bytes`` is not positive.
        """
        if max_bytes <= 0:
            raise ValueError("range cache max_bytes must be positive")
        self.max_bytes = int(max_bytes)
        self._entries: OrderedDict[tuple[str, int, int], bytes] = OrderedDict()
        self._pending: dict[tuple[str, int, int], asyncio.Task[bytes]] = {}
        self._background: set[asyncio.Task[None]] = set()
        self._size = 0
        self._lock = asyncio.Lock()

    async def get(self, key: str, offset: int, limit: int) -> bytes | None:
        """Return and refresh an exact cached range or ``None`` on a cache miss.

        Args:
            key: Stable media identity partitioning cache entries.
            offset: Exact starting byte offset of the desired range.
            limit: Exact requested byte length.
        """
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
        """Store a non-empty fitting range and evict least-recently-used entries.

        Args:
            key: Stable media identity partitioning cache entries.
            offset: Exact starting byte offset represented by ``payload``.
            limit: Wire request length associated with the cache key.
            payload: Non-empty response bytes; oversized bytes are intentionally not cached or zeroized.
        """
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
        """Return a cached range or await one task shared by concurrent callers.

        Args:
            key: Stable media identity partitioning cache entries.
            offset: Exact starting byte offset of the desired range.
            limit: Exact wire request length used in the cache key.
            fetch: Async producer called once when no cache entry or pending task exists.

        Cancellation Semantics:
            Each waiter shields the shared owner task, so cancelling one caller
            does not cancel the producer or other waiters. Explicit cache
            clearing still cancels pending producers.
        """
        cached = await self.get(key, offset, limit)
        if cached is not None:
            return cached
        cache_key = (key, offset, limit)

        async def run_fetch() -> bytes:
            """Populate the cache and retire this key's shared owner task."""
            try:
                payload = await fetch()
                await self.put(key, offset, limit, payload)
                return payload
            finally:
                current = asyncio.current_task()
                async with self._lock:
                    if self._pending.get(cache_key) is current:
                        del self._pending[cache_key]

        async with self._lock:
            task = self._pending.get(cache_key)
            if task is None:
                task = asyncio.create_task(run_fetch())
                self._pending[cache_key] = task
                record_metric("media.download.range_cache_fetches", 1)
            else:
                record_metric("media.download.range_cache_deduped", 1)
        return await asyncio.shield(task)

    def prefetch(self, key: str, offset: int, limit: int, fetch: Callable[[], Awaitable[bytes]]) -> None:
        """Schedule a bounded best-effort cached fetch without awaiting its outcome.

        Args:
            key: Stable media identity partitioning cache entries.
            offset: Starting byte of the speculative range.
            limit: Requested speculative range length.
            fetch: Async producer used if this range is not cached or pending.
        """
        if len(self._background) >= _MAX_BACKGROUND_PREFETCHES:
            # Unbounded background fetches were 3x slower than no read-ahead at
            # all on live benches; skip instead of queueing ever more work.
            record_metric("media.download.range_cache_prefetch_skipped", 1)
            return

        async def run() -> None:
            """Populate the cache and convert prefetch failures into telemetry only."""
            try:
                await self.get_or_fetch(key, offset, limit, fetch)
            except Exception:
                record_metric("media.download.range_cache_prefetch_errors", 1)

        task = asyncio.create_task(run())
        self._background.add(task)
        task.add_done_callback(self._background.discard)

    async def clear(self) -> None:
        """Evict all values and cancel deduplicated or background cache tasks."""
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
    """Internal demand-loaded verifier for Telegram plain-file SHA-256 intervals."""

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
        """Configure metadata, refreshed-location and bounded verified-payload state.

        Args:
            invoke: Raw RPC invoker for file hashes and missing validation ranges.
            location_state: Mutable active location used to reject stale verification state.
            precise: Whether validation range requests use 1 KiB protocol alignment.
            cdn_supported: Whether nested recovery requests may follow CDN redirects.
            request_timeout: Optional per-RPC timeout in seconds.
            max_retries: Non-flood transient retry budget for nested range recovery.
            flood_sleep_threshold: Largest server flood wait retried during recovery.
            reference_deduper: Shared stale-reference refresh coordinator.
            file_reference_refresher: Optional callback renewing stale file locations.
            max_cached_bytes: Upper byte bound for retained verified payload intervals.
        """
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
        """Verify every byte of a plain response against stable Telegram hash intervals.

        Args:
            location: Raw location whose identity must stay stable while validating.
            offset: File byte offset of the first response byte.
            payload: Plain response bytes; they are retained in verification caches and not zeroized.
        """
        if not payload:
            return
        end = offset + len(payload)
        for refresh_attempt in range(2):
            identity = _plain_location_identity(location)
            await self._ensure_identity(identity)
            try:
                intervals = await self._ensure_hash_coverage(location, offset, end)
                break
            except Exception as exc:
                if self._file_reference_refresher is None or refresh_attempt > 0 or not _is_file_reference_error(exc):
                    raise
                record_metric("media.download.file_reference_refresh_attempts", 1)
                location = await self._location_state.refresh(
                    reference_deduper=self._reference_deduper, refresher=self._file_reference_refresher
                )
        else:
            raise AssertionError("plain hash reference-refresh loop did not terminate")
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
        """Discard cached metadata whenever the mutable file location changes identity.

        Args:
            identity: Normalized immutable fields of the current raw location.
        """
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
        """Fail verification if concurrent reference refresh changed the source location.

        Args:
            identity: Expected normalized location identity.
            offset: Affected byte offset reported on mismatch.
            limit: Affected byte length reported on mismatch.
        """
        if self._identity != identity or _plain_location_identity(self._location_state.current) != identity:
            raise MediaIntegrityError("location changed during verification", offset=offset, limit=limit)

    async def _ensure_hash_coverage(self, location: object, start: int, end: int) -> tuple[tuple[int, int, bytes], ...]:
        """Fetch enough non-overlapping hash metadata to cover an interval or raise.

        Args:
            location: Current raw location for ``upload.getFileHashes`` requests.
            start: Inclusive byte offset requiring coverage.
            end: Exclusive byte offset requiring coverage.
        """
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
        """Validate and retain one non-overlapping raw Telegram file hash.

        Args:
            item: Candidate raw ``FileHash`` metadata object.
        """
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
        """Return contiguous cached hash intervals spanning the target, if available.

        Args:
            start: Inclusive byte offset requiring coverage.
            end: Exclusive byte offset requiring coverage.
        """
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
        """Find the first byte in an interval not spanned by cached hash metadata.

        Args:
            start: Inclusive range start.
            end: Exclusive range end.
        """
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
        """Reuse or coalesce retrieval of one fully verified hash interval.

        Args:
            identity: Expected raw-location identity for the cached bytes.
            offset: Beginning of the hash interval.
            limit: Exact verified hash-interval byte length.
            expected_hash: SHA-256 digest required for the interval.
        """
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
        """Download every fragment of a hash interval before validating its digest.

        Args:
            identity: Location identity that must remain stable through recovery.
            offset: Beginning of the full hash interval.
            limit: Exact full hash-interval byte length.
            expected_hash: SHA-256 digest for the assembled interval.
        """
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
        """Return ``payload`` after matching its SHA-256 digest, otherwise raise.

        Args:
            payload: Complete byte interval to hash; it is returned unchanged and not zeroized.
            expected_hash: Expected SHA-256 digest bytes.
            offset: Interval start reported if hashes differ.
            limit: Interval length reported if hashes differ.
        """
        if hashlib.sha256(payload).digest() != expected_hash:
            record_metric("media.download.plain_hash_mismatches", 1)
            raise MediaIntegrityError("hash mismatch", offset=offset, limit=limit)
        record_metric("media.download.plain_hash_verified_bytes", limit, unit="bytes")
        return payload

    def _remember_validated(self, key: tuple[tuple[object, ...], int, int, bytes], payload: bytes) -> None:
        """Insert verified bytes into the bounded LRU payload cache.

        Args:
            key: Location identity, interval and expected-hash cache key.
            payload: Verified bytes retained until LRU eviction; buffers are not zeroized.
        """
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

    Args:
        offset: Requested byte offset at which protocol alignment is evaluated.
        max_bytes: Maximum caller-desired request length before protocol restrictions.
        precise: Select 1 KiB precise mode instead of ordinary 4 KiB constraints.
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

    Args:
        start_offset: Initial download offset to align against protocol requirements.
        precise: Caller-requested precise-mode setting.
        part_size: Initial requested part size used to infer required granularity.
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
    """Report whether a requested range covers the whole known file from its start.

    Args:
        offset: Requested range start.
        limit: Requested byte count or ``None`` for stream-to-EOF.
        total_size: Known full media size, if available.
    """
    if limit is None:
        return True
    return total_size is not None and offset + limit >= total_size


class _TransferWindow:
    """Slot/byte budget for in-flight download requests.

    A part task sleeping out a ``FLOOD_WAIT`` keeps holding its slot: floods
    are the server's pacing signal and backfilling freed slots with new
    requests sustains the request rate the server just objected to (observed
    live as an escalation from FLOOD_WAIT_2 to FLOOD_WAIT_15 and thousands of
    retries). Holding the slot lets pressure drop naturally while every other
    slot keeps flowing -- mtcute's fixed-slot model.
    """

    def __init__(self, max_bytes: int) -> None:
        """Initialize a slot budget that admits an oversized first request.

        Args:
            max_bytes: Nominal in-flight byte capacity; coerced to at least one byte.
        """
        self.max_bytes = max(1, max_bytes)
        self.in_flight_bytes = 0
        self.active = 0
        self._refill = asyncio.Event()

    def _has_room(self, nbytes: int) -> bool:
        """Check whether the next request can enter the byte window.

        Args:
            nbytes: Requested wire bytes to reserve.
        """
        return self.in_flight_bytes == 0 or self.in_flight_bytes + nbytes <= self.max_bytes

    def try_acquire(self, nbytes: int) -> bool:
        """Reserve bytes and a request slot when capacity is currently available.

        Args:
            nbytes: Requested wire bytes to reserve.
        """
        if not self._has_room(nbytes):
            return False
        self.in_flight_bytes += nbytes
        self.active += 1
        return True

    def release(self, nbytes: int) -> None:
        """Return a completed request's byte reservation and wake refill waiters.

        Args:
            nbytes: Wire-byte charge recorded when the request was admitted.
        """
        self.in_flight_bytes = max(0, self.in_flight_bytes - nbytes)
        self.active = max(0, self.active - 1)
        self._refill.set()

    async def wait_refill(self) -> None:
        """Wait until a release signals that the transfer window may have capacity."""
        await self._refill.wait()
        self._refill.clear()


class _DownloadDelayGate:
    """Stagger request launches at transfer start (mtcute's DownloadDelayGate)."""

    def __init__(
        self, *, initial: float = _STAGGER_INITIAL_DELAY, decay: float = _STAGGER_DECAY, floor: float = _STAGGER_FLOOR
    ) -> None:
        """Initialize the decaying launch-delay parameters.

        Args:
            initial: Initial launch delay in seconds.
            decay: Multiplicative decrease after each delayed launch.
            floor: Minimum retained launch delay in seconds.
        """
        self._initial = initial
        self._delay = initial
        self._decay = decay
        self._floor = floor

    async def wait(self) -> None:
        """Sleep once using the current delay, then decay it toward its floor."""
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
        """Initialize launch-rate state using injectable time and sleep functions.

        Args:
            concurrency: Fixed request-slot count used for conservative pacing estimates.
            clock: Monotonic time source returning seconds.
            sleep: Awaitable sleep implementation receiving seconds.
        """
        self._concurrency = max(1, concurrency)
        self._clock = clock
        self._sleep = sleep
        self._stagger = _DownloadDelayGate() if self._concurrency > 1 else None
        self._success_times: deque[float] = deque(maxlen=64)
        self._min_interval = 0.0
        self._next_launch_at = 0.0
        self._clean_successes = 0

    async def wait(self) -> None:
        """Honor flood-derived pacing before applying the start-of-transfer stagger."""
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
        """Gradually relax additional pacing after sufficient clean request completions."""
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
        """Tighten launch pacing after server-side rate limiting.

        Args:
            exc: Server flood-wait signal used only to classify pacing telemetry.
        """
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
        """Remove flood pacing and re-arm the initial stagger."""
        if self._stagger is not None:
            self._stagger.reset()
        self._min_interval = 0.0
        self._next_launch_at = 0.0
        self._clean_successes = 0

    @property
    def current_rate_per_s(self) -> float:
        """Return the currently enforced maximum launch rate or zero when unpaced."""
        if self._min_interval <= 0:
            return 0.0
        return 1.0 / self._min_interval

    def _target_rate(self) -> float:
        """Estimate a conservative launch rate from the recent success window."""
        now = self._clock()
        while self._success_times and now - self._success_times[0] > 10.0:
            self._success_times.popleft()
        if len(self._success_times) >= 2:
            span = max(now - self._success_times[0], 1e-9)
            return max(1.0, len(self._success_times) / span * 0.9)
        return max(1.0, float(self._concurrency))


class _ProgressReporter:
    """Coalesce progress callbacks using configurable interval and part thresholds.

    The default policy reports no more often than every 250 ms unless eight
    completed parts arrive first. Per-part callbacks add measurable latency on
    512 KiB parts; ``finish()`` emits the final value if needed.
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
        """Store callback coalescing policy and the transfer total for later reports.

        Args:
            progress: Optional callback receiving committed byte counts and total bytes.
            total: Known total byte count or ``None`` for unknown stream length.
            min_interval: Minimum seconds between ordinary reports; defaults to 250 ms.
            max_parts: Completed-parts threshold that bypasses the time interval; defaults to eight.
            clock: Monotonic seconds source used to coalesce callbacks.
        """
        self._progress = progress
        self._total = total
        self._min_interval = min_interval
        self._max_parts = max_parts
        self._clock = clock
        self._last_time = float("-inf")
        self._parts_since_report = 0
        self._last_reported: int | None = None

    async def report(self, current: int) -> None:
        """Deliver progress only when the time or completed-part threshold is met.

        Args:
            current: Byte count committed/yielded since this operation's initial offset.
        """
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
        """Deliver the final progress value if it has not already been reported.

        Args:
            current: Final byte count in the same units and origin as :meth:`report`.
        """
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
    launch_stagger: bool = True,
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
    """Stream an exact media range as ordered, bounded byte chunks.

    Args:
        invoke: Async raw-RPC invoker used for Telegram file requests.
        location: Telegram input file location to retrieve.
        offset: Starting byte offset; defaults to ``0``.
        limit: Exact byte count to yield or ``None`` to stream until EOF.
        part_size: Initial power-of-two request size; defaults to 512 KiB.
        progress: Optional synchronous or async ``(current, total)`` callback;
            ``current`` is bytes yielded from this invocation, while ``total`` is
            ``limit`` for a finite range or ``total_size`` when streaming to EOF.
        precise: Request Telegram's 1 KiB precise mode; it is enabled automatically when needed.
        cdn_supported: Allow Telegram to redirect requests to its CDN; defaults to ``True``.
        total_size: Known full size, used for exact range completion and concurrency.
        request_timeout: Optional timeout passed to each raw request.
        max_retries: Non-flood transient retry budget per part; defaults to ``2``.
        flood_sleep_threshold: Retry server flood waits at or below this number of seconds; ``None`` disables them.
            Eligible waits do not consume ``max_retries`` but are capped at 16 per part.
        max_buffer_size: Legacy byte window alias used when ``max_in_flight_bytes`` is absent.
        concurrency: Maximum concurrent part requests; defaults to :data:`DEFAULT_DOWNLOAD_CONCURRENCY`.
        adaptive_concurrency: Reduce the active window on connection-health failures.
        launch_stagger: Pace launch bursts and flood recovery; defaults to ``True``.
        max_in_flight_bytes: Maximum requested but unyielded bytes.
        adaptive_part_size: Probe larger legal parts for sufficiently large transfers.
        max_part_size: Largest legal adaptive part size, at most one MiB.
        range_cache: Exact-range cache instance, ``True`` for the shared cache or ``False``/``None`` to disable it.
        range_cache_key: Stable identity used to share cached ranges.
        range_cache_max_bytes: Capacity for an implicitly created shared cache.
        read_ahead_bytes: Best-effort cached prefetch budget for ranged reads only.
        verify_plain_hashes: Validate non-CDN chunks against Telegram's file hashes.
        file_reference_refresher: Optional sync/async callback to renew an expired file reference once per part.

    Yields:
        Contiguous ``bytes`` in increasing offset order. A bounded request window
        limits in-flight resources; closing the generator cancels outstanding parts.
        Progress reports ``current`` bytes only after a chunk has been yielded,
        unlike :func:`download_file`, which reports after destination-write
        acknowledgement and starts ``current`` at any retained resume prefix.

    Raises:
        ValueError: A range, alignment, part size, retry or cache option is invalid.
        TypeError: ``verify_plain_hashes`` or ``launch_stagger`` is not boolean.
        MediaDownloadError: Telegram ends a finite requested interval before full coverage.
        MediaIntegrityError: Optional plain-file verification finds missing or mismatched hashes.
        asyncio.CancelledError: Iteration or an awaiting caller is cancelled.
    """

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
    if not isinstance(launch_stagger, bool):
        raise TypeError("launch_stagger must be a bool")
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
        launch_stagger=launch_stagger,
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
    launch_stagger: bool,
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
    """Coordinate ordered concurrent part requests for the public streaming API.

    Args:
        invoke: Raw RPC invoker for file-part requests.
        location_state: Mutable raw-location holder supporting stale-reference refresh.
        offset: Initial requested byte offset.
        limit: Exact remaining range length or ``None`` for stream-to-EOF.
        part_size: Initial legal request size in bytes.
        progress: Optional callback receiving yielded byte counts and total bytes.
        precise: Whether requests use 1 KiB precise protocol alignment.
        cdn_supported: Whether file requests can be redirected to the CDN.
        total_size: Known complete file size used for finite planning and prefetch bounds.
        request_timeout: Optional raw-RPC timeout in seconds.
        max_retries: Non-flood transient retry allowance per part.
        flood_sleep_threshold: Largest retryable server flood wait in seconds.
        concurrency: Maximum simultaneous requested parts for finite ranges.
        adaptive_concurrency: Whether connection health signals lower active slots.
        launch_stagger: Whether start/flood launch pacing is enabled.
        max_in_flight_bytes: Maximum wire-byte reservation before new work waits.
        adaptive_part_size: Whether large transfers may probe larger legal part sizes.
        max_part_size: Maximum adaptive request size in bytes.
        range_cache: Optional cache used to deduplicate exact requested ranges.
        range_cache_key: Stable cache identity, required to use ``range_cache``.
        read_ahead_bytes: Best-effort speculative cache-fill budget in bytes.
        verify_plain_hashes: Whether non-CDN responses require Telegram file-hash validation.
        reference_deduper: Shared coordinator for concurrent stale-reference refreshes.
        file_reference_refresher: Optional callback supplying a renewed raw location.
    """
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
    launch_pacer = (
        _DownloadLaunchPacer(concurrency=effective_concurrency)
        if launch_stagger and effective_concurrency > 1
        else None
    )
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
        """Feed retry outcomes into adaptive concurrency and launch pacing controls.

        Args:
            exc: Retryable transport or flood exception just observed.
            attempt: One-based applicable retry/flood attempt number for this part.
        """
        if throttle is not None:
            await throttle.on_retry(exc, attempt)
            if launch_pacer is not None and throttle.limit <= 1:
                launch_pacer.reset()
        if launch_pacer is not None and isinstance(exc, FloodWait) and (throttle is None or throttle.limit > 1):
            launch_pacer.on_flood(exc)

    async def fetch(request_offset: int, wire_limit: int, expect_limit: int) -> tuple[int, bytes, int, int, bool]:
        """Fetch one scheduled range, normalize its length and record adaptation samples.

        Args:
            request_offset: Starting byte offset of the scheduled wire request.
            wire_limit: Protocol-legal request length and byte-window charge.
            expect_limit: Exact bytes required for the finite target after tail trimming.
        """
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
        """Launch legal parts until a slot, byte or target boundary prevents more work."""
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
    launch_stagger: bool = True,
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
    """Download media into memory, a path or a caller-owned binary stream.

    Args:
        invoke: Async raw-RPC invoker used for Telegram file requests.
        location: Telegram input file location to retrieve.
        destination: ``None`` for in-memory bytes, a path to create/overwrite or an open binary stream.
        offset: Starting byte offset; defaults to ``0``.
        limit: Exact requested byte count or ``None`` to continue until EOF.
        part_size: Initial power-of-two request size; defaults to 512 KiB.
        resume: Append to an existing path from its 1 KiB-aligned size; defaults to ``False``.
        progress: Optional synchronous or async ``(current, total)`` callback;
            ``current`` is committed operation bytes and begins at any retained
            resume prefix, while ``total`` is ``limit`` or otherwise ``total_size``.
        precise: Request Telegram's 1 KiB precise mode; enabled automatically when required.
        cdn_supported: Permit CDN redirects and their mandatory block verification.
        total_size: Known full file size used to preserve finite concurrent coverage.
        request_timeout: Optional timeout passed to each raw request.
        max_retries: Non-flood transient retry budget per part; defaults to ``2``.
        flood_sleep_threshold: Retry eligible flood waits at or below this number of seconds; ``None`` disables them.
            Eligible waits retain their slot and are separately capped at 16 per part.
        max_buffer_size: Legacy maximum in-flight byte window alias.
        concurrency: Maximum concurrent requests and queued writes.
        adaptive_concurrency: Adapt the active request window to connection failures.
        launch_stagger: Pace start and flood-recovery request launches.
        max_in_flight_bytes: Maximum requested bytes not yet released by the stream.
        adaptive_part_size: Probe larger legal part sizes for large transfers.
        max_part_size: Upper bound for adaptive parts, no greater than one MiB.
        range_cache: Exact-range cache instance, ``True`` for shared cache or disabled value.
        range_cache_key: Stable media identity for range-cache sharing.
        range_cache_max_bytes: Capacity used by an implicit shared cache.
        read_ahead_bytes: Best-effort range prefetch budget; disabled for a full-file transfer.
        verify_plain_hashes: Verify non-CDN data with Telegram plain-file SHA-256 metadata.
        file_reference_refresher: Optional sync/async callback for one stale-reference refresh per part.

    Returns:
        Metadata including the resolved output. ``data`` is populated only for
        an in-memory destination; caller-provided streams remain open.

    Destination Ownership and Rollback:
        ``None`` creates an internal ``BytesIO`` returned as ``data`` and clears it
        on failure. A path creates parent directories; a new path is removed on
        cancellation/failure, while an existing non-resume path is overwritten
        rather than restored. A resumed path preserves its existing prefix after
        truncating any non-1-KiB tail and failure truncates it back to that
        aligned prefix. A caller ``BytesIO`` is restored to its original contents
        and position; arbitrary caller streams remain open and are not generally
        restorable. Payload/key buffers are not explicitly zeroized.

    Raises:
        ValueError: An offset, limit, part/cache/window option is invalid.
        TypeError: A boolean option has the wrong type.
        MediaDownloadError: A response, finite range or destination write is invalid.
        MediaIntegrityError: CDN or requested plain-file integrity verification fails.
        OSError: A path destination cannot be created, written or restored.
        asyncio.CancelledError: The transfer is cancelled; created paths are removed and owned buffers restored.
    """
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
    if not isinstance(launch_stagger, bool):
        raise TypeError("launch_stagger must be a bool")
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
        """Advance progress only after the serialized writer acknowledges durable bytes.

        Args:
            drain_all: Await every queued acknowledgement instead of only completed heads.
        """
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
            launch_stagger=launch_stagger,
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
    """Resolve a supported media object and stream it through :func:`iter_download`.

    Args:
        invoke: Async raw-RPC invoker used for file requests.
        media: A :class:`Media`, file ID, raw document/photo/message or input file location.
        kwargs: Forwarded ``**kwargs`` download options; a missing cache key and total size are inferred when possible.

    Yields:
        Ordered byte chunks with the cancellation, caching, CDN and integrity semantics of :func:`iter_download`.

    Raises:
        MediaDownloadError: ``media`` cannot be resolved to an input file location.
        asyncio.CancelledError: The active stream is cancelled and its pending requests are cleaned up.
    """
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
    """Resolve media and materialize it through :func:`download_file`.

    Args:
        invoke: Async raw-RPC invoker used for file requests.
        media: A :class:`Media`, file ID, raw document/photo/message or input file location.
        destination: In-memory, path or binary-stream destination forwarded to :func:`download_file`.
        kwargs: Remaining forwarded ``**kwargs`` download options; cache identity and total size are inferred when possible.

    Returns:
        The same result and destination-ownership semantics as :func:`download_file`.

    Raises:
        MediaDownloadError: The supplied media cannot produce a download location.
        MediaIntegrityError: CDN or enabled plain-file verification fails.
        asyncio.CancelledError: The transfer is cancelled and destination cleanup runs.
    """
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
    """Resolve a media model, raw Telegram object, file ID or input location for download.

    Args:
        media: Supported high-level, raw, encoded or already-resolved media input.

    Returns:
        A raw Telegram ``InputFileLocation`` suitable for ``upload.getFile``.

    Raises:
        MediaDownloadError: The object has no download-capable document or photo location.
    """
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
    """Normalize supported raw Telegram media shapes into a :class:`Media` record.

    Args:
        raw: Media, message/update, document, photo or input file location.

    Returns:
        A normalized media record or ``None`` when ``raw`` is unsupported or absent.
    """
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
    """Concurrency-safe mutable location holder for expired file-reference recovery."""

    def __init__(self, location: object) -> None:
        """Initialize the state with the location used by the first request.

        Args:
            location: Initial raw location whose file reference can later be replaced.
        """
        self._location = location
        self._lock = asyncio.Lock()

    @property
    def current(self) -> object:
        """Return the currently active raw file location without waiting."""
        return self._location

    async def refresh(
        self, *, reference_deduper: _FileReferenceRefreshDeduper, refresher: FileReferenceRefresher
    ) -> object:
        """Refresh stale reference metadata once and retain it unless another refresh won.

        Args:
            reference_deduper: Coordinator sharing refresh work for the old reference.
            refresher: Sync or async callback returning an updated raw location.
        """
        old_location = self._location
        new_location = await reference_deduper.refresh(old_location, refresher)
        async with self._lock:
            if _file_reference_bytes(self._location) == _file_reference_bytes(old_location):
                self._location = new_location
            return self._location


class _FileReferenceRefreshDeduper:
    """Share concurrent stale-reference refreshes keyed by their old reference bytes."""

    def __init__(self) -> None:
        """Initialize the in-flight refresher registry."""
        self._pending: dict[bytes, asyncio.Task[object]] = {}
        self._lock = asyncio.Lock()

    async def refresh(self, location: object, refresher: FileReferenceRefresher) -> object:
        """Return a refreshed location while coalescing requests for the same stale reference.

        Args:
            location: Raw location with a possibly expired file reference.
            refresher: Sync or async callback producing its renewed location.
        """
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
    """Call a sync or async reference refresher and normalize it to an awaited result.

    Args:
        refresher: Callback returning a raw location directly or as an awaitable.
        location: Stale raw location supplied to the callback.
    """
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
    """Extract plain bytes or follow a CDN redirect from one ``upload.getFile`` result.

    Args:
        invoke: Raw RPC invoker used for CDN reupload/hash operations.
        result: Raw ``upload.getFile`` response to interpret.
        location: Plain-file location used by optional hash verification.
        offset: Response starting byte offset.
        limit: Requested byte length for CDN retrieval.
        request_timeout: Optional raw-RPC timeout in seconds.
        plain_verifier: Optional non-CDN SHA-256 verifier.
    """
    redirect = cdn_redirect_from_raw(result)
    if redirect is not None:
        cdn_invoke = getattr(invoke, "invoke_cdn", None)
        if not callable(cdn_invoke):
            raise MediaDownloadError("CDN redirect requires an invoker with dedicated CDN-DC routing")
        return await get_cdn_file_part(
            invoke, cdn_invoke, redirect, offset=offset, limit=limit, request_timeout=request_timeout
        )
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
    """Fetch a part directly or through the exact-range cache, then optionally verify it.

    Args:
        invoke: Raw RPC invoker for the requested part.
        location_state: Current mutable raw location and refresh state.
        offset: Requested part starting byte offset.
        limit: Protocol-legal requested part length.
        precise: Whether to use precise 1 KiB file-request alignment.
        cdn_supported: Whether the request permits a CDN redirect.
        request_timeout: Optional per-request timeout in seconds.
        max_retries: Non-flood transient retry allowance.
        flood_sleep_threshold: Largest server flood wait retried in seconds.
        range_cache: Optional exact-range cache.
        range_cache_key: Stable cache identity required to use the cache.
        reference_deduper: Shared stale-reference refresh coordinator.
        file_reference_refresher: Optional callback supplying a renewed location.
        retry_observer: Optional sync/async listener for retry attempts.
        plain_verifier: Optional plain-file hash verifier run after cache retrieval.
    """
    use_range_cache = range_cache is not None and range_cache_key is not None

    async def fetch() -> bytes:
        """Fetch the uncached range while preserving reference-refresh retry behavior."""
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
    """Retry a part once with a refreshed file reference when Telegram reports it stale.

    Args:
        invoke: Raw RPC invoker for file-part requests.
        location_state: Mutable location holder updated by successful refresh.
        offset: Requested part start byte.
        limit: Requested part length.
        precise: Whether to request precise 1 KiB alignment.
        cdn_supported: Whether CDN redirects are accepted.
        request_timeout: Optional request timeout in seconds.
        max_retries: Non-flood transient retry allowance.
        flood_sleep_threshold: Largest retryable flood wait in seconds.
        retry_observer: Optional observer notified before transient retries.
        reference_deduper: Shared stale-reference refresh coordinator.
        file_reference_refresher: Optional callback producing a renewed location.
        plain_verifier: Optional plain-file hash verifier.
    """
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
    """Request one file part with transient retry and server flood-pacing semantics.

    Args:
        invoke: Raw RPC invoker for the file request.
        location: Raw input location for the requested range.
        offset: Requested range start byte.
        limit: Protocol-legal request length in bytes.
        precise: Whether to use Telegram's 1 KiB precise mode.
        cdn_supported: Whether Telegram may return a CDN redirect.
        request_timeout: Optional raw-RPC timeout in seconds.
        max_retries: Retry budget for non-flood transient failures.
        flood_sleep_threshold: Largest eligible flood wait in seconds; eligible waits
            retain their scheduler slot and use a separate 16-retry cap.
        retry_observer: Optional sync/async callback observing retry attempts.
        plain_verifier: Optional non-CDN hash verifier for returned bytes.
    """
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
    """Build normalized media metadata and a full-size location from a raw document.

    Args:
        document: Raw Telegram document supplying identifiers and attributes.
        raw: Original enclosing raw object retained on the normalized record.
    """
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
    """Build normalized media metadata and the largest-photo location from a raw photo.

    Args:
        photo: Raw Telegram photo supplying identifiers and size variants.
        raw: Original enclosing raw object retained on the normalized record.
    """
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
    """Return the declared document filename attribute, if Telegram supplied one.

    Args:
        attributes: Raw document attributes to inspect.
    """
    for attribute in attributes:
        if isinstance(attribute, types.DocumentAttributeFilename):
            return attribute.file_name
    return None


def _largest_photo_size(sizes: tuple[object, ...]) -> int | None:
    """Return the greatest numeric photo-size value from heterogeneous size entries.

    Args:
        sizes: Raw photo-size variants exposing optional numeric ``size`` attributes.
    """
    candidates: list[int] = []
    for size in sizes:
        value = getattr(size, "size", None)
        if isinstance(value, int):
            candidates.append(value)
    return max(candidates) if candidates else None


def _largest_photo_thumb_size(sizes: tuple[object, ...]) -> str:
    """Select the type of the largest known photo size, with a typed fallback.

    Args:
        sizes: Raw photo-size variants exposing optional type and size attributes.
    """
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
    """Identify raw Telegram input file-location objects without importing every variant.

    Args:
        value: Candidate raw object to inspect for its generated result type.
    """
    return getattr(type(value), "RESULT_TYPE", None) == "InputFileLocation"


def _range_cache_key_from_media(media: object) -> str | None:
    """Derive a stable cache identity from encoded, normalized or raw media.

    Args:
        media: Encoded file ID, normalized media or supported raw Telegram media.
    """
    if is_file_id(media):
        return str(media)
    if isinstance(media, Media):
        return media.file_id
    resolved = media_from_raw(media)
    return resolved.file_id if resolved is not None else None


def _resolve_range_cache(
    range_cache: DownloadRangeCache | bool | None, *, max_bytes: int, read_ahead_bytes: int
) -> DownloadRangeCache | None:
    """Choose an explicit, implicit shared or disabled range cache for a transfer.

    Args:
        range_cache: Explicit cache, ``True`` for shared cache or disabled value.
        max_bytes: Capacity required if a shared cache is selected.
        read_ahead_bytes: Positive value that requires an implicit shared cache.
    """
    if isinstance(range_cache, DownloadRangeCache):
        return range_cache
    if range_cache is False:
        return None
    if range_cache is True or read_ahead_bytes > 0:
        return _default_range_cache(max_bytes)
    return None


def _default_range_cache(max_bytes: int) -> DownloadRangeCache:
    """Return the process-local shared cache, replacing it when its capacity changes.

    Args:
        max_bytes: Required capacity for the shared cache.
    """
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
    """Schedule aligned low-priority cached ranges ahead of the yielded cursor.

    Args:
        invoke: Raw RPC invoker wrapped with background request priority.
        location_state: Mutable raw location used for prefetches and refreshes.
        precise: Whether planned prefetches use 1 KiB precise alignment.
        cdn_supported: Whether prefetched requests may use CDN redirects.
        request_timeout: Optional per-request timeout in seconds.
        max_retries: Non-flood transient retry allowance for prefetches.
        flood_sleep_threshold: Largest retryable server wait for prefetches.
        range_cache: Cache that owns best-effort background task lifecycle.
        range_cache_key: Stable media identity to cache planned ranges under.
        start_offset: First byte after the latest yielded range.
        part_size: Target legal request size used to partition prefetches.
        read_ahead_bytes: Maximum speculative byte distance to schedule.
        hard_end: Known exclusive file end that prefetching must not exceed.
        reference_deduper: Shared stale-reference refresh coordinator.
        file_reference_refresher: Optional callback producing a renewed location.
    """
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
            """Retrieve one prefetched range using background transport priority.

            Args:
                offset: Captured starting byte offset for this background range.
                limit: Captured protocol-legal background request length.
            """

            async def background_invoke(request: object, **kwargs: Any) -> object:
                """Mark a raw request as background work before delegating it to the caller.

                Args:
                    request: Raw Telegram request to execute with background priority.
                    kwargs: Forwarded ``**kwargs`` transport options augmented with priority.
                """
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
    """Normalize a location's file reference to immutable bytes for identity comparisons.

    Args:
        location: Raw location whose ``file_reference`` field may have several byte-like types.
    """
    reference = getattr(location, "file_reference", b"")
    if isinstance(reference, bytes):
        return reference
    if isinstance(reference, bytearray | memoryview):
        return bytes(reference)
    if isinstance(reference, str):
        return reference.encode("utf-8")
    return b""


def _plain_location_identity(location: object) -> tuple[object, ...]:
    """Build the location fields that must remain stable during plain-hash verification.

    Args:
        location: Raw location whose identifier, access, thumbnail and reference fields are captured.
    """
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
    """Recognize raw RPC failures that request a refreshed file reference.

    Args:
        exc: Exception raised by a raw file request.
    """
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
    """Reject invalid transfer sizing, retry, cache and memory-window configuration.

    Args:
        offset: Requested non-negative starting byte offset.
        limit: Optional non-negative requested byte count.
        part_size: Initial power-of-two part size between 1 KiB and one MiB.
        max_retries: Non-negative non-flood transient retry budget.
        flood_sleep_threshold: Optional non-negative maximum retryable server wait.
        max_buffer_size: Legacy optional byte-window limit.
        concurrency: Positive requested concurrent-part count.
        max_in_flight_bytes: Preferred optional byte-window limit.
        adaptive_part_size: Accepted feature setting; behavior is consumed by the caller.
        max_part_size: Power-of-two adaptive ceiling between ``part_size`` and one MiB.
        range_cache_max_bytes: Positive capacity for implicitly created range caches.
        read_ahead_bytes: Non-negative speculative cache-fill length.
        precise: Accepted alignment setting; 1 KiB mode is inferred separately.
    """
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
    """Serialize asynchronous writes and surface destination failure to every submitter."""

    def __init__(
        self,
        destination: _DestinationHandle,
        *,
        queue_size: int,
        preallocate_size: int | None,
        sequential: bool = False,
    ) -> None:
        """Start the writer worker and optionally preallocate a path-backed output.

        Args:
            destination: Handle ownership and rollback policy for the output.
            queue_size: Maximum queued writes admitted before submitters wait.
            preallocate_size: Optional byte length applied to a path-backed file before writes.
            sequential: Append in submitted order instead of seeking each write offset.
        """
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
        """Queue a write and return its acknowledgement after optional completion waiting.

        Cancellation before admission releases any acquired queue slot; failures
        are propagated to this and every pending acknowledgement.

        Args:
            offset: Destination byte offset when non-sequential seeking is enabled.
            payload: Bytes to write; ownership remains with the caller and no zeroization occurs.
            wait_for_completion: Await the acknowledgement before returning when true.
        """
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
        """Flush queued writes, await the worker and return timing statistics."""
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
        """Cancel queued acknowledgements, stop admission and drain the worker safely."""
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
        """Consume write requests until a flush sentinel or terminal destination failure."""
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
        """Seek when required and require the destination to accept the full payload.

        Args:
            offset: Byte seek target for non-sequential output.
            payload: Bytes that the underlying output must write completely.
        """
        if not self._sequential:
            self._destination.handle.seek(offset)
        written = self._destination.handle.write(payload)
        if written != len(payload):
            raise MediaDownloadError(
                f"destination write at offset {offset} expected {len(payload)} bytes but wrote {written}"
            )

    async def _flush(self) -> None:
        """Flush the output, moving path-backed blocking I/O off the event loop."""
        if self._threaded:
            await asyncio.to_thread(self._destination.handle.flush)
        else:
            self._destination.handle.flush()

    async def _record_failure(self, exc: BaseException) -> None:
        """Publish the first writer failure and fail all queued acknowledgements.

        Args:
            exc: First terminal write/flush exception to propagate to submitters.
        """
        async with self._state_lock:
            if self._failure is None:
                self._failure = exc
            self._closed = True
            self._terminal.set()
            self._fail_all_acknowledgements(self._failure)
            self._drain_queued_requests(self._failure)

    def _fail_all_acknowledgements(self, exc: BaseException) -> None:
        """Set an exception on every unresolved submitted-write future.

        Args:
            exc: Terminal exception assigned to each unresolved future.
        """
        for acknowledgement in tuple(self._acknowledgements):
            if not acknowledgement.done():
                acknowledgement.set_exception(exc)

    def _drain_queued_requests(self, exc: BaseException) -> None:
        """Remove queued writes, release slots and fail their acknowledgements.

        Args:
            exc: Terminal exception assigned to drained write acknowledgements.
        """
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
        """Fail one queued request's acknowledgement when it has not settled yet.

        Args:
            item: Optional queued write carrying the acknowledgement to fail.
            exc: Exception assigned if that acknowledgement remains unresolved.
        """
        if item is not None and not item.acknowledgement.done():
            item.acknowledgement.set_exception(exc)

    def _consume_acknowledgement(self, acknowledgement: asyncio.Future[None]) -> None:
        """Release acknowledgement bookkeeping and consume unobserved future errors.

        Args:
            acknowledgement: Settled/cancelled writer-completion future to unregister.
        """
        self._acknowledgements.discard(acknowledgement)
        if acknowledgement.cancelled():
            return
        with suppress(BaseException):
            acknowledgement.exception()


def _record_writer_stats(stats: _DownloadWriterStats) -> None:
    """Emit writer queue and blocking-I/O metrics when at least one write completed.

    Args:
        stats: Aggregate durations in seconds and successfully committed write count.
    """
    if stats.writes <= 0:
        return
    record_metric("media.download.writer_writes", stats.writes)
    record_metric("media.download.writer_queue_seconds", stats.queued_seconds, unit="s")
    record_metric("media.download.writer_write_seconds", stats.write_seconds, unit="s")


class _AdaptivePartSizer:
    """Probe progressively larger legal chunks and settle at the best observed size."""

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
        """Initialize adaptation thresholds and disable probing for unsuitable transfers.

        Args:
            initial_size: Starting legal request size in bytes.
            max_size: Maximum legal request size in bytes.
            total_bytes: Known transfer length or ``None`` when unknown.
            enabled: Whether adaptive probing is requested.
            min_total_bytes: Minimum known transfer size that enables probing.
            min_samples: Full-part samples required before choosing a larger size.
            worse_tolerance: Relative throughput regression tolerated before settling.
        """
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
        """Record a full part and grow or settle only after enough comparable samples.

        Args:
            requested_size: Wire request size for the completed sample.
            received_size: Actual response bytes; short reads do not drive adaptation.
            duration_s: Measured part elapsed time in seconds.
        """
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
        """Double the legal part size, reset samples or settle at the configured maximum.

        Args:
            previous: Previous request size recorded in metrics.
            reason: Metric/event explanation for this growth attempt.
        """
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
    """Open or wrap a download target with explicit ownership and rollback semantics.

    Args:
        destination: ``None``, a path-like target or caller-owned binary stream.
        resume: Reuse an existing path from its aligned size when true.

    ``None`` creates a new internal buffer. Path parents are created; a new path
    is removed after failure, an existing non-resume path is overwritten and a
    resumed path is truncated to an aligned prefix then restored to that prefix
    after failure. A ``BytesIO`` input is restored to original data/position;
    arbitrary streams remain caller-owned and are not rolled back or closed.
    """
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
            """Restore caller-owned in-memory stream contents after a failed transfer."""
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
    """Truncate and flush a destination, moving path I/O off the event loop.

    Args:
        destination: Open destination handle to resize.
        size: New destination length in bytes.
    """

    def truncate_and_flush() -> None:
        """Apply the blocking truncate-and-flush operation to the destination handle."""
        destination.handle.truncate(size)
        destination.handle.flush()

    if destination.path is not None:
        await asyncio.to_thread(truncate_and_flush)
    else:
        truncate_and_flush()


async def _cleanup_failed_destination(destination: _DestinationHandle) -> None:
    """Apply the target's cancellation/failure cleanup policy without closing caller streams.

    Args:
        destination: Ownership and rollback policy chosen when opening the target.
    """
    if destination.path is not None:
        if destination.remove_on_cancel:
            if destination.should_close and not destination.handle.closed:
                destination.handle.close()
            destination.path.unlink(missing_ok=True)
            return

        def restore_prefix() -> None:
            """Restore a resumed path to the aligned bytes present before this transfer."""
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
    """Cancel every pending task and await their terminal cleanup without propagating errors.

    Args:
        pending: Outstanding tasks to cancel and gather with exceptions suppressed.
    """
    if not pending:
        return
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)


async def _call_progress(progress: ProgressCallback | None, current: int, total: int | None) -> None:
    """Invoke an optional sync or async progress callback with committed transfer bytes.

    Args:
        progress: Optional callback receiving ``(current, total)`` byte counts.
        current: Current committed/yielded operation bytes.
        total: Known operation bytes or ``None`` when unknown.
    """
    if progress is None:
        return
    result = progress(current, total)
    if inspect.isawaitable(result):
        await result


def _is_premium_flood(exc: Exception) -> bool:
    """Identify the premium flood-wait class without importing an optional subtype.

    Args:
        exc: Exception observed during a part request.
    """
    return isinstance(exc, FloodWait) and type(exc).__name__ == "FloodPremiumWait"


def _is_transient_download_error(exc: Exception, *, flood_sleep_threshold: int | None = 30) -> bool:
    """Classify retryable transport, timeout, server and eligible flood errors.

    Args:
        exc: Exception raised by a part request.
        flood_sleep_threshold: Maximum server flood wait in seconds accepted as retryable.
    """
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
    """Emit observability records describing a retry and optional server wait duration.

    Args:
        offset: Retried part start byte.
        limit: Retried part request length in bytes.
        attempt: Retry/flood attempt number for this part.
        max_retries: Non-flood retry budget shown in telemetry.
        error_type: Exception type name used as a metric attribute.
        flood_wait_seconds: Optional server-prescribed delay in seconds.
    """
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
    """Sleep for server pacing or jittered transient backoff before retrying a part.

    Args:
        exc: Flood wait or other transient exception determining the sleep policy.
        attempt: Zero-based non-flood failure count used for exponential backoff.
    """
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
    pacer. Disconnects/timeouts still shrink the window by one and the
    start-of-transfer burst is handled by ``_DownloadLaunchPacer``, so there is
    no slow start either.
    """

    def __init__(self, max_limit: int, *, clock: Clock = time.monotonic) -> None:
        """Initialize a fixed upper window and an immediately usable current limit.

        Args:
            max_limit: Maximum concurrent request slots allowed by the caller.
            clock: Monotonic seconds source used for recovery cooldowns.
        """
        self.max_limit = max(1, max_limit)
        self.limit = self.max_limit
        self._clock = clock
        self._successes_since_change = 0
        self._cooldown_until = 0.0
        self._premium_fallback = False

    async def on_retry(self, exc: Exception, attempt: int) -> None:
        """Reduce on connection health failures and force one slot for premium floods.

        Args:
            exc: Retryable error that indicates flood pacing or connection health.
            attempt: Current retry/flood attempt number recorded in telemetry.
        """
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
        """Increase the active limit slowly after cooldown and enough clean completions."""
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
