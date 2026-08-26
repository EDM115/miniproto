---
title: "miniproto.crypto.native.aes_256_gcm_decrypt_native"
description: "Authenticate and decrypt with explicit compiled Rust AES-256-GCM."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_gcm_decrypt_native"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L999"
aliases: ["miniproto.crypto.aes_256_gcm_decrypt_native"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_gcm_decrypt_native`

```python
aes_256_gcm_decrypt_native(ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes
```

Authenticate and decrypt with explicit compiled Rust AES-256-GCM.

**Parameters:**

- **ciphertext_and_tag** (<code>[bytes](#bytes)</code>) – Ciphertext with its appended authentication tag.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **nonce** (<code>[bytes](#bytes)</code>) – Exactly 12 bytes used for encryption.
- **associated_data** (<code>[bytes](#bytes)</code>) – Exact associated data used for encryption.

**Returns:**

- <code>[bytes](#bytes)</code> – Verified plaintext.

**Raises:**

- <code>[RuntimeError](#RuntimeError)</code> – If native session AES-GCM is unavailable.
- <code>[ValueError](#ValueError)</code> – If inputs are invalid or authentication fails.

This no-fallback variant is suitable only when native capability is an
explicit requirement; do not consume plaintext when it raises.
