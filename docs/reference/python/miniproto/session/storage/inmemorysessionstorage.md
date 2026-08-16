---
title: "miniproto.session.storage.InMemorySessionStorage"
description: "Thread-safe in-process storage that snapshots all values by serialization."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.storage.InMemorySessionStorage"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L102"
aliases: ["miniproto.InMemorySessionStorage","miniproto.session.InMemorySessionStorage"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.InMemorySessionStorage`

```python
InMemorySessionStorage(initial: SessionPayload | None = None) -> None
```

Thread-safe in-process storage that snapshots all values by serialization.

Initialize optional state and independent per-domain revision counters.

**Parameters:**

- **initial** (<code>[SessionPayload](#miniproto.session.storage.SessionPayload) | None</code>) – Optional mapping or typed record copied into initial storage state.
