---
title: "miniproto.auth.key_exchange.ServerDHParamsFail"
description: "``server_DH_params_fail`` response proving Telegram rejected the request."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.ServerDHParamsFail"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L253"
aliases: ["miniproto.auth.ServerDHParamsFail"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ServerDHParamsFail`

```python
ServerDHParamsFail(nonce: int, server_nonce: int, new_nonce_hash: int) -> None
```

``server_DH_params_fail`` response proving Telegram rejected the request.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce echoed by Telegram.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce echoed by Telegram.
- **new_nonce_hash** (<code>[int](#int)</code>) – Telegram confirmation hash for the rejected exchange.
