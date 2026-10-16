---
title: "miniproto.tl.codec.encode_int128"
description: "Encode an unsigned 128-bit TL integer."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_int128"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L126"
aliases: ["miniproto.tl.encode_int128"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_int128`

```python
encode_int128(value: int) -> bytes
```

Encode an unsigned 128-bit TL integer.

**Parameters:**

- **value** (<code>[int](#int)</code>) – Integer in the inclusive range ``0`` through ``2**128 - 1``.

**Returns:**

- <code>[bytes](#bytes)</code> – Sixteen little-endian bytes.
