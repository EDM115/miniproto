---
title: "miniproto.updates.manager.UpdateManager.stop"
description: "Cancel and await the raw-update drainer without closing either queue."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.stop"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L107"
aliases: ["miniproto.updates.UpdateManager.stop"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.stop`

```python
stop() -> None
```

Cancel and await the raw-update drainer without closing either queue.

Cancellation while a raw item is being processed can interrupt that processing. If an already-completed drainer failed, this method re-raises its exception.

**Raises:**

- <code>[Exception](#Exception)</code> – The completed drainer's exception, if any.
