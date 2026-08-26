---
title: "miniproto.media.upload.MediaUploadResult"
description: "Completed upload metadata and the MTProto input-file reference to reuse."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.upload.MediaUploadResult"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py#L63"
aliases: ["miniproto.MediaUploadResult","miniproto.media.MediaUploadResult"]
module: "miniproto.media.upload"
---

## `miniproto.media.upload.MediaUploadResult`

```python
MediaUploadResult(file_id: int, name: str, size: int, parts: int, part_size: int, big: bool, input_file: types.InputFile | types.InputFileBig, md5_checksum: str | None = None) -> None
```

Completed upload metadata and the MTProto input-file reference to reuse.

**Attributes:**

- [**file_id**](#miniproto.media.upload.MediaUploadResult.file_id) (<code>[int](#int)</code>) – Generated ID or ``int(file_id)`` supplied by the caller; zero is accepted when supplied.
- [**name**](#miniproto.media.upload.MediaUploadResult.name) (<code>[str](#str)</code>) – File name sent to Telegram.
- [**size**](#miniproto.media.upload.MediaUploadResult.size) (<code>[int](#int)</code>) – Exact uploaded source size in bytes.
- [**parts**](#miniproto.media.upload.MediaUploadResult.parts) (<code>[int](#int)</code>) – Total successfully saved part count.
- [**part_size**](#miniproto.media.upload.MediaUploadResult.part_size) (<code>[int](#int)</code>) – Final KiB-aligned part size in bytes.
- [**big**](#miniproto.media.upload.MediaUploadResult.big) (<code>[bool](#bool)</code>) – Whether the source exceeded the big-file threshold.
- [**input_file**](#miniproto.media.upload.MediaUploadResult.input_file) (<code>[InputFile](#miniproto.raw.types.InputFile) | [InputFileBig](#miniproto.raw.types.InputFileBig)</code>) – Matching Telegram small or big input-file reference.
- [**md5_checksum**](#miniproto.media.upload.MediaUploadResult.md5_checksum) (<code>[str](#str) | None</code>) – Small-file MD5 of uploaded bytes, otherwise ``None``.
