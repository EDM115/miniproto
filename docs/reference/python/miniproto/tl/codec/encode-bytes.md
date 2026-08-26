---
title: "miniproto.tl.codec.encode_bytes"
description: "Encode TL's length-prefixed, padded byte-string value."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_bytes"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L201"
aliases: ["miniproto.tl.encode_bytes"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_bytes`

```python
encode_bytes(value: bytes) -> bytes
```

Encode TL's length-prefixed, padded byte-string value.

**Parameters:**

- **value** (<code>[bytes](#bytes)</code>) – Raw byte value.

**Returns:**

- <code>[bytes](#bytes)</code> – TL byte-string encoding including its length and padding.
