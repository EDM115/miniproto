---
title: "miniproto.media.download.MediaDownloadResult"
description: "Completed materialized-download metadata and optional in-memory payload."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.download.MediaDownloadResult"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L100"
aliases: ["miniproto.MediaDownloadResult","miniproto.media.MediaDownloadResult"]
module: "miniproto.media.download"
---

## `miniproto.media.download.MediaDownloadResult`

```python
MediaDownloadResult(bytes_downloaded: int, offset: int, destination: Path | BinaryIO | None = None, data: bytes | None = None, raw_location: object | None = None) -> None
```

Completed materialized-download metadata and optional in-memory payload.

**Attributes:**

- [**bytes_downloaded**](#miniproto.media.download.MediaDownloadResult.bytes_downloaded) (<code>[int](#int)</code>) – Bytes committed for this operation, including resumed bytes.
- [**offset**](#miniproto.media.download.MediaDownloadResult.offset) (<code>[int](#int)</code>) – Requested starting byte offset.
- [**destination**](#miniproto.media.download.MediaDownloadResult.destination) (<code>[Path](#pathlib.Path) | [BinaryIO](#typing.BinaryIO) | None</code>) – Resolved path or caller-owned stream, if one was used.
- [**data**](#miniproto.media.download.MediaDownloadResult.data) (<code>[bytes](#bytes) | None</code>) – Downloaded bytes only when the destination was omitted.
- [**raw_location**](#miniproto.media.download.MediaDownloadResult.raw_location) (<code>[object](#object) | None</code>) – Effective raw location, potentially refreshed after a stale reference.
