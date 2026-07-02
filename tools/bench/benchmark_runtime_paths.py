from __future__ import annotations

import asyncio
import statistics
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from miniproto import ClientConfig, event_loop
from miniproto.media import DEFAULT_CHUNK_SIZE, download_file, upload_file
from miniproto.raw import functions, types
from miniproto.session.storage import InMemorySessionStorage
from miniproto.types import Update
from miniproto.updates.manager import UpdateManager


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    name: str
    runs: int
    best_ms: float
    median_ms: float


@dataclass(frozen=True, slots=True)
class AsyncBenchmarkCase:
    name: str
    func: Callable[[], Awaitable[object]]


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
            raise TypeError(f"unexpected download request: {type(request).__name__}")
        offset = int(request.offset)
        limit = int(request.limit)
        chunk = self.payload[offset : offset + limit]
        return types.UploadFile(type=types.StorageFileUnknown(), mtime=1_700_000_000, bytes=chunk)


@dataclass(slots=True)
class ConcurrentInvoker:
    count: int = 0

    async def __call__(self, request: object) -> object:
        self.count += 1
        await asyncio.sleep(0)
        return types.BoolTrue()


def main() -> int:
    print(
        f"event_loop_backend={event_loop.backend_name()} "
        f"installed={event_loop.installed()} version={event_loop.backend_version()}"
    )
    return event_loop.run(_main())


async def _main() -> int:
    payload = bytes((index * 17) % 256 for index in range(8 * 1024 * 1024))
    cases = (
        AsyncBenchmarkCase("update_dispatch_10k", lambda: _bench_update_dispatch(10_000)),
        AsyncBenchmarkCase("media_upload_8m_concurrency_8", lambda: _bench_upload(payload)),
        AsyncBenchmarkCase("media_download_8m", lambda: _bench_download(payload)),
        AsyncBenchmarkCase("synthetic_pending_requests_1k", lambda: _bench_pending_requests(1_000)),
    )
    for case in cases:
        result = await _run(case.name, case.func)
        print(
            f"{result.name}: best={result.best_ms:.3f}ms "
            f"median={result.median_ms:.3f}ms runs={result.runs}"
        )
    return 0


async def _run(name: str, func: Callable[[], Awaitable[object]], runs: int = 10) -> BenchmarkResult:
    durations: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        await func()
        durations.append((time.perf_counter() - start) * 1000)
    return BenchmarkResult(
        name=name, runs=runs, best_ms=min(durations), median_ms=statistics.median(durations)
    )


async def _bench_update_dispatch(count: int) -> int:
    manager = UpdateManager(
        ClientConfig(api_id=1, api_hash="hash", update_queue_size=count + 1),
        InMemorySessionStorage(),
        _noop_invoke,
    )
    consumed = 0

    async def consume() -> None:
        nonlocal consumed
        async for _update in manager.iter_updates():
            consumed += 1
            if consumed >= count:
                return

    consumer = asyncio.create_task(consume())
    for index in range(count):
        await manager.emit_update(Update(raw=index))
    await consumer
    return consumed


async def _bench_upload(payload: bytes) -> int:
    invoker = UploadInvoker()
    result = await upload_file(
        invoker,
        payload,
        file_name="bench.bin",
        part_size=DEFAULT_CHUNK_SIZE,
        concurrency=8,
        file_id=123,
    )
    return result.size


async def _bench_download(payload: bytes) -> int:
    invoker = DownloadInvoker(payload)
    location = types.InputDocumentFileLocation(
        id=1, access_hash=2, file_reference=b"ref", thumb_size=""
    )
    result = await download_file(
        invoker, location, limit=len(payload), part_size=DEFAULT_CHUNK_SIZE, total_size=len(payload)
    )
    return result.bytes_downloaded


async def _bench_pending_requests(count: int) -> int:
    invoker = ConcurrentInvoker()
    await asyncio.gather(*(invoker(types.BoolTrue()) for _ in range(count)))
    return invoker.count


async def _noop_invoke(request: object) -> object:
    raise AssertionError(f"unexpected update recovery request: {type(request).__name__}")


if __name__ == "__main__":
    raise SystemExit(main())
