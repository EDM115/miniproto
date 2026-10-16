---
title: "miniproto.tl.codec.encode_uint"
description: "Encode an unsigned 32-bit TL value."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_uint"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L51"
aliases: ["miniproto.tl.encode_uint"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_uint`

```python
encode_uint(value: int) -> bytes
```

Encode an unsigned 32-bit TL value.

**Parameters:**

- **value** (<code>[int](#int)</code>) – Unsigned integer to encode.

**Returns:**

- <code>[bytes](#bytes)</code> – Four little-endian bytes.
