---
title: "miniproto.client.Client.iter_download"
description: "Stream ordered media bytes without materializing the complete download."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.iter_download"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1130"
aliases: ["miniproto.Client.iter_download"]
module: "miniproto.client"
---

## `miniproto.client.Client.iter_download`

```python
iter_download(media: object, **kwargs: Any) -> AsyncGenerator[bytes]
```

Stream ordered media bytes without materializing the complete download.

**Parameters:**

- **media** (<code>[object](#object)</code>) – Normalized media, raw media or compatible miniproto file ID to stream.
- ****kwargs** (<code>[Any](#typing.Any)</code>) – Range, buffering, per-part retry, caching, verification and media-lane options. ``multi_session`` and ``resume`` must remain false. Use ``offset`` for an explicit starting position.

**Yields:**

- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code> – Ordered downloaded byte chunks as the media layer makes them available.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``multi_session`` or ``resume`` is enabled.
- <code>[TypeError](#TypeError)</code> – If an unsupported keyword option is supplied.

<details class="lifecycle" open markdown="1">
<summary>Lifecycle</summary>

Await ``aclose`` when stopping early so the iterator cleans up its owned requests. Shared cache producers and read-ahead work retain the cache owner's lifetime.

</details>
