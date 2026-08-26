---
title: "miniproto.observability.MemoryMonitor.finish"
description: "Capture the final snapshot and summarize the monitored interval."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.MemoryMonitor.finish"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L191"
aliases: ["miniproto.MemoryMonitor.finish"]
module: "miniproto.observability"
---

## `miniproto.observability.MemoryMonitor.finish`

```python
finish() -> MemoryDelta
```

Capture the final snapshot and summarize the monitored interval.

**Returns:**

- <code>[MemoryDelta](#miniproto.observability.MemoryDelta)</code> – Start, end and highest-observed snapshot data.
