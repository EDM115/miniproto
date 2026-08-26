---
title: "miniproto.file_id.DecodedFileId.to_input_media"
description: "Build the matching Telegram input-media object."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.file_id.DecodedFileId.to_input_media"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py#L73"
aliases: ["miniproto.DecodedFileId.to_input_media"]
module: "miniproto.file_id"
---

## `miniproto.file_id.DecodedFileId.to_input_media`

```python
to_input_media(*, spoiler: bool = False, ttl_seconds: int | None = None, video_cover: object | None = None, video_timestamp: int | None = None) -> object
```

Build the matching Telegram input-media object.

**Parameters:**

- **spoiler** (<code>[bool](#bool)</code>) – Request Telegram's spoiler presentation for the media.
- **ttl_seconds** (<code>[int](#int) | None</code>) – Optional self-destruct timer forwarded to Telegram.
- **video_cover** (<code>[object](#object) | None</code>) – Optional document video-cover input object.
- **video_timestamp** (<code>[int](#int) | None</code>) – Optional document video start timestamp.

**Returns:**

- <code>[object](#object)</code> – ``InputMediaPhoto`` for photo IDs or ``InputMediaDocument`` for document IDs.
