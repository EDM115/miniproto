---
title: "miniproto.session.storage.SessionStorage.mutate"
description: "Atomically apply a synchronous transform to an isolated current snapshot."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.SessionStorage.mutate"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L77"
aliases: ["miniproto.SessionStorage.mutate","miniproto.session.SessionStorage.mutate"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.SessionStorage.mutate`

```python
mutate(transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]) -> Mapping[str, Any] | None
```

Atomically apply a synchronous transform to an isolated current snapshot.

**Parameters:**

- **transform** (<code>[Callable](#collections.abc.Callable)[[[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None], [SessionPayload](#miniproto.session.storage.SessionPayload) | None]</code>) – Synchronous callback receiving detached stored data and returning replacement data. Returning ``None`` clears the session.

**Returns:**

- <code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code> – A detached snapshot of the committed replacement, or ``None`` after clearing.
