---
title: "miniproto.crypto.native.aes_256_cbc_encrypt"
description: "Encrypt block-aligned bytes with AES-256-CBC."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_cbc_encrypt"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L856"
aliases: ["miniproto.crypto.aes_256_cbc_encrypt"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_cbc_encrypt`

```python
aes_256_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes
```

Encrypt block-aligned bytes with AES-256-CBC.

**Parameters:**

- **plaintext** (<code>[bytes](#bytes)</code>) – Bytes whose length is a multiple of 16; no padding is added.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 16 bytes of initialization value.

**Returns:**

- <code>[bytes](#bytes)</code> – Ciphertext equal in length to ``plaintext``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If key/IV lengths or block alignment are invalid.

The caller owns padding and IV uniqueness.  CBC has no authenticity here;
dispatch prefers ``cryptography`` when available for the measured media path.
