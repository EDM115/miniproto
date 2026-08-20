---
title: "miniproto.session.storage.InMemorySessionStorage.mutate"
description: "Run a synchronous transform atomically against an isolated snapshot."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.InMemorySessionStorage.mutate"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L162"
aliases: ["miniproto.InMemorySessionStorage.mutate","miniproto.session.InMemorySessionStorage.mutate"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.InMemorySessionStorage.mutate`

```python
mutate(transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]) -> Mapping[str, Any] | None
```

Run a synchronous transform atomically against an isolated snapshot.

Awaitable transforms are rejected so locks are never held across an await.

**Parameters:**

- **transform** (<code>[Callable](#collections.abc.Callable)[[[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None], [SessionPayload](#miniproto.session.storage.SessionPayload) | None]</code>) – Synchronous callback receiving a detached current snapshot.
