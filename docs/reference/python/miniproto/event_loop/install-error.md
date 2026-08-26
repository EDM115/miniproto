---
title: "miniproto.event_loop.install_error"
description: "Return the most recent explicit-install or backend-load error, if any."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.install_error"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L89"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.install_error`

```python
install_error() -> Exception | None
```

Return the most recent explicit-install or backend-load error, if any.

**Returns:**

- <code>[Exception](#Exception) | None</code> – The stored exception from :func:`install` or backend import, otherwise
- <code>[Exception](#Exception) | None</code> – ``None``. Reading this value never retries installation.
