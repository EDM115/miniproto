---
title: "miniproto.media.download.DownloadRangeCache.get"
description: "Return and refresh an exact cached range or ``None`` on a cache miss."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.DownloadRangeCache.get"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L229"
aliases: ["miniproto.media.DownloadRangeCache.get"]
module: "miniproto.media.download"
---

## `miniproto.media.download.DownloadRangeCache.get`

```python
get(key: str, offset: int, limit: int) -> bytes | None
```

Return and refresh an exact cached range or ``None`` on a cache miss.

**Parameters:**

- **key** (<code>[str](#str)</code>) – Stable media identity partitioning cache entries.
- **offset** (<code>[int](#int)</code>) – Exact starting byte offset of the desired range.
- **limit** (<code>[int](#int)</code>) – Exact requested byte length.
