---
title: "miniproto.auth.key_exchange.DHGenRetry"
description: "``dh_gen_retry`` response containing the second new-nonce hash."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.DHGenRetry"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L406"
aliases: ["miniproto.auth.DHGenRetry"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.DHGenRetry`

```python
DHGenRetry(nonce: int, server_nonce: int, new_nonce_hash2: int) -> None
```

``dh_gen_retry`` response containing the second new-nonce hash.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce echoed by Telegram.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce echoed by Telegram.
- **new_nonce_hash2** (<code>[int](#int)</code>) – Second confirmation hash indicating Telegram requests a retry.
