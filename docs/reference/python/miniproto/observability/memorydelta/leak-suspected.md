---
title: "miniproto.observability.MemoryDelta.leak_suspected"
description: "Report whether reported RSS/peak-RSS growth exceeds the configured threshold."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.MemoryDelta.leak_suspected"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L137"
aliases: ["miniproto.MemoryDelta.leak_suspected"]
module: "miniproto.observability"
---

## `miniproto.observability.MemoryDelta.leak_suspected`

```python
leak_suspected(*, rss_threshold_bytes: int = 64 * 1024 * 1024) -> bool
```

Report whether reported RSS/peak-RSS growth exceeds the configured threshold.

**Parameters:**

- **rss_threshold_bytes** (<code>[int](#int)</code>) – Strict reported-RSS growth threshold; defaults to 64 MiB.

**Returns:**

- <code>[bool](#bool)</code> – ``True`` only when both RSS snapshots exist and reported growth exceeds the threshold.
- <code>[bool](#bool)</code> – On Unix this evaluates lifetime-peak RSS growth, not a leak diagnosis from current RSS.
