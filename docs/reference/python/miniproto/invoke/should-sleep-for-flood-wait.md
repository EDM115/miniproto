---
title: "miniproto.invoke.should_sleep_for_flood_wait"
description: "Return whether a flood wait is short enough for automatic sleeping."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.should_sleep_for_flood_wait"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L321"
module: "miniproto.invoke"
---

## `miniproto.invoke.should_sleep_for_flood_wait`

```python
should_sleep_for_flood_wait(error: FloodWait, threshold: int | None) -> bool
```

Return whether a flood wait is short enough for automatic sleeping.

A ``None`` threshold disables automatic waiting; otherwise the wait must not
exceed the configured threshold in seconds.

**Parameters:**

- **error** (<code>[FloodWait](#miniproto.errors.FloodWait)</code>) – Classified Telegram flood-wait response.
- **threshold** (<code>[int](#int) | None</code>) – Maximum automatically slept duration in seconds, or ``None`` to disable it.
