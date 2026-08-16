---
title: "miniproto.file_id.input_media_from_file_id"
description: "Decode a file ID into Telegram input media."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.file_id.input_media_from_file_id"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py#L212"
aliases: ["miniproto.input_media_from_file_id"]
module: "miniproto.file_id"
---

## `miniproto.file_id.input_media_from_file_id`

```python
input_media_from_file_id(file_id: str, *, spoiler: bool = False, ttl_seconds: int | None = None, video_cover: object | None = None, video_timestamp: int | None = None) -> object
```

Decode a file ID into Telegram input media.

**Parameters:**

- **file_id** (<code>[str](#str)</code>) – Local identifier produced by :func:`encode_file_id`.
- **spoiler** (<code>[bool](#bool)</code>) – Request spoiler presentation; defaults to ``False``.
- **ttl_seconds** (<code>[int](#int) | None</code>) – Optional self-destruct timer.
- **video_cover** (<code>[object](#object) | None</code>) – Optional cover input for document media.
- **video_timestamp** (<code>[int](#int) | None</code>) – Optional start timestamp for document media.

**Returns:**

- <code>[object](#object)</code> – Matching generated input-media object.
