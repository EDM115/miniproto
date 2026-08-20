---
title: "miniproto.client.Client.iter_download"
description: "Stream ordered media bytes without materializing the complete download."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.iter_download"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1087"
aliases: ["miniproto.Client.iter_download"]
module: "miniproto.client"
---

## `miniproto.client.Client.iter_download`

```python
iter_download(media: object, **kwargs: Any) -> AsyncGenerator[bytes]
```

Stream ordered media bytes without materializing the complete download.

**Parameters:**

- **media** (<code>[object](#object)</code>) – Normalized media, raw media, or compatible miniproto file ID to stream.
- ****kwargs** (<code>[Any](#typing.Any)</code>) – Download options accepted by ``_download_media_options`` except ``multi_session`` and ``resume``, which this streaming API rejects.

**Yields:**

- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code> – Ordered downloaded byte chunks as the media layer makes them available.
