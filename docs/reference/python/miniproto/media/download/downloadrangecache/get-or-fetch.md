---
title: "miniproto.media.download.DownloadRangeCache.get_or_fetch"
description: "Return a cached range or await one task shared by concurrent callers."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.DownloadRangeCache.get_or_fetch"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L270"
aliases: ["miniproto.media.DownloadRangeCache.get_or_fetch"]
module: "miniproto.media.download"
---

## `miniproto.media.download.DownloadRangeCache.get_or_fetch`

```python
get_or_fetch(key: str, offset: int, limit: int, fetch: Callable[[], Awaitable[bytes]]) -> bytes
```

Return a cached range or await one task shared by concurrent callers.

**Parameters:**

- **key** (<code>[str](#str)</code>) – Stable media identity partitioning cache entries.
- **offset** (<code>[int](#int)</code>) – Exact starting byte offset of the desired range.
- **limit** (<code>[int](#int)</code>) – Exact wire request length used in the cache key.
- **fetch** (<code>[Callable](#collections.abc.Callable)[[], [Awaitable](#collections.abc.Awaitable)[[bytes](#bytes)]]</code>) – Async producer called once when no cache entry or pending task exists.

<details class="cancellation-semantics" open markdown="1">
<summary>Cancellation Semantics</summary>

Each waiter shields the shared owner task, so cancelling one caller
does not cancel the producer or other waiters. Explicit cache
clearing still cancels pending producers.

</details>
