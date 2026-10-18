---
title: "miniproto.file_id.is_file_id"
description: "Return whether a value has the miniproto file-id prefix."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.file_id.is_file_id"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py#L110"
aliases: ["miniproto.is_file_id"]
module: "miniproto.file_id"
---

## `miniproto.file_id.is_file_id`

```python
is_file_id(value: object) -> TypeGuard[str]
```

Return whether a value has the miniproto file-id prefix.

This checks the prefix only. Use ``decode_file_id`` to validate the payload.

**Parameters:**

- **value** (<code>[object](#object)</code>) – Arbitrary candidate value.

**Returns:**

- <code>[TypeGuard](#typing.TypeGuard)[[str](#str)]</code> – ``True`` only for strings beginning with ``mpf1_``.
