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
    """Summarize a non-empty numeric sample using linearly interpolated percentiles."""
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
    """Collect non-secret runtime information used to interpret benchmark results."""
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
    """Build the shared machine-readable benchmark envelope."""
    if not benchmark:
        raise ValueError("benchmark must not be empty")
    if mode not in {"smoke", "full", "live", "tglib"}:
        raise ValueError("mode must be smoke, full, live, or tglib")
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
    """Write one normalized report using deterministic key ordering and UTF-8 newlines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


class LoopLagProbe:
    """Measure event-loop scheduling delay at a fixed cadence when explicitly enabled."""

    def __init__(self, *, interval_s: float = 0.01, stall_threshold_s: float = 0.005) -> None:
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
        """Start sampling; a probe instance may be started exactly once."""
        if self._task is not None:
            raise RuntimeError("loop-lag probe has already been started")
        self._task = asyncio.create_task(self._run(), name="miniproto-benchmark-loop-lag")
        await asyncio.sleep(0)

    async def stop(self) -> dict[str, Any]:
        """Stop sampling and return latency plus callback-overhead distributions."""
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
    """Advance beyond missed cadences so one stall produces one sample rather than a catch-up burst."""
    missed = max(math.floor((observed - target) / interval), 0)
    return target + (missed + 1) * interval


def _percentile(ordered: Sequence[float], quantile: float) -> float:
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _redact_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
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
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _command_output(command: tuple[str, ...]) -> str | None:
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
