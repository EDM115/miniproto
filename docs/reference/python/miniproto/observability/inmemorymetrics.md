---
title: "miniproto.observability.InMemoryMetrics"
description: "Simple in-memory ``MetricsSink`` useful for tests and local diagnostics."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.observability.InMemoryMetrics"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L62"
aliases: ["miniproto.InMemoryMetrics"]
module: "miniproto.observability"
---

## `miniproto.observability.InMemoryMetrics`

```python
InMemoryMetrics(events: list[MetricEvent] = list()) -> None
```

Simple in-memory ``MetricsSink`` useful for tests and local diagnostics.

**Attributes:**

- [**events**](#miniproto.observability.InMemoryMetrics.events) (<code>[list](#list)[[MetricEvent](#miniproto.observability.MetricEvent)]</code>) – Recorded metric events in insertion order.
