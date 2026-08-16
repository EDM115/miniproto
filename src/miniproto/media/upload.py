"""Upload media in bounded concurrent parts with cancellation-safe cleanup."""

from __future__ import annotations

import asyncio
import hashlib
import inspect
import io
import logging
import math
import os
import random
import secrets
import tempfile
import time
from collections.abc import AsyncIterable, Awaitable, Callable, Iterable, Iterator
from contextlib import AbstractContextManager, contextmanager, suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, cast

from miniproto.errors import ClientDisconnected, FloodWait, InternalServerError, RequestTimeout, RpcError, RpcTimeout
from miniproto.media.retry import backoff_delay
from miniproto.observability import emit_event, get_logger, record_metric
from miniproto.raw import functions, types

DEFAULT_CHUNK_SIZE = 512 * 1024
BIG_FILE_THRESHOLD = 10 * 1024 * 1024
DEFAULT_UPLOAD_FLOOD_SLEEP_THRESHOLD = 30
# Floods within the threshold are server pacing and retry without consuming
# the transient-failure budget; this cap only bounds pathological storms.
MAX_FLOOD_RETRIES_PER_PART = 16
_MIN_FLOOD_SLEEP_S = 1.0
_FLOOD_SLEEP_JITTER_S = 0.3
# Stale parts occupying a lane for the global 30 s hurt upload tails; 45 s is
# the live-bench default that sustained 15-16 MiB/s uploads on DC4.
DEFAULT_UPLOAD_PART_TIMEOUT = 45.0
# mtcute reads 24 parts ahead, MTKruto 16: one window of read-ahead keeps the
# network from ever waiting on disk without unbounded buffering.
DEFAULT_UPLOAD_CONCURRENCY = 8
_LOGGER = get_logger("media.upload")

type ProgressCallback = Callable[[int, int | None], Awaitable[None] | None]
type FileSource = (
    str | os.PathLike[str] | bytes | bytearray | memoryview | BinaryIO | Iterable[bytes] | AsyncIterable[bytes]
)


class MediaUploadError(RuntimeError):
    """Raised only for unsatisfiable part-count configuration or ``BoolFalse`` replies.

    Transport, RPC, cancellation, source, and other invocation failures propagate
    their original exceptions; this error marks a maximum-part-size constraint or
    Telegram returning false after the configured false-result retry budget.
    """

    pass


type RawInvoker = Callable[..., Awaitable[object]]


@dataclass(frozen=True, slots=True)
class MediaUploadResult:
    """Completed upload metadata and the MTProto input-file reference to reuse.

    Attributes:
        file_id: Generated ID or ``int(file_id)`` supplied by the caller; zero is accepted when supplied.
        name: File name sent to Telegram.
        size: Exact uploaded source size in bytes.
        parts: Total successfully saved part count.
        part_size: Final KiB-aligned part size in bytes.
        big: Whether the source exceeded the big-file threshold.
        input_file: Matching Telegram small or big input-file reference.
        md5_checksum: Small-file MD5 of uploaded bytes, otherwise ``None``.
    """

    file_id: int
    name: str
    size: int
    parts: int
    part_size: int
    big: bool
    input_file: types.InputFile | types.InputFileBig
    md5_checksum: str | None = None


@dataclass(slots=True)
class _PreparedUpload:
    """A replayable reader plus cleanup callback for one normalized source.

    Attributes:
        name: Resolved upload filename.
        size: Exact source length in bytes.
        open_reader: Context-manager factory exposing the normalized bytes from offset zero.
        cleanup: Callback that releases temporary spool resources, if any.
    """

    name: str
    size: int
    open_reader: Callable[[], AbstractContextManager[BinaryIO]]
    cleanup: Callable[[], None]


async def upload_file(
    invoke: RawInvoker,
    source: FileSource,
    *,
    file_name: str | None = None,
    part_size: int = DEFAULT_CHUNK_SIZE,
    concurrency: int = DEFAULT_UPLOAD_CONCURRENCY,
    progress: ProgressCallback | None = None,
    file_id: int | None = None,
    max_retries: int = 2,
    max_buffer_size: int | None = None,
    request_timeout: float | None = None,
    flood_sleep_threshold: int | None = DEFAULT_UPLOAD_FLOOD_SLEEP_THRESHOLD,
    max_file_parts: int | None = 4000,
) -> MediaUploadResult:
    """Upload a source as MTProto file parts and return its input-file handle.

    Args:
        invoke: Raw request callable used to save each part.
        source: Path, bytes, readable stream, or synchronous/asynchronous byte iterable. Paths are opened by this function; caller-owned readers are not closed.
        file_name: Optional override for the Telegram file name.
        part_size: KiB-aligned part size in bytes, at most 512 KiB.
        concurrency: Maximum in-flight save requests and bounded read-ahead queue slots.
        progress: Optional callback receiving ``(completed_bytes, total_bytes)`` after accepted parts, serialized in completion order rather than part-index order.
        file_id: Optional ID converted with ``int`` and used verbatim, including zero; absent IDs are generated non-zero.
        max_retries: Transient non-flood retry attempts per part.
        max_buffer_size: Required to cover the configured concurrency window when set.
        request_timeout: Per-part timeout; defaults to the upload-tail-safe timeout.
        flood_sleep_threshold: Largest server flood wait in seconds treated as retryable pacing; each part has a separate cap of 16 accepted flood retries.
        max_file_parts: Maximum accepted part count; size is increased when possible.

    Returns:
        The completed file metadata and a matching ``InputFile`` or ``InputFileBig``.

    Raises:
        ValueError: If options are invalid or the normalized source is empty.
        TypeError: If a streamed source yields a non-byte chunk.
        MediaUploadError: If part-count constraints cannot be met or Telegram rejects a part.
        asyncio.CancelledError: After cancelling producer and in-flight part tasks and cleaning up.

    The checksum covers exactly the bytes read for small files. Seekable callers
    are rewound to their initial offset before uploading and left at their final
    read position; one-shot streams and iterables are consumed into an owned
    temporary spool that is closed on success, failure, or cancellation.
    """
    _validate_upload_options(
        part_size, concurrency, max_retries, max_buffer_size, flood_sleep_threshold, max_file_parts
    )
    if request_timeout is None:
        request_timeout = DEFAULT_UPLOAD_PART_TIMEOUT
    started = time.perf_counter()
    prepared = await _prepare_upload_source(source, file_name=file_name, chunk_size=part_size)
    if prepared.size <= 0:
        prepared.cleanup()
        raise ValueError("empty file upload is not supported")
    part_size = _part_size_for_part_limit(prepared.size, part_size, max_file_parts)
    register_transfer = getattr(invoke, "register_transfer", None)
    if callable(register_transfer):
        registered = register_transfer(prepared.size)
        if inspect.isawaitable(registered):
            await registered
    actual_file_id = secrets.randbits(63) or 1 if file_id is None else int(file_id)
    total_parts = math.ceil(prepared.size / part_size)
    is_big = prepared.size > BIG_FILE_THRESHOLD
    md5 = None if is_big else hashlib.md5(usedforsecurity=False)
    completed = 0
    progress_lock = asyncio.Lock()
    pending: set[asyncio.Task[None]] = set()
    # One window of parts is read ahead of the sends (mtcute: 24, MTKruto: 16)
    # on a worker thread, so the event loop never blocks on disk and the
    # network never waits for a read. Memory stays bounded by ~2 windows.
    read_queue: asyncio.Queue[tuple[int, bytes] | None] = asyncio.Queue(maxsize=max(2, concurrency))

    async def produce_parts(reader: BinaryIO) -> None:
        """Read ordered parts into the bounded queue and always signal completion.

        Args:
            reader: Normalized binary reader positioned at the upload start.
        """
        try:
            for part_index in range(total_parts):
                payload = await _read_chunk_threaded(reader, part_size)
                if not payload:
                    break
                if md5 is not None:
                    md5.update(payload)
                await read_queue.put((part_index, payload))
        finally:
            # Always unblock the consumer, even when a read fails; the awaited
            # producer task re-raises the original error afterwards. If the
            # producer itself is cancelled while the bounded queue is full,
            # the consumer is already unwinding and cannot make room: do not
            # deadlock cancellation waiting to enqueue an unused sentinel.
            current_task = asyncio.current_task()
            if current_task is not None and current_task.cancelling():
                with suppress(asyncio.QueueFull):
                    read_queue.put_nowait(None)
            else:
                try:
                    await read_queue.put(None)
                except asyncio.CancelledError:
                    with suppress(asyncio.QueueFull):
                        read_queue.put_nowait(None)
                    raise

    async def upload_part(part_index: int, payload: bytes) -> None:
        """Save one queued part and serialize byte-count progress updates.

        Args:
            part_index: Zero-based Telegram part index.
            payload: Exact bytes for this part.
        """
        nonlocal completed
        await _save_part(
            invoke,
            file_id=actual_file_id,
            part_index=part_index,
            total_parts=total_parts,
            payload=payload,
            big=is_big,
            max_retries=max_retries,
            request_timeout=request_timeout,
            flood_sleep_threshold=flood_sleep_threshold,
        )
        async with progress_lock:
            completed += len(payload)
            await _call_progress(progress, min(completed, prepared.size), prepared.size)

    producer: asyncio.Task[None] | None = None
    try:
        with prepared.open_reader() as reader:
            producer = asyncio.create_task(produce_parts(reader))
            while True:
                item = await read_queue.get()
                if item is None:
                    break
                part_index, payload = item
                task = asyncio.create_task(upload_part(part_index, payload))
                pending.add(task)
                if len(pending) >= concurrency:
                    pending = await _await_some(pending)
            await producer
            if pending:
                await _await_all(pending)
    except BaseException:
        duration_ms = (time.perf_counter() - started) * 1000
        record_metric(
            "media.upload.errors", 1, attributes={"big": is_big, "parts": total_parts, "concurrency": concurrency}
        )
        emit_event(
            _LOGGER,
            40,
            "media.upload",
            outcome="error",
            size_bytes=prepared.size,
            parts=total_parts,
            part_size=part_size,
            concurrency=concurrency,
            big=is_big,
            duration_ms=duration_ms,
        )
        if producer is not None and not producer.done():
            producer.cancel()
            await asyncio.gather(producer, return_exceptions=True)
        await _cancel_pending(pending)
        raise
    finally:
        prepared.cleanup()

    duration_ms = (time.perf_counter() - started) * 1000
    throughput_bytes_s = prepared.size / max(duration_ms / 1000, 1e-9)
    record_metric(
        "media.upload.bytes",
        prepared.size,
        unit="bytes",
        attributes={"big": is_big, "parts": total_parts, "concurrency": concurrency},
    )
    record_metric(
        "media.upload.duration",
        duration_ms,
        unit="ms",
        attributes={"big": is_big, "parts": total_parts, "concurrency": concurrency},
    )
    record_metric(
        "media.upload.throughput",
        throughput_bytes_s,
        unit="bytes/s",
        attributes={"big": is_big, "parts": total_parts, "concurrency": concurrency},
    )
    emit_event(
        _LOGGER,
        20,
        "media.upload",
        outcome="success",
        size_bytes=prepared.size,
        parts=total_parts,
        part_size=part_size,
        concurrency=concurrency,
        big=is_big,
        duration_ms=duration_ms,
        throughput_bytes_s=throughput_bytes_s,
    )
    checksum = md5.hexdigest() if md5 is not None else None
    if is_big:
        input_file = types.InputFileBig(id=actual_file_id, parts=total_parts, name=prepared.name)
    else:
        input_file = types.InputFile(
            id=actual_file_id, parts=total_parts, name=prepared.name, md5_checksum=checksum or ""
        )
    return MediaUploadResult(
        file_id=actual_file_id,
        name=prepared.name,
        size=prepared.size,
        parts=total_parts,
        part_size=part_size,
        big=is_big,
        input_file=input_file,
        md5_checksum=checksum,
    )


def _validate_upload_options(
    part_size: int,
    concurrency: int,
    max_retries: int,
    max_buffer_size: int | None,
    flood_sleep_threshold: int | None = None,
    max_file_parts: int | None = None,
) -> None:
    """Validate upload window, retry, flood-pacing, and part-count options.

    Args:
        part_size: Requested KiB-aligned part size in bytes.
        concurrency: Number of in-flight request slots.
        max_retries: Non-flood retry count per part.
        max_buffer_size: Optional required lower bound for the concurrent window.
        flood_sleep_threshold: Optional non-negative retryable flood-wait maximum.
        max_file_parts: Optional positive Telegram part-count limit.
    """
    if part_size <= 0:
        raise ValueError("part_size must be positive")
    if part_size % 1024:
        raise ValueError("part_size must be a multiple of 1024 bytes")
    if part_size > DEFAULT_CHUNK_SIZE:
        raise ValueError("part_size must not exceed 512 KiB")
    if concurrency <= 0:
        raise ValueError("concurrency must be positive")
    if max_retries < 0:
        raise ValueError("max_retries must not be negative")
    if flood_sleep_threshold is not None and flood_sleep_threshold < 0:
        raise ValueError("flood_sleep_threshold must not be negative")
    if max_file_parts is not None and max_file_parts <= 0:
        raise ValueError("max_file_parts must be positive")
    ceiling = part_size * concurrency if max_buffer_size is None else max_buffer_size
    if ceiling < part_size * concurrency:
        raise ValueError("max_buffer_size is lower than the configured upload concurrency window")


def _part_size_for_part_limit(size: int, part_size: int, max_file_parts: int | None) -> int:
    """Increase the KiB-aligned part size just enough to satisfy a part cap.

    Args:
        size: Exact source size in bytes.
        part_size: Initially validated part size in bytes.
        max_file_parts: Optional maximum number of Telegram parts.
    """
    if max_file_parts is None:
        return part_size
    total_parts = math.ceil(size / part_size)
    if total_parts <= max_file_parts:
        return part_size
    required = math.ceil(size / max_file_parts)
    adjusted = math.ceil(required / 1024) * 1024
    if adjusted > DEFAULT_CHUNK_SIZE:
        raise MediaUploadError(f"file requires more than {max_file_parts} upload parts at the maximum part size")
    return max(part_size, adjusted)


async def _prepare_upload_source(source: FileSource, *, file_name: str | None, chunk_size: int) -> _PreparedUpload:
    """Normalize replayable sources directly and materialize one-shot sources.

    Args:
        source: Input path, bytes, stream, or iterable.
        file_name: Optional file-name override.
        chunk_size: Spool/read chunk size in bytes.
    """
    if isinstance(source, str | os.PathLike):
        path = Path(cast(str | os.PathLike[str], source))
        stat = await asyncio.to_thread(path.stat)

        @contextmanager
        def open_path() -> Iterator[BinaryIO]:
            """Open the path afresh for the upload reader context."""
            with path.open("rb") as handle:
                yield handle

        return _PreparedUpload(
            name=file_name or path.name or "file", size=stat.st_size, open_reader=open_path, cleanup=lambda: None
        )
    if isinstance(source, bytes | bytearray | memoryview):
        payload = bytes(source)

        @contextmanager
        def open_bytes() -> Iterator[BinaryIO]:
            """Expose immutable input bytes through a fresh in-memory reader."""
            yield io.BytesIO(payload)

        return _PreparedUpload(
            name=file_name or "file", size=len(payload), open_reader=open_bytes, cleanup=lambda: None
        )
    if _is_seekable_reader(source):
        reader = cast(BinaryIO, source)
        start = reader.tell()
        reader.seek(0, os.SEEK_END)
        end = reader.tell()
        reader.seek(start)

        @contextmanager
        def open_existing_reader() -> Iterator[BinaryIO]:
            """Reset the seekable source to its initial offset for this upload."""
            reader.seek(start)
            yield reader

        return _PreparedUpload(
            name=file_name or _source_name(source),
            size=end - start,
            open_reader=open_existing_reader,
            cleanup=lambda: None,
        )
    return await _materialize_unknown_source(source, file_name=file_name, chunk_size=chunk_size)


async def _materialize_unknown_source(source: object, *, file_name: str | None, chunk_size: int) -> _PreparedUpload:
    """Spool an unknown-length source to a temporary replayable binary reader.

    Args:
        source: Non-seekable reader or synchronous/asynchronous chunk iterable.
        file_name: Optional file-name override.
        chunk_size: Requested read size in bytes for reader sources.
    """
    temporary = tempfile.TemporaryFile("w+b")  # noqa: SIM115 - cleanup is returned with the prepared source.
    size = 0
    try:
        if _has_read(source):
            while True:
                chunk = await _maybe_await(cast(Any, source).read(chunk_size))
                payload = _coerce_chunk(chunk)
                if not payload:
                    break
                temporary.write(payload)
                size += len(payload)
        elif hasattr(source, "__aiter__"):
            async for chunk in cast(AsyncIterable[bytes], source):
                payload = _coerce_chunk(chunk)
                temporary.write(payload)
                size += len(payload)
        else:
            for chunk in cast(Iterable[bytes], source):
                payload = _coerce_chunk(chunk)
                temporary.write(payload)
                size += len(payload)
        temporary.flush()

        @contextmanager
        def open_temporary() -> Iterator[BinaryIO]:
            """Rewind the completed temporary spool for a consumer context."""
            temporary.seek(0)
            yield cast(BinaryIO, temporary)

        return _PreparedUpload(
            name=file_name or _source_name(source), size=size, open_reader=open_temporary, cleanup=temporary.close
        )
    except BaseException:
        temporary.close()
        raise


async def _read_chunk_threaded(reader: BinaryIO, size: int) -> bytes:
    """Read one part without blocking the event loop.

    Async readers are awaited directly; synchronous file objects (the common
    case) do their blocking ``read()`` on a worker thread. In-memory readers
    skip the thread hop -- their reads cannot block.

    Args:
        reader: Normalized binary reader to consume.
        size: Maximum bytes requested from one read.
    """
    read = reader.read
    if inspect.iscoroutinefunction(read):
        return _coerce_chunk(await read(size))
    if isinstance(reader, io.BytesIO):
        return _coerce_chunk(read(size))
    return _coerce_chunk(await asyncio.to_thread(read, size))


async def _save_part(
    invoke: RawInvoker,
    *,
    file_id: int,
    part_index: int,
    total_parts: int,
    payload: bytes,
    big: bool,
    max_retries: int,
    request_timeout: float | None,
    flood_sleep_threshold: int | None = DEFAULT_UPLOAD_FLOOD_SLEEP_THRESHOLD,
) -> None:
    """Save one part, retrying transient transport errors and short flood waits.

    Flood pacing has its own bounded retry counter and does not consume the
    transient-failure budget, preserving late-upload integrity under throttling.

    Args:
        invoke: Raw request callable used to save the encoded part.
        file_id: File identifier used in the Telegram save request.
        part_index: Zero-based part index.
        total_parts: Total expected number of parts for big-file requests.
        payload: Exact bytes to save.
        big: Whether to use Telegram's big-file request type.
        max_retries: Retry budget for transient failures and false results.
        request_timeout: Per-request timeout forwarded to the invoker.
        flood_sleep_threshold: Maximum retryable server flood wait in seconds.
    """
    request: object
    if big:
        request = functions.UploadSaveBigFilePart(
            file_id=file_id, file_part=part_index, file_total_parts=total_parts, bytes=payload
        )
    else:
        request = functions.UploadSaveFilePart(file_id=file_id, file_part=part_index, bytes=payload)
    failures = 0
    flood_retries = 0
    while True:
        try:
            record_metric("media.upload.part_requests", 1, attributes={"big": big})
            result = await invoke(request, request_timeout=request_timeout, retry=False, flood_sleep_threshold=0)
        except Exception as exc:
            if not _is_transient_upload_error(exc, flood_sleep_threshold=flood_sleep_threshold):
                raise
            if isinstance(exc, FloodWait):
                # Server pacing, not a failure: floods never consume the
                # transient retry budget (one flood used to abort a 2000 MiB
                # upload at 99%); a generous separate cap bounds storms.
                flood_retries += 1
                if flood_retries > MAX_FLOOD_RETRIES_PER_PART:
                    record_metric("media.upload.flood_retry_budget_exhausted", 1)
                    raise
                attempt = flood_retries
            else:
                failures += 1
                if failures > max_retries:
                    raise
                attempt = failures
            _emit_part_retry(
                part_index=part_index,
                total_parts=total_parts,
                attempt=attempt,
                max_retries=max_retries,
                big=big,
                error_type=type(exc).__name__,
                flood_wait_seconds=exc.seconds if isinstance(exc, FloodWait) else None,
            )
            await _sleep_before_retry(exc, failures, big=big)
            continue
        if _is_true(result):
            return
        failures += 1
        if failures > max_retries:
            break
        _emit_part_retry(
            part_index=part_index,
            total_parts=total_parts,
            attempt=failures,
            max_retries=max_retries,
            big=big,
            error_type="BoolFalse",
        )
        await _sleep_before_retry(None, failures, big=big)
    raise MediaUploadError(f"Telegram did not accept upload part {part_index}")


async def _sleep_before_retry(exc: Exception | None, attempt: int, *, big: bool) -> None:
    """Apply server flood pacing or exponential transient-error backoff.

    Args:
        exc: Flood error carrying server pacing, or another/absent retry cause.
        attempt: One-based transient attempt used for exponential backoff.
        big: Whether retry telemetry is for a big-file upload.
    """
    if isinstance(exc, FloodWait):
        # FLOOD_WAIT_0 retried instantly just re-triggers the flood. Positive
        # waits already carry server pacing, so only add tight jitter to
        # desynchronize lockstep wakers without over-sleeping at scale.
        base = _MIN_FLOOD_SLEEP_S if exc.seconds <= 0 else float(exc.seconds)
        delay = base + random.uniform(0.0, _FLOOD_SLEEP_JITTER_S)  # noqa: S311
    else:
        delay = backoff_delay(attempt)
    record_metric("media.upload.retry_sleep_seconds", delay, unit="s", attributes={"big": big})
    await asyncio.sleep(delay)


async def _await_some(pending: set[asyncio.Task[None]]) -> set[asyncio.Task[None]]:
    """Await one completion set, propagating any completed task exception.

    Args:
        pending: Current in-flight part tasks occupying concurrency slots.
    """
    done, remaining = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
    for task in done:
        await task
    return set(remaining)


async def _await_all(pending: set[asyncio.Task[None]]) -> None:
    """Await every remaining part task and propagate its first exception.

    Args:
        pending: Remaining in-flight part tasks to drain.
    """
    for task in asyncio.as_completed(pending):
        await task


async def _cancel_pending(pending: set[asyncio.Task[None]]) -> None:
    """Cancel and drain in-flight tasks so upload cancellation cannot leak them.

    Args:
        pending: In-flight part tasks to cancel and gather.
    """
    if not pending:
        return
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)


async def _call_progress(progress: ProgressCallback | None, current: int, total: int | None) -> None:
    """Call a synchronous or asynchronous progress callback when configured.

    Args:
        progress: Callback receiving completed and total byte counts, if any.
        current: Cumulative successfully uploaded bytes.
        total: Exact total source bytes, or ``None`` when unavailable.
    """
    if progress is None:
        return
    result = progress(current, total)
    if inspect.isawaitable(result):
        await result


async def _maybe_await(value: object) -> object:
    """Await awaitable stream reads while preserving immediate values.

    Args:
        value: Immediate or awaitable read result.
    """
    if inspect.isawaitable(value):
        return await value
    return value


def _coerce_chunk(chunk: object) -> bytes:
    """Accept supported byte-like chunks and reject all other stream values.

    Args:
        chunk: Reader or iterable item expected to be byte-like or an EOF marker.
    """
    if chunk in (None, b""):
        return b""
    if isinstance(chunk, bytes):
        return chunk
    if isinstance(chunk, bytearray | memoryview):
        return bytes(chunk)
    raise TypeError("file sources must yield bytes")


def _has_read(source: object) -> bool:
    """Return whether ``source`` exposes a callable ``read`` method.

    Args:
        source: Candidate upload source.
    """
    return callable(getattr(source, "read", None))


def _is_seekable_reader(source: object) -> bool:
    """Return whether a readable source can be safely rewound for upload.

    Args:
        source: Candidate reader whose read/seek/tell capabilities are inspected.
    """
    if not _has_read(source) or not callable(getattr(source, "seek", None)):
        return False
    tell = getattr(source, "tell", None)
    if not callable(tell):
        return False
    seekable = getattr(source, "seekable", None)
    if callable(seekable):
        try:
            return bool(seekable())
        except OSError:
            return False
    return True


def _source_name(source: object) -> str:
    """Derive a portable basename, falling back to Telegram's generic ``file``.

    Args:
        source: Candidate source whose optional ``name`` attribute is inspected.
    """
    name = getattr(source, "name", None)
    if isinstance(name, str) and name:
        return Path(name).name or "file"
    return "file"


def _is_true(result: object) -> bool:
    """Recognize MTProto's two accepted true-result representations.

    Args:
        result: Raw response returned by Telegram's part-save request.
    """
    return result is True or isinstance(result, types.BoolTrue)


def _is_transient_upload_error(
    exc: Exception, *, flood_sleep_threshold: int | None = DEFAULT_UPLOAD_FLOOD_SLEEP_THRESHOLD
) -> bool:
    """Return whether an exception is retryable under the configured flood policy.

    Args:
        exc: Exception raised by a part-save invocation.
        flood_sleep_threshold: Optional largest retryable flood wait in seconds.
    """
    if isinstance(exc, FloodWait):
        # Flood waits (including FLOOD_PREMIUM_WAIT throughput throttles) are retried by
        # sleeping inside the media layer, capped by the caller's threshold.
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
    *,
    part_index: int,
    total_parts: int,
    attempt: int,
    max_retries: int,
    big: bool,
    error_type: str,
    flood_wait_seconds: int | None = None,
) -> None:
    """Record structured metrics and an event for one scheduled part retry.

    Args:
        part_index: Zero-based part index being retried.
        total_parts: Total expected upload part count.
        attempt: Retry number within the applicable retry category.
        max_retries: Configured non-flood/false-result retry cap.
        big: Whether telemetry is for a big-file upload.
        error_type: Stable exception or ``BoolFalse`` classification.
        flood_wait_seconds: Server pacing delay when the retry was a flood wait.
    """
    record_metric("media.upload.part_retries", 1, attributes={"big": big, "error_type": error_type})
    fields: dict[str, object] = {
        "outcome": "retry",
        "part_index": part_index,
        "total_parts": total_parts,
        "attempt": attempt,
        "max_retries": max_retries,
        "big": big,
        "error_type": error_type,
    }
    if flood_wait_seconds is not None:
        fields["flood_wait_seconds"] = flood_wait_seconds
        attrs = {"error_type": error_type}
        record_metric("media.upload.flood_waits", 1, attributes=attrs)
        record_metric("media.upload.flood_wait_seconds", flood_wait_seconds, unit="s", attributes=attrs)
    emit_event(_LOGGER, logging.WARNING, "media.upload.part_retry", **fields)


__all__ = [
    "BIG_FILE_THRESHOLD",
    "DEFAULT_CHUNK_SIZE",
    "DEFAULT_UPLOAD_CONCURRENCY",
    "DEFAULT_UPLOAD_FLOOD_SLEEP_THRESHOLD",
    "DEFAULT_UPLOAD_PART_TIMEOUT",
    "FileSource",
    "MediaUploadError",
    "MediaUploadResult",
    "ProgressCallback",
    "RawInvoker",
    "upload_file",
]
