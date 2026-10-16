---
title: "miniproto.client.Client.connect"
description: "Mark the client connected and start update handling when enabled."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.connect"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L511"
aliases: ["miniproto.Client.connect"]
module: "miniproto.client"
---

## `miniproto.client.Client.connect`

```python
connect() -> None
```

Mark the client connected and start update handling when enabled.

Repeated calls retain the running update manager. The method serializes with ``disconnect`` and rolls back local connection state if startup fails. Network senders remain lazy unless an imported session requires update-state bootstrap.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates storage, sender or update-manager startup failures.
