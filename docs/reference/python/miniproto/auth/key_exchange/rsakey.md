---
title: "miniproto.auth.key_exchange.RSAKey"
description: "Telegram RSA public key used to encrypt the ``req_DH_params`` payload."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.auth.key_exchange.RSAKey"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L55"
aliases: ["miniproto.auth.RSAKey"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.RSAKey`

```python
RSAKey(modulus: int, exponent: int) -> None
```

Telegram RSA public key used to encrypt the ``req_DH_params`` payload.

**Parameters:**

- **modulus** (<code>[int](#int)</code>) – RSA modulus as an unsigned integer.
- **exponent** (<code>[int](#int)</code>) – RSA public exponent as an unsigned integer.
