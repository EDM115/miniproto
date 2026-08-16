---
title: "miniproto.media.download.DownloadRangeCache.prefetch"
description: "Schedule a bounded best-effort cached fetch without awaiting its outcome."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.DownloadRangeCache.prefetch"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L311"
aliases: ["miniproto.media.DownloadRangeCache.prefetch"]
module: "miniproto.media.download"
---

## `miniproto.media.download.DownloadRangeCache.prefetch`

```python
prefetch(key: str, offset: int, limit: int, fetch: Callable[[], Awaitable[bytes]]) -> None
```

Schedule a bounded best-effort cached fetch without awaiting its outcome.

**Parameters:**

- **key** (<code>[str](#str)</code>) – Stable media identity partitioning cache entries.
- **offset** (<code>[int](#int)</code>) – Starting byte of the speculative range.
- **limit** (<code>[int](#int)</code>) – Requested speculative range length.
- **fetch** (<code>[Callable](#collections.abc.Callable)[[], [Awaitable](#collections.abc.Awaitable)[[bytes](#bytes)]]</code>) – Async producer used if this range is not cached or pending.
