---
title: "miniproto.client.Client.download_media"
description: "Download media to memory, a path or a writable destination."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.download_media"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1071"
aliases: ["miniproto.Client.download_media"]
module: "miniproto.client"
---

## `miniproto.client.Client.download_media`

```python
download_media(media: object, destination: Destination = None, **kwargs: Any) -> MediaDownloadResult
```

Download media to memory, a path or a writable destination.

Downloads default to two media lanes and bounded in-flight bytes. Multi-session mode requires a complete, known-size bot download and sibling session storage. Unsupported cases fall back to one session and emit telemetry.

**Parameters:**

- **media** (<code>[object](#object)</code>) – Normalized media, raw media or compatible miniproto file ID to download.
- **destination** (<code>[Destination](#miniproto.media.Destination)</code>) – ``None`` for an in-memory result, a path or a caller-owned writable binary stream.
- ****kwargs** (<code>[Any](#typing.Any)</code>) – Range, resume, buffering, per-part retry and verification options from the media layer, plus ``media_lanes`` (default 2) and ``multi_session`` (default false). ``media_lanes=0`` uses the main sender.

**Returns:**

- <code>[MediaDownloadResult](#miniproto.media.MediaDownloadResult)</code> – Download metadata, with ``data`` containing bytes when ``destination`` is omitted.

<details class="lifecycle" open markdown="1">
<summary>Lifecycle</summary>

Range caches own shared producers and read-ahead work, which may outlive this call. Keep their client available or await the supplied cache's ``clear`` method before disconnecting it.

</details>

**Raises:**

- <code>[TypeError](#TypeError)</code> – If unsupported keyword options are provided.
- <code>[Exception](#Exception)</code> – Propagates media-location, destination and RPC failures.
