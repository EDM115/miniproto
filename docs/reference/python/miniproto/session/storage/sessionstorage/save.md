---
title: "miniproto.session.storage.SessionStorage.save"
description: "Replace stored state using a detached copy of ``data``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.SessionStorage.save"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L69"
aliases: ["miniproto.SessionStorage.save","miniproto.session.SessionStorage.save"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.SessionStorage.save`

```python
save(data: SessionPayload) -> None
```

Replace stored state using a detached copy of ``data``.

**Parameters:**

- **data** (<code>[SessionPayload](#miniproto.session.storage.SessionPayload)</code>) – Session mapping or typed record to persist.
