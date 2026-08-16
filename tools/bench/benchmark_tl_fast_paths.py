"""Benchmark a parity-checked generated TL serialization/deserialization mix.

Native and fallback runs perform the same constructor workload over a fixed
payload, with three warmup batches and alternating timing order. Durations are
milliseconds per complete batch; throughput derives from that median and the
configured batch iteration count. Native availability is required because this
is an implementation comparison. ``--check`` applies the local 1.5x
representative-mix threshold only; platform, interpreter, extension, payload,
and system state variation prevent generalized speed claims.
"""

from __future__ import annotations

import argparse
import importlib
import json
import statistics
import time
from dataclasses import dataclass
from pathlib import Path

from miniproto.raw import functions, types
from miniproto.tl import fast

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


@dataclass(frozen=True, slots=True)
class Result:
    """Per-batch native and fallback timing samples for the generated TL mix.

    Attributes:
        native_ms: Retained native complete-batch durations in milliseconds.
        fallback_ms: Retained fallback complete-batch durations in milliseconds.
    """

    native_ms: tuple[float, ...]
    fallback_ms: tuple[float, ...]

    @property
    def native_median_ms(self) -> float:
        """Return the median native batch duration in milliseconds."""
        return statistics.median(self.native_ms)

    @property
    def fallback_median_ms(self) -> float:
        """Return the median fallback batch duration in milliseconds."""
        return statistics.median(self.fallback_ms)

    @property
    def speedup(self) -> float:
        """Return this run's fallback/native median ratio without generalizing it."""
        return self.fallback_median_ms / self.native_median_ms


def main() -> int:
    """Run the generated TL mix and emit a normalized JSON comparison report.

    ``--iterations`` is complete mix executions per timed batch and ``--rounds``
    retains one native and fallback batch sample each. A missing native fast path,
    non-positive sizing input, parity failure, or a failed ``--check`` threshold
    raises instead of silently changing the comparison.
    """
    parser = argparse.ArgumentParser(description="Benchmark the generated Rust TL hot-constructor mix")
    parser.add_argument(
        "--iterations", type=int, default=32, help="hot-constructor operations per timed round; defaults to 32"
    )
    parser.add_argument(
        "--payload-bytes", type=int, default=256 * 1024, help="bytes in the benchmark payload field; defaults to 262144"
    )
    parser.add_argument(
        "--rounds", type=int, default=10, help="timed samples collected per implementation; defaults to 10"
    )
    parser.add_argument(
        "--mode",
        choices=("smoke", "full"),
        default="full",
        help="workload size; smoke caps iterations, payload, and rounds while full uses the supplied values",
    )
    parser.add_argument("--json", type=Path, help="write the normalized report to this path")
    parser.add_argument("--check", action="store_true", help="fail unless the representative mix reaches 1.5x")
    args = parser.parse_args()
    if not fast.native_fast_paths_available():
        raise RuntimeError("native generated TL fast paths are unavailable")
    if args.iterations <= 0 or args.payload_bytes <= 0 or args.rounds <= 0:
        raise ValueError("iterations, payload-bytes, and rounds must be positive")

    result = _benchmark(iterations=args.iterations, payload_bytes=args.payload_bytes, rounds=args.rounds)
    report = build_benchmark_report(
        benchmark="generated_tl_hot_mix",
        mode=args.mode,
        warmup=3,
        samples=result.native_ms,
        unit="ms",
        configuration={"iterations": args.iterations, "payload_bytes": args.payload_bytes, "rounds": args.rounds},
        environment=collect_environment(),
        throughput={
            "native_operations_per_second": args.iterations / max(result.native_median_ms / 1000, 1e-9),
            "fallback_operations_per_second": args.iterations / max(result.fallback_median_ms / 1000, 1e-9),
        },
        results=[
            {
                "name": "representative_generated_constructor_mix",
                "native_ms": list(result.native_ms),
                "native_statistics_ms": sample_statistics(result.native_ms),
                "fallback_ms": list(result.fallback_ms),
                "fallback_statistics_ms": sample_statistics(result.fallback_ms),
                "speedup": result.speedup,
            }
        ],
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.json is not None:
        write_benchmark_report(args.json, report)
    if args.check and result.speedup < 1.5:
        raise RuntimeError(f"generated TL hot mix missed the 1.5x target: {result.speedup:.2f}x")
    return 0


def _benchmark(*, iterations: int, payload_bytes: int, rounds: int) -> Result:
    """Build fixtures, prove parity, warm, then alternate timed implementation batches.

    Args:
        iterations: Positive complete constructor-mix executions per timed batch.
        payload_bytes: Positive fixed payload size used by generated raw objects.
        rounds: Positive number of retained native and fallback batch samples.
    """
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
        """Run the fixed constructor mix with native fast paths enabled or disabled.

        Args:
            native: Whether to restore captured native encoders/decoders for this batch.
        """
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
