---
title: "miniproto.tl.codec.decode_bool"
description: "Decode a TL ``Bool`` constructor."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_bool"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L263"
aliases: ["miniproto.tl.decode_bool"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_bool`

```python
decode_bool(data: bytes | memoryview, offset: int = 0) -> tuple[bool, int]
```

Decode a TL ``Bool`` constructor.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[bool](#bool), [int](#int)]</code> – Boolean value and first unread offset.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If the constructor is not a TL boolean.
