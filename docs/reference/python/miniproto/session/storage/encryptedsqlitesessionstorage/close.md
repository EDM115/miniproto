---
title: "miniproto.session.storage.EncryptedSQLiteSessionStorage.close"
description: "Close load, save, mutate, and clear after queued worker work reaches the lock."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.EncryptedSQLiteSessionStorage.close"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L350"
aliases: ["miniproto.EncryptedSQLiteSessionStorage.close","miniproto.session.EncryptedSQLiteSessionStorage.close"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.EncryptedSQLiteSessionStorage.close`

```python
close() -> None
```

Close load, save, mutate, and clear after queued worker work reaches the lock.

``sibling`` and ``domain_revisions`` remain usable after closure.
