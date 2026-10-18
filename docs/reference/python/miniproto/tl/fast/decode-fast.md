---
title: "miniproto.tl.fast.decode_fast"
description: "Attempt native deserialization for a generated TL constructor."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.fast.decode_fast"
source_path: "src/miniproto/tl/fast.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/fast.py#L36"
module: "miniproto.tl.fast"
---

## `miniproto.tl.fast.decode_fast`

```python
decode_fast(constructor_id: int, data: bytes | memoryview, offset: int = 0, *, boxed: bool = True) -> tuple[tuple[object, ...], int] | None
```

Attempt native deserialization for a generated TL constructor.

**Parameters:**

- **constructor_id** (<code>[int](#int)</code>) – Unsigned 32-bit TL constructor identifier.
- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – Wire bytes; memoryviews deliberately use the Python path.
- **offset** (<code>[int](#int)</code>) – Initial byte offset, defaulting to ``0``.
- **boxed** (<code>[bool](#bool)</code>) – Whether the input includes a constructor identifier.

**Returns:**

- <code>[tuple](#tuple)[[tuple](#tuple)[[object](#object), ...], [int](#int)] | None</code> – Decoded field values and next offset or ``None`` when no fast path applies.
