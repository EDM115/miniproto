---
title: "miniproto.mtproto.codec.GzipPacked.unpack"
description: "Decompress the contained gzip payload."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.GzipPacked.unpack"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L173"
aliases: ["miniproto.mtproto.GzipPacked.unpack"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.GzipPacked.unpack`

```python
unpack() -> bytes
```

Decompress the contained gzip payload.

**Returns:**

- <code>[bytes](#bytes)</code> – Uncompressed message-body bytes.

**Raises:**

- <code>[OSError](#OSError)</code> – If the stored bytes are not a valid gzip stream.
