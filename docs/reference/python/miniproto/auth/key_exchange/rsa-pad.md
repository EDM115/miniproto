---
title: "miniproto.auth.key_exchange.rsa_pad"
description: "Apply Telegram's randomized RSA_PAD encryption to a small inner payload."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.rsa_pad"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L743"
aliases: ["miniproto.auth.rsa_pad"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.rsa_pad`

```python
rsa_pad(data: bytes, key: RSAKey, *, random_bytes: Callable[[int], bytes] | None = None) -> bytes
```

Apply Telegram's randomized RSA_PAD encryption to a small inner payload.

**Parameters:**

- **data** (<code>[bytes](#bytes)</code>) – Plaintext inner data no longer than 144 bytes.
- **key** (<code>[RSAKey](#miniproto.auth.key_exchange.RSAKey)</code>) – Trusted server RSA public key.
- **random_bytes** (<code>[Callable](#collections.abc.Callable)[[[int](#int)], [bytes](#bytes)] | None</code>) – Secure random source for padding and temporary AES key material.

**Returns:**

- <code>[bytes](#bytes)</code> – A 256-byte RSA ciphertext below the server modulus.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the input is oversized or no valid padded integer is produced in 32 attempts.
