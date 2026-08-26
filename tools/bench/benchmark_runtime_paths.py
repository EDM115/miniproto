"""Run deterministic, in-process benchmarks for representative miniproto runtime paths.

This script deliberately uses synthetic payloads, in-memory storage, fake invokers and a loopback-only sender state. It exercises no live Telegram session, network transport, credential or filesystem transfer path. Timings use ``perf_counter`` and report the best and median of ten complete runs; they are comparative local measurements, not service-level performance claims.
"""

from __future__ import annotations

import argparse
import asyncio
import statistics
import sys
import time
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import UTC, datetime
from typing import Any

from miniproto import ClientConfig, event_loop
from miniproto.client import _CachedSessionStorage
from miniproto.config import TransportConfig
from miniproto.connection.sender import MTProtoSender
from miniproto.connection.transport import ConnectionEndpoint
from miniproto.media import DEFAULT_CHUNK_SIZE, download_file, upload_file
from miniproto.mtproto.state import MTProtoState
from miniproto.peers import (
    USERNAME_CACHE_TTL,
    PeerCache,
    _entry_has_username,
    _normalize_phone,
    _normalize_username,
    _resolve_numeric_peer_from_record,
)
from miniproto.raw import functions, types
from miniproto.session.models import PeerCacheEntry, SessionRecord, UserIdentity
from miniproto.session.storage import InMemorySessionStorage
from miniproto.tl import decode_object
from miniproto.types import Peer, Update
from miniproto.updates.manager import UpdateManager


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """Aggregate wall-clock timing for one benchmark case.

    Attributes:
        name: Stable benchmark output label.
        runs: Number of complete measured invocations.
        best_ms: Minimum wall-clock duration in milliseconds.
        median_ms: Median wall-clock duration in milliseconds.
    """

    name: str
    runs: int
    best_ms: float
    median_ms: float


@dataclass(frozen=True, slots=True)
class AsyncBenchmarkCase:
    """Named asynchronous benchmark workload invoked once per measured run.

    Attributes:
        name: Stable output label for the synthetic comparison case.
        func: Zero-argument awaitable synthetic workload; it has no live transport boundary.
    """

    name: str
    func: Callable[[], Awaitable[object]]


@dataclass(slots=True)
class UploadInvoker:
    """Fake upload RPC invoker that records requests and always returns ``BoolTrue``.

    Attributes:
        requests: Raw synthetic upload requests observed in benchmark memory.
    """

    requests: list[object] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        """Record ``request`` without network I/O and return a successful synthetic response.

        Args:
            request: Synthetic raw upload request to retain for workload validation.
            kwargs: Ignored forwarded ``**kwargs`` accepted for invoker compatibility.
        """
        self.requests.append(request)
        return types.BoolTrue()


@dataclass(slots=True)
class DownloadInvoker:
    """Fake ``upload.getFile`` invoker serving slices from an in-memory benchmark payload.

    Attributes:
        payload: Immutable synthetic source bytes sliced by requested offsets and limits.
        requests: Raw file requests observed without any network I/O.
    """

    payload: bytes
    requests: list[object] = field(default_factory=list)

    async def __call__(self, request: object, **kwargs: object) -> object:
        """Record and validate a file request, then return its requested payload slice.

        Raises:
            TypeError: If the workload sends a request other than ``upload.getFile``.

        Args:
            request: Synthetic file request whose offset and limit select payload bytes.
            kwargs: Ignored forwarded ``**kwargs`` accepted for invoker compatibility.
        """
        self.requests.append(request)
        if not isinstance(request, functions.UploadGetFile):
            raise TypeError(f"unexpected download request: {type(request).__name__}")
        offset = int(request.offset)
        limit = int(request.limit)
        chunk = self.payload[offset : offset + limit]
        return types.UploadFile(type=types.StorageFileUnknown(), mtime=1_700_000_000, bytes=chunk)


@dataclass(slots=True)
class ConcurrentInvoker:
    """Synthetic awaitable invoker that yields once to measure pending-task scheduling.

    Attributes:
        count: Number of benchmark invocations that reached the cooperative yield.
    """

    count: int = 0

    async def __call__(self, request: object) -> object:
        """Count one invocation, cooperatively yield and return a synthetic success value.

        Args:
            request: Ignored synthetic request accepted to match an RPC invoker protocol.
        """
        self.count += 1
        await asyncio.sleep(0)
        return types.BoolTrue()


class CountingPeerBackendStorage(InMemorySessionStorage):
    """In-memory session backend instrumented to count underlying ``load`` calls."""

    def __init__(self, initial: SessionRecord) -> None:
        """Initialize the inherited record and reset the backend load counter.

        Args:
            initial: Synthetic session record returned by each in-memory backend load.
        """
        super().__init__(initial)
        self.load_count = 0

    async def load(self):
        """Count and delegate an in-memory session load."""
        self.load_count += 1
        return await super().load()


class CountingCachedPeerStorage(_CachedSessionStorage):
    """Cached storage wrapper instrumented to count wrapper-level loads."""

    def __init__(self, storage: CountingPeerBackendStorage) -> None:
        """Wrap the counting backend and reset the wrapper load counter.

        Args:
            storage: Instrumented in-memory backend delegated to by the cache wrapper.
        """
        super().__init__(storage)
        self.load_count = 0

    async def load(self):
        """Count and delegate a cached session load."""
        self.load_count += 1
        return await super().load()


def main(argv: Sequence[str] | None = None) -> int:
    """Parse command-line arguments, print event-loop metadata and run all synthetic cases.

    Args:
        argv: Optional argument sequence; only standard argparse help is accepted.

    Returns:
        Zero after every benchmark and speed gate completes.
    """
    parser = argparse.ArgumentParser(description="Benchmark representative miniproto runtime paths")
    parser.parse_args(argv)
    print(
        f"event_loop_backend={event_loop.backend_name()} "
        f"installed={event_loop.installed()} version={event_loop.backend_version()}"
    )
    return event_loop.run(_main())


async def _main() -> int:
    """Run fixed-size synthetic workloads and print their measured units and gates."""
    payload = bytes((index * 17) % 256 for index in range(8 * 1024 * 1024))
    cases = (
        AsyncBenchmarkCase("update_dispatch_10k", lambda: _bench_update_dispatch(10_000)),
        AsyncBenchmarkCase("media_upload_8m_concurrency_8", lambda: _bench_upload(payload)),
        AsyncBenchmarkCase("media_download_8m", lambda: _bench_download(payload)),
        AsyncBenchmarkCase("tl_upload_get_file_encode_10k", lambda: _bench_tl_upload_get_file_encode(10_000)),
        AsyncBenchmarkCase("tl_upload_file_decode_100", lambda: _bench_tl_upload_file_decode(100)),
    )
    for case in cases:
        result = await _run(case.name, case.func)
        print(f"{result.name}: best={result.best_ms:.3f}ms median={result.median_ms:.3f}ms runs={result.runs}")
    sender = _benchmark_sender(max_pending_rpcs=100_001)
    noop = await _run("pending_slot_noop_100k", lambda: _bench_pending_slot_noop(100_000))
    slots = await _run("pending_slot_reserve_release_100k", lambda: _bench_pending_slot_pairs(sender, 100_000))
    for result in (noop, slots):
        print(f"{result.name}: best={result.best_ms:.3f}ms median={result.median_ms:.3f}ms runs={result.runs}")
    print(
        "pending_slot_reserve_release_delta: "
        f"best_ns_per_pair={(slots.best_ms - noop.best_ms) * 1_000_000 / 100_000:.1f} "
        f"median_ns_per_pair={(slots.median_ms - noop.median_ms) * 1_000_000 / 100_000:.1f} "
        f"best_overhead_pct={(slots.best_ms / noop.best_ms - 1) * 100:.1f}% "
        f"median_overhead_pct={(slots.median_ms / noop.median_ms - 1) * 100:.1f}%"
    )
    scheduling = await _run("synthetic_pending_requests_1k", lambda: _bench_pending_requests(1_000))
    contended_sender = _benchmark_sender(max_pending_rpcs=1_000)
    contended = await _run(
        "pending_slot_held_burst_1k", lambda: _bench_pending_slot_held_burst(contended_sender, 1_000)
    )
    for result in (scheduling, contended):
        print(f"{result.name}: best={result.best_ms:.3f}ms median={result.median_ms:.3f}ms runs={result.runs}")
    print(
        "pending_slot_held_burst_delta: "
        f"best_us_per_task={(contended.best_ms - scheduling.best_ms) * 1_000 / 1_000:.3f} "
        f"median_us_per_task={(contended.median_ms - scheduling.median_ms) * 1_000 / 1_000:.3f} "
        f"best_overhead_pct={(contended.best_ms / scheduling.best_ms - 1) * 100:.1f}% "
        f"median_overhead_pct={(contended.median_ms / scheduling.median_ms - 1) * 100:.1f}%"
    )
    await _bench_peer_cache_10k()
    return 0


async def _run(name: str, func: Callable[[], Awaitable[object]], runs: int = 10) -> BenchmarkResult:
    """Measure ``runs`` complete awaits of one workload without a separate warm-up pass.

    Returns:
        Best and median wall-clock milliseconds measured with ``perf_counter``.

    Args:
        name: Stable result label for the measured workload.
        func: Zero-argument awaitable benchmark workload.
        runs: Number of complete in-process invocations; defaults to ten.
    """
    durations: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        await func()
        durations.append((time.perf_counter() - start) * 1000)
    return BenchmarkResult(name=name, runs=runs, best_ms=min(durations), median_ms=statistics.median(durations))


async def _bench_update_dispatch(count: int) -> int:
    """Measure public update queue/iterator dispatch for ``count`` synthetic updates.

    Args:
        count: Number of synthetic updates emitted and consumed without an RPC path.
    """
    manager = UpdateManager(
        ClientConfig(api_id=1, api_hash="hash", update_queue_size=count + 1), InMemorySessionStorage(), _noop_invoke
    )
    consumed = 0

    async def consume() -> None:
        """Drain exactly the benchmark's emitted updates before returning."""
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
    """Measure 8-way synthetic media upload chunking against an in-memory success invoker.

    Args:
        payload: Synthetic immutable source bytes; no file, session or live request is used.
    """
    invoker = UploadInvoker()
    result = await upload_file(
        invoker, payload, file_name="bench.bin", part_size=DEFAULT_CHUNK_SIZE, concurrency=8, file_id=123
    )
    return result.size


async def _bench_download(payload: bytes) -> int:
    """Measure synthetic file download assembly from an in-memory payload provider.

    Args:
        payload: Synthetic immutable bytes returned by the loopback file invoker.
    """
    invoker = DownloadInvoker(payload)
    location = types.InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"ref", thumb_size="")
    result = await download_file(
        invoker, location, limit=len(payload), part_size=DEFAULT_CHUNK_SIZE, total_size=len(payload)
    )
    return result.bytes_downloaded


async def _bench_tl_upload_get_file_encode(count: int) -> int:
    """Serialize one fixed ``upload.getFile`` request ``count`` times and return encoded bytes.

    Args:
        count: Fixed number of request serializations included in the local timing.
    """
    request = functions.UploadGetFile(
        precise=True,
        cdn_supported=True,
        location=types.InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"ref", thumb_size=""),
        offset=0,
        limit=DEFAULT_CHUNK_SIZE,
    )
    total = 0
    for _ in range(count):
        total += len(request.serialize())
    return total


async def _bench_tl_upload_file_decode(count: int) -> int:
    """Decode one fixed ``upload.File`` payload ``count`` times and validate each result.

    Args:
        count: Fixed number of local object decodes included in the timing.
    """
    encoded = types.UploadFile(
        type=types.StorageFileUnknown(), mtime=1_700_000_000, bytes=b"x" * DEFAULT_CHUNK_SIZE
    ).serialize()
    total = 0
    for _ in range(count):
        decoded, offset = decode_object(encoded)
        if offset != len(encoded) or not isinstance(decoded, types.UploadFile):
            raise AssertionError("upload.File decode benchmark produced an unexpected object")
        total += len(decoded.bytes)
    return total


async def _bench_pending_requests(count: int) -> int:
    """Measure cooperative scheduling of ``count`` synthetic pending invocations.

    Args:
        count: Number of in-process synthetic tasks created and awaited.
    """
    invoker = ConcurrentInvoker()
    await asyncio.gather(*(invoker(types.BoolTrue()) for _ in range(count)))
    return invoker.count


async def _bench_pending_slot_noop(count: int) -> int:
    """Measure the loop-only baseline used to isolate pending-slot pair overhead.

    Args:
        count: Number of local loop increments forming the comparison baseline.
    """
    completed = 0
    for _ in range(count):
        completed += 1
    return completed


async def _bench_pending_slot_pairs(sender: MTProtoSender, count: int) -> int:
    """Measure ``count`` reserve/release pairs and assert no pending-slot occupancy leaks.

    Args:
        sender: Never-connected loopback sender whose local pending-slot state is exercised.
        count: Number of reserve/release pairs included in the timing.
    """
    for _ in range(count):
        sender._reserve_pending_slot()
        sender._release_pending_slot()
    if sender.sender_state.pending_count != 0:
        raise AssertionError("pending slot pair benchmark leaked occupancy")
    return count


async def _bench_pending_slot_held_burst(sender: MTProtoSender, count: int) -> int:
    """Measure a burst that holds every pending slot until one shared gate opens.

    Args:
        sender: Never-connected loopback sender providing local pending-slot state.
        count: Number of synthetic tasks/slots held until the shared gate opens.
    """
    gate = asyncio.Event()

    async def hold_slot() -> None:
        """Reserve one slot until the gate opens, always releasing it on cancellation."""
        sender._reserve_pending_slot()
        try:
            await gate.wait()
        finally:
            sender._release_pending_slot()

    tasks = [asyncio.create_task(hold_slot()) for _ in range(count)]
    await asyncio.sleep(0)
    if sender.sender_state.pending_count != count:
        raise AssertionError("pending slot burst benchmark did not reserve every slot")
    gate.set()
    await asyncio.gather(*tasks)
    if sender.sender_state.pending_count != 0:
        raise AssertionError("pending slot burst benchmark leaked occupancy")
    return count


async def _bench_peer_cache_10k() -> None:
    """Benchmark a 10,000-entry peer cache against canonical scans and enforce local gates.

    Reports cold construction, warm lookup medians in nanoseconds, estimated incremental index heap and a one-entity incremental reconciliation. It asserts fixed local speed/memory/load-count thresholds; these gates intentionally depend on the executing environment.
    """
    entries = _peer_entries_10k()
    record = SessionRecord(user=UserIdentity(id=50_000, access_hash=500_000, phone="+12025559999"), peers=entries)
    backend = CountingPeerBackendStorage(record)
    storage = CountingCachedPeerStorage(backend)
    cache = PeerCache(ClientConfig(api_id=1, api_hash="hash"), storage, _noop_peer_invoke)
    user_entries = tuple(entry for entry in entries if entry.kind == "user")
    selected = (user_entries[333], user_entries[len(user_entries) // 2], user_entries[-334])
    kind_queries = tuple(Peer(id=entry.id, kind=entry.kind) for entry in selected)
    numeric_queries = tuple(entry.id for entry in selected)
    username_queries = tuple(f"@{entry.username}" for entry in selected)
    phone_queries = tuple(f"+{_normalize_phone(entry.phone)}" for entry in selected)
    cold_started = time.perf_counter_ns()
    await cache.resolve_peer(kind_queries[0])
    cold_ns = time.perf_counter_ns() - cold_started
    warm_wrapper_loads = storage.load_count
    warm_backend_loads = backend.load_count
    warm_stats = dict(cache.index_stats)
    if warm_wrapper_loads != 1 or warm_backend_loads != 1 or warm_stats["canonical_tuple_visits"] != len(entries):
        raise AssertionError("peer cache cold build did not visit/load the cached wrapper and backend exactly once")
    indexed_ns = {
        "kind": await _median_lookup_ns(cache.resolve_peer, kind_queries),
        "numeric": await _median_lookup_ns(cache.resolve_peer, numeric_queries),
        "username": await _median_lookup_ns(cache.resolve_peer, username_queries),
        "phone": await _median_lookup_ns(cache.resolve_peer, phone_queries),
    }
    baseline_ns = {
        "kind": await _median_lookup_ns(lambda query: _legacy_kind_lookup(record, query), kind_queries),
        "numeric": await _median_lookup_ns(lambda query: _legacy_numeric_lookup(record, query), numeric_queries),
        "username": await _median_lookup_ns(lambda query: _legacy_username_lookup(record, query), username_queries),
        "phone": await _median_lookup_ns(lambda query: _legacy_phone_lookup(record, query), phone_queries),
    }
    if (
        storage.load_count != warm_wrapper_loads
        or backend.load_count != warm_backend_loads
        or cache.index_stats != warm_stats
    ):
        raise AssertionError(
            "warm peer lookups reloaded the cached wrapper/backend, rebuilt or visited the canonical tuple"
        )
    ratios = {name: baseline_ns[name] / indexed_ns[name] for name in indexed_ns}
    if any(ratio < 20.0 for ratio in ratios.values()):
        raise AssertionError(f"peer cache warm lookup speed gate failed: {ratios}")
    combined_ratio = sum(baseline_ns.values()) / sum(indexed_ns.values())
    canonical_seen: set[int] = set()
    canonical_heap = _deep_size(entries, canonical_seen)
    incremental_index_heap = _deep_size(cache._index_bundle, canonical_seen)
    incremental_ratio = incremental_index_heap / canonical_heap
    total_ratio = (canonical_heap + incremental_index_heap) / canonical_heap
    if incremental_ratio >= 2.5:
        raise AssertionError(f"peer cache incremental heap gate failed: {incremental_ratio:.3f} >= 2.5")
    before_update = dict(cache.index_stats)
    update_started = time.perf_counter_ns()
    await cache.remember_raw_entities(
        types.User(id=selected[1].id, access_hash=9_999_999, username="updated-bench-user")
    )
    update_total_ns = time.perf_counter_ns() - update_started
    after_update = dict(cache.index_stats)
    if after_update["rebuilds"] != before_update["rebuilds"]:
        raise AssertionError("one-peer direct commit rebuilt the peer indexes")
    if after_update["incremental_reconciliations"] != before_update["incremental_reconciliations"] + 1:
        raise AssertionError("one-peer direct commit did not reconcile indexes incrementally")
    reconciliation_ns = after_update["incremental_reconciliation_ns"] - before_update["incremental_reconciliation_ns"]
    print(
        "peer_cache_10k: "
        f"cold_build_ms={cold_ns / 1_000_000:.3f} entries={len(entries)} "
        f"cached_wrapper_loads={warm_wrapper_loads} backend_loads={warm_backend_loads} "
        f"rebuilds={warm_stats['rebuilds']} "
        f"canonical_tuple_visits={warm_stats['canonical_tuple_visits']}"
    )
    for name in ("kind", "numeric", "username", "phone"):
        print(
            f"peer_cache_10k_{name}: indexed_ns={indexed_ns[name]:.1f} "
            f"canonical_scan_ns={baseline_ns[name]:.1f} speedup={ratios[name]:.2f}x"
        )
    print(f"peer_cache_10k_combined: speedup={combined_ratio:.2f}x")
    print(
        "peer_cache_10k_heap: "
        f"canonical_bytes={canonical_heap} incremental_index_bytes={incremental_index_heap} "
        f"incremental_ratio={incremental_ratio:.3f} total_ratio={total_ratio:.3f}"
    )
    print(
        "peer_cache_10k_update: "
        f"end_to_end_ms={update_total_ns / 1_000_000:.3f} "
        f"index_reconciliation_us={reconciliation_ns / 1_000:.3f} "
        f"rebuild_delta={after_update['rebuilds'] - before_update['rebuilds']}"
    )


def _peer_entries_10k() -> tuple[PeerCacheEntry, ...]:
    """Create a deterministic 10,000-entry mixture of synthetic users, chats and channels."""
    entries: list[PeerCacheEntry] = []
    now = datetime.now(UTC)
    for index in range(10_000):
        peer_id = index // 3 + 1
        variant = index % 3
        if variant == 0:
            entries.append(
                PeerCacheEntry(
                    id=peer_id,
                    kind="user",
                    access_hash=1_000_000 + index,
                    username=f"bench_user_{index}",
                    phone=f"+1202{index:07d}",
                    updated_at=now,
                    raw={"usernames": [f"bench_alt_{index}"], "first_name": "Benchmark"},
                )
            )
        elif variant == 1:
            entries.append(PeerCacheEntry(id=peer_id, kind="chat", raw={"title": f"Chat {index}"}))
        else:
            entries.append(
                PeerCacheEntry(
                    id=peer_id,
                    kind="channel",
                    access_hash=2_000_000 + index,
                    username=f"bench_channel_{index}",
                    updated_at=now,
                    raw={"usernames": [f"bench_channel_alt_{index}"], "title": f"Channel {index}"},
                )
            )
    return tuple(entries)


async def _median_lookup_ns(
    lookup: Callable[[Any], Awaitable[object]], queries: tuple[Any, ...], *, runs: int = 7, repeats: int = 40
) -> float:
    """Return the median nanoseconds per awaited lookup across fixed runs and repeats.

    Args:
        lookup: Awaitable lookup implementation under comparison.
        queries: Fixed queries issued in order during each repeated run.
        runs: Number of independent timing runs; defaults to seven.
        repeats: Whole query-sequence repetitions per run; defaults to forty.
    """
    durations: list[float] = []
    count = len(queries) * repeats
    for _ in range(runs):
        started = time.perf_counter_ns()
        for _repeat in range(repeats):
            for query in queries:
                await lookup(query)
        durations.append((time.perf_counter_ns() - started) / count)
    return statistics.median(durations)


async def _legacy_kind_lookup(record: SessionRecord, query: Peer) -> Peer:
    """Perform the canonical linear kind-and-ID scan used as the peer-cache baseline.

    Args:
        record: Synthetic record whose canonical peer tuple is scanned.
        query: Kind-and-ID peer key selected from the generated entries.
    """
    entry = next(entry for entry in record.peers if entry.kind == query.kind and entry.id == query.id)
    return Peer(id=entry.id, kind=entry.kind, access_hash=entry.access_hash)


async def _legacy_numeric_lookup(record: SessionRecord, query: int) -> Peer:
    """Perform the legacy numeric peer lookup and fail when its known query is absent.

    Args:
        record: Synthetic record used by the legacy lookup helper.
        query: Numeric peer identifier known to be present in the generated data.
    """
    resolved = _resolve_numeric_peer_from_record(record, query)
    if resolved is None:
        raise AssertionError("legacy numeric benchmark query missed")
    return resolved


async def _legacy_username_lookup(record: SessionRecord, query: str) -> Peer | None:
    """Perform the legacy TTL-filtered username scan used as the benchmark baseline.

    Args:
        record: Synthetic record whose peer tuple is scanned.
        query: Username query normalized before comparison.
    """
    normalized = _normalize_username(query)
    if normalized is None:
        return None
    now = datetime.now(UTC)
    for entry in record.peers:
        if now - entry.updated_at > USERNAME_CACHE_TTL:
            continue
        if _entry_has_username(entry, normalized):
            return Peer(id=entry.id, kind=entry.kind, access_hash=entry.access_hash)
    return None


async def _legacy_phone_lookup(record: SessionRecord, query: str) -> Peer:
    """Perform the legacy normalized-phone linear scan used as the benchmark baseline.

    Args:
        record: Synthetic record whose peer tuple is scanned.
        query: Phone query normalized before comparison.
    """
    normalized = _normalize_phone(query)
    entry = next(entry for entry in record.peers if _normalize_phone(entry.phone) == normalized)
    return Peer(id=entry.id, kind=entry.kind, access_hash=entry.access_hash)


def _deep_size(value: object, seen: set[int]) -> int:
    """Estimate recursively reachable heap size while charging each object identity once.

    Args:
        value: Root object/subgraph whose Python heap footprint is estimated.
        seen: Mutable identity set shared across recursive visits to avoid double charging.
    """
    object_id = id(value)
    if object_id in seen:
        return 0
    seen.add(object_id)
    size = sys.getsizeof(value)
    if is_dataclass(value) and not isinstance(value, type):
        return size + sum(_deep_size(getattr(value, item.name), seen) for item in fields(value))
    if isinstance(value, Mapping):
        return size + sum(_deep_size(key, seen) + _deep_size(item, seen) for key, item in value.items())
    if isinstance(value, tuple | list | set | frozenset):
        return size + sum(_deep_size(item, seen) for item in value)
    attributes = getattr(value, "__dict__", None)
    if isinstance(attributes, Mapping):
        size += _deep_size(attributes, seen)
    return size


async def _noop_peer_invoke(request: object) -> object:
    """Fail if a synthetic peer-cache workload unexpectedly attempts an RPC.

    Args:
        request: Unexpected raw request proving the no-network benchmark boundary was crossed.
    """
    raise AssertionError(f"unexpected peer benchmark request: {type(request).__name__}")


def _benchmark_sender(*, max_pending_rpcs: int) -> MTProtoSender:
    """Create a loopback-only sender with deterministic in-memory MTProto state.

    The sender is never connected; its synthetic auth key is benchmark data, not a usable credential.

    Args:
        max_pending_rpcs: Local pending-slot capacity used by synthetic scheduler cases.
    """
    return MTProtoSender(
        ConnectionEndpoint("127.0.0.1", 443),
        TransportConfig(),
        MTProtoState(auth_key=bytes(range(256)), server_salt=1, session_id=2),
        max_pending_rpcs=max_pending_rpcs,
    )


async def _noop_invoke(request: object) -> object:
    """Fail if the synthetic update-dispatch workload unexpectedly attempts recovery RPCs.

    Args:
        request: Unexpected raw recovery request proving the synthetic boundary was crossed.
    """
    raise AssertionError(f"unexpected update recovery request: {type(request).__name__}")


if __name__ == "__main__":
    raise SystemExit(main())
