---
title: "miniproto.tl.codec.decode_constructor_id"
description: "Decode an unsigned TL constructor identifier."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_constructor_id"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L88"
aliases: ["miniproto.tl.decode_constructor_id"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_constructor_id`

```python
decode_constructor_id(data: bytes | memoryview, offset: int = 0) -> tuple[int, int]
```

Decode an unsigned TL constructor identifier.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[int](#int), [int](#int)]</code> – Constructor ID and first unread offset.
