---
title: "miniproto.tl.codec.decode_int256"
description: "Decode an unsigned 256-bit TL integer."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_int256"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L163"
aliases: ["miniproto.tl.decode_int256"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_int256`

```python
decode_int256(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]
```

Decode an unsigned 256-bit TL integer.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[int](#int), [int](#int)]</code> – Decoded integer and first unread offset.
