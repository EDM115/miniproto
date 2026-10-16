---
title: "miniproto.media.upload.MediaUploadResult"
description: "Upload metadata and the MTProto input-file reference to reuse."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.upload.MediaUploadResult"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py#L58"
aliases: ["miniproto.MediaUploadResult","miniproto.media.MediaUploadResult"]
module: "miniproto.media.upload"
---

## `miniproto.media.upload.MediaUploadResult`

```python
MediaUploadResult(file_id: int, name: str, size: int, parts: int, part_size: int, big: bool, input_file: types.InputFile | types.InputFileBig, md5_checksum: str | None = None) -> None
```

Upload metadata and the MTProto input-file reference to reuse.

**Attributes:**

- [**file_id**](#miniproto.media.upload.MediaUploadResult.file_id) (<code>[int](#int)</code>) – Generated ID or ``int(file_id)`` supplied by the caller, including zero.
- [**name**](#miniproto.media.upload.MediaUploadResult.name) (<code>[str](#str)</code>) – File name sent to Telegram.
- [**size**](#miniproto.media.upload.MediaUploadResult.size) (<code>[int](#int)</code>) – Source size measured before part transfer, in bytes.
- [**parts**](#miniproto.media.upload.MediaUploadResult.parts) (<code>[int](#int)</code>) – Part count in the returned input-file reference.
- [**part_size**](#miniproto.media.upload.MediaUploadResult.part_size) (<code>[int](#int)</code>) – Final part size in bytes, a KiB-aligned divisor of 512 KiB.
- [**big**](#miniproto.media.upload.MediaUploadResult.big) (<code>[bool](#bool)</code>) – Whether the measured source size exceeds 10 MiB.
- [**input_file**](#miniproto.media.upload.MediaUploadResult.input_file) (<code>[InputFile](#miniproto.raw.types.InputFile) | [InputFileBig](#miniproto.raw.types.InputFileBig)</code>) – Matching Telegram small or big input-file reference.
- [**md5_checksum**](#miniproto.media.upload.MediaUploadResult.md5_checksum) (<code>[str](#str) | None</code>) – Small-file MD5 of uploaded bytes, otherwise ``None``.
