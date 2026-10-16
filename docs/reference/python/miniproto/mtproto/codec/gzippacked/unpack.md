---
title: "miniproto.mtproto.codec.GzipPacked.unpack"
description: "Decompress valid gzip members under input, output and member bounds."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.GzipPacked.unpack"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L181"
aliases: ["miniproto.mtproto.GzipPacked.unpack"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.GzipPacked.unpack`

```python
unpack(*, max_output_size: int = DEFAULT_GZIP_MAX_OUTPUT_SIZE, max_input_size: int = DEFAULT_GZIP_MAX_INPUT_SIZE, max_members: int = DEFAULT_GZIP_MAX_MEMBERS) -> bytes
```

Decompress valid gzip members under input, output and member bounds.

**Parameters:**

- **max_output_size** (<code>[int](#int)</code>) – Maximum combined decompressed bytes, defaulting to 16 MiB.
- **max_input_size** (<code>[int](#int)</code>) – Maximum compressed bytes including padding, defaulting to 32 MiB.
- **max_members** (<code>[int](#int)</code>) – Maximum concatenated members including empty members, defaulting to 1024.

**Returns:**

- <code>[bytes](#bytes)</code> – Uncompressed message-body bytes.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If a bound is not positive.
- <code>[ProtocolValidationError](#miniproto.errors.ProtocolValidationError)</code> – If gzip data is invalid, truncated or exceeds a bound.
