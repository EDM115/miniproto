---
title: "miniproto.auth.key_exchange.public_rsa_fingerprint"
description: "Calculate Telegram's signed little-endian 64-bit RSA fingerprint."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.public_rsa_fingerprint"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L682"
aliases: ["miniproto.auth.public_rsa_fingerprint"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.public_rsa_fingerprint`

```python
public_rsa_fingerprint(key: RSAKey) -> int
```

Calculate Telegram's signed little-endian 64-bit RSA fingerprint.

**Parameters:**

- **key** (<code>[RSAKey](#miniproto.auth.key_exchange.RSAKey)</code>) – RSA public key whose minimal modulus and exponent are fingerprinted.
