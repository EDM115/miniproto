---
title: "miniproto.observability.process_rss_bytes"
description: "Return current Windows working set or process lifetime peak Unix RSS in bytes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.process_rss_bytes"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L353"
aliases: ["miniproto.process_rss_bytes"]
module: "miniproto.observability"
---

## `miniproto.observability.process_rss_bytes`

```python
process_rss_bytes() -> int | None
```

Return current Windows working set or process lifetime peak Unix RSS in bytes.

**Returns:**

- <code>[int](#int) | None</code> – The Windows ``WorkingSetSize`` or Unix ``ru_maxrss`` counter, including macOS, normalized to bytes. Return ``None`` when the platform cannot provide it.
