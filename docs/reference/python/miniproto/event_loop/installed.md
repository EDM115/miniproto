---
title: "miniproto.event_loop.installed"
description: "Return whether :func:`install` last installed a legacy backend policy."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.installed"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L80"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.installed`

```python
installed() -> bool
```

Return whether :func:`install` last installed a legacy backend policy.

This flag does not probe asyncio's current policy and remains false when
applications use :func:`run` or :func:`new_event_loop` instead.
