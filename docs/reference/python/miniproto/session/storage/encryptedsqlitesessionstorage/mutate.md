---
title: "miniproto.session.storage.EncryptedSQLiteSessionStorage.mutate"
description: "Atomically transform detached state under SQLite's write transaction."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.EncryptedSQLiteSessionStorage.mutate"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L310"
aliases: ["miniproto.EncryptedSQLiteSessionStorage.mutate","miniproto.session.EncryptedSQLiteSessionStorage.mutate"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.EncryptedSQLiteSessionStorage.mutate`

```python
mutate(transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]) -> Mapping[str, Any] | None
```

Atomically transform detached state under SQLite's write transaction.

The transform must be synchronous; it executes while the backend lock and
``BEGIN IMMEDIATE`` transaction ensure no lost update.

**Parameters:**

- **transform** (<code>[Callable](#collections.abc.Callable)[[[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None], [SessionPayload](#miniproto.session.storage.SessionPayload) | None]</code>) – Synchronous callback receiving a detached current snapshot.
