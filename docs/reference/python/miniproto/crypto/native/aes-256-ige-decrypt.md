---
title: "miniproto.crypto.native.aes_256_ige_decrypt"
description: "Decrypt block-aligned AES-256-IGE bytes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_ige_decrypt"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L812"
aliases: ["miniproto.crypto.aes_256_ige_decrypt"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_ige_decrypt`

```python
aes_256_ige_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes
```

Decrypt block-aligned AES-256-IGE bytes.

**Parameters:**

- **ciphertext** (<code>[bytes](#bytes)</code>) – Bytes whose length is a multiple of 16.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes in IGE chaining order.

**Returns:**

- <code>[bytes](#bytes)</code> – Raw plaintext equal in length to ``ciphertext``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If key/IV lengths or block alignment are invalid.

Decryption alone does not authenticate arbitrary ciphertext; the MTProto
message-key verification wrapper provides the construction-specific check.
