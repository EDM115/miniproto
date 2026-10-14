---
title: "miniproto.session.storage.EncryptedSQLiteSessionStorage.close"
description: "Mark storage closed under the backend lock, after any active locked operation."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.EncryptedSQLiteSessionStorage.close"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L368"
aliases: ["miniproto.EncryptedSQLiteSessionStorage.close","miniproto.session.EncryptedSQLiteSessionStorage.close"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.EncryptedSQLiteSessionStorage.close`

```python
close() -> None
```

Mark storage closed under the backend lock, after any active locked operation.

Workers that acquire the lock after closure fail, even if queued earlier. ``sibling`` and ``domain_revisions`` remain usable.
