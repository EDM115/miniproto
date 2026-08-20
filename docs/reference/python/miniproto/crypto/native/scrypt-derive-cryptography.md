---
title: "miniproto.crypto.native.scrypt_derive_cryptography"
description: "Derive Scrypt key material with the explicit ``cryptography`` backend."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.scrypt_derive_cryptography"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L1092"
aliases: ["miniproto.crypto.scrypt_derive_cryptography"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.scrypt_derive_cryptography`

```python
scrypt_derive_cryptography(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes
```

Derive Scrypt key material with the explicit ``cryptography`` backend.

**Parameters:**

- **password** (<code>[bytes](#bytes)</code>) – Secret input bytes.
- **salt** (<code>[bytes](#bytes)</code>) – Caller-selected salt bytes.
- **n** (<code>[int](#int)</code>) – Power-of-two CPU/memory cost.
- **r** (<code>[int](#int)</code>) – Block-size cost parameter.
- **p** (<code>[int](#int)</code>) – Parallelization cost parameter.
- **length** (<code>[int](#int)</code>) – Requested output length.

**Returns:**

- <code>[bytes](#bytes)</code> – Derived key bytes.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the backend rejects the Scrypt parameters.

This bypasses Rust while retaining the public parameter and resource limits;
salt generation and secret lifetime remain caller-owned.
