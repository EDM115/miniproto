---
title: "miniproto.auth.key_exchange.ServerDHParamsOk"
description: "Successful ``server_DH_params_ok`` wrapper for encrypted DH parameters."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.ServerDHParamsOk"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L215"
aliases: ["miniproto.auth.ServerDHParamsOk"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ServerDHParamsOk`

```python
ServerDHParamsOk(nonce: int, server_nonce: int, encrypted_answer: bytes) -> None
```

Successful ``server_DH_params_ok`` wrapper for encrypted DH parameters.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce echoed by Telegram.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce echoed by Telegram.
- **encrypted_answer** (<code>[bytes](#bytes)</code>) – Temporary-AES-IGE encrypted ``server_DH_inner_data`` bytes.
