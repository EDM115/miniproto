---
title: "miniproto.event_loop.backend_name"
description: "Return the optimized event-loop package selected for this platform."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.backend_name"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L26"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.backend_name`

```python
backend_name() -> str
```

Return the optimized event-loop package selected for this platform.

**Returns:**

- <code>[str](#str)</code> – ``winloop`` on Windows and ``uvloop`` on every other platform. The name
- <code>[str](#str)</code> – is selected without importing or installing the package.
