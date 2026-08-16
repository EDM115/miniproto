---
title: "miniproto.mtproto.codec.gzip_pack"
description: "Compress an encodable MTProto body into a ``gzip_packed`` service object."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.gzip_pack"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L644"
aliases: ["miniproto.mtproto.gzip_pack"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.gzip_pack`

```python
gzip_pack(body: ByteBuffer | object) -> GzipPacked
```

Compress an encodable MTProto body into a ``gzip_packed`` service object.

**Parameters:**

- **body** (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer) | [object](#object)</code>) – Raw or supported encodable body.

**Returns:**

- <code>[GzipPacked](#miniproto.mtproto.codec.GzipPacked)</code> – Service object containing gzip-compressed body bytes.
