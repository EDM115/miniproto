---
title: "miniproto.updates.manager.UpdateManager.wait_stopped"
description: "Wait for the current drainer to stop, propagating its processing failure"
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.wait_stopped"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L153"
aliases: ["miniproto.updates.UpdateManager.wait_stopped"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.wait_stopped`

```python
wait_stopped() -> None
```

Wait for the current drainer to stop, propagating its processing failure

Call after ``start`` and before ``stop``. Normal shutdown completes the wait. Cancelling this wait leaves the drainer running. Restarting the manager creates a new drainer and requires a new wait.

**Raises:**

- <code>[RuntimeError](#RuntimeError)</code> – If no drainer has been started or it has already been stopped.
- <code>[Exception](#Exception)</code> – The current drainer's processing failure, including queue or handler errors.
