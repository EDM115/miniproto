---
title: "miniproto.crypto.native.aes_256_gcm_decrypt"
description: "Authenticate and decrypt AES-256-GCM session bytes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_gcm_decrypt"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L901"
aliases: ["miniproto.crypto.aes_256_gcm_decrypt"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_gcm_decrypt`

```python
aes_256_gcm_decrypt(ciphertext_and_tag: bytes, key: bytes, nonce: bytes, associated_data: bytes) -> bytes
```

Authenticate and decrypt AES-256-GCM session bytes.

**Parameters:**

- **ciphertext_and_tag** (<code>[bytes](#bytes)</code>) – Ciphertext with its appended 16-byte GCM tag.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **nonce** (<code>[bytes](#bytes)</code>) – Exactly 12 bytes used for encryption.
- **associated_data** (<code>[bytes](#bytes)</code>) – The exact authenticated but unencrypted bytes.

**Returns:**

- <code>[bytes](#bytes)</code> – Verified plaintext.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the key/nonce is invalid or tag authentication fails.

Selects Rust only if its optional session-crypto capability is available,
otherwise ``cryptography``.  Never use returned plaintext after an error.
