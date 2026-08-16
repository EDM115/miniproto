---
title: "miniproto.tl.codec.decode_object"
description: "Decode a primitive or generated TL object selected by its constructor."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_object"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L396"
aliases: ["miniproto.tl.decode_object"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_object`

```python
decode_object(data: bytes | memoryview, offset: int = 0, expected_type: str | None = None) -> tuple[Any, int]
```

Decode a primitive or generated TL object selected by its constructor.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.
- **expected_type** (<code>[str](#str) | None</code>) – Optional schema type used for primitive dispatch.

**Returns:**

- <code>[tuple](#tuple)[[Any](#typing.Any), [int](#int)]</code> – Decoded value and first unread offset.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If the constructor is unknown or a bare type lacks a concrete class.
