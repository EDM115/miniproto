---
title: "miniproto.event_loop.backend"
description: "Load and return the optimized backend module when it is available."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.backend"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L36"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.backend`

```python
backend() -> ModuleType | None
```

Load and return the optimized backend module when it is available.

**Returns:**

- <code>[ModuleType](#types.ModuleType) | None</code> – The cached import of the platform-selected backend, or ``None`` when
- <code>[ModuleType](#types.ModuleType) | None</code> – that package is not installed.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates an import failure raised inside the backend rather
than treating a broken installation as unavailable.
