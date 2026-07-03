from __future__ import annotations

import asyncio
import hashlib
import inspect
import io
import logging
import math
import os
import secrets
import tempfile
import time
from collections.abc import AsyncIterable, Awaitable, Callable, Iterable, Iterator
from contextlib import AbstractContextManager, contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, cast

from miniproto.errors import (
    ClientDisconnected,
    InternalServerError,
    RequestTimeout,
    RpcError,
    RpcTimeout,
)
from miniproto.observability import emit_event, get_logger, record_metric
from miniproto.raw import functions, types

DEFAULT_CHUNK_SIZE = 512 * 1024
BIG_FILE_THRESHOLD = 10 * 1024 * 1024
_LOGGER = get_logger("media.upload")

type ProgressCallback = Callable[[int, int | None], Awaitable[None] | None]
type FileSource = (
    str
    | os.PathLike[str]
    | bytes
    | bytearray
    | memoryview
    | BinaryIO
    | Iterable[bytes]
    | AsyncIterable[bytes]
)


class MediaUploadError(RuntimeError):
    pass


type RawInvoker = Callable[..., Awaitable[object]]


@dataclass(frozen=True, slots=True)
class MediaUploadResult:
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
    concurrency: int = 1,
    progress: ProgressCallback | None = None,
    file_id: int | None = None,
    max_retries: int = 2,
    max_buffer_size: int | None = None,
    request_timeout: float | None = None,
) -> MediaUploadResult:
    _validate_upload_options(part_size, concurrency, max_retries, max_buffer_size)
    started = time.perf_counter()
    prepared = await _prepare_upload_source(source, file_name=file_name, chunk_size=part_size)
    if prepared.size <= 0:
        prepared.cleanup()
        raise ValueError("empty file upload is not supported")
    actual_file_id = secrets.randbits(63) or 1 if file_id is None else int(file_id)
    total_parts = math.ceil(prepared.size / part_size)
    is_big = prepared.size > BIG_FILE_THRESHOLD
    md5 = None if is_big else hashlib.md5(usedforsecurity=False)
    completed = 0
    progress_lock = asyncio.Lock()
    pending: set[asyncio.Task[None]] = set()

    async def upload_part(part_index: int, payload: bytes) -> None:
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
        )
        async with progress_lock:
            completed += len(payload)
            await _call_progress(progress, min(completed, prepared.size), prepared.size)

    try:
        with prepared.open_reader() as reader:
            for part_index in range(total_parts):
                payload = await _read_chunk(reader, part_size)
                if not payload:
                    break
                if md5 is not None:
                    md5.update(payload)
                task = asyncio.create_task(upload_part(part_index, payload))
                pending.add(task)
                if len(pending) >= concurrency:
                    pending = await _await_some(pending)
            if pending:
                await _await_all(pending)
    except BaseException:
        duration_ms = (time.perf_counter() - started) * 1000
        record_metric(
            "media.upload.errors",
            1,
            attributes={"big": is_big, "parts": total_parts, "concurrency": concurrency},
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
    part_size: int, concurrency: int, max_retries: int, max_buffer_size: int | None
) -> None:
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
    ceiling = part_size * concurrency if max_buffer_size is None else max_buffer_size
    if ceiling < part_size * concurrency:
        raise ValueError("max_buffer_size is lower than the configured upload concurrency window")


async def _prepare_upload_source(
    source: FileSource, *, file_name: str | None, chunk_size: int
) -> _PreparedUpload:
    if isinstance(source, str | os.PathLike):
        path = Path(cast(str | os.PathLike[str], source))
        stat = await asyncio.to_thread(path.stat)

        @contextmanager
        def open_path() -> Iterator[BinaryIO]:
            with path.open("rb") as handle:
                yield handle

        return _PreparedUpload(
            name=file_name or path.name or "file",
            size=stat.st_size,
            open_reader=open_path,
            cleanup=lambda: None,
        )
    if isinstance(source, bytes | bytearray | memoryview):
        payload = bytes(source)

        @contextmanager
        def open_bytes() -> Iterator[BinaryIO]:
            yield io.BytesIO(payload)

        return _PreparedUpload(
            name=file_name or "file",
            size=len(payload),
            open_reader=open_bytes,
            cleanup=lambda: None,
        )
    if _is_seekable_reader(source):
        reader = cast(BinaryIO, source)
        start = reader.tell()
        reader.seek(0, os.SEEK_END)
        end = reader.tell()
        reader.seek(start)

        @contextmanager
        def open_existing_reader() -> Iterator[BinaryIO]:
            reader.seek(start)
            yield reader

        return _PreparedUpload(
            name=file_name or _source_name(source),
            size=end - start,
            open_reader=open_existing_reader,
            cleanup=lambda: None,
        )
    return await _materialize_unknown_source(source, file_name=file_name, chunk_size=chunk_size)


async def _materialize_unknown_source(
    source: object, *, file_name: str | None, chunk_size: int
) -> _PreparedUpload:
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
            temporary.seek(0)
            yield cast(BinaryIO, temporary)

        return _PreparedUpload(
            name=file_name or _source_name(source),
            size=size,
            open_reader=open_temporary,
            cleanup=temporary.close,
        )
    except BaseException:
        temporary.close()
        raise


async def _read_chunk(reader: BinaryIO, size: int) -> bytes:
    return _coerce_chunk(await _maybe_await(reader.read(size)))


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
) -> None:
    request: object
    if big:
        request = functions.UploadSaveBigFilePart(
            file_id=file_id, file_part=part_index, file_total_parts=total_parts, bytes=payload
        )
    else:
        request = functions.UploadSaveFilePart(file_id=file_id, file_part=part_index, bytes=payload)
    for attempt in range(max_retries + 1):
        try:
            result = await invoke(request, request_timeout=request_timeout, retry=False)
        except Exception as exc:
            if attempt >= max_retries or not _is_transient_upload_error(exc):
                raise
            _emit_part_retry(
                part_index=part_index,
                total_parts=total_parts,
                attempt=attempt + 1,
                max_retries=max_retries,
                big=big,
                error_type=type(exc).__name__,
            )
            await asyncio.sleep(0)
            continue
        if _is_true(result):
            return
        if attempt >= max_retries:
            break
        _emit_part_retry(
            part_index=part_index,
            total_parts=total_parts,
            attempt=attempt + 1,
            max_retries=max_retries,
            big=big,
            error_type="BoolFalse",
        )
        await asyncio.sleep(0)
    raise MediaUploadError(f"Telegram did not accept upload part {part_index}")


async def _await_some(pending: set[asyncio.Task[None]]) -> set[asyncio.Task[None]]:
    done, remaining = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
    for task in done:
        await task
    return set(remaining)


async def _await_all(pending: set[asyncio.Task[None]]) -> None:
    for task in asyncio.as_completed(pending):
        await task


async def _cancel_pending(pending: set[asyncio.Task[None]]) -> None:
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


async def _maybe_await(value: object) -> object:
    if inspect.isawaitable(value):
        return await value
    return value


def _coerce_chunk(chunk: object) -> bytes:
    if chunk in (None, b""):
        return b""
    if isinstance(chunk, bytes):
        return chunk
    if isinstance(chunk, bytearray | memoryview):
        return bytes(chunk)
    raise TypeError("file sources must yield bytes")


def _has_read(source: object) -> bool:
    return callable(getattr(source, "read", None))


def _is_seekable_reader(source: object) -> bool:
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
    name = getattr(source, "name", None)
    if isinstance(name, str) and name:
        return Path(name).name or "file"
    return "file"


def _is_true(result: object) -> bool:
    return result is True or isinstance(result, types.BoolTrue)


def _is_transient_upload_error(exc: Exception) -> bool:
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
    *, part_index: int, total_parts: int, attempt: int, max_retries: int, big: bool, error_type: str
) -> None:
    record_metric("media.upload.part_retries", 1, attributes={"big": big, "error_type": error_type})
    emit_event(
        _LOGGER,
        logging.WARNING,
        "media.upload.part_retry",
        outcome="retry",
        part_index=part_index,
        total_parts=total_parts,
        attempt=attempt,
        max_retries=max_retries,
        big=big,
        error_type=error_type,
    )


__all__ = [
    "BIG_FILE_THRESHOLD",
    "DEFAULT_CHUNK_SIZE",
    "FileSource",
    "MediaUploadError",
    "MediaUploadResult",
    "ProgressCallback",
    "RawInvoker",
    "upload_file",
]
