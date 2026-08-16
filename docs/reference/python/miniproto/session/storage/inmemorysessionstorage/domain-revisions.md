---
title: "miniproto.session.storage.InMemorySessionStorage.domain_revisions"
description: "Return a detached revision mapping safe to inspect without locking callers."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.InMemorySessionStorage.domain_revisions"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L186"
aliases: ["miniproto.InMemorySessionStorage.domain_revisions","miniproto.session.InMemorySessionStorage.domain_revisions"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.InMemorySessionStorage.domain_revisions`

```python
domain_revisions() -> Mapping[str, int]
```

Return a detached revision mapping safe to inspect without locking callers.
