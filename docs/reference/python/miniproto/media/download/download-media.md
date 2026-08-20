---
title: "miniproto.media.download.download_media"
description: "Resolve media and materialize it through :func:`download_file`."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.download_media"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L1685"
aliases: ["miniproto.media.download_media"]
module: "miniproto.media.download"
---

## `miniproto.media.download.download_media`

```python
download_media(invoke: RawInvoker, media: object, destination: Destination = None, **kwargs: Any) -> MediaDownloadResult
```

Resolve media and materialize it through :func:`download_file`.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.download.RawInvoker)</code>) – Async raw-RPC invoker used for file requests.
- **media** (<code>[object](#object)</code>) – A :class:`Media`, file ID, raw document/photo/message, or input file location.
- **destination** (<code>[Destination](#miniproto.media.download.Destination)</code>) – In-memory, path, or binary-stream destination forwarded to :func:`download_file`.
- **kwargs** (<code>[Any](#typing.Any)</code>) – Remaining forwarded ``**kwargs`` download options; cache identity and total size are inferred when possible.

**Returns:**

- <code>[MediaDownloadResult](#miniproto.media.download.MediaDownloadResult)</code> – The same result and destination-ownership semantics as :func:`download_file`.

**Raises:**

- <code>[MediaDownloadError](#miniproto.media.download.MediaDownloadError)</code> – The supplied media cannot produce a download location.
- <code>[MediaIntegrityError](#miniproto.media.download.MediaIntegrityError)</code> – CDN or enabled plain-file verification fails.
- <code>[CancelledError](#asyncio.CancelledError)</code> – The transfer is cancelled and destination cleanup runs.
