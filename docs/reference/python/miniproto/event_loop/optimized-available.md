---
title: "miniproto.event_loop.optimized_available"
description: "Return whether the platform's optimized event-loop backend can be loaded."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.optimized_available"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L70"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.optimized_available`

```python
optimized_available() -> bool
```

Return whether the platform's optimized event-loop backend can be loaded.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates import failures other than an absent selected
backend package.
