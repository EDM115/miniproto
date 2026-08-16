---
title: "miniproto.invoke.MethodFloodWaitCache"
description: "Bounded client-local cache for Telegram's method-scoped flood waits."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.invoke.MethodFloodWaitCache"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L353"
module: "miniproto.invoke"
---

## `miniproto.invoke.MethodFloodWaitCache`

```python
MethodFloodWaitCache(max_entries: int, *, clock: Callable[[], float] = time.monotonic) -> None
```

Bounded client-local cache for Telegram's method-scoped flood waits.

Create a bounded LRU cache using a monotonic clock.

**Parameters:**

- **max_entries** (<code>[int](#int)</code>) – Maximum number of method-level waits to retain; must be positive.
- **clock** (<code>[Callable](#collections.abc.Callable)[[], [float](#float)]</code>) – Monotonic time source, injectable for deterministic tests.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``max_entries`` is not positive.
