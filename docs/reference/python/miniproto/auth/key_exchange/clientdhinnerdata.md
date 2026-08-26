---
title: "miniproto.auth.key_exchange.ClientDHInnerData"
description: "Client DH public value encrypted into ``set_client_DH_params``."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.ClientDHInnerData"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L346"
aliases: ["miniproto.auth.ClientDHInnerData"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ClientDHInnerData`

```python
ClientDHInnerData(nonce: int, server_nonce: int, retry_id: int, g_b: bytes) -> None
```

Client DH public value encrypted into ``set_client_DH_params``.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce for the active exchange.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce for the active exchange.
- **retry_id** (<code>[int](#int)</code>) – Telegram retry identifier; zero for the first attempt.
- **g_b** (<code>[bytes](#bytes)</code>) – Fixed-width big-endian client DH public value.
