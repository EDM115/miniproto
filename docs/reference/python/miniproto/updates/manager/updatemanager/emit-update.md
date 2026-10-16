---
title: "miniproto.updates.manager.UpdateManager.emit_update"
description: "Offer a normalized update to consumers, then invoke matching handlers sequentially."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.emit_update"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L213"
aliases: ["miniproto.updates.UpdateManager.emit_update"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.emit_update`

```python
emit_update(update: Update) -> None
```

Offer a normalized update to consumers, then invoke matching handlers sequentially.

Registered handlers without an active iterator receive updates without retaining iterator copies. Otherwise public-queue admission precedes handlers, and a rejected item is not passed to handlers. Matching registered types are visited in registration-mapping order and each handler is awaited before the next one when it returns an awaitable.

**Parameters:**

- **update** (<code>[Update](#miniproto.types.Update)</code>) – Normalized public update to queue and dispatch.

**Raises:**

- <code>[QueueFull](#asyncio.QueueFull)</code> – If the public queue is full and policy is ``"raise"``.
- <code>[Exception](#Exception)</code> – Propagates a matching handler failure.
