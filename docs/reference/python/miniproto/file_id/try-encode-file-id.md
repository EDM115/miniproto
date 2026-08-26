---
title: "miniproto.file_id.try_encode_file_id"
description: "Best-effort variant of :func:`encode_file_id`."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.file_id.try_encode_file_id"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py#L153"
aliases: ["miniproto.try_encode_file_id"]
module: "miniproto.file_id"
---

## `miniproto.file_id.try_encode_file_id`

```python
try_encode_file_id(media: Media | object | None) -> str | None
```

Best-effort variant of :func:`encode_file_id`.

**Parameters:**

- **media** (<code>[Media](#miniproto.types.Media) | [object](#object) | None</code>) – Candidate media or ``None``.

**Returns:**

- <code>[str](#str) | None</code> – The encoded local ID or ``None`` for absent or unsupported media.
