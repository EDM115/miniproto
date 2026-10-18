---
title: "miniproto.tl.codec.encode_long"
description: "Encode a signed TL ``long``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_long"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L101"
aliases: ["miniproto.tl.encode_long"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_long`

```python
encode_long(value: int) -> bytes
```

Encode a signed TL ``long``.

**Parameters:**

- **value** (<code>[int](#int)</code>) – Integer to encode.

**Returns:**

- <code>[bytes](#bytes)</code> – Eight little-endian TL bytes.
