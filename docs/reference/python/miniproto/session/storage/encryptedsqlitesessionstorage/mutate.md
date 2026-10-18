---
title: "miniproto.session.storage.EncryptedSQLiteSessionStorage.mutate"
description: "Atomically transform detached state under SQLite's write transaction."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.EncryptedSQLiteSessionStorage.mutate"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L323"
aliases: ["miniproto.EncryptedSQLiteSessionStorage.mutate","miniproto.session.EncryptedSQLiteSessionStorage.mutate"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.EncryptedSQLiteSessionStorage.mutate`

```python
mutate(transform: Callable[[Mapping[str, Any] | None], SessionPayload | None]) -> Mapping[str, Any] | None
```

Atomically transform detached state under SQLite's write transaction.

The synchronous transform runs on a worker thread while the backend lock and ``BEGIN IMMEDIATE`` transaction prevent competing writes from losing updates.

**Parameters:**

- **transform** (<code>[Callable](#collections.abc.Callable)[[[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None], [SessionPayload](#miniproto.session.storage.SessionPayload) | None]</code>) – Synchronous callback receiving a detached current snapshot and returning replacement state, or ``None`` to clear it.

**Returns:**

- <code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code> – A detached committed snapshot or ``None`` after clearing.

**Raises:**

- <code>[TypeError](#TypeError)</code> – If the transform returns an awaitable or unsupported payload.
- <code>[SessionStorageError](#miniproto.errors.SessionStorageError)</code> – If storage is closed or a SQLite operation fails.
