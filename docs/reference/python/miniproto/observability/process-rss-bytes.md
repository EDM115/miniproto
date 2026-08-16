---
title: "miniproto.observability.process_rss_bytes"
description: "Return this process's reported RSS/working-set byte count when available."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.process_rss_bytes"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L352"
aliases: ["miniproto.process_rss_bytes"]
module: "miniproto.observability"
---

## `miniproto.observability.process_rss_bytes`

```python
process_rss_bytes() -> int | None
```

Return this process's reported RSS/working-set byte count when available.

**Returns:**

- <code>[int](#int) | None</code> – Platform-reported byte count, or ``None`` when the platform cannot provide it.
