---
title: "miniproto.observability.ResourceSnapshot"
description: "Point-in-time process and tracemalloc memory counters."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.observability.ResourceSnapshot"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L86"
aliases: ["miniproto.ResourceSnapshot"]
module: "miniproto.observability"
---

## `miniproto.observability.ResourceSnapshot`

```python
ResourceSnapshot(timestamp: float, rss_bytes: int | None, traced_current_bytes: int | None, traced_peak_bytes: int | None, gc_objects: int) -> None
```

Point-in-time process and tracemalloc memory counters.

**Attributes:**

- [**timestamp**](#miniproto.observability.ResourceSnapshot.timestamp) (<code>[float](#float)</code>) – Wall-clock capture time in seconds since the epoch.
- [**rss_bytes**](#miniproto.observability.ResourceSnapshot.rss_bytes) (<code>[int](#int) | None</code>) – Reported RSS on Windows or macOS, or lifetime peak RSS on Unix; ``None`` if unavailable.
- [**traced_current_bytes**](#miniproto.observability.ResourceSnapshot.traced_current_bytes) (<code>[int](#int) | None</code>) – Current tracemalloc allocation bytes, if tracing.
- [**traced_peak_bytes**](#miniproto.observability.ResourceSnapshot.traced_peak_bytes) (<code>[int](#int) | None</code>) – Peak tracemalloc allocation bytes, if tracing.
- [**gc_objects**](#miniproto.observability.ResourceSnapshot.gc_objects) (<code>[int](#int)</code>) – Number of objects tracked by the garbage collector.
