---
title: "miniproto.crypto.native.aes_256_ige_encrypt"
description: "Encrypt block-aligned bytes with AES-256-IGE."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_ige_encrypt"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L769"
aliases: ["miniproto.crypto.aes_256_ige_encrypt"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_ige_encrypt`

```python
aes_256_ige_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes
```

Encrypt block-aligned bytes with AES-256-IGE.

**Parameters:**

- **plaintext** (<code>[bytes](#bytes)</code>) – Bytes whose length is a multiple of 16; no padding is added.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes: previous ciphertext followed by previous plaintext.

**Returns:**

- <code>[bytes](#bytes)</code> – Ciphertext equal in length to ``plaintext``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If key/IV lengths or block alignment are invalid.

This selects the loaded backend.  IGE supplies no standalone authentication;
use it only in the MTProto construction that defines its integrity checks.
