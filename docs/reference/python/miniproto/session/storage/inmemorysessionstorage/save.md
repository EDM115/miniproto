---
title: "miniproto.session.storage.InMemorySessionStorage.save"
description: "Atomically replace state and advance only changed domain revisions."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.InMemorySessionStorage.save"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L145"
aliases: ["miniproto.InMemorySessionStorage.save","miniproto.session.InMemorySessionStorage.save"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.InMemorySessionStorage.save`

```python
save(data: SessionPayload) -> None
```

Atomically replace state and advance only changed domain revisions.

**Parameters:**

- **data** (<code>[SessionPayload](#miniproto.session.storage.SessionPayload)</code>) – Session mapping or typed record to deep-copy and persist.
