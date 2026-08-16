---
title: "miniproto.tl.codec.serialize_object"
description: "Serialize a generated TL object using its generated or generic metadata path."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.codec.serialize_object"
source_path: "src/miniproto/tl/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/codec.py#L339"
aliases: ["miniproto.tl.serialize_object"]
module: "miniproto.tl.codec"
---

## `miniproto.tl.codec.serialize_object`

```python
serialize_object(obj: Any, *, boxed: bool = True) -> bytes
```

Serialize a generated TL object using its generated or generic metadata path.

**Parameters:**

- **obj** (<code>[Any](#typing.Any)</code>) – Generated TL object instance.
- **boxed** (<code>[bool](#bool)</code>) – Include its constructor ID, defaulting to ``True``.

**Returns:**

- <code>[bytes](#bytes)</code> – TL wire representation of the object.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If ``obj`` does not expose generated TL metadata.
