---
title: "miniproto.session.storage.SessionStorage.close"
description: "Close this storage instance to later load, save, mutate and clear operations."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.SessionStorage.close"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L95"
aliases: ["miniproto.SessionStorage.close","miniproto.session.SessionStorage.close"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.SessionStorage.close`

```python
close() -> None
```

Close this storage instance to later load, save, mutate and clear operations.

``sibling`` and ``domain_revisions`` remain available after closure.
