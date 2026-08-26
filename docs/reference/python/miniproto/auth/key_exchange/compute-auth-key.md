---
title: "miniproto.auth.key_exchange.compute_auth_key"
description: "Compute the 256-byte MTProto key from validated DH peer and private values."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.compute_auth_key"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L851"
aliases: ["miniproto.auth.compute_auth_key"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.compute_auth_key`

```python
compute_auth_key(*, g_a: int, b: int, dh_prime: int) -> bytes
```

Compute the 256-byte MTProto key from validated DH peer and private values.

**Parameters:**

- **g_a** (<code>[int](#int)</code>) – Server DH public value as an integer.
- **b** (<code>[int](#int)</code>) – Positive client DH private exponent.
- **dh_prime** (<code>[int](#int)</code>) – DH modulus used for modular exponentiation.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the peer public value or private exponent is out of range.
