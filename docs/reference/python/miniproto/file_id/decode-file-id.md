---
title: "miniproto.file_id.decode_file_id"
description: "Decode an ``mpf1_`` file ID without contacting Telegram."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.file_id.decode_file_id"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py#L170"
aliases: ["miniproto.decode_file_id"]
module: "miniproto.file_id"
---

## `miniproto.file_id.decode_file_id`

```python
decode_file_id(file_id: str) -> DecodedFileId
```

Decode an ``mpf1_`` file ID without contacting Telegram.

**Parameters:**

- **file_id** (<code>[str](#str)</code>) – Local identifier produced by :func:`encode_file_id`.

**Returns:**

- <code>[DecodedFileId](#miniproto.file_id.DecodedFileId)</code> – Parsed reusable media fields.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the prefix, payload encoding or required fields are invalid.
