---
title: "miniproto.auth.key_exchange.server_salt"
description: "Derive the MTProto server salt by XORing the first nonce bytes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.server_salt"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L888"
aliases: ["miniproto.auth.server_salt"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.server_salt`

```python
server_salt(new_nonce: int, server_nonce: int) -> int
```

Derive the MTProto server salt by XORing the first nonce bytes.

**Parameters:**

- **new_nonce** (<code>[int](#int)</code>) – Fresh client nonce from the active exchange.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce from the active exchange.
