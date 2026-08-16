---
title: "miniproto.tl.codec.encode_constructor_id"
description: "Encode a TL constructor identifier as an unsigned 32-bit value."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_constructor_id"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L76"
aliases: ["miniproto.tl.encode_constructor_id"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_constructor_id`

```python
encode_constructor_id(value: int) -> bytes
```

Encode a TL constructor identifier as an unsigned 32-bit value.

**Parameters:**

- **value** (<code>[int](#int)</code>) – Constructor ID; only its low 32 bits are encoded.

**Returns:**

- <code>[bytes](#bytes)</code> – Four little-endian constructor bytes.
