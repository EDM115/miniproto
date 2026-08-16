---
title: "miniproto.event_loop.new_event_loop"
description: "Create and register an optimized loop, falling back to asyncio's loop."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.new_event_loop"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L146"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.new_event_loop`

```python
new_event_loop() -> asyncio.AbstractEventLoop
```

Create and register an optimized loop, falling back to asyncio's loop.

**Returns:**

- <code>[AbstractEventLoop](#asyncio.AbstractEventLoop)</code> – A newly created event loop, also made current with
- <code>[AbstractEventLoop](#asyncio.AbstractEventLoop)</code> – func:`asyncio.set_event_loop` for the calling thread.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates a selected backend import failure other than a
missing package.

<details class="notes" open markdown="1">
<summary>Notes</summary>

Callers own the returned loop's lifecycle. Use it as an
``asyncio.Runner`` factory or close it after standalone use.

</details>
