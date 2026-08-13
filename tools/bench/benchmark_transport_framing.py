from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import platform
import statistics
import sys
import time
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from miniproto import event_loop
from miniproto.connection.framing import NativeFrameCodec, PayloadFrame, native_transport_available

_SOCKET_READ_SIZE = 64 * 1024


class FramePump(Protocol):
    def feed_transport_data(self, data: bytes) -> Iterable[object]: ...


@dataclass(frozen=True, slots=True)
class Result:
    mode: str
    native_ms: tuple[float, ...]
    legacy_ms: tuple[float, ...]

    @property
    def native_median_ms(self) -> float:
        return statistics.median(self.native_ms)

    @property
    def legacy_median_ms(self) -> float:
        return statistics.median(self.legacy_ms)

    @property
    def speedup(self) -> float:
        return self.legacy_median_ms / self.native_median_ms


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Benchmark the warmed native MTProto frame pump against the former readexactly socket path"
    )
    parser.add_argument("--frames", type=int, default=4096)
    parser.add_argument("--payload-bytes", type=int, default=72)
    parser.add_argument("--rounds", type=int, default=10)
    parser.add_argument(
        "--raw-native", action="store_true", help="diagnose the Rust/PyO3 boundary without adapter objects"
    )
    parser.add_argument("--check", action="store_true", help="fail unless every mode reaches the 2x Wave 3 target")
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
    report = {
        "benchmark": "transport_frame_pump",
        "environment": {
            "event_loop": loop_backend,
            "machine": platform.machine(),
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
        "frames": args.frames,
        "payload_bytes": args.payload_bytes,
        "rounds": args.rounds,
        "modes": [
            {
                "mode": result.mode,
                "legacy_max_batch_ms": max(result.legacy_ms),
                "native_median_ms": result.native_median_ms,
                "native_max_batch_ms": max(result.native_ms),
                "native_ms": result.native_ms,
                "legacy_median_ms": result.legacy_median_ms,
                "legacy_ms": result.legacy_ms,
                "speedup": result.speedup,
            }
            for result in results
        ],
    }
    json.dump(report, sys.stdout, indent=2)
    print()
    if args.check:
        below_target = tuple(result for result in results if result.speedup < 2.0)
        if below_target:
            rendered = ", ".join(f"{result.mode}={result.speedup:.2f}x" for result in below_target)
            raise RuntimeError(f"native socket frame pump missed the 2x target: {rendered}")
    return 0


async def _benchmark_all(
    payload: bytes, *, frames: int, rounds: int, raw_native: bool
) -> tuple[tuple[Result, ...], str]:
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
    first = await reader.readexactly(1)
    if first[0] < 0x7F:
        payload_length = first[0] * 4
        prefix = await reader.readexactly(3) if payload_length >= 3 else b""
        return prefix + await reader.readexactly(payload_length - len(prefix))
    words = int.from_bytes(await reader.readexactly(3), "little")
    return await reader.readexactly(words * 4)


def _legacy_encoded_stream(mode: str, payload: bytes, frames: int) -> bytes:
    if mode == "tcp_abridged":
        words = len(payload) // 4
        if len(payload) % 4:
            raise ValueError("abridged benchmark payload must be divisible by four")
        header = bytes([words]) if words < 0x7F else b"\x7f" + words.to_bytes(3, "little")
    else:
        header = len(payload).to_bytes(4, "little", signed=True)
    return (header + payload) * frames


def _prefed_reader(stream: bytes) -> asyncio.StreamReader:
    reader = asyncio.StreamReader(limit=max(_SOCKET_READ_SIZE * 2, len(stream)))
    reader.feed_data(stream)
    reader.feed_eof()
    return reader


def _payload_from_event(event: object) -> bytes:
    if isinstance(event, bytes):
        return event
    if isinstance(event, PayloadFrame):
        return event.payload
    if isinstance(event, tuple) and len(event) == 4 and event[0] == 0 and isinstance(event[1], bytes):
        return event[1]
    raise AssertionError("native frame pump benchmark decoded a non-payload event")


if __name__ == "__main__":
    raise SystemExit(main())
