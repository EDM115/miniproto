---
title: "miniproto.observability.resource_snapshot"
description: "Capture current RSS, active tracemalloc counters and GC object count."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.resource_snapshot"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L333"
aliases: ["miniproto.resource_snapshot"]
module: "miniproto.observability"
---

## `miniproto.observability.resource_snapshot`

```python
resource_snapshot() -> ResourceSnapshot
```

Capture current RSS, active tracemalloc counters and GC object count.

**Returns:**

- <code>[ResourceSnapshot](#miniproto.observability.ResourceSnapshot)</code> – A point-in-time resource snapshot; RSS may be unavailable on some platforms.
