---
title: "miniproto.auth.key_exchange.DHGenFail"
description: "``dh_gen_fail`` response containing the third new-nonce hash."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.DHGenFail"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L421"
aliases: ["miniproto.auth.DHGenFail"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.DHGenFail`

```python
DHGenFail(nonce: int, server_nonce: int, new_nonce_hash3: int) -> None
```

``dh_gen_fail`` response containing the third new-nonce hash.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce echoed by Telegram.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce echoed by Telegram.
- **new_nonce_hash3** (<code>[int](#int)</code>) – Failure confirmation hash for the rejected key exchange.
