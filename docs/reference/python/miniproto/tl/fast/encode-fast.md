---
title: "miniproto.tl.fast.encode_fast"
description: "Attempt native serialization for a generated TL constructor."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.fast.encode_fast"
source_path: "src/miniproto/tl/fast.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/fast.py#L19"
module: "miniproto.tl.fast"
---

## `miniproto.tl.fast.encode_fast`

```python
encode_fast(constructor_id: int, values: tuple[object, ...], *, boxed: bool = True) -> bytes | None
```

Attempt native serialization for a generated TL constructor.

**Parameters:**

- **constructor_id** (<code>[int](#int)</code>) – Unsigned 32-bit TL constructor identifier.
- **values** (<code>[tuple](#tuple)[[object](#object), ...]</code>) – Constructor field values in generated-field order.
- **boxed** (<code>[bool](#bool)</code>) – Whether the wire value includes its constructor identifier.

**Returns:**

- <code>[bytes](#bytes) | None</code> – Encoded bytes when the native fast path accepts the constructor, otherwise ``None``.
