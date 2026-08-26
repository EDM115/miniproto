---
title: "miniproto.client.Client.disconnect"
description: "Stop updates, senders, schedulers, auxiliary clients and session storage."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.disconnect"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L442"
aliases: ["miniproto.Client.disconnect"]
module: "miniproto.client"
---

## `miniproto.client.Client.disconnect`

```python
disconnect() -> None
```

Stop updates, senders, schedulers, auxiliary clients and session storage.

Cleanup continues after individual failures so resources are released; after cleanup it re-raises the first captured error. Calling it makes the client unusable because session storage is closed.

**Raises:**

- <code>[Exception](#Exception)</code> – The first failure encountered while stopping client resources.
