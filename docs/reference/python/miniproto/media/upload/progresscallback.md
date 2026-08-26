---
title: "miniproto.media.upload.ProgressCallback"
description: "Public type alias `miniproto.media.upload.ProgressCallback`."
generated: true
editUrl: false
language: "python"
kind: "type"
qualified_name: "miniproto.media.upload.ProgressCallback"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py#L43"
aliases: ["miniproto.media.ProgressCallback"]
module: "miniproto.media.upload"
---

## `miniproto.media.upload.ProgressCallback`

```python
type ProgressCallback = Callable[[int, int | None], Awaitable[None] | None]
```
