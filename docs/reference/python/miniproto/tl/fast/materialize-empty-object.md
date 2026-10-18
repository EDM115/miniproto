---
title: "miniproto.tl.fast.materialize_empty_object"
description: "Resolve a native empty-object token to its generated TL instance."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.tl.fast.materialize_empty_object"
source_path: "src/miniproto/tl/fast.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/fast.py#L59"
module: "miniproto.tl.fast"
---

## `miniproto.tl.fast.materialize_empty_object`

```python
materialize_empty_object(constructor_id: object) -> object
```

Resolve a native empty-object token to its generated TL instance.

**Parameters:**

- **constructor_id** (<code>[object](#object)</code>) – Integer TL constructor identifier returned by native code.

**Returns:**

- <code>[object](#object)</code> – A newly constructed generated object with no TL fields.

**Raises:**

- <code>[TypeError](#TypeError)</code> – If the token is not an integer or resolves to a non-empty constructor.
- <code>[KeyError](#KeyError)</code> – If no generated constructor has the identifier.
