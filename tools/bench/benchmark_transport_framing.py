"""Benchmark in-memory native and legacy MTProto transport frame decoding.

Each mode uses the same pre-fed encoded stream and compares complete batches in
wall-clock milliseconds after three warmup batches. Native and legacy timing
orders alternate each round, while payload equality and end-of-stream checks
protect comparison validity. Results are not socket, network, latency, or
cross-platform benchmarks: event-loop implementation, extension build, CPU
state and adapter choice (especially ``--raw-native``) can change them.
``--check`` is a local acceptance threshold of 2x for every measured
mode, not a universal performance guarantee.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import statistics
import sys
import time
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from miniproto import event_loop
from miniproto.connection.framing import NativeFrameCodec, PayloadFrame, native_transport_available

if __package__:
    from tools.bench.reporting import (
        build_benchmark_report,
        collect_environment,
        sample_statistics,
        write_benchmark_report,
    )
else:
    _reporting = importlib.import_module("reporting")
    build_benchmark_report = _reporting.build_benchmark_report
    collect_environment = _reporting.collect_environment
    sample_statistics = _reporting.sample_statistics
    write_benchmark_report = _reporting.write_benchmark_report

_SOCKET_READ_SIZE = 64 * 1024


class FramePump(Protocol):
    """Internal frame-decoder contract used by native and adapter benchmarks."""

    def feed_transport_data(self, data: bytes) -> Iterable[object]:
        """Accept a transport chunk and yield decoded framing events.

        Args:
            data: One raw transport chunk to feed into the frame decoder.
        """
        ...


@dataclass(frozen=True, slots=True)
class Result:
    """Per-batch native and legacy timing samples for one transport mode.

    Attributes:
        mode: Transport framing mode used for both compared implementations.
        native_ms: Retained native complete-batch durations in milliseconds.
        legacy_ms: Retained legacy complete-batch durations in milliseconds.
    """

    mode: str
    native_ms: tuple[float, ...]
    legacy_ms: tuple[float, ...]

    @property
    def native_median_ms(self) -> float:
        """Return the median native batch duration in milliseconds."""
        return statistics.median(self.native_ms)

    @property
    def legacy_median_ms(self) -> float:
        """Return the median legacy batch duration in milliseconds."""
        return statistics.median(self.legacy_ms)

    @property
    def speedup(self) -> float:
        """Return this run's legacy/native median ratio without generalizing it."""
        return self.legacy_median_ms / self.native_median_ms


def main() -> int:
    """Run validated frame-pump comparisons and emit their JSON report.

    ``--frames`` counts complete payloads per timed batch, ``--rounds`` supplies
    one sample per side per mode and durations are milliseconds per batch.
    ``--check`` fails below the project-local 2x target; invalid input, missing
    native transport support or decoding mismatch also fails rather than
    reporting an incomparable result.
    """
    parser = argparse.ArgumentParser(
        description="Benchmark the warmed native MTProto frame pump against the former readexactly socket path"
    )
    parser.add_argument(
        "--frames", type=int, default=4096, help="transport frames processed per timed round; defaults to 4096"
    )
    parser.add_argument(
        "--payload-bytes",
        type=int,
        default=72,
        help="encrypted-frame payload bytes; must be at least 40 and congruent to 8 modulo 16",
    )
    parser.add_argument(
        "--rounds", type=int, default=10, help="timed samples collected per implementation; defaults to 10"
    )
    parser.add_argument(
        "--mode",
        choices=("smoke", "full"),
        default="full",
        help="workload size; smoke caps frames and rounds while full uses the supplied values",
    )
    parser.add_argument(
        "--raw-native", action="store_true", help="diagnose the Rust/PyO3 boundary without adapter objects"
    )
    parser.add_argument("--json", type=Path, help="write the normalized report to this path")
    parser.add_argument("--check", action="store_true", help="fail unless every mode reaches the 2x target")
    args = parser.parse_args()
    if not native_transport_available():
        raise RuntimeError("native transport frame codec is unavailable")
    if args.payload_bytes < 40 or args.payload_bytes % 16 != 8:
        raise ValueError("payload-bytes must be at least 40 and congruent to 8 modulo 16")
    if args.frames <= 0 or args.rounds <= 0:
        raise ValueError("frames and rounds must be positive")

    payload = b"x" * args.payload_bytes
    results, loop_backend = event_loop.run(
        _benchmark_all(payload, frames=args.frames, rounds=args.rounds, raw_native=args.raw_native)
    )
    environment = collect_environment()
    environment["benchmark_event_loop"] = loop_backend
    mode_results = [
        {
            "name": result.mode,
            "legacy_max_batch_ms": max(result.legacy_ms),
            "native_median_ms": result.native_median_ms,
            "native_max_batch_ms": max(result.native_ms),
            "native_ms": list(result.native_ms),
            "native_statistics_ms": sample_statistics(result.native_ms),
            "native_frames_per_second": args.frames / max(result.native_median_ms / 1000, 1e-9),
            "legacy_median_ms": result.legacy_median_ms,
            "legacy_ms": list(result.legacy_ms),
            "legacy_statistics_ms": sample_statistics(result.legacy_ms),
            "legacy_frames_per_second": args.frames / max(result.legacy_median_ms / 1000, 1e-9),
            "speedup": result.speedup,
        }
        for result in results
    ]
    report = build_benchmark_report(
        benchmark="transport_frame_pump",
        mode=args.mode,
        warmup=3,
        samples=tuple(duration for result in results for duration in result.native_ms),
        unit="ms",
        configuration={
            "frames": args.frames,
            "payload_bytes": args.payload_bytes,
            "rounds": args.rounds,
            "raw_native": args.raw_native,
        },
        environment=environment,
        throughput={"unit": "frames_per_second"},
        results=mode_results,
    )
    json.dump(report, sys.stdout, indent=2)
    print()
    if args.json is not None:
        write_benchmark_report(args.json, report)
    if args.check:
        below_target = tuple(result for result in results if result.speedup < 2.0)
        if below_target:
            rendered = ", ".join(f"{result.mode}={result.speedup:.2f}x" for result in below_target)
            raise RuntimeError(f"native socket frame pump missed the 2x target: {rendered}")
    return 0


async def _benchmark_all(
    payload: bytes, *, frames: int, rounds: int, raw_native: bool
) -> tuple[tuple[Result, ...], str]:
    """Benchmark each supported mode and return its running event-loop identity.

    Args:
        payload: Fixed decoded payload bytes placed in every test frame.
        frames: Positive number of payload frames per timed batch.
        rounds: Positive number of retained samples per side and mode.
        raw_native: Whether to benchmark the Rust/PyO3 codec directly.
    """
    return (
        tuple(
            [
                await _benchmark_mode(mode, payload, frames=frames, rounds=rounds, raw_native=raw_native)
                for mode in ("tcp_abridged", "tcp_intermediate", "tcp_padded_intermediate")
            ]
        ),
        f"{type(asyncio.get_running_loop()).__module__}.{type(asyncio.get_running_loop()).__name__}",
    )


async def _benchmark_mode(mode: str, payload: bytes, *, frames: int, rounds: int, raw_native: bool) -> Result:
    """Warm and interleave native/legacy batches for one fixed framing mode.

    Args:
        mode: Supported TCP framing mode to encode and decode.
        payload: Fixed decoded payload bytes in every frame.
        frames: Positive number of frames in each complete batch.
        rounds: Positive number of retained samples per implementation.
        raw_native: Whether to bypass the adapter and construct Rust codec directly.
    """
    stream = _legacy_encoded_stream(mode, payload, frames)
    native: FramePump = (
        importlib.import_module("miniproto._native").TransportCodec(mode, len(payload), False)
        if raw_native
        else NativeFrameCodec(mode, max_payload_size=len(payload))
    )
    for _ in range(3):
        await _decode_native(native, _prefed_reader(stream), frames, payload)
        await _decode_legacy(mode, _prefed_reader(stream), frames, payload)
    native_durations: list[float] = []
    legacy_durations: list[float] = []
    for index in range(rounds):
        order = ("native", "legacy") if index % 2 == 0 else ("legacy", "native")
        for implementation in order:
            reader = _prefed_reader(stream)
            started = time.perf_counter()
            if implementation == "native":
                await _decode_native(native, reader, frames, payload)
                native_durations.append((time.perf_counter() - started) * 1000)
            else:
                await _decode_legacy(mode, reader, frames, payload)
                legacy_durations.append((time.perf_counter() - started) * 1000)
    return Result(mode=mode, native_ms=tuple(native_durations), legacy_ms=tuple(legacy_durations))


async def _decode_native(codec: FramePump, reader: asyncio.StreamReader, frames: int, payload: bytes) -> None:
    """Decode every native event and reject mismatch, EOF or leftovers.

    Args:
        codec: Native codec or adapter that accepts transport data chunks.
        reader: EOF-terminated in-memory stream containing the encoded batch.
        frames: Exact number of payload events required.
        payload: Expected decoded payload for each event.
    """
    events: deque[object] = deque()
    for _ in range(frames):
        while not events:
            chunk = await reader.read(_SOCKET_READ_SIZE)
            if not chunk:
                raise AssertionError("native frame pump reached EOF before decoding every frame")
            events.extend(codec.feed_transport_data(chunk))
        if _payload_from_event(events.popleft()) != payload:
            raise AssertionError("native frame pump benchmark decoded different output")
    if events or await reader.read(1):
        raise AssertionError("native frame pump benchmark left unread output")


async def _decode_legacy(mode: str, reader: asyncio.StreamReader, frames: int, payload: bytes) -> None:
    """Decode every legacy-framed payload and reject mismatch or leftovers.

    Args:
        mode: TCP framing mode that selects legacy header decoding.
        reader: EOF-terminated in-memory stream containing the encoded batch.
        frames: Exact number of payloads required.
        payload: Expected decoded payload for every frame.
    """
    for _ in range(frames):
        if mode == "tcp_abridged":
            decoded = await _read_legacy_abridged(reader)
        else:
            length = int.from_bytes(await reader.readexactly(4), "little", signed=True)
            if length < 0:
                raise AssertionError("legacy benchmark unexpectedly decoded a transport error")
            decoded = await reader.readexactly(length)
        if decoded != payload:
            raise AssertionError("legacy transport benchmark decoded different output")
    if await reader.read(1):
        raise AssertionError("legacy transport benchmark left unread output")


async def _read_legacy_abridged(reader: asyncio.StreamReader) -> bytes:
    """Read one abridged legacy frame, including its short or extended header.

    Args:
        reader: Stream positioned at an abridged frame header.
    """
    first = await reader.readexactly(1)
    if first[0] < 0x7F:
        payload_length = first[0] * 4
        prefix = await reader.readexactly(3) if payload_length >= 3 else b""
        return prefix + await reader.readexactly(payload_length - len(prefix))
    words = int.from_bytes(await reader.readexactly(3), "little")
    return await reader.readexactly(words * 4)


def _legacy_encoded_stream(mode: str, payload: bytes, frames: int) -> bytes:
    """Build the deterministic pre-fed legacy byte stream for a timed batch.

    Args:
        mode: TCP framing mode whose header encoding is used.
        payload: Bytes placed in every frame.
        frames: Number of repeated header-and-payload frames to produce.
    """
    if mode == "tcp_abridged":
        words = len(payload) // 4
        if len(payload) % 4:
            raise ValueError("abridged benchmark payload must be divisible by four")
        header = bytes([words]) if words < 0x7F else b"\x7f" + words.to_bytes(3, "little")
    else:
        header = len(payload).to_bytes(4, "little", signed=True)
    return (header + payload) * frames


def _prefed_reader(stream: bytes) -> asyncio.StreamReader:
    """Return an EOF-terminated in-memory reader sized for the fixed stream.

    Args:
        stream: Complete encoded batch bytes to pre-feed before EOF.
    """
    reader = asyncio.StreamReader(limit=max(_SOCKET_READ_SIZE * 2, len(stream)))
    reader.feed_data(stream)
    reader.feed_eof()
    return reader


def _payload_from_event(event: object) -> bytes:
    """Extract one payload shape accepted from the native framing boundary.

    Args:
        event: Decoder event expected to carry one payload in a supported shape.
    """
    if isinstance(event, bytes):
        return event
    if isinstance(event, PayloadFrame):
        return event.payload
    if isinstance(event, tuple) and len(event) == 4 and event[0] == 0 and isinstance(event[1], bytes):
        return event[1]
    raise AssertionError("native frame pump benchmark decoded a non-payload event")


if __name__ == "__main__":
    raise SystemExit(main())
