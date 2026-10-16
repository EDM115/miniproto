---
title: "miniproto.media.download.iter_download_media"
description: "Resolve a supported media object and stream it through :func:`iter_download`."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.iter_download_media"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L1723"
aliases: ["miniproto.media.iter_download_media"]
module: "miniproto.media.download"
---

## `miniproto.media.download.iter_download_media`

```python
iter_download_media(invoke: RawInvoker, media: object, **kwargs: Any) -> AsyncGenerator[bytes]
```

Resolve a supported media object and stream it through :func:`iter_download`.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.download.RawInvoker)</code>) – Async raw-RPC invoker used for file requests.
- **media** (<code>[object](#object)</code>) – A :class:`Media`, file ID, raw document/photo/message or input file location.
- **kwargs** (<code>[Any](#typing.Any)</code>) – Download options forwarded to :func:`iter_download`, missing cache keys and total sizes are inferred when possible.

**Yields:**

- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code> – Ordered byte chunks with the caching, CDN and integrity checks of :func:`iter_download`. Closing this wrapper closes its nested iterator and joins transfer-owned tasks, borrowed cache work remains cache-owned.

**Raises:**

- <code>[MediaDownloadError](#miniproto.media.download.MediaDownloadError)</code> – ``media`` cannot be resolved to an input file location.
- <code>[CancelledError](#asyncio.CancelledError)</code> – The active stream is cancelled, transfer-owned part tasks are cancelled and joined.
