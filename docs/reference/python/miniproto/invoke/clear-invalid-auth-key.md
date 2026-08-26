---
title: "miniproto.invoke.clear_invalid_auth_key"
description: "Atomically clear an unusable persisted authorization key and user identity."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.clear_invalid_auth_key"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L560"
module: "miniproto.invoke"
---

## `miniproto.invoke.clear_invalid_auth_key`

```python
clear_invalid_auth_key(storage: SessionStorage, config: ClientConfig) -> None
```

Atomically clear an unusable persisted authorization key and user identity.

**Parameters:**

- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Session storage to mutate.
- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Supplies the fallback DC when parsing a legacy session mapping.
