---
title: "miniproto.invoke.clear_invalid_auth_key"
description: "Atomically clear rejected origin credentials, preserving replacements and unrelated DCs."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.clear_invalid_auth_key"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L578"
module: "miniproto.invoke"
---

## `miniproto.invoke.clear_invalid_auth_key`

```python
clear_invalid_auth_key(storage: SessionStorage, config: ClientConfig, *, expected_auth_key: AuthKey | None = None) -> None
```

Atomically clear rejected origin credentials, preserving replacements and unrelated DCs.

**Parameters:**

- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Session storage to mutate.
- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Supplies the fallback DC when parsing a legacy session mapping.
- **expected_auth_key** (<code>[AuthKey](#miniproto.session.models.AuthKey) | None</code>) – Rejected key and owning DC to compare atomically. Omission explicitly clears the current primary key and user without comparing provenance.
