---
title: "miniproto.client.Client.disconnect"
description: "Stop updates, senders, schedulers, auxiliary clients and session storage."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.disconnect"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L466"
aliases: ["miniproto.Client.disconnect"]
module: "miniproto.client"
---

## `miniproto.client.Client.disconnect`

```python
disconnect() -> None
```

Stop updates, senders, schedulers, auxiliary clients and session storage.

Cleanup attempts continue after individual failures, then the first captured error is re-raised. Successful storage closure prevents reusing this client. Update iterators receive no end marker. Cancel a waiting consumer yourself.

**Raises:**

- <code>[Exception](#Exception)</code> – The first failure encountered while stopping client resources.
