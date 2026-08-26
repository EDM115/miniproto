---
title: "miniproto.auth.key_exchange.SetClientDHParams"
description: "Serialized ``set_client_DH_params`` request carrying AES-IGE ciphertext."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.SetClientDHParams"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L367"
aliases: ["miniproto.auth.SetClientDHParams"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.SetClientDHParams`

```python
SetClientDHParams(nonce: int, server_nonce: int, encrypted_data: bytes) -> None
```

Serialized ``set_client_DH_params`` request carrying AES-IGE ciphertext.

**Parameters:**

- **nonce** (<code>[int](#int)</code>) – Client nonce for the active exchange.
- **server_nonce** (<code>[int](#int)</code>) – Server nonce for the active exchange.
- **encrypted_data** (<code>[bytes](#bytes)</code>) – Temporary-AES-IGE encrypted client DH inner payload.
