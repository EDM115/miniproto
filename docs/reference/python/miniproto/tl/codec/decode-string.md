---
title: "miniproto.tl.codec.decode_string"
description: "Decode a UTF-8 TL string."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.decode_string"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L238"
aliases: ["miniproto.tl.decode_string"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.decode_string`

```python
decode_string(data: bytes | memoryview, offset: int = 0) -> tuple[str, int]
```

Decode a UTF-8 TL string.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – TL wire bytes.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, defaulting to ``0``.

**Returns:**

- <code>[tuple](#tuple)[[str](#str), [int](#int)]</code> – Decoded text and first unread offset.
