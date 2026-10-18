---
title: "miniproto.observability.InMemoryMetrics.record_metric"
description: "Append one metric event to this sink."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.InMemoryMetrics.record_metric"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L72"
aliases: ["miniproto.InMemoryMetrics.record_metric"]
module: "miniproto.observability"
---

## `miniproto.observability.InMemoryMetrics.record_metric`

```python
record_metric(name: str, value: float, *, unit: str = 'count', attributes: Mapping[str, object] | None = None) -> None
```

Append one metric event to this sink.

**Parameters:**

- **name** (<code>[str](#str)</code>) – Metric name.
- **value** (<code>[float](#float)</code>) – Numeric measurement.
- **unit** (<code>[str](#str)</code>) – Unit label, defaulting to ``"count"``.
- **attributes** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [object](#object)] | None</code>) – Optional metric dimensions copied into the event.
