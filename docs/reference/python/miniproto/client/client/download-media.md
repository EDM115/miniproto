---
title: "miniproto.client.Client.download_media"
description: "Download media to memory, a path, or a writable destination."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.download_media"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1034"
aliases: ["miniproto.Client.download_media"]
module: "miniproto.client"
---

## `miniproto.client.Client.download_media`

```python
download_media(media: object, destination: Destination = None, **kwargs: Any) -> MediaDownloadResult
```

Download media to memory, a path, or a writable destination.

The default scheduler uses two media lanes and bounded in-flight bytes. Multi-session downloading is only used for complete, known-size bot downloads with sibling session storage; unsupported cases fall back to one session and emit telemetry.

**Parameters:**

- **media** (<code>[object](#object)</code>) – Normalized media, raw media, or compatible miniproto file ID to download.
- **destination** (<code>[Destination](#miniproto.media.Destination)</code>) – Memory, path, or writable destination accepted by the media download layer; defaults to in-memory output.
- ****kwargs** (<code>[Any](#typing.Any)</code>) – Supported range, resume, buffering, retry, verification, media-lane, and scheduling options accepted by ``_download_media_options``.

**Raises:**

- <code>[TypeError](#TypeError)</code> – If unsupported keyword options are provided.
- <code>[Exception](#Exception)</code> – Propagates media-location, destination, and RPC failures.
