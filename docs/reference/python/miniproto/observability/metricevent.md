---
title: "miniproto.observability.MetricEvent"
description: "Immutable metric event recorded with a unit, attributes, and wall-clock timestamp."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.observability.MetricEvent"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L43"
aliases: ["miniproto.MetricEvent"]
module: "miniproto.observability"
---

## `miniproto.observability.MetricEvent`

```python
MetricEvent(name: str, value: float, unit: str = 'count', attributes: Mapping[str, object] = dict(), timestamp: float = time.time()) -> None
```

Immutable metric event recorded with a unit, attributes, and wall-clock timestamp.

**Attributes:**

- [**name**](#miniproto.observability.MetricEvent.name) (<code>[str](#str)</code>) – Metric name.
- [**value**](#miniproto.observability.MetricEvent.value) (<code>[float](#float)</code>) – Numeric measurement.
- [**unit**](#miniproto.observability.MetricEvent.unit) (<code>[str](#str)</code>) – Unit label, defaulting to ``"count"``.
- [**attributes**](#miniproto.observability.MetricEvent.attributes) (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [object](#object)]</code>) – Immutable-by-convention metric dimensions copied at record time.
- [**timestamp**](#miniproto.observability.MetricEvent.timestamp) (<code>[float](#float)</code>) – Wall-clock record time in seconds since the epoch.
