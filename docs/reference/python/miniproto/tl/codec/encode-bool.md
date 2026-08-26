---
title: "miniproto.tl.codec.encode_bool"
description: "Encode a TL ``Bool`` constructor."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_bool"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L251"
aliases: ["miniproto.tl.encode_bool"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_bool`

```python
encode_bool(value: bool) -> bytes
```

Encode a TL ``Bool`` constructor.

**Parameters:**

- **value** (<code>[bool](#bool)</code>) – Boolean value.

**Returns:**

- <code>[bytes](#bytes)</code> – ``boolTrue`` or ``boolFalse`` constructor bytes.
