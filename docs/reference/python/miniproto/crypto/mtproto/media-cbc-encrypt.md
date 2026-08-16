---
title: "miniproto.crypto.mtproto.media_cbc_encrypt"
description: "Encrypt block-aligned media data with AES-256-CBC."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.mtproto.media_cbc_encrypt"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L181"
aliases: ["miniproto.crypto.media_cbc_encrypt"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.media_cbc_encrypt`

```python
media_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes
```

Encrypt block-aligned media data with AES-256-CBC.

**Parameters:**

- **plaintext** (<code>[bytes](#bytes)</code>) – Bytes whose length is a multiple of 16; no padding is added.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 16 bytes of initialization value.

**Returns:**

- <code>[bytes](#bytes)</code> – CBC ciphertext equal in length to ``plaintext``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If key/IV lengths or block alignment are invalid.

The caller owns padding and IV uniqueness.  Backend selection is
output-compatible and may use ``cryptography`` rather than Rust.
