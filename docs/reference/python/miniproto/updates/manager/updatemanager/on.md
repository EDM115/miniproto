---
title: "miniproto.updates.manager.UpdateManager.on"
description: "Register a handler directly or return a decorator for one update subtype."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.on"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L218"
aliases: ["miniproto.updates.UpdateManager.on"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.on`

```python
on(update_type: type[UpdateT], handler: UpdateHandler[UpdateT] | None = None) -> UpdateHandler[UpdateT] | Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]
```

Register a handler directly or return a decorator for one update subtype.

**Parameters:**

- **update_type** (<code>[type](#type)[[UpdateT](#miniproto.updates.manager.UpdateT)]</code>) – Normalized update subclass to match with ``isinstance``.
- **handler** (<code>[UpdateHandler](#miniproto.updates.manager.UpdateHandler)[[UpdateT](#miniproto.updates.manager.UpdateT)] | None</code>) – Optional synchronous or asynchronous callback.

**Returns:**

- <code>[UpdateHandler](#miniproto.updates.manager.UpdateHandler)[[UpdateT](#miniproto.updates.manager.UpdateT)] | [Callable](#collections.abc.Callable)[[[UpdateHandler](#miniproto.updates.manager.UpdateHandler)[[UpdateT](#miniproto.updates.manager.UpdateT)]], [UpdateHandler](#miniproto.updates.manager.UpdateHandler)[[UpdateT](#miniproto.updates.manager.UpdateT)]]</code> – The registered handler or a decorator that registers a supplied handler.
