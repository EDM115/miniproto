---
title: "miniproto.tl.codec.decode_int"
description: "Decode a signed TL ``int``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_int"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L38"
aliases: ["miniproto.tl.decode_int"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_int`

```python
decode_int(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]
```

Decode a signed TL ``int``.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[int](#int), [int](#int)]</code> – Decoded integer and first unread offset.
