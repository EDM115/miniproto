---
title: "miniproto.session.storage.SessionStorage.domain_revisions"
description: "Return detached, instance-local change counters per logical domain."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.storage.SessionStorage.domain_revisions"
source_path: "src/miniproto/session/storage.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/storage.py#L90"
aliases: ["miniproto.SessionStorage.domain_revisions","miniproto.session.SessionStorage.domain_revisions"]
module: "miniproto.session.storage"
---

## `miniproto.session.storage.SessionStorage.domain_revisions`

```python
domain_revisions() -> Mapping[str, int]
```

Return detached, instance-local change counters per logical domain.

Counters increase after logical changes through this instance. They are neither persisted nor a signal of writes through other storage instances.
