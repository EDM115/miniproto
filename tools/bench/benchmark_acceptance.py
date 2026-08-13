from __future__ import annotations

import argparse
import asyncio
import gc
import os
import time
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from tests.support.fake_mtproto import FakeMTProtoServer

from miniproto import (
    AuthKey,
    Client,
    ClientConfig,
    DCOption,
    InMemorySessionStorage,
    Media,
    SessionRecord,
    TransportConfig,
)
from miniproto.connection.sender import MTProtoSender
from miniproto.media import iter_download
from miniproto.mtproto.codec import DecodedEncryptedMessage, RpcResult
from miniproto.observability import process_rss_bytes
from miniproto.raw import functions, types
from miniproto.tl.codec import decode_object
from tools.bench.benchmark_media_scheduler import run_scheduler_benchmark
from tools.bench.benchmark_runtime_paths import (
    _bench_download,
    _bench_update_dispatch,
    _bench_upload,
    _benchmark_sender,
)
from tools.bench.reporting import (
    LoopLagProbe,
    build_benchmark_report,
    collect_environment,
    sample_statistics,
    write_benchmark_report,
)

_AUTH_KEY = b"a" * 256


@dataclass(frozen=True, slots=True)
class BenchmarkProfile:
    mode: str
    warmup: int
    samples: int
    update_count: int
    pending_count: int
    generic_tl_count: int
    media_bytes: int
    part_size: int
    scheduler_transfers: int
    scheduler_parts: int
    scheduler_max_bytes: int
    soak_cycles: int


@dataclass(slots=True)
class _BackpressureInvoker:
    payload: bytes
    active: int = 0
    max_active: int = 0
    requests: int = 0

    async def __call__(self, request: object, **kwargs: object) -> object:
        del kwargs
        if not isinstance(request, functions.UploadGetFile):
            raise TypeError(f"unexpected backpressure request: {type(request).__name__}")
        self.requests += 1
        self.active += 1
        self.max_active = max(self.max_active, self.active)
        try:
            await asyncio.sleep(0.002)
            return types.UploadFile(
                type=types.StorageFileUnknown(),
                mtime=1_700_000_000,
                bytes=self.payload[request.offset : request.offset + request.limit],
            )
        finally:
            self.active -= 1


def parse_args(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> argparse.Namespace:
    """Parse the deterministic benchmark CLI, with explicit arguments winning over environment defaults."""
    values = os.environ if env is None else env
    parser = argparse.ArgumentParser(description="Run deterministic miniproto runtime acceptance benchmarks")
    parser.add_argument("--mode", choices=("smoke", "full"), default=values.get("MINIPROTO_BENCH_MODE", "smoke"))
    parser.add_argument(
        "--samples",
        type=int,
        default=int(values["MINIPROTO_BENCH_SAMPLES"]) if values.get("MINIPROTO_BENCH_SAMPLES") else None,
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=Path(values["MINIPROTO_BENCH_JSON"]) if values.get("MINIPROTO_BENCH_JSON") else None,
    )
    loop_lag_default = values.get("MINIPROTO_BENCH_LOOP_LAG", "1") == "1"
    parser.add_argument("--loop-lag", action=argparse.BooleanOptionalAction, default=loop_lag_default)
    args = parser.parse_args(argv)
    if args.samples is not None and args.samples < 1:
        parser.error("--samples must be positive")
    return args


def resolve_profile(args: argparse.Namespace) -> BenchmarkProfile:
    """Resolve bounded smoke or statistically broader full benchmark dimensions."""
    if args.mode == "smoke":
        profile = BenchmarkProfile(
            mode="smoke",
            warmup=1,
            samples=3,
            update_count=1_000,
            pending_count=1_000,
            generic_tl_count=1_000,
            media_bytes=1024 * 1024,
            part_size=64 * 1024,
            scheduler_transfers=4,
            scheduler_parts=8,
            scheduler_max_bytes=256 * 1024,
            soak_cycles=3,
        )
    else:
        profile = BenchmarkProfile(
            mode="full",
            warmup=2,
            samples=9,
            update_count=10_000,
            pending_count=1_000,
            generic_tl_count=10_000,
            media_bytes=8 * 1024 * 1024,
            part_size=64 * 1024,
            scheduler_transfers=10,
            scheduler_parts=64,
            scheduler_max_bytes=8 * 1024 * 1024,
            soak_cycles=25,
        )
    return replace(profile, samples=args.samples) if args.samples is not None else profile


def evaluate_acceptance_invariants(results: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    """Evaluate correctness and resource-accounting thresholds without host-dependent timing limits."""
    by_name = {str(result.get("name")): result for result in results}
    failures: list[dict[str, str]] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append({"type": "AcceptanceThresholdError", "message": message})

    pending = by_name.get("pending_rpc_burst")
    if pending is not None:
        require(
            pending.get("peak") == pending.get("configured"), "pending RPC burst did not reach its configured capacity"
        )
        require(pending.get("remaining") == 0, "pending RPC burst leaked reserved slots")

    iterator = by_name.get("iterator_backpressure")
    if iterator is not None:
        require(
            int(iterator.get("max_active_requests", 0)) <= 2,
            "download iterator exceeded its two-request prefetch bound",
        )
        require(
            int(iterator.get("requests_before_close", 0)) <= 2,
            "download iterator fetched beyond its two-request backpressure window",
        )

    scheduler = by_name.get("scheduler_fairness")
    if scheduler is not None:
        require(float(scheduler.get("fairness_ratio", 0.0)) >= 0.95, "scheduler fairness ratio fell below 0.95")
        require(
            int(scheduler.get("peak_active_bytes", 0)) <= int(scheduler.get("configured_max_bytes", 0)),
            "scheduler exceeded its configured byte window",
        )
        require(int(scheduler.get("leaked_bytes", 0)) == 0, "scheduler leaked reserved bytes after cancellation")

    soak = by_name.get("reconnect_transfer_cancel_soak")
    if soak is not None:
        require(int(soak.get("pending_after", 0)) == 0, "reconnect soak left pending RPCs after disconnect")
    return failures


async def run_acceptance_benchmark(profile: BenchmarkProfile, *, probe_loop_lag: bool) -> dict[str, Any]:
    """Run the deterministic runtime, media, reconnect, memory, and scheduling acceptance set."""
    started = time.perf_counter()
    probe = LoopLagProbe(interval_s=0.005, stall_threshold_s=0.005) if probe_loop_lag else None
    if probe is not None:
        await probe.start()
    payload = bytes((index * 17) % 256 for index in range(profile.media_bytes))
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    try:
        results.append(
            await _measured_result(
                "generic_tl_roundtrip",
                lambda: _generic_tl_roundtrip(profile.generic_tl_count),
                warmup=profile.warmup,
                samples=profile.samples,
                details={"operations": profile.generic_tl_count},
            )
        )
        results.append(
            await _measured_result(
                "pending_rpc_burst",
                lambda: _pending_rpc_burst(profile.pending_count),
                warmup=profile.warmup,
                samples=profile.samples,
            )
        )
        results.append(
            await _measured_result(
                "update_dispatch",
                lambda: _bench_update_dispatch(profile.update_count),
                warmup=profile.warmup,
                samples=profile.samples,
                details={"updates": profile.update_count},
            )
        )
        results.append(
            await _measured_result(
                "media_upload",
                lambda: _bench_upload(payload),
                warmup=profile.warmup,
                samples=profile.samples,
                details={"bytes": len(payload)},
            )
        )
        results.append(
            await _measured_result(
                "media_download",
                lambda: _bench_download(payload),
                warmup=profile.warmup,
                samples=profile.samples,
                details={"bytes": len(payload)},
            )
        )
        results.append(await _iterator_backpressure(payload, profile.part_size))
        scheduler = await run_scheduler_benchmark(
            transfers=profile.scheduler_transfers,
            parts_per_transfer=profile.scheduler_parts,
            part_size=profile.part_size,
            max_bytes=profile.scheduler_max_bytes,
        )
        results.append(
            {
                "name": "scheduler_fairness",
                "duration_ms": scheduler["aggregate"]["duration_seconds"] * 1000,
                "throughput_bytes_per_second": scheduler["aggregate"]["throughput_bytes_per_second"],
                "fairness_ratio": scheduler["fairness"]["grant_ratio"],
                "peak_active_bytes": scheduler["accounting"]["peak_active_bytes"],
                "configured_max_bytes": scheduler["accounting"]["configured_max_bytes"],
                "leaked_bytes": scheduler["cancellation"]["leaked_bytes"],
            }
        )
        soak = await _reconnect_transfer_cancel_soak(profile.soak_cycles, profile.part_size)
        results.append(soak)
        failures.extend(evaluate_acceptance_invariants(results))
    except Exception as exc:
        failures.append({"type": type(exc).__name__, "message": str(exc)})
    finally:
        loop_lag = await probe.stop() if probe is not None else {"enabled": False, "samples": 0}
    total_ms = (time.perf_counter() - started) * 1000
    soak_result = next((result for result in results if result["name"] == "reconnect_transfer_cancel_soak"), {})
    return build_benchmark_report(
        benchmark="runtime_acceptance",
        mode=profile.mode,
        warmup=profile.warmup,
        samples=[total_ms],
        unit="ms",
        configuration={
            "samples": profile.samples,
            "update_count": profile.update_count,
            "pending_count": profile.pending_count,
            "generic_tl_count": profile.generic_tl_count,
            "media_bytes": profile.media_bytes,
            "part_size": profile.part_size,
            "scheduler_transfers": profile.scheduler_transfers,
            "scheduler_parts": profile.scheduler_parts,
            "scheduler_max_bytes": profile.scheduler_max_bytes,
            "soak_cycles": profile.soak_cycles,
        },
        environment=collect_environment(),
        throughput={"aggregate_cases_per_second": len(results) / max(total_ms / 1000, 1e-9)},
        rss=soak_result.get("rss", {}),
        loop_lag=loop_lag,
        failures=failures,
        results=results,
    )


async def _generic_tl_roundtrip(count: int) -> int:
    request = functions.HelpGetNearestDc()
    encoded = request.serialize()
    checksum = 0
    for _ in range(count):
        decoded, offset = decode_object(encoded)
        if offset != len(encoded) or not isinstance(decoded, functions.HelpGetNearestDc):
            raise AssertionError("generic TL benchmark produced an unexpected object")
        checksum ^= type(decoded).CONSTRUCTOR_ID
    return checksum


async def _pending_rpc_burst(count: int) -> dict[str, int]:
    sender = _benchmark_sender(max_pending_rpcs=count)
    gate = asyncio.Event()
    peak = 0

    async def hold() -> None:
        nonlocal peak
        sender._reserve_pending_slot()
        peak = max(peak, sender.sender_state.pending_count)
        try:
            await gate.wait()
        finally:
            sender._release_pending_slot()

    tasks = [asyncio.create_task(hold()) for _ in range(count)]
    await asyncio.sleep(0)
    gate.set()
    await asyncio.gather(*tasks)
    return {"configured": count, "peak": peak, "remaining": sender.sender_state.pending_count}


async def _iterator_backpressure(payload: bytes, part_size: int) -> dict[str, Any]:
    invoker = _BackpressureInvoker(payload)
    location = types.InputDocumentFileLocation(id=1, access_hash=2, file_reference=b"bench", thumb_size="")
    started = time.perf_counter()
    iterator = iter_download(
        invoker,
        location,
        limit=len(payload),
        total_size=len(payload),
        part_size=part_size,
        concurrency=8,
        max_in_flight_bytes=part_size * 2,
        adaptive_concurrency=False,
        adaptive_part_size=False,
    )
    first = await anext(iterator)
    if first != payload[:part_size]:
        raise AssertionError("iterator benchmark yielded unexpected first part")
    await asyncio.sleep(0.01)
    requests_before_close = invoker.requests
    await iterator.aclose()
    if invoker.active != 0:
        raise AssertionError("iterator benchmark left active requests")
    return {
        "name": "iterator_backpressure",
        "duration_ms": (time.perf_counter() - started) * 1000,
        "bytes_yielded": len(first),
        "max_active_requests": invoker.max_active,
        "requests_before_close": requests_before_close,
    }


async def _reconnect_transfer_cancel_soak(cycles: int, part_size: int) -> dict[str, Any]:
    rss_start = process_rss_bytes()
    rss_peak = rss_start
    objects_start = len(gc.get_objects())
    durations_ms: list[float] = []
    connections = 0
    pending_after = 0
    for cycle in range(cycles):
        started = time.perf_counter()
        cycle_result = await _reconnect_transfer_cancel_cycle(cycle, part_size)
        durations_ms.append((time.perf_counter() - started) * 1000)
        connections += cycle_result["connections"]
        pending_after += cycle_result["pending_after"]
        rss_sample = process_rss_bytes()
        if rss_sample is not None:
            rss_peak = rss_sample if rss_peak is None else max(rss_peak, rss_sample)
    gc.collect()
    rss_end = process_rss_bytes()
    return {
        "name": "reconnect_transfer_cancel_soak",
        "cycles": cycles,
        "connections": connections,
        "pending_after": pending_after,
        "samples_ms": durations_ms,
        "statistics_ms": sample_statistics(durations_ms),
        "rss": {
            "start_bytes": rss_start,
            "peak_bytes": rss_peak,
            "end_bytes": rss_end,
            "delta_bytes": rss_end - rss_start if rss_end is not None and rss_start is not None else None,
        },
        "gc_objects_delta": len(gc.get_objects()) - objects_start,
    }


async def _reconnect_transfer_cancel_cycle(cycle: int, part_size: int) -> dict[str, int]:
    payload = bytes([cycle % 251]) * (part_size * 4)
    later_started = asyncio.Event()
    release = asyncio.Event()

    async def handle(message: DecodedEncryptedMessage) -> object | None:
        if message.seq_no % 2 == 0:
            return None
        request = _decode_innermost_request(message)
        if isinstance(request, functions.HelpGetNearestDc):
            return RpcResult(req_msg_id=message.msg_id, result=types.NearestDc(country="CH", this_dc=2, nearest_dc=2))
        if isinstance(request, functions.UploadGetFile):
            if request.offset > 0:
                later_started.set()
                await release.wait()
            return RpcResult(
                req_msg_id=message.msg_id,
                result=types.UploadFile(
                    type=types.StorageFileUnknown(),
                    mtime=1_700_000_000,
                    bytes=payload[request.offset : request.offset + request.limit],
                ),
            )
        raise TypeError(f"unexpected soak request: {type(request).__name__}")

    transport = TransportConfig(
        mode="tcp_intermediate", read_timeout=2.0, reconnect_backoff_initial=0, reconnect_backoff_max=0
    )
    async with FakeMTProtoServer(_AUTH_KEY, transport, handle, drop_connections_before_packet=1) as server:
        client = Client(
            ClientConfig(api_id=1, api_hash="hash", session_storage=_fake_server_storage(server), transport=transport),
            _updates_enabled=False,
        )
        await client.connect()
        nearest = await client.invoke(functions.HelpGetNearestDc())
        if not isinstance(nearest, types.NearestDc):
            raise AssertionError("reconnect benchmark returned unexpected RPC result")
        iterator = client.iter_download(
            Media(
                id=cycle + 1,
                size=len(payload),
                location=types.InputDocumentFileLocation(
                    id=cycle + 1, access_hash=cycle + 2, file_reference=b"soak", thumb_size=""
                ),
            ),
            part_size=part_size,
            max_part_size=part_size,
            concurrency=2,
            media_lanes=0,
            adaptive_concurrency=False,
            adaptive_part_size=False,
        )
        first = await asyncio.wait_for(anext(iterator), timeout=2.0)
        if first != payload[:part_size]:
            raise AssertionError("soak iterator returned unexpected first part")
        await asyncio.wait_for(later_started.wait(), timeout=2.0)
        await iterator.aclose()
        release.set()
        await asyncio.sleep(0)
        sender = getattr(client, "_sender", None)
        await client.disconnect()
        pending = sender.sender_state.pending_count if isinstance(sender, MTProtoSender) else 0
        if server.errors:
            raise RuntimeError("fake server error during soak") from server.errors[0]
        return {"connections": server.connections_accepted, "pending_after": pending}


def _decode_innermost_request(message: DecodedEncryptedMessage) -> object:
    request, offset = decode_object(message.body)
    if offset != len(message.body):
        raise ValueError("soak request has trailing TL bytes")
    while isinstance(request, functions.InvokeWithLayer | functions.InitConnection | functions.InvokeWithoutUpdates):
        request = request.query
    return request


def _fake_server_storage(server: FakeMTProtoServer) -> InMemorySessionStorage:
    endpoint = server.endpoint
    return InMemorySessionStorage(
        SessionRecord(
            dc_id=2,
            auth_key=AuthKey(dc_id=2, key=_AUTH_KEY, key_id=123),
            dc_options=(DCOption(id=2, ip_address=endpoint.host, port=endpoint.port),),
        )
    )


async def _measured_result[T](
    name: str,
    operation: Callable[[], Awaitable[T]],
    *,
    warmup: int,
    samples: int,
    details: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    for _ in range(warmup):
        await operation()
    durations_ms: list[float] = []
    value: T | None = None
    for _ in range(samples):
        started = time.perf_counter()
        value = await operation()
        durations_ms.append((time.perf_counter() - started) * 1000)
    result: dict[str, Any] = {
        "name": name,
        "samples_ms": durations_ms,
        "statistics_ms": sample_statistics(durations_ms),
    }
    if details is not None:
        result.update(details)
    if isinstance(value, Mapping):
        result.update(value)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    profile = resolve_profile(args)
    report = asyncio.run(run_acceptance_benchmark(profile, probe_loop_lag=args.loop_lag))
    if args.json is not None:
        write_benchmark_report(args.json, report)
    print(__import__("json").dumps(report, indent=2, sort_keys=True))
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
