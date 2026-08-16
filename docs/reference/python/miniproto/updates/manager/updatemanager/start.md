---
title: "miniproto.updates.manager.UpdateManager.start"
description: "Restore persistent state and start draining queued raw updates."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.start"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L90"
aliases: ["miniproto.updates.UpdateManager.start"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.start`

```python
start() -> None
```

Restore persistent state and start draining queued raw updates.

Repeated calls retain the existing drainer when it is still running. A failed load propagates and no new drainer is started.
