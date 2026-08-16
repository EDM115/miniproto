---
title: "miniproto.media.download.media_from_raw"
description: "Normalize supported raw Telegram media shapes into a :class:`Media` record."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.media_from_raw"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L1750"
aliases: ["miniproto.media.media_from_raw"]
module: "miniproto.media.download"
---

## `miniproto.media.download.media_from_raw`

```python
media_from_raw(raw: object) -> Media | None
```

Normalize supported raw Telegram media shapes into a :class:`Media` record.

**Parameters:**

- **raw** (<code>[object](#object)</code>) – Media, message/update, document, photo, or input file location.

**Returns:**

- <code>[Media](#miniproto.types.Media) | None</code> – A normalized media record, or ``None`` when ``raw`` is unsupported or absent.
