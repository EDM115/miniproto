---
title: "miniproto.event_loop.install"
description: "Install the backend's deprecated global policy on Python before 3.16."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.event_loop.install"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py#L99"
module: "miniproto.event_loop"
---

## `miniproto.event_loop.install`

```python
install() -> bool
```

Install the backend's deprecated global policy on Python before 3.16.

**Returns:**

- <code>[bool](#bool)</code> – ``True`` after the selected backend's legacy ``install`` hook succeeds;
- <code>[bool](#bool)</code> – ``False`` if no backend/hook is available, installation fails, or Python
- <code>[bool](#bool)</code> – 3.16+ rejects policy installation.

**Raises:**

- <code>[DeprecationWarning](#DeprecationWarning)</code> – Always warns because policy installation is a
deprecated asyncio integration path.

<details class="notes" open markdown="1">
<summary>Notes</summary>

This process-global operation is not safe to race with other tasks that
create loops. Prefer :func:`run` or ``asyncio.Runner`` with
:func:`new_event_loop` for scoped lifecycle control.

</details>
