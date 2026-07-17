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
    def record_metric(
        self, name: str, value: float, *, unit: str = "count", attributes: Mapping[str, object] | None = None
    ) -> None: ...


@dataclass(frozen=True, slots=True)
class MetricEvent:
    name: str
    value: float
    unit: str = "count"
    attributes: Mapping[str, object] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass(slots=True)
class InMemoryMetrics:
    events: list[MetricEvent] = field(default_factory=list)

    def record_metric(
        self, name: str, value: float, *, unit: str = "count", attributes: Mapping[str, object] | None = None
    ) -> None:
        self.events.append(MetricEvent(name=name, value=value, unit=unit, attributes=dict(attributes or {})))


@dataclass(frozen=True, slots=True)
class ResourceSnapshot:
    timestamp: float
    rss_bytes: int | None
    traced_current_bytes: int | None
    traced_peak_bytes: int | None
    gc_objects: int


@dataclass(frozen=True, slots=True)
class MemoryDelta:
    start: ResourceSnapshot
    end: ResourceSnapshot
    peak: ResourceSnapshot

    @property
    def rss_delta_bytes(self) -> int | None:
        if self.start.rss_bytes is None or self.end.rss_bytes is None:
            return None
        return self.end.rss_bytes - self.start.rss_bytes

    @property
    def traced_delta_bytes(self) -> int | None:
        if self.start.traced_current_bytes is None or self.end.traced_current_bytes is None:
            return None
        return self.end.traced_current_bytes - self.start.traced_current_bytes

    def leak_suspected(self, *, rss_threshold_bytes: int = 64 * 1024 * 1024) -> bool:
        delta = self.rss_delta_bytes
        return delta is not None and delta > rss_threshold_bytes


class MemoryMonitor:
    def __init__(self, *, trace_allocations: bool = False) -> None:
        self.trace_allocations = trace_allocations
        self._started_trace = False
        self._snapshots: list[ResourceSnapshot] = []

    def start(self) -> ResourceSnapshot:
        if self.trace_allocations and not tracemalloc.is_tracing():
            tracemalloc.start()
            self._started_trace = True
        snapshot = resource_snapshot()
        self._snapshots = [snapshot]
        return snapshot

    def sample(self) -> ResourceSnapshot:
        snapshot = resource_snapshot()
        self._snapshots.append(snapshot)
        return snapshot

    def finish(self) -> MemoryDelta:
        end = self.sample()
        if len(self._snapshots) == 1:
            return MemoryDelta(start=end, end=end, peak=end)
        peak = max(self._snapshots, key=_snapshot_peak_key)
        delta = MemoryDelta(start=self._snapshots[0], end=end, peak=peak)
        if self._started_trace:
            tracemalloc.stop()
        return delta


class StructuredFormatter(logging.Formatter):
    def __init__(self, *, fmt: LogFormat = "text") -> None:
        super().__init__()
        self.fmt = fmt

    def format(self, record: logging.LogRecord) -> str:
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
    return logging.getLogger(_LOGGER_NAME if name is None else f"{_LOGGER_NAME}.{name}")


def configure_logging(level: str | int = "INFO", *, format: LogFormat = "text", stream: TextIO | None = None) -> None:
    handler = logging.StreamHandler(stream)
    handler.setFormatter(StructuredFormatter(fmt=format))
    logger = get_logger()
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False


def emit_event(logger: logging.Logger, level: int, event: str, **fields: object) -> None:
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
    global _METRICS_SINK
    _METRICS_SINK = sink


def get_metrics_sink() -> MetricsSink | None:
    return _METRICS_SINK


def record_metric(
    name: str, value: float, *, unit: str = "count", attributes: Mapping[str, object] | None = None
) -> None:
    sink = _METRICS_SINK
    if sink is not None:
        with suppress(Exception):
            sink.record_metric(name, value, unit=unit, attributes=attributes)


def resource_snapshot() -> ResourceSnapshot:
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
    from ctypes import wintypes

    class ProcessMemoryCounters(ctypes.Structure):
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
    return snapshot.rss_bytes or snapshot.traced_peak_bytes or 0


def current_process_id() -> int:
    return os.getpid()


def to_jsonable(value: object) -> object:
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
