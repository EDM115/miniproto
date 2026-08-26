---
title: "miniproto.crypto.native.aes_256_cbc_decrypt"
description: "Decrypt block-aligned AES-256-CBC bytes without unpadding."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_cbc_decrypt"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L877"
aliases: ["miniproto.crypto.aes_256_cbc_decrypt"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_cbc_decrypt`

```python
aes_256_cbc_decrypt(ciphertext: BytesLike, key: bytes, iv: bytes) -> bytes
```

Decrypt block-aligned AES-256-CBC bytes without unpadding.

**Parameters:**

- **ciphertext** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Bytes whose length is a multiple of 16.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 16 bytes of initialization value.

**Returns:**

- <code>[bytes](#bytes)</code> – Raw plaintext equal in length to ``ciphertext``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If key/IV lengths or block alignment are invalid.

This operation does not authenticate ciphertext or validate a padding scheme;
callers must supply the applicable integrity and decoding checks.
