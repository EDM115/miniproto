---
title: "miniproto.session.storage.EncryptedSQLiteSessionStorage.load"
description: "Load and authenticate a detached session snapshot on a worker thread."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.EncryptedSQLiteSessionStorage.load"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L276"
aliases: ["miniproto.EncryptedSQLiteSessionStorage.load","miniproto.session.EncryptedSQLiteSessionStorage.load"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.EncryptedSQLiteSessionStorage.load`

```python
load() -> Mapping[str, Any] | None
```

Load and authenticate a detached session snapshot on a worker thread.

**Raises:**

- <code>[SessionEnvelopeError](#miniproto.errors.SessionEnvelopeError)</code> – If encrypted content cannot be authenticated or decoded.
- <code>[SessionStorageError](#miniproto.errors.SessionStorageError)</code> – If SQLite loading fails or storage is closed.
