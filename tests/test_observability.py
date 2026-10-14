from __future__ import annotations

import io
import json
import logging
import tracemalloc

import pytest

from miniproto.observability import (
    InMemoryMetrics,
    MemoryMonitor,
    ResourceSnapshot,
    configure_logging,
    emit_event,
    get_logger,
    process_rss_bytes,
    record_metric,
    set_metrics_sink,
    to_jsonable,
)


def test_structured_logging_redacts_sensitive_event_fields() -> None:
    stream = io.StringIO()
    configure_logging("INFO", format="json", stream=stream)
    emit_event(get_logger("test"), logging.INFO, "auth.sample", api_hash="secret", phone="+33123456789", request="ok")
    payload = json.loads(stream.getvalue())
    assert payload["event"] == "auth.sample"
    assert payload["api_hash"] == "[redacted]"
    assert payload["phone"] == "[redacted]"
    assert payload["request"] == "ok"
    assert isinstance(payload["pid"], int)


def test_record_metric_forwards_to_configured_sink() -> None:
    sink = InMemoryMetrics()
    set_metrics_sink(sink)
    try:
        record_metric("rpc.duration", 12.5, unit="ms", attributes={"request": "help.getConfig"})
    finally:
        set_metrics_sink(None)
    assert len(sink.events) == 1
    assert sink.events[0].name == "rpc.duration"
    assert sink.events[0].value == 12.5
    assert sink.events[0].unit == "ms"
    assert sink.events[0].attributes == {"request": "help.getConfig"}


def test_record_metric_redacts_recognized_attributes_without_mutating_the_caller() -> None:
    attributes = {
        "bot_token": "synthetic bearer",
        "context": {"API_HASH": "synthetic hash", "request": "help.getConfig"},
        "detail": "password=synthetic",
    }
    sink = InMemoryMetrics()
    set_metrics_sink(sink)
    try:
        record_metric("rpc.duration", 12.5, unit="ms", attributes=attributes)
    finally:
        set_metrics_sink(None)
    assert sink.events[0].attributes == {
        "bot_token": "[redacted]",
        "context": {"API_HASH": "[redacted]", "request": "help.getConfig"},
        "detail": "password=[redacted]",
    }
    assert attributes["bot_token"] == "synthetic bearer"  # noqa: S105 - synthetic redaction input
    assert attributes["context"] == {"API_HASH": "synthetic hash", "request": "help.getConfig"}


def test_disabled_metrics_do_not_inspect_attributes() -> None:
    class UnreadableAttributes(dict[str, object]):
        def items(self):
            raise AssertionError("disabled metrics must not inspect attributes")

    set_metrics_sink(None)
    record_metric("rpc.duration", 12.5, attributes=UnreadableAttributes(request="help.getConfig"))


def test_record_metric_isolates_ordinary_sink_exceptions() -> None:
    class RaisingMetrics:
        def record_metric(self, *args: object, **kwargs: object) -> None:
            del args, kwargs
            raise RuntimeError("metrics sink failed")

    set_metrics_sink(RaisingMetrics())
    try:
        record_metric("rpc.duration", 12.5, unit="ms")
    finally:
        set_metrics_sink(None)


def test_record_metric_does_not_suppress_process_control_exceptions() -> None:
    class InterruptingMetrics:
        def record_metric(self, *args: object, **kwargs: object) -> None:
            del args, kwargs
            raise KeyboardInterrupt

    set_metrics_sink(InterruptingMetrics())
    try:
        with pytest.raises(KeyboardInterrupt):
            record_metric("rpc.duration", 12.5, unit="ms")
    finally:
        set_metrics_sink(None)


def test_memory_monitor_reports_delta_and_jsonable_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_payloads = (
        {"timestamp": 1.0, "rss_bytes": 100, "traced_current_bytes": 20, "traced_peak_bytes": 20, "gc_objects": 1},
        {"timestamp": 2.0, "rss_bytes": 700, "traced_current_bytes": 90, "traced_peak_bytes": 90, "gc_objects": 2},
        {"timestamp": 3.0, "rss_bytes": 300, "traced_current_bytes": 30, "traced_peak_bytes": 90, "gc_objects": 3},
    )
    snapshots = (
        ResourceSnapshot(timestamp=1.0, rss_bytes=100, traced_current_bytes=20, traced_peak_bytes=20, gc_objects=1),
        ResourceSnapshot(timestamp=2.0, rss_bytes=700, traced_current_bytes=90, traced_peak_bytes=90, gc_objects=2),
        ResourceSnapshot(timestamp=3.0, rss_bytes=300, traced_current_bytes=30, traced_peak_bytes=90, gc_objects=3),
    )
    remaining_snapshots = iter(snapshots)
    monkeypatch.setattr("miniproto.observability.resource_snapshot", lambda: next(remaining_snapshots))
    was_tracing = tracemalloc.is_tracing()
    monitor = MemoryMonitor(trace_allocations=True)
    try:
        start = monitor.start()
        assert tracemalloc.is_tracing()
        sample = monitor.sample()
        delta = monitor.finish()
        assert tracemalloc.is_tracing() is was_tracing
    finally:
        if not was_tracing and tracemalloc.is_tracing():
            tracemalloc.stop()
    encoded = to_jsonable(delta)
    assert start is delta.start is snapshots[0]
    assert sample is delta.peak is snapshots[1]
    assert delta.end is snapshots[2]
    assert delta.rss_delta_bytes == 200
    assert delta.traced_delta_bytes == 10
    assert not delta.leak_suspected(rss_threshold_bytes=200)
    assert delta.leak_suspected(rss_threshold_bytes=199)
    assert encoded == {"start": expected_payloads[0], "end": expected_payloads[2], "peak": expected_payloads[1]}


def test_process_rss_bytes_reports_current_process_memory() -> None:
    rss = process_rss_bytes()
    assert isinstance(rss, int)
    assert rss > 0
