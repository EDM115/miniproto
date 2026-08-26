---
title: "miniproto.tl.codec.deserialize_object"
description: "Deserialize one generated TL object of an expected class."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.deserialize_object"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L365"
aliases: ["miniproto.tl.deserialize_object"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.deserialize_object`

```python
deserialize_object(cls: type[TLObjectT], data: bytes | memoryview, offset: int = 0, *, boxed: bool = True) -> tuple[TLObjectT, int]
```

Deserialize one generated TL object of an expected class.

**Parameters:**

- **cls** (<code>[type](#type)[[deserialize_object[TLObjectT]](#miniproto.tl.codec.deserialize_object[TLObjectT])]</code>) – Generated class defining constructor and field metadata.
- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.
- **boxed** (<code>[bool](#bool)</code>) – Whether input begins with a constructor ID.

**Returns:**

- <code>[tuple](#tuple)[[deserialize_object[TLObjectT]](#miniproto.tl.codec.deserialize_object[TLObjectT]), [int](#int)]</code> – Object instance and first unread offset.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If class metadata or a boxed constructor is invalid.
