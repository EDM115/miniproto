---
title: "miniproto.updates.manager.UpdateManager.handle_raw_update"
description: "Process one raw update synchronously, persist resulting state, then emit its public events."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.handle_raw_update"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L146"
aliases: ["miniproto.updates.UpdateManager.handle_raw_update"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.handle_raw_update`

```python
handle_raw_update(raw_update: object) -> None
```

Process one raw update synchronously, persist resulting state, then emit its public events.

Gap recovery and cursor mutation are serialized under the manager's state lock. Recovered events are date-ordered within a difference response; callers should not infer global ordering guarantees across independent input calls.

**Parameters:**

- **raw_update** (<code>[object](#object)</code>) – Decoded Telegram update or update-container object to process.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates storage, RPC, gap-recovery, queue and handler failures.
