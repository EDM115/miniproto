---
title: "miniproto.event_loop.run"
description: "Run one coroutine with an optimized ``asyncio.Runner`` when possible."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.run"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L168"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.run`

```python
run(main: Coroutine[Any, Any, T], *, debug: bool | None = None) -> T
```

Run one coroutine with an optimized ``asyncio.Runner`` when possible.

**Parameters:**

- **main** (<code>[Coroutine](#collections.abc.Coroutine)[[Any](#typing.Any), [Any](#typing.Any), [run[T]](#miniproto.event_loop.run[T])]</code>) – The coroutine to execute until it returns or raises.
- **debug** (<code>[bool](#bool) | None</code>) – Passed to ``asyncio.Runner``. ``None`` preserves asyncio's
default; known backend/debug incompatibilities use the stdlib loop.

**Returns:**

- <code>[run[T]](#miniproto.event_loop.run[T])</code> – The coroutine's result.

**Raises:**

- <code>[BaseException](#BaseException)</code> – Any exception raised by ``main`` or backend setup.

<details class="notes" open markdown="1">
<summary>Notes</summary>

The runner creates, closes and clears its loop. It must not be called
while another event loop is running in this thread.

</details>
