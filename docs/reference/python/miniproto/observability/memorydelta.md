---
title: "miniproto.observability.MemoryDelta"
description: "Start, end and peak resource snapshots for one monitored interval."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.observability.MemoryDelta"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L105"
aliases: ["miniproto.MemoryDelta"]
module: "miniproto.observability"
---

## `miniproto.observability.MemoryDelta`

```python
MemoryDelta(start: ResourceSnapshot, end: ResourceSnapshot, peak: ResourceSnapshot) -> None
```

Start, end and peak resource snapshots for one monitored interval.

**Attributes:**

- [**start**](#miniproto.observability.MemoryDelta.start) (<code>[ResourceSnapshot](#miniproto.observability.ResourceSnapshot)</code>) – First captured resource snapshot.
- [**end**](#miniproto.observability.MemoryDelta.end) (<code>[ResourceSnapshot](#miniproto.observability.ResourceSnapshot)</code>) – Final captured resource snapshot.
- [**peak**](#miniproto.observability.MemoryDelta.peak) (<code>[ResourceSnapshot](#miniproto.observability.ResourceSnapshot)</code>) – Snapshot selected by reported RSS or tracemalloc peak bytes.
