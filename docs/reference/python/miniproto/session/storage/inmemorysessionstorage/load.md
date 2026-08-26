---
title: "miniproto.session.storage.InMemorySessionStorage.load"
description: "Return a detached current snapshot while holding the storage lock."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.InMemorySessionStorage.load"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L136"
aliases: ["miniproto.InMemorySessionStorage.load","miniproto.session.InMemorySessionStorage.load"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.InMemorySessionStorage.load`

```python
load() -> Mapping[str, Any] | None
```

Return a detached current snapshot while holding the storage lock.
