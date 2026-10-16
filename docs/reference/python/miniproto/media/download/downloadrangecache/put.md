---
title: "miniproto.media.download.DownloadRangeCache.put"
description: "Store a non-empty fitting range and evict least-recently-used entries."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.DownloadRangeCache.put"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L259"
aliases: ["miniproto.media.DownloadRangeCache.put"]
module: "miniproto.media.download"
---

## `miniproto.media.download.DownloadRangeCache.put`

```python
put(key: str, offset: int, limit: int, payload: bytes) -> None
```

Store a non-empty fitting range and evict least-recently-used entries.

**Parameters:**

- **key** (<code>[str](#str)</code>) – Stable media identity partitioning cache entries.
- **offset** (<code>[int](#int)</code>) – Exact starting byte offset represented by ``payload``.
- **limit** (<code>[int](#int)</code>) – Wire request length associated with the cache key.
- **payload** (<code>[bytes](#bytes)</code>) – Non-empty response bytes, oversized payloads are skipped and buffers are not zeroized.
