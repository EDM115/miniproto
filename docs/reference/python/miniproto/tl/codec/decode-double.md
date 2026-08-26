---
title: "miniproto.tl.codec.decode_double"
description: "Decode a TL ``double``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_double"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L188"
aliases: ["miniproto.tl.decode_double"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_double`

```python
decode_double(data: bytes | memoryview, offset: int = 0) -> tuple[float, int]
```

Decode a TL ``double``.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[float](#float), [int](#int)]</code> – Decoded float and first unread offset.
