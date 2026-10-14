---
title: "miniproto.auth.bootstrap.ensure_auth_key"
description: "Preserve an existing MTProto key or create and store one with DC options."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.bootstrap.ensure_auth_key"
source_path: "src/miniproto/auth/bootstrap.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/bootstrap.py#L99"
module: "miniproto.auth.bootstrap"
---

## `miniproto.auth.bootstrap.ensure_auth_key`

```python
ensure_auth_key(config: ClientConfig, storage: SessionStorage) -> None
```

Preserve an existing MTProto key or create and store one with DC options.

An existing key is retained without contacting Telegram to check its validity. When no key is present, perform the unencrypted authorization-key exchange, then atomically store its key, salt, server-time offset and selected data-center options.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client configuration, including target DC and test-mode selection.
- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Mutable session store to inspect and update.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the configured DC or Telegram key-exchange response is invalid.
- <code>[ConnectionError](#ConnectionError)</code> – If the unencrypted exchange receives an unexpected quick ACK.
