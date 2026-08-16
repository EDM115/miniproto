---
title: "miniproto.observability"
description: "Structured logging, lightweight metrics, and process-memory observation helpers."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.observability"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py"
module: "miniproto.observability"
---

## `miniproto.observability`

Structured logging, lightweight metrics, and process-memory observation helpers.

## Public objects

- [`LogFormat`](./logformat/) — Public attribute `miniproto.observability.LogFormat`.
- [`MetricsSink`](./metricssink/) — Protocol implemented by destinations that accept metric events.
- [`MetricEvent`](./metricevent/) — Immutable metric event recorded with a unit, attributes, and wall-clock timestamp.
- [`InMemoryMetrics`](./inmemorymetrics/) — Simple in-memory ``MetricsSink`` useful for tests and local diagnostics.
- [`ResourceSnapshot`](./resourcesnapshot/) — Point-in-time process and tracemalloc memory counters.
- [`MemoryDelta`](./memorydelta/) — Start, end, and peak resource snapshots for one monitored interval.
- [`MemoryMonitor`](./memorymonitor/) — Collect resource snapshots and optionally manage a temporary tracemalloc session.
- [`StructuredFormatter`](./structuredformatter/) — Formatter that redacts structured events and optionally emits compact JSON.
- [`get_logger`](./get-logger/) — Return the root miniproto logger or a named child logger.
- [`configure_logging`](./configure-logging/) — Install one redacting handler on the miniproto root logger.
- [`emit_event`](./emit-event/) — Emit one structured miniproto event if the level is enabled.
- [`set_metrics_sink`](./set-metrics-sink/) — Set the process-global metrics destination, or disable metric recording.
- [`get_metrics_sink`](./get-metrics-sink/) — Return the currently configured process-global metrics sink, if any.
- [`record_metric`](./record-metric/) — Record a metric through the configured sink, suppressing sink failures.
- [`resource_snapshot`](./resource-snapshot/) — Capture current RSS, active tracemalloc counters, and GC object count.
- [`process_rss_bytes`](./process-rss-bytes/) — Return this process's reported RSS/working-set byte count when available.
- [`current_process_id`](./current-process-id/) — Return the current operating-system process identifier.
- [`to_jsonable`](./to-jsonable/) — Recursively convert supported observability values into JSON-compatible shapes.
