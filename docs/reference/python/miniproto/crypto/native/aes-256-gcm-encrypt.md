---
title: "miniproto.crypto.native.aes_256_gcm_encrypt"
description: "Encrypt and authenticate session bytes with AES-256-GCM."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_gcm_encrypt"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L875"
aliases: ["miniproto.crypto.aes_256_gcm_encrypt"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_gcm_encrypt`

```python
aes_256_gcm_encrypt(plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes
```

Encrypt and authenticate session bytes with AES-256-GCM.

**Parameters:**

- **plaintext** (<code>[bytes](#bytes)</code>) – Bytes to protect.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **nonce** (<code>[bytes](#bytes)</code>) – Exactly 12 bytes and unique for this key.
- **associated_data** (<code>[bytes](#bytes)</code>) – Authenticated but unencrypted bytes.

**Returns:**

- <code>[bytes](#bytes)</code> – Ciphertext followed by the 16-byte GCM authentication tag.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the key or nonce is invalid, or the backend rejects
encryption.

Uses Rust only when that optional session-crypto symbol exists; otherwise
uses ``cryptography``.  Both routes preserve the same wire result.  Nonce
uniqueness remains a caller requirement and is not tracked here.
