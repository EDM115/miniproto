---
title: "miniproto.tl.codec.encode_vector"
description: "Encode a boxed TL vector."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.encode_vector"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L284"
aliases: ["miniproto.tl.encode_vector"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.encode_vector`

```python
encode_vector(values: Iterable[Any], item_type: str) -> bytes
```

Encode a boxed TL vector.

**Parameters:**

- **values** (<code>[Iterable](#collections.abc.Iterable)[[Any](#typing.Any)]</code>) – Items to serialize.
- **item_type** (<code>[str](#str)</code>) – Schema type of each item.

**Returns:**

- <code>[bytes](#bytes)</code> – Vector constructor, item count, and encoded items.
