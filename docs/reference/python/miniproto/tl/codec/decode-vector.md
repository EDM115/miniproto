---
title: "miniproto.tl.codec.decode_vector"
description: "Decode a boxed TL vector."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_vector"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L307"
aliases: ["miniproto.tl.decode_vector"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_vector`

```python
decode_vector(data: bytes | memoryview, offset: int, item_type: str) -> tuple[tuple[Any, ...], int]
```

Decode a boxed TL vector.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Offset at the vector constructor.
- **item_type** (<code>[str](#str)</code>) – Schema type of each item.

**Returns:**

- <code>[tuple](#tuple)[[tuple](#tuple)[[Any](#typing.Any), ...], [int](#int)]</code> – Decoded immutable item tuple and first unread offset.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If the constructor or count is invalid.
