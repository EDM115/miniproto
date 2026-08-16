---
title: "miniproto.auth.key_exchange.RSAKey.from_bytes"
description: "Create a key from unsigned big-endian modulus and exponent bytes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.RSAKey.from_bytes"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L67"
aliases: ["miniproto.auth.RSAKey.from_bytes"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.RSAKey.from_bytes`

```python
from_bytes(modulus: bytes, exponent: bytes) -> Self
```

Create a key from unsigned big-endian modulus and exponent bytes.

**Parameters:**

- **modulus** (<code>[bytes](#bytes)</code>) – Big-endian unsigned RSA modulus bytes.
- **exponent** (<code>[bytes](#bytes)</code>) – Big-endian unsigned RSA public exponent bytes.
