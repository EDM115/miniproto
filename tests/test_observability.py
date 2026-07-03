from __future__ import annotations

import io
import json
import logging

from miniproto.observability import (
    InMemoryMetrics,
    MemoryMonitor,
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
    emit_event(
        get_logger("test"),
        logging.INFO,
        "auth.sample",
        api_hash="secret",
        phone="+33123456789",
        request="ok",
    )
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


def test_memory_monitor_reports_delta_and_jsonable_payload() -> None:
    monitor = MemoryMonitor(trace_allocations=True)
    start = monitor.start()
    payload = bytearray(1024)
    assert payload
    sample = monitor.sample()
    delta = monitor.finish()
    encoded = to_jsonable(delta)
    assert sample.timestamp >= start.timestamp
    assert delta.end.timestamp >= delta.start.timestamp
    assert isinstance(delta.leak_suspected(), bool)
    assert isinstance(encoded, dict)
    assert "start" in encoded


def test_process_rss_bytes_reports_current_process_memory() -> None:
    rss = process_rss_bytes()
    assert isinstance(rss, int)
    assert rss > 0
