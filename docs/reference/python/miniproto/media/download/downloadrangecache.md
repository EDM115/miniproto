---
title: "miniproto.media.download.DownloadRangeCache"
description: "Async LRU cache that deduplicates exact media-range requests and bounded prefetches."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.download.DownloadRangeCache"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L198"
aliases: ["miniproto.media.DownloadRangeCache"]
module: "miniproto.media.download"
---

## `miniproto.media.download.DownloadRangeCache`

```python
DownloadRangeCache(*, max_bytes: int = DEFAULT_RANGE_CACHE_BYTES) -> None
```

Async LRU cache that deduplicates exact media-range requests and bounded prefetches.

**Parameters:**

- **max_bytes** (<code>[int](#int)</code>) – Maximum payload bytes retained by the LRU; defaults to
:data:`DEFAULT_RANGE_CACHE_BYTES`.

<details class="resource-semantics" open markdown="1">
<summary>Resource Semantics</summary>

Cache entries are shared by ``(key, offset, limit)``. ``clear()`` cancels
in-progress owner and background prefetch tasks; callers awaiting them
receive their normal task outcome or cancellation.

</details>

Initialize an empty bounded cache.

**Parameters:**

- **max_bytes** (<code>[int](#int)</code>) – Positive aggregate byte capacity for cached payloads.

**Raises:**

- <code>[ValueError](#ValueError)</code> – ``max_bytes`` is not positive.
