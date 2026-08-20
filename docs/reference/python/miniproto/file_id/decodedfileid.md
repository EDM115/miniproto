---
title: "miniproto.file_id.DecodedFileId"
description: "Decoded local file-id fields used to recreate a media location or input media."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.file_id.DecodedFileId"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py#L21"
aliases: ["miniproto.DecodedFileId"]
module: "miniproto.file_id"
---

## `miniproto.file_id.DecodedFileId`

```python
DecodedFileId(kind: FileIdKind, id: int, access_hash: int, file_reference: bytes, dc_id: int | None = None, size: int | None = None, file_name: str | None = None, mime_type: str | None = None, thumb_size: str = '') -> None
```

Decoded local file-id fields used to recreate a media location or input media.

**Attributes:**

- [**kind**](#miniproto.file_id.DecodedFileId.kind) (<code>[FileIdKind](#miniproto.file_id.FileIdKind)</code>) – Encoded media kind, either ``"document"`` or ``"photo"``.
- [**id**](#miniproto.file_id.DecodedFileId.id) (<code>[int](#int)</code>) – Telegram document or photo ID.
- [**access_hash**](#miniproto.file_id.DecodedFileId.access_hash) (<code>[int](#int)</code>) – Telegram access hash required for reuse.
- [**file_reference**](#miniproto.file_id.DecodedFileId.file_reference) (<code>[bytes](#bytes)</code>) – Telegram file reference required for reuse.
- [**dc_id**](#miniproto.file_id.DecodedFileId.dc_id) (<code>[int](#int) | None</code>) – Optional data-center ID retained as metadata.
- [**size**](#miniproto.file_id.DecodedFileId.size) (<code>[int](#int) | None</code>) – Optional known media size retained as metadata.
- [**file_name**](#miniproto.file_id.DecodedFileId.file_name) (<code>[str](#str) | None</code>) – Optional document filename retained as metadata.
- [**mime_type**](#miniproto.file_id.DecodedFileId.mime_type) (<code>[str](#str) | None</code>) – Optional MIME type retained as metadata.
- [**thumb_size**](#miniproto.file_id.DecodedFileId.thumb_size) (<code>[str](#str)</code>) – Input-location thumbnail size, defaulting to the empty size.
