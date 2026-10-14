---
title: "miniproto.mtproto.codec.GzipPacked.unpack"
description: "Decompress valid gzip members under one total output bound."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.GzipPacked.unpack"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L177"
aliases: ["miniproto.mtproto.GzipPacked.unpack"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.GzipPacked.unpack`

```python
unpack(*, max_output_size: int = DEFAULT_GZIP_MAX_OUTPUT_SIZE) -> bytes
```

Decompress valid gzip members under one total output bound.

**Parameters:**

- **max_output_size** (<code>[int](#int)</code>) – Maximum combined decompressed bytes, defaulting to 16 MiB.

**Returns:**

- <code>[bytes](#bytes)</code> – Uncompressed message-body bytes.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the output bound is not positive.
- <code>[ProtocolValidationError](#miniproto.errors.ProtocolValidationError)</code> – If gzip data is invalid, truncated or expands beyond the bound.
