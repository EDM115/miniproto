"""Structured logging, lightweight metrics and process-memory observation helpers."""

from __future__ import annotations

import ctypes
import gc
import json
import logging
import os
import sys
import time
import tracemalloc
from collections.abc import Mapping
from contextlib import suppress
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Literal, Protocol, TextIO

from miniproto.security.redaction import redact_mapping, redact_text

LogFormat = Literal["text", "json"]

_LOGGER_NAME = "miniproto"
_METRICS_SINK: MetricsSink | None = None


class MetricsSink(Protocol):
    """Protocol implemented by destinations that accept metric events."""

    def record_metric(
        self, name: str, value: float, *, unit: str = "count", attributes: Mapping[str, object] | None = None
    ) -> None:
        """Accept one metric measurement from miniproto.

        Args:
            name: Metric name.
            value: Numeric measurement.
            unit: Unit label, defaulting to ``"count"``.
            attributes: Optional metric dimensions.
        """


@dataclass(frozen=True, slots=True)
class MetricEvent:
    """Immutable metric event recorded with a unit, attributes and wall-clock timestamp.

    Attributes:
        name: Metric name.
        value: Numeric measurement.
        unit: Unit label, defaulting to ``"count"``.
        attributes: Immutable-by-convention metric dimensions copied at record time.
        timestamp: Wall-clock record time in seconds since the epoch.
    """

    name: str
    value: float
    unit: str = "count"
    attributes: Mapping[str, object] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass(slots=True)
class InMemoryMetrics:
    """Simple in-memory ``MetricsSink`` useful for tests and local diagnostics.

    Attributes:
        events: Recorded metric events in insertion order.
    """

    events: list[MetricEvent] = field(default_factory=list)

    def record_metric(
        self, name: str, value: float, *, unit: str = "count", attributes: Mapping[str, object] | None = None
    ) -> None:
        """Append one metric event to this sink.

        Args:
            name: Metric name.
            value: Numeric measurement.
            unit: Unit label, defaulting to ``"count"``.
            attributes: Optional metric dimensions copied into the event.
        """
        self.events.append(MetricEvent(name=name, value=value, unit=unit, attributes=dict(attributes or {})))


@dataclass(frozen=True, slots=True)
class ResourceSnapshot:
    """Point-in-time process and tracemalloc memory counters.

    Attributes:
        timestamp: Wall-clock capture time in seconds since the epoch.
        rss_bytes: Reported RSS on Windows or macOS or lifetime peak RSS on Unix; ``None`` if unavailable.
        traced_current_bytes: Current tracemalloc allocation bytes, if tracing.
        traced_peak_bytes: Peak tracemalloc allocation bytes, if tracing.
        gc_objects: Number of objects tracked by the garbage collector.
    """

    timestamp: float
    rss_bytes: int | None
    traced_current_bytes: int | None
    traced_peak_bytes: int | None
    gc_objects: int


@dataclass(frozen=True, slots=True)
class MemoryDelta:
    """Start, end and peak resource snapshots for one monitored interval.

    Attributes:
        start: First captured resource snapshot.
        end: Final captured resource snapshot.
        peak: Snapshot selected by reported RSS or tracemalloc peak bytes.
    """

    start: ResourceSnapshot
    end: ResourceSnapshot
    peak: ResourceSnapshot

    @property
    def rss_delta_bytes(self) -> int | None:
        """Return end minus start reported RSS or ``None`` when unavailable.

        On Unix this is growth in the process lifetime peak reported by ``getrusage``,
        rather than current resident-memory growth.
        """
        if self.start.rss_bytes is None or self.end.rss_bytes is None:
            return None
        return self.end.rss_bytes - self.start.rss_bytes

    @property
    def traced_delta_bytes(self) -> int | None:
        """Return end minus start traced allocation bytes or ``None`` when unavailable."""
        if self.start.traced_current_bytes is None or self.end.traced_current_bytes is None:
            return None
        return self.end.traced_current_bytes - self.start.traced_current_bytes

    def leak_suspected(self, *, rss_threshold_bytes: int = 64 * 1024 * 1024) -> bool:
        """Report whether reported RSS/peak-RSS growth exceeds the configured threshold.

        Args:
            rss_threshold_bytes: Strict reported-RSS growth threshold; defaults to 64 MiB.

        Returns:
            ``True`` only when both RSS snapshots exist and reported growth exceeds the threshold.
            On Unix this evaluates lifetime-peak RSS growth, not a leak diagnosis from current RSS.
        """
        delta = self.rss_delta_bytes
        return delta is not None and delta > rss_threshold_bytes


class MemoryMonitor:
    """Collect resource snapshots and optionally manage a temporary tracemalloc session.

    Attributes:
        trace_allocations: Whether :meth:`start` may enable tracemalloc.
    """

    def __init__(self, *, trace_allocations: bool = False) -> None:
        """Initialize a monitor.

        Args:
            trace_allocations: Start tracemalloc on :meth:`start` only when it is not already active.
        """
        self.trace_allocations = trace_allocations
        self._started_trace = False
        self._snapshots: list[ResourceSnapshot] = []

    def start(self) -> ResourceSnapshot:
        """Start a monitoring interval and return its initial resource snapshot.

        Returns:
            The first captured snapshot.
        """
        if self.trace_allocations and not tracemalloc.is_tracing():
            tracemalloc.start()
            self._started_trace = True
        snapshot = resource_snapshot()
        self._snapshots = [snapshot]
        return snapshot

    def sample(self) -> ResourceSnapshot:
        """Capture and retain an additional snapshot.

        Returns:
            The newly captured snapshot.
        """
        snapshot = resource_snapshot()
        self._snapshots.append(snapshot)
        return snapshot

    def finish(self) -> MemoryDelta:
        """Capture the final snapshot and summarize the monitored interval.

        Returns:
            Start, end and highest-observed snapshot data.
        """
        end = self.sample()
        if len(self._snapshots) == 1:
            return MemoryDelta(start=end, end=end, peak=end)
        peak = max(self._snapshots, key=_snapshot_peak_key)
        delta = MemoryDelta(start=self._snapshots[0], end=end, peak=peak)
        if self._started_trace:
            tracemalloc.stop()
        return delta


class StructuredFormatter(logging.Formatter):
    """Formatter that redacts structured events and optionally emits compact JSON."""

    def __init__(self, *, fmt: LogFormat = "text") -> None:
        """Initialize the formatter.

        Args:
            fmt: ``"text"`` (default) or compact ``"json"`` event output.
        """
        super().__init__()
        self.fmt = fmt

    def format(self, record: logging.LogRecord) -> str:
        """Format a record while redacting event fields and exception text.

        Args:
            record: Standard-library log record.

        Returns:
            Redacted text or compact JSON according to the configured format.
        """
        event = getattr(record, "miniproto_event", None)
        if isinstance(event, Mapping):
            payload = {
                "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                **redact_mapping(event),
            }
            if record.exc_info:
                payload["exception"] = redact_text(self.formatException(record.exc_info))
            if self.fmt == "json":
                return json.dumps(payload, sort_keys=True, separators=(",", ":"))
            fields = " ".join(f"{key}={value!r}" for key, value in payload.items())
            return fields
        return redact_text(super().format(record))


def get_logger(name: str | None = None) -> logging.Logger:
    """Return the root miniproto logger or a named child logger.

    Args:
        name: Optional child-name suffix.

    Returns:
        The requested standard-library logger.
    """
    return logging.getLogger(_LOGGER_NAME if name is None else f"{_LOGGER_NAME}.{name}")


def configure_logging(level: str | int = "INFO", *, format: LogFormat = "text", stream: TextIO | None = None) -> None:
    """Install one redacting handler on the miniproto root logger.

    Args:
        level: Logging level name or numeric level, defaulting to ``"INFO"``.
        format: Event format, either ``"text"`` (default) or ``"json"``.
        stream: Optional handler output stream; defaults to standard error.
    """
    handler = logging.StreamHandler(stream)
    handler.setFormatter(StructuredFormatter(fmt=format))
    logger = get_logger()
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False


def emit_event(logger: logging.Logger, level: int, event: str, **fields: object) -> None:
    """Emit one structured miniproto event if the level is enabled.

    Args:
        logger: Destination logger.
        level: Standard-library numeric log level.
        event: Stable event name used as the log message and event field.
        **fields: Additional fields passed to the redacting formatter.
    """
    if not logger.isEnabledFor(level):
        return
    logger.log(
        level,
        event,
        extra={
            "miniproto_event": {
                "event": event,
                "service": _LOGGER_NAME,
                "pid": current_process_id(),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform,
                **fields,
            }
        },
    )


def set_metrics_sink(sink: MetricsSink | None) -> None:
    """Set the process-global metrics destination or disable metric recording.

    Args:
        sink: Metrics sink to use; ``None`` disables the global sink.
    """
    global _METRICS_SINK
    _METRICS_SINK = sink


def get_metrics_sink() -> MetricsSink | None:
    """Return the currently configured process-global metrics sink, if any."""
    return _METRICS_SINK


def record_metric(
    name: str, value: float, *, unit: str = "count", attributes: Mapping[str, object] | None = None
) -> None:
    """Record a metric through the configured sink, suppressing sink failures.

    Args:
        name: Metric name.
        value: Numeric measurement.
        unit: Unit label, defaulting to ``"count"``.
        attributes: Optional metric dimensions.
    """
    sink = _METRICS_SINK
    if sink is not None:
        with suppress(Exception):
            sink.record_metric(name, value, unit=unit, attributes=attributes)


def resource_snapshot() -> ResourceSnapshot:
    """Capture current RSS, active tracemalloc counters and GC object count.

    Returns:
        A point-in-time resource snapshot; RSS may be unavailable on some platforms.
    """
    traced_current = None
    traced_peak = None
    if tracemalloc.is_tracing():
        traced_current, traced_peak = tracemalloc.get_traced_memory()
    return ResourceSnapshot(
        timestamp=time.time(),
        rss_bytes=process_rss_bytes(),
        traced_current_bytes=traced_current,
        traced_peak_bytes=traced_peak,
        gc_objects=len(gc.get_objects()),
    )


def process_rss_bytes() -> int | None:
    """Return this process's reported RSS/working-set byte count when available.

    Returns:
        Platform-reported byte count or ``None`` when the platform cannot provide it.
    """
    if sys.platform == "win32":
        return _windows_rss_bytes()
    try:
        import resource
    except ImportError:
        return None
    usage = resource.getrusage(resource.RUSAGE_SELF)
    multiplier = 1 if sys.platform == "darwin" else 1024
    return int(usage.ru_maxrss) * multiplier


def _windows_rss_bytes() -> int | None:
    """Read the current Windows process working set through ``psapi``."""
    from ctypes import wintypes

    class ProcessMemoryCounters(ctypes.Structure):
        """Windows ``PROCESS_MEMORY_COUNTERS`` layout used by ``GetProcessMemoryInfo``."""

        _fields_ = [
            ("cb", ctypes.c_ulong),
            ("PageFaultCount", ctypes.c_ulong),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    win_dll = getattr(ctypes, "WinDLL", None)
    if win_dll is None:
        return None
    kernel32 = win_dll("kernel32", use_last_error=True)
    psapi = win_dll("psapi", use_last_error=True)
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = (wintypes.HANDLE, ctypes.POINTER(ProcessMemoryCounters), wintypes.DWORD)
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    handle = kernel32.GetCurrentProcess()
    ok = psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb)
    if not ok:
        return None
    return int(counters.WorkingSetSize)


def _snapshot_peak_key(snapshot: ResourceSnapshot) -> int:
    """Return the preferred byte counter for selecting an interval peak snapshot.

    Args:
        snapshot: Candidate resource snapshot.
    """
    return snapshot.rss_bytes or snapshot.traced_peak_bytes or 0


def current_process_id() -> int:
    """Return the current operating-system process identifier."""
    return os.getpid()


def to_jsonable(value: object) -> object:
    """Recursively convert supported observability values into JSON-compatible shapes.

    Args:
        value: Snapshot, event, mapping, list, tuple or leaf value.

    Returns:
        Dataclasses as dictionaries, mappings with string keys, sequences as lists or the leaf unchanged.
    """
    if isinstance(value, ResourceSnapshot | MemoryDelta | MetricEvent):
        return asdict(value)
    if isinstance(value, Mapping):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [to_jsonable(item) for item in value]
    return value


__all__ = [
    "InMemoryMetrics",
    "LogFormat",
    "MemoryDelta",
    "MemoryMonitor",
    "MetricEvent",
    "MetricsSink",
    "ResourceSnapshot",
    "StructuredFormatter",
    "configure_logging",
    "current_process_id",
    "emit_event",
    "get_logger",
    "get_metrics_sink",
    "process_rss_bytes",
    "record_metric",
    "resource_snapshot",
    "set_metrics_sink",
    "to_jsonable",
]
