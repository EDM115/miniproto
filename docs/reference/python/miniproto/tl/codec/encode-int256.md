---
title: "miniproto.tl.codec.encode_int256"
description: "Encode an unsigned 256-bit TL integer."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_int256"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L151"
aliases: ["miniproto.tl.encode_int256"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_int256`

```python
encode_int256(value: int) -> bytes
```

Encode an unsigned 256-bit TL integer.

**Parameters:**

- **value** (<code>[int](#int)</code>) – Integer in the inclusive range ``0`` through ``2**256 - 1``.

**Returns:**

- <code>[bytes](#bytes)</code> – Thirty-two little-endian bytes.
