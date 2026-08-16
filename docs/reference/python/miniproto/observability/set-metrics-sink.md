---
title: "miniproto.observability.set_metrics_sink"
description: "Set the process-global metrics destination, or disable metric recording."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.set_metrics_sink"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L301"
aliases: ["miniproto.set_metrics_sink"]
module: "miniproto.observability"
---

## `miniproto.observability.set_metrics_sink`

```python
set_metrics_sink(sink: MetricsSink | None) -> None
```

Set the process-global metrics destination, or disable metric recording.

**Parameters:**

- **sink** (<code>[MetricsSink](#miniproto.observability.MetricsSink) | None</code>) – Metrics sink to use; ``None`` disables the global sink.
