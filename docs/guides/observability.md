---
title: Observability
description: Configure redacting logs, best-effort metric sinks and resource snapshots without changing client behavior.
slug: /guides/observability
generated: false
---

# Observability

Use the package logging configuration at application startup, before client activity begins. It installs one handler on the `miniproto` root logger, clears handlers already attached to that logger and sets `propagate` to `False`. Treat this as ownership of the miniproto logging branch rather than a global logging configuration.

```python
from miniproto import MemoryMonitor, configure_logging


configure_logging("INFO", format="json")

monitor = MemoryMonitor(trace_allocations=True)
before = monitor.start()
# Run a bounded workload here.
after = monitor.finish()
```

`format="text"` is the default; `format="json"` emits compact structured records. The formatter redacts recognized secret-bearing mapping keys and key/value-like text before output. It cannot discover every secret embedded in arbitrary strings, exception messages or user-provided objects. Keep authorization material, passphrases, proxy URLs with credentials and session strings out of log fields before they reach the formatter. The [production-operation guide](./production-operation.md) has the operational credential boundary.

## Metrics are intentionally non-blocking

Use `set_metrics_sink(...)` to install the process-global sink consumed by `record_metric(...)`. A sink receives a name, numeric value, unit and optional attributes. Sink exceptions are suppressed so telemetry does not break a protocol operation. That makes a missing metric an observability incident to detect independently; it is not evidence that the operation failed or succeeded.

The process-global sink also means libraries should not replace it casually. Let the application owner choose the sink, establish allowed attributes and apply its own cardinality and retention policy. Do not place credentials or unbounded user identifiers in metric attributes merely because the formatter redacts known keys.

## Resource snapshots measure a point in time

`resource_snapshot()` records current RSS when the platform can report it, active `tracemalloc` counters when tracing is enabled and the current garbage-collector object count. `MemoryMonitor.start()` stores the first snapshot. `sample()` adds another snapshot and `finish()` returns the interval delta.

With `trace_allocations=True`, the monitor starts `tracemalloc` only when tracing was not already active; `finish()` stops tracing only if that monitor started it. This prevents a short benchmark from taking ownership away from an outer profiler. RSS may be unavailable and Unix RSS can be a lifetime peak, so an RSS increase is a signal for investigation rather than proof of a memory leak.

For useful comparisons, sample the same workload boundary, warm-up state, input size and process configuration. The [performance and benchmarks guide](./performance-and-benchmarks.md) explains the repository commands and what their output can establish.
