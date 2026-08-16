---
title: "miniproto.updates.manager.UpdateManager.sync_state"
description: "Fetch Telegram's current global update state and persist it atomically."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.sync_state"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L244"
aliases: ["miniproto.updates.UpdateManager.sync_state"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.sync_state`

```python
sync_state() -> UpdateCursor
```

Fetch Telegram's current global update state and persist it atomically.

**Returns:**

- <code>[UpdateCursor](#miniproto.updates.state.UpdateCursor)</code> – The loaded cursor after replacing its global PTS, QTS, sequence, and date fields.

**Raises:**

- <code>[TypeError](#TypeError)</code> – If ``updates.getState`` does not return ``updates.State``.
- <code>[Exception](#Exception)</code> – Propagates RPC and session-storage failures.
