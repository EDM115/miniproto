---
title: "miniproto.crypto.native.aes_256_gcm_decrypt_cryptography"
description: "Authenticate and decrypt through the explicit ``cryptography`` AES-GCM path."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_gcm_decrypt_cryptography"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L1070"
aliases: ["miniproto.crypto.aes_256_gcm_decrypt_cryptography"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_gcm_decrypt_cryptography`

```python
aes_256_gcm_decrypt_cryptography(ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes
```

Authenticate and decrypt through the explicit ``cryptography`` AES-GCM path.

**Parameters:**

- **ciphertext_and_tag** (<code>[bytes](#bytes)</code>) – Ciphertext with its authentication tag.
- **key** (<code>[bytes](#bytes)</code>) – AES-256 key material accepted by ``cryptography``.
- **nonce** (<code>[bytes](#bytes)</code>) – The nonce used during encryption.
- **associated_data** (<code>[bytes](#bytes)</code>) – Exact associated data used during encryption.

**Returns:**

- <code>[bytes](#bytes)</code> – Verified plaintext.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If inputs are rejected or GCM authentication fails.

This explicitly bypasses Rust; discard all output state after an error.
