---
title: "miniproto.media.download.DownloadRangeCache"
description: "Async LRU cache that shares exact media-range fetches and limits background prefetch tasks."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.download.DownloadRangeCache"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L187"
aliases: ["miniproto.media.DownloadRangeCache"]
module: "miniproto.media.download"
---

## `miniproto.media.download.DownloadRangeCache`

```python
DownloadRangeCache(*, max_bytes: int = DEFAULT_RANGE_CACHE_BYTES) -> None
```

Async LRU cache that shares exact media-range fetches and limits background prefetch tasks.

**Parameters:**

- **max_bytes** (<code>[int](#int)</code>) – Maximum completed payload bytes retained by the LRU, defaults to :data:`DEFAULT_RANGE_CACHE_BYTES`. Pending fetches have a separate lifetime and do not count against this capacity.

<details class="resource-semantics" open markdown="1">
<summary>Resource Semantics</summary>

Entries use ``(key, offset, limit)``. Cancelling a waiter leaves the shared fetch running. Downloads borrow this cache and do not clear it when they finish or close. Keep the fetch's invoker available until its work finishes or ``clear()`` cancels and joins it. Cached payloads are not zeroized.

</details>

Initialize an empty bounded cache.

**Parameters:**

- **max_bytes** (<code>[int](#int)</code>) – Positive aggregate byte capacity for cached payloads.

**Raises:**

- <code>[ValueError](#ValueError)</code> – ``max_bytes`` is not positive.
