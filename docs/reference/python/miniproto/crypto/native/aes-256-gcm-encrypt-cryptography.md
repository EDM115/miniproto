---
title: "miniproto.crypto.native.aes_256_gcm_encrypt_cryptography"
description: "Encrypt and authenticate with the explicit ``cryptography`` AES-GCM path."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_gcm_encrypt_cryptography"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L1048"
aliases: ["miniproto.crypto.aes_256_gcm_encrypt_cryptography"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_gcm_encrypt_cryptography`

```python
aes_256_gcm_encrypt_cryptography(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes
```

Encrypt and authenticate with the explicit ``cryptography`` AES-GCM path.

**Parameters:**

- **plaintext** (<code>[bytes](#bytes)</code>) – Bytes to protect.
- **key** (<code>[bytes](#bytes)</code>) – AES-256 key material accepted by ``cryptography``.
- **nonce** (<code>[bytes](#bytes)</code>) – Nonce bytes accepted by ``cryptography``; use a unique 12-byte nonce
for interoperable native parity.
- **associated_data** (<code>[bytes](#bytes)</code>) – Authenticated but unencrypted bytes.

**Returns:**

- <code>[bytes](#bytes)</code> – Ciphertext with its appended authentication tag.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``cryptography`` rejects the inputs.

This explicitly bypasses Rust.  It does not track nonce reuse or clear secret
buffers.
