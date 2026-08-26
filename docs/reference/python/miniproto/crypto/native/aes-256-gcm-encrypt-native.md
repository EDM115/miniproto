---
title: "miniproto.crypto.native.aes_256_gcm_encrypt_native"
description: "Encrypt with the explicit compiled Rust AES-256-GCM capability."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_gcm_encrypt_native"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L976"
aliases: ["miniproto.crypto.aes_256_gcm_encrypt_native"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_gcm_encrypt_native`

```python
aes_256_gcm_encrypt_native(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes
```

Encrypt with the explicit compiled Rust AES-256-GCM capability.

**Parameters:**

- **plaintext** (<code>[bytes](#bytes)</code>) – Bytes to protect.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **nonce** (<code>[bytes](#bytes)</code>) – Exactly 12 unique bytes for this key.
- **associated_data** (<code>[bytes](#bytes)</code>) – Authenticated but unencrypted bytes.

**Returns:**

- <code>[bytes](#bytes)</code> – Ciphertext followed by the GCM tag.

**Raises:**

- <code>[RuntimeError](#RuntimeError)</code> – If native session AES-GCM is unavailable.
- <code>[ValueError](#ValueError)</code> – If cryptographic inputs are invalid.

Unlike :func:`aes_256_gcm_encrypt`, this never falls back.  It does not
manage nonce uniqueness or key lifetime.
