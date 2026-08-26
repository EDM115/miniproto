---
title: "miniproto.tl.codec.encode_int"
description: "Encode a signed TL ``int``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_int"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L26"
aliases: ["miniproto.tl.encode_int"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_int`

```python
encode_int(value: int) -> bytes
```

Encode a signed TL ``int``.

**Parameters:**

- **value** (<code>[int](#int)</code>) – Integer to encode.

**Returns:**

- <code>[bytes](#bytes)</code> – Four little-endian TL bytes.
