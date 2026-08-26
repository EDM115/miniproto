---
title: "miniproto.client.Client.on"
description: "Register an update handler directly or return a decorator for that handler type."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.on"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1781"
aliases: ["miniproto.Client.on"]
module: "miniproto.client"
---

## `miniproto.client.Client.on`

```python
on(update_type: type[UpdateT], handler: UpdateHandler[UpdateT] | None = None) -> UpdateHandler[UpdateT] | Callable[[UpdateHandler[UpdateT]], UpdateHandler[UpdateT]]
```

Register an update handler directly or return a decorator for that handler type.

**Parameters:**

- **update_type** (<code>[type](#type)[[UpdateT](#miniproto.client.UpdateT)]</code>) – Normalized update subclass accepted by the handler.
- **handler** (<code>[UpdateHandler](#miniproto.updates.manager.UpdateHandler)[[UpdateT](#miniproto.client.UpdateT)] | None</code>) – Optional handler; when omitted, the returned callable decorates one.

**Returns:**

- <code>[UpdateHandler](#miniproto.updates.manager.UpdateHandler)[[UpdateT](#miniproto.client.UpdateT)] | [Callable](#collections.abc.Callable)[[[UpdateHandler](#miniproto.updates.manager.UpdateHandler)[[UpdateT](#miniproto.client.UpdateT)]], [UpdateHandler](#miniproto.updates.manager.UpdateHandler)[[UpdateT](#miniproto.client.UpdateT)]]</code> – The registered handler or a decorator that registers it.
