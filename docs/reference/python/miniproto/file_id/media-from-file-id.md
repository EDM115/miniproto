---
title: "miniproto.file_id.media_from_file_id"
description: "Decode a local file ID into a reusable ``Media`` value."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.file_id.media_from_file_id"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py#L200"
aliases: ["miniproto.media_from_file_id"]
module: "miniproto.file_id"
---

## `miniproto.file_id.media_from_file_id`

```python
media_from_file_id(file_id: str) -> Media
```

Decode a local file ID into a reusable ``Media`` value.

**Parameters:**

- **file_id** (<code>[str](#str)</code>) – Local identifier produced by :func:`encode_file_id`.

**Returns:**

- <code>[Media](#miniproto.types.Media)</code> – Media retaining the ID's input location and metadata.
