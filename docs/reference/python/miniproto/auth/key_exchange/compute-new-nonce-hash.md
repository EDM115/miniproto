---
title: "miniproto.auth.key_exchange.compute_new_nonce_hash"
description: "Compute Telegram's keyed new-nonce confirmation hash number 1, 2, or 3."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.compute_new_nonce_hash"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L870"
aliases: ["miniproto.auth.compute_new_nonce_hash"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.compute_new_nonce_hash`

```python
compute_new_nonce_hash(new_nonce: int, auth_key: bytes, number: int) -> int
```

Compute Telegram's keyed new-nonce confirmation hash number 1, 2, or 3.

**Parameters:**

- **new_nonce** (<code>[int](#int)</code>) – Fresh client nonce from the active exchange.
- **auth_key** (<code>[bytes](#bytes)</code>) – Newly derived MTProto authorization key bytes.
- **number** (<code>[int](#int)</code>) – Telegram confirmation-hash selector, restricted to 1, 2, or 3.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``number`` is not a Telegram-defined confirmation index.
