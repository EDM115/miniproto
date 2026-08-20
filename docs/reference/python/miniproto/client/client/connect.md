---
title: "miniproto.client.Client.connect"
description: "Mark the client connected and start update handling when enabled."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.connect"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L415"
aliases: ["miniproto.Client.connect"]
module: "miniproto.client"
---

## `miniproto.client.Client.connect`

```python
connect() -> None
```

Mark the client connected and start update handling when enabled.

The method is serialized with ``disconnect`` and is safe to call repeatedly. If update startup fails, it rolls back the connection state and closes any sender it created.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates storage, sender, or update-manager startup failures.
