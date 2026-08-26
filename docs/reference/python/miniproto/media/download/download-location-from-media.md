---
title: "miniproto.media.download.download_location_from_media"
description: "Resolve a media model, raw Telegram object, file ID or input location for download."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.download_location_from_media"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L1723"
aliases: ["miniproto.media.download_location_from_media"]
module: "miniproto.media.download"
---

## `miniproto.media.download.download_location_from_media`

```python
download_location_from_media(media: object) -> object
```

Resolve a media model, raw Telegram object, file ID or input location for download.

**Parameters:**

- **media** (<code>[object](#object)</code>) – Supported high-level, raw, encoded or already-resolved media input.

**Returns:**

- <code>[object](#object)</code> – A raw Telegram ``InputFileLocation`` suitable for ``upload.getFile``.

**Raises:**

- <code>[MediaDownloadError](#miniproto.media.download.MediaDownloadError)</code> – The object has no download-capable document or photo location.
