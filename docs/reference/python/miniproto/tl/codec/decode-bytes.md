---
title: "miniproto.tl.codec.decode_bytes"
description: "Decode a TL length-prefixed byte string."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_bytes"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L213"
aliases: ["miniproto.tl.decode_bytes"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_bytes`

```python
decode_bytes(data: bytes | memoryview, offset: int = 0) -> tuple[bytes, int]
```

Decode a TL length-prefixed byte string.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[bytes](#bytes), [int](#int)]</code> – Decoded bytes and first unread offset.
