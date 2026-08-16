---
title: "miniproto.client.Client.iter_updates"
description: "Yield normalized updates from the running update manager in arrival order."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.iter_updates"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1735"
aliases: ["miniproto.Client.iter_updates"]
module: "miniproto.client"
---

## `miniproto.client.Client.iter_updates`

```python
iter_updates() -> AsyncIterator[Update]
```

Yield normalized updates from the running update manager in arrival order.

**Yields:**

- <code>[AsyncIterator](#collections.abc.AsyncIterator)[[Update](#miniproto.types.Update)]</code> – Normalized ``Update`` instances until the underlying update stream ends or is cancelled.
