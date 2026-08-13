from __future__ import annotations

import argparse
import json
import platform
import statistics
import time
from dataclasses import dataclass

from miniproto.raw import functions, types
from miniproto.tl import fast


@dataclass(frozen=True, slots=True)
class Result:
    native_ms: tuple[float, ...]
    fallback_ms: tuple[float, ...]

    @property
    def native_median_ms(self) -> float:
        return statistics.median(self.native_ms)

    @property
    def fallback_median_ms(self) -> float:
        return statistics.median(self.fallback_ms)

    @property
    def speedup(self) -> float:
        return self.fallback_median_ms / self.native_median_ms


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark the generated Rust TL hot-constructor mix")
    parser.add_argument("--iterations", type=int, default=32)
    parser.add_argument("--payload-bytes", type=int, default=256 * 1024)
    parser.add_argument("--rounds", type=int, default=10)
    parser.add_argument("--check", action="store_true", help="fail unless the representative mix reaches 1.5x")
    args = parser.parse_args()
    if not fast.native_fast_paths_available():
        raise RuntimeError("native generated TL fast paths are unavailable")
    if args.iterations <= 0 or args.payload_bytes <= 0 or args.rounds <= 0:
        raise ValueError("iterations, payload-bytes, and rounds must be positive")

    result = _benchmark(iterations=args.iterations, payload_bytes=args.payload_bytes, rounds=args.rounds)
    report = {
        "benchmark": "generated_tl_hot_mix",
        "environment": {
            "machine": platform.machine(),
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
        "iterations": args.iterations,
        "payload_bytes": args.payload_bytes,
        "rounds": args.rounds,
        "native_ms": list(result.native_ms),
        "fallback_ms": list(result.fallback_ms),
        "native_median_ms": result.native_median_ms,
        "fallback_median_ms": result.fallback_median_ms,
        "speedup": result.speedup,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.check and result.speedup < 1.5:
        raise RuntimeError(f"generated TL hot mix missed the 1.5x target: {result.speedup:.2f}x")
    return 0


def _benchmark(*, iterations: int, payload_bytes: int, rounds: int) -> Result:
    payload = bytes(index & 0xFF for index in range(payload_bytes))
    location = types.InputDocumentFileLocation(
        id=123, access_hash=-456, file_reference=b"file-reference", thumb_size=""
    )
    upload_part = functions.UploadSaveBigFilePart(file_id=123456789, file_part=7, file_total_parts=4096, bytes=payload)
    get_file = functions.UploadGetFile(
        precise=True, cdn_supported=True, location=location, offset=1 << 40, limit=512 * 1024
    )
    file_hash = types.FileHash(offset=1 << 40, limit=512 * 1024, hash=b"h" * 32)
    cdn_file = types.UploadCdnFile(bytes=payload)
    encoded_hash = file_hash.serialize()
    encoded_cdn = cdn_file.serialize()
    native_encode = fast._native_encode
    native_decode = fast._native_decode

    def run_batch(*, native: bool) -> int:
        fast._native_encode = native_encode if native else None
        fast._native_decode = native_decode if native else None
        checksum = 0
        for _ in range(iterations):
            checksum += len(upload_part.serialize())
            checksum += len(get_file.serialize())
            checksum += types.FileHash.deserialize(encoded_hash).limit
            checksum += len(types.UploadCdnFile.deserialize(encoded_cdn).bytes)
        return checksum

    try:
        expected = run_batch(native=False)
        if run_batch(native=True) != expected:
            raise AssertionError("native and fallback TL benchmark mixes produced different output")
        for _ in range(3):
            run_batch(native=True)
            run_batch(native=False)
        native_durations: list[float] = []
        fallback_durations: list[float] = []
        for index in range(rounds):
            order = (True, False) if index % 2 == 0 else (False, True)
            for native in order:
                started = time.perf_counter()
                if run_batch(native=native) != expected:
                    raise AssertionError("TL benchmark checksum changed")
                duration = (time.perf_counter() - started) * 1000
                (native_durations if native else fallback_durations).append(duration)
    finally:
        fast._native_encode = native_encode
        fast._native_decode = native_decode
    return Result(native_ms=tuple(native_durations), fallback_ms=tuple(fallback_durations))


if __name__ == "__main__":
    raise SystemExit(main())
