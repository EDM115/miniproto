---
title: "miniproto.auth.key_exchange.DHGenOk"
description: "``dh_gen_ok`` response containing the first new-nonce hash."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.DHGenOk"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L391"
aliases: ["miniproto.auth.DHGenOk"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.DHGenOk`

```python
DHGenOk(nonce: int, server_nonce: int, new_nonce_hash1: int) -> None
```

``dh_gen_ok`` response containing the first new-nonce hash.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce echoed by Telegram.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce echoed by Telegram.
- **new_nonce_hash1** (<code>[int](#int)</code>) – Expected first confirmation hash for the new authorization key.
