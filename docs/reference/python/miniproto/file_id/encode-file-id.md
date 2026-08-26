---
title: "miniproto.file_id.encode_file_id"
description: "Encode supported Telegram media or input locations into a local file ID."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.file_id.encode_file_id"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py#L119"
aliases: ["miniproto.encode_file_id"]
module: "miniproto.file_id"
---

## `miniproto.file_id.encode_file_id`

```python
encode_file_id(media: Media | object) -> str
```

Encode supported Telegram media or input locations into a local file ID.

**Parameters:**

- **media** (<code>[Media](#miniproto.types.Media) | [object](#object)</code>) – A ``Media`` value, supported generated media object or input file location.

**Returns:**

- <code>[str](#str)</code> – Canonical URL-safe ``mpf1_`` identifier containing the reusable location fields.

**Raises:**

- <code>[TypeError](#TypeError)</code> – If the media cannot supply a supported reusable location.
- <code>[ValueError](#ValueError)</code> – If an extracted field cannot be encoded.
