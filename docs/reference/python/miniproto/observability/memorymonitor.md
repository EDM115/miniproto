---
title: "miniproto.observability.MemoryMonitor"
description: "Collect resource snapshots and optionally manage a temporary tracemalloc session."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.observability.MemoryMonitor"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L151"
aliases: ["miniproto.MemoryMonitor"]
module: "miniproto.observability"
---

## `miniproto.observability.MemoryMonitor`

```python
MemoryMonitor(*, trace_allocations: bool = False) -> None
```

Collect resource snapshots and optionally manage a temporary tracemalloc session.

**Attributes:**

- [**trace_allocations**](#miniproto.observability.MemoryMonitor.trace_allocations) – Whether :meth:`start` may enable tracemalloc.

Initialize a monitor.

**Parameters:**

- **trace_allocations** (<code>[bool](#bool)</code>) – Start tracemalloc on :meth:`start` only when it is not already active.
