---
title: "miniproto.tl.codec.encode_string"
description: "UTF-8 encode a string as a TL byte string."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_string"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L226"
aliases: ["miniproto.tl.encode_string"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_string`

```python
encode_string(value: str) -> bytes
```

UTF-8 encode a string as a TL byte string.

**Parameters:**

- **value** (<code>[str](#str)</code>) – Text to encode.

**Returns:**

- <code>[bytes](#bytes)</code> – Length-prefixed, padded TL string bytes.
