---
title: "miniproto.tl.codec.decode_long"
description: "Decode a signed TL ``long``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_long"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L113"
aliases: ["miniproto.tl.decode_long"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_long`

```python
decode_long(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]
```

Decode a signed TL ``long``.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[int](#int), [int](#int)]</code> – Decoded integer and first unread offset.
