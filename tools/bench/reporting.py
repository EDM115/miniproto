"""Normalized benchmark reporting with recursive configuration redaction and loop-lag sampling.

Reports retain measurements in their declared units. Configuration keys whose
names indicate credentials or personal identifiers are replaced recursively;
callers must still avoid placing secrets in free-form values or result text.
Loop lag measures event-loop scheduling delay and probe callback overhead, not
network latency, transfer duration or application throughput.
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.metadata
import json
import math
import os
import platform
import statistics
import subprocess
import time
from collections.abc import Mapping, Sequence
from contextlib import suppress
from pathlib import Path
from typing import Any

from miniproto import event_loop

BENCHMARK_SCHEMA = "miniproto.benchmark.v1"
_SECRET_KEY_PARTS = ("api_hash", "auth_key", "file_id", "password", "phone", "secret", "session", "token")


def sample_statistics(samples: Sequence[float]) -> dict[str, float | int]:
    """Summarize finite numeric samples in their caller-declared unit.

    Args:
        samples: Non-empty finite measurements, such as seconds, milliseconds or bytes.

    Returns:
        Count, extrema, mean, median and linearly interpolated p50/p95/p99 values.
        No unit conversion occurs.

    Raises:
        ValueError: ``samples`` is empty or contains a non-finite value.
    """
    if not samples:
        raise ValueError("samples must not be empty")
    ordered = sorted(float(sample) for sample in samples)
    if not all(math.isfinite(sample) for sample in ordered):
        raise ValueError("samples must be finite")
    return {
        "count": len(ordered),
        "min": ordered[0],
        "max": ordered[-1],
        "mean": statistics.fmean(ordered),
        "median": statistics.median(ordered),
        "p50": _percentile(ordered, 0.50),
        "p95": _percentile(ordered, 0.95),
        "p99": _percentile(ordered, 0.99),
    }


def collect_environment() -> dict[str, Any]:
    """Collect non-secret local runtime evidence used to interpret benchmark results.

    Returns:
        Package/native availability, platform, interpreter, tool, Git and event-loop
        metadata. Missing commands and distributions are represented by ``None``.

    Evidence Limits:
        This is contextual metadata only. It does not prove clean-tree state,
        native correctness, live connectivity or that a benchmark is comparable
        across machines.
    """
    native_version: str | None = None
    native_available = False
    try:
        native = importlib.import_module("miniproto._native")
    except ImportError:
        pass
    else:
        native_available = True
        candidate = getattr(native, "__version__", None)
        native_version = candidate if isinstance(candidate, str) else _distribution_version("miniproto")
    return {
        "package_version": _distribution_version("miniproto"),
        "native_available": native_available,
        "native_version": native_version,
        "commit": _command_output(("git", "rev-parse", "HEAD")),
        "dirty": bool(_command_output(("git", "status", "--porcelain"))),
        "os": platform.platform(),
        "cpu": platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER") or platform.machine(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "rust": _command_output(("rustc", "--version")),
        "event_loop": {
            "backend": event_loop.backend_name(),
            "installed": event_loop.installed(),
            "version": event_loop.backend_version(),
        },
    }


def build_benchmark_report(
    *,
    benchmark: str,
    mode: str,
    warmup: int,
    samples: Sequence[float],
    unit: str,
    configuration: Mapping[str, Any],
    environment: Mapping[str, Any] | None = None,
    throughput: Mapping[str, Any] | None = None,
    rss: Mapping[str, Any] | None = None,
    loop_lag: Mapping[str, Any] | None = None,
    failures: Sequence[Mapping[str, Any]] = (),
    results: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Build the shared machine-readable benchmark envelope with key-based redaction.

    Args:
        benchmark: Non-empty benchmark identifier.
        mode: Supported execution mode: ``smoke``, ``full`` or ``live``.
        warmup: Number of excluded warmup iterations.
        samples: Measurement values expressed in ``unit``.
        unit: Unit label applied to every sample and statistic without conversion.
        configuration: Settings recursively redacted when a mapping key appears secret-bearing.
        environment: Optional non-secret environment evidence; collected when omitted.
        throughput: Optional derived throughput values with caller-specified key units.
        rss: Optional resident-memory values with caller-specified key units.
        loop_lag: Optional event-loop scheduling probe results; distinct from workload latency.
        failures: Optional serializable failure records.
        results: Optional serializable benchmark-specific records.

    Returns:
        A JSON-compatible schema-v1 envelope. Secret-looking configuration keys
        become ``<redacted>``; arbitrary non-configuration values are normalized,
        not automatically scrubbed.

    Raises:
        ValueError: ``benchmark`` is empty, mode is unsupported or ``warmup`` is negative.
    """
    if not benchmark:
        raise ValueError("benchmark must not be empty")
    if mode not in {"smoke", "full", "live"}:
        raise ValueError("mode must be smoke, full or live")
    if warmup < 0:
        raise ValueError("warmup must be non-negative")
    normalized_samples = [float(sample) for sample in samples]
    report: dict[str, Any] = {
        "schema": BENCHMARK_SCHEMA,
        "benchmark": benchmark,
        "mode": mode,
        "environment": _json_value(dict(environment) if environment is not None else collect_environment()),
        "configuration": _redact_mapping(configuration),
        "warmup": warmup,
        "sample_unit": unit,
        "samples": normalized_samples,
        "statistics": sample_statistics(normalized_samples) if normalized_samples else None,
        "throughput": _json_value(dict(throughput or {})),
        "rss": _json_value(dict(rss or {})),
        "loop_lag": _json_value(dict(loop_lag or {"enabled": False, "samples": 0})),
        "failures": [_json_value(dict(failure)) for failure in failures],
        "results": [_json_value(dict(result)) for result in results],
    }
    return report


def write_benchmark_report(path: Path, report: Mapping[str, Any]) -> None:
    """Write a normalized report with deterministic keys and UTF-8 LF newlines.

    Args:
        path: Destination JSON file; missing parent directories are created.
        report: JSON-compatible normalized report mapping.

    Raises:
        OSError: The report path cannot be created or written.

    Redaction:
        This writer does not redact independently; callers should use
        :func:`build_benchmark_report` before persisting untrusted configuration.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


class LoopLagProbe:
    """Measure event-loop scheduling delay and callback overhead at a fixed cadence.

    Args:
        interval_s: Requested probe cadence in seconds; defaults to 10 ms.
        stall_threshold_s: Delay above which a sample is counted as a stall; defaults to 5 ms.

    Semantics:
        Each sample is non-negative delay from its scheduled loop-time target,
        measured in milliseconds. Missed cadences collapse into one subsequent
        sample, preventing catch-up bursts from inflating the distribution.
    """

    def __init__(self, *, interval_s: float = 0.01, stall_threshold_s: float = 0.005) -> None:
        """Validate cadence thresholds and initialize a single-use stopped probe.

        Args:
            interval_s: Positive requested scheduling cadence in seconds.
            stall_threshold_s: Non-negative delay threshold in seconds used for stall counts.

        Raises:
            ValueError: ``interval_s`` is non-positive or ``stall_threshold_s`` is negative.
        """
        if interval_s <= 0:
            raise ValueError("interval_s must be positive")
        if stall_threshold_s < 0:
            raise ValueError("stall_threshold_s must be non-negative")
        self._interval_s = interval_s
        self._stall_threshold_s = stall_threshold_s
        self._stop = asyncio.Event()
        self._task: asyncio.Task[None] | None = None
        self._delays_ms: list[float] = []
        self._overhead_ns: list[float] = []
        self._report: dict[str, Any] | None = None

    async def start(self) -> None:
        """Start asynchronous sampling; a probe instance may be started exactly once.

        Raises:
            RuntimeError: The probe has already been started.
        """
        if self._task is not None:
            raise RuntimeError("loop-lag probe has already been started")
        self._task = asyncio.create_task(self._run(), name="miniproto-benchmark-loop-lag")
        await asyncio.sleep(0)

    async def stop(self) -> dict[str, Any]:
        """Stop sampling and return scheduling-delay plus probe-overhead distributions.

        Returns:
            A copy with delay percentiles in milliseconds and callback overhead
            in nanoseconds; it never claims network or workload latency.

        Raises:
            RuntimeError: The probe was never started.
            asyncio.CancelledError: Awaiting the probe task is cancelled.
        """
        if self._task is None:
            raise RuntimeError("loop-lag probe has not been started")
        if self._report is not None:
            return dict(self._report)
        self._stop.set()
        await self._task
        stats = sample_statistics(self._delays_ms) if self._delays_ms else None
        self._report = {
            "enabled": True,
            "interval_ms": self._interval_s * 1000,
            "stall_threshold_ms": self._stall_threshold_s * 1000,
            "samples": len(self._delays_ms),
            "max_ms": stats["max"] if stats is not None else 0.0,
            "p50_ms": stats["p50"] if stats is not None else 0.0,
            "p95_ms": stats["p95"] if stats is not None else 0.0,
            "p99_ms": stats["p99"] if stats is not None else 0.0,
            "stalls_over_threshold": sum(delay > self._stall_threshold_s * 1000 for delay in self._delays_ms),
            "callback_overhead_ns": sample_statistics(self._overhead_ns) if self._overhead_ns else {"count": 0},
        }
        return dict(self._report)

    async def _run(self) -> None:
        """Sample scheduled loop-time delay until stop, skipping missed cadence catch-up."""
        loop = asyncio.get_running_loop()
        target = loop.time() + self._interval_s
        while not self._stop.is_set():
            timeout = max(target - loop.time(), 0.0)
            with suppress(TimeoutError):
                await asyncio.wait_for(self._stop.wait(), timeout=timeout)
            if self._stop.is_set():
                return
            started_ns = time.perf_counter_ns()
            self._delays_ms.append(max(loop.time() - target, 0.0) * 1000)
            self._overhead_ns.append(float(time.perf_counter_ns() - started_ns))
            target = _advance_probe_target(target=target, observed=loop.time(), interval=self._interval_s)


def _advance_probe_target(*, target: float, observed: float, interval: float) -> float:
    """Advance beyond missed cadences so one stall produces one sample rather than a catch-up burst.

    Args:
        target: Previously scheduled event-loop time in seconds.
        observed: Current observed event-loop time in seconds.
        interval: Requested cadence in seconds.
    """
    missed = max(math.floor((observed - target) / interval), 0)
    return target + (missed + 1) * interval


def _percentile(ordered: Sequence[float], quantile: float) -> float:
    """Interpolate a percentile from an already sorted non-empty numeric sequence.

    Args:
        ordered: Non-empty sample values sorted in ascending caller-declared units.
        quantile: Desired percentile from zero through one.
    """
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _redact_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively redact values whose mapping keys contain configured secret fragments.

    Args:
        value: Configuration mapping to normalize and redact by key name.
    """
    redacted: dict[str, Any] = {}
    for key in sorted(value):
        item = value[key]
        lowered = key.casefold()
        if any(secret in lowered for secret in _SECRET_KEY_PARTS):
            redacted[key] = "<redacted>"
        elif isinstance(item, Mapping):
            redacted[key] = _redact_mapping(item)
        else:
            redacted[key] = _json_value(item)
    return redacted


def _json_value(value: Any) -> Any:
    """Convert nested report values to stable JSON-compatible primitives.

    Args:
        value: Nested report value to normalize without independent redaction.
    """
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [_json_value(item) for item in value]
    return str(value)


def _distribution_version(name: str) -> str | None:
    """Return an installed distribution version or ``None`` when it is absent.

    Args:
        name: Installed Python distribution name to query.
    """
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _command_output(command: tuple[str, ...]) -> str | None:
    """Run one fixed diagnostic subprocess for at most five seconds and return stdout only.

    Args:
        command: Fixed diagnostic executable and arguments, never shell text.
    """
    try:
        completed = subprocess.run(  # noqa: S603 - callers pass fixed diagnostic commands only
            command, check=False, capture_output=True, text=True, timeout=5
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = completed.stdout.strip()
    return output if completed.returncode == 0 and output else None


__all__ = [
    "BENCHMARK_SCHEMA",
    "LoopLagProbe",
    "build_benchmark_report",
    "collect_environment",
    "sample_statistics",
    "write_benchmark_report",
]
