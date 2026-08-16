---
title: "miniproto.observability.record_metric"
description: "Record a metric through the configured sink, suppressing sink failures."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.record_metric"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L316"
aliases: ["miniproto.record_metric"]
module: "miniproto.observability"
---

## `miniproto.observability.record_metric`

```python
record_metric(name: str, value: float, *, unit: str = 'count', attributes: Mapping[str, object] | None = None) -> None
```

Record a metric through the configured sink, suppressing sink failures.

**Parameters:**

- **name** (<code>[str](#str)</code>) – Metric name.
- **value** (<code>[float](#float)</code>) – Numeric measurement.
- **unit** (<code>[str](#str)</code>) – Unit label, defaulting to ``"count"``.
- **attributes** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [object](#object)] | None</code>) – Optional metric dimensions.
