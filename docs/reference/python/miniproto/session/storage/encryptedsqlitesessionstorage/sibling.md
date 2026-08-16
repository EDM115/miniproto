---
title: "miniproto.session.storage.EncryptedSQLiteSessionStorage.sibling"
description: "Create an independent sibling database that reuses derived secret keys."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.EncryptedSQLiteSessionStorage.sibling"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L244"
aliases: ["miniproto.EncryptedSQLiteSessionStorage.sibling","miniproto.session.EncryptedSQLiteSessionStorage.sibling"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.EncryptedSQLiteSessionStorage.sibling`

```python
sibling(name: str) -> EncryptedSQLiteSessionStorage
```

Create an independent sibling database that reuses derived secret keys.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``name`` contains unsafe path characters.

**Parameters:**

- **name** (<code>[str](#str)</code>) – Portable suffix used to construct the sibling database filename.
