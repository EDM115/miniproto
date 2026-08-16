---
title: "miniproto.session.storage.EncryptedSQLiteSessionStorage.save"
description: "Atomically replace changed encrypted domains on a worker thread."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.EncryptedSQLiteSessionStorage.save"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L294"
aliases: ["miniproto.EncryptedSQLiteSessionStorage.save","miniproto.session.EncryptedSQLiteSessionStorage.save"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.EncryptedSQLiteSessionStorage.save`

```python
save(data: SessionPayload) -> None
```

Atomically replace changed encrypted domains on a worker thread.

**Parameters:**

- **data** (<code>[SessionPayload](#miniproto.session.storage.SessionPayload)</code>) – Session mapping or typed record to serialize and protect.
