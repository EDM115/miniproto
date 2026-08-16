---
title: "miniproto.types.Media"
description: "Normalized Telegram media descriptor used for upload and download helpers."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.types.Media"
source_path: "src/miniproto/types.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/types.py#L64"
aliases: ["miniproto.Media"]
module: "miniproto.types"
---

## `miniproto.types.Media`

```python
Media(id: int, mime_type: str | None = None, size: int | None = None, file_name: str | None = None, raw: object | None = None, access_hash: int | None = None, file_reference: bytes | None = None, dc_id: int | None = None, location: object | None = None) -> None
```

Normalized Telegram media descriptor used for upload and download helpers.

**Attributes:**

- [**id**](#miniproto.types.Media.id) (<code>[int](#int)</code>) – Telegram media identifier.
- [**mime_type**](#miniproto.types.Media.mime_type) (<code>[str](#str) | None</code>) – Optional declared content type.
- [**size**](#miniproto.types.Media.size) (<code>[int](#int) | None</code>) – Optional byte size.
- [**file_name**](#miniproto.types.Media.file_name) (<code>[str](#str) | None</code>) – Optional file name.
- [**raw**](#miniproto.types.Media.raw) (<code>[object](#object) | None</code>) – Optional underlying TL object.
- [**access_hash**](#miniproto.types.Media.access_hash) (<code>[int](#int) | None</code>) – Optional Telegram media access hash.
- [**file_reference**](#miniproto.types.Media.file_reference) (<code>[bytes](#bytes) | None</code>) – Optional opaque reference that Telegram may require to fetch the media.
- [**dc_id**](#miniproto.types.Media.dc_id) (<code>[int](#int) | None</code>) – Optional datacenter that hosts the media.
- [**location**](#miniproto.types.Media.location) (<code>[object](#object) | None</code>) – Optional low-level download location.
