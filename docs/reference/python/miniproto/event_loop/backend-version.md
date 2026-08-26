---
title: "miniproto.event_loop.backend_version"
description: "Return the installed optimized backend version, if available."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.backend_version"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L50"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.backend_version`

```python
backend_version() -> str | None
```

Return the installed optimized backend version, if available.

**Returns:**

- <code>[str](#str) | None</code> – Distribution metadata, then the backend's ``__version__`` fallback, or
- <code>[str](#str) | None</code> – ``None`` when no backend is importable or exposes a version.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates failures while importing the selected backend.
