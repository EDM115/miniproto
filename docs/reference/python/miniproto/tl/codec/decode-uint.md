---
title: "miniproto.tl.codec.decode_uint"
description: "Decode an unsigned 32-bit TL value."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_uint"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L63"
aliases: ["miniproto.tl.decode_uint"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_uint`

```python
decode_uint(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]
```

Decode an unsigned 32-bit TL value.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[int](#int), [int](#int)]</code> – Decoded unsigned integer and first unread offset.
