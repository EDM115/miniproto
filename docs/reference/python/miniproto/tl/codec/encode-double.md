---
title: "miniproto.tl.codec.encode_double"
description: "Encode a TL ``double``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_double"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L176"
aliases: ["miniproto.tl.encode_double"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_double`

```python
encode_double(value: float) -> bytes
```

Encode a TL ``double``.

**Parameters:**

- **value** (<code>[float](#float)</code>) – Floating-point value to encode.

**Returns:**

- <code>[bytes](#bytes)</code> – Eight little-endian IEEE-754 bytes.
