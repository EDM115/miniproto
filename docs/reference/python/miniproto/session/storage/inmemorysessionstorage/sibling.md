---
title: "miniproto.session.storage.InMemorySessionStorage.sibling"
description: "Return a stable independent named in-memory sibling storage."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.InMemorySessionStorage.sibling"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L119"
aliases: ["miniproto.InMemorySessionStorage.sibling","miniproto.session.InMemorySessionStorage.sibling"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.InMemorySessionStorage.sibling`

```python
sibling(name: str) -> InMemorySessionStorage
```

Return a stable independent named in-memory sibling storage.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the portable sibling name contains unsafe characters.

**Parameters:**

- **name** (<code>[str](#str)</code>) – Portable sibling identifier used as the stable lookup key.
