---
title: "miniproto.crypto.mtproto.media_cbc_decrypt"
description: "Decrypt block-aligned AES-256-CBC media data without unpadding it."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.mtproto.media_cbc_decrypt"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L201"
aliases: ["miniproto.crypto.media_cbc_decrypt"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.media_cbc_decrypt`

```python
media_cbc_decrypt(ciphertext: BytesLike, key: bytes, iv: bytes) -> bytes
```

Decrypt block-aligned AES-256-CBC media data without unpadding it.

**Parameters:**

- **ciphertext** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Bytes whose length is a multiple of 16.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 16 bytes of initialization value.

**Returns:**

- <code>[bytes](#bytes)</code> – The raw decrypted bytes.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If key/IV lengths or block alignment are invalid.

CBC decryption here supplies confidentiality transformation only; it does not
authenticate the input.  Validate integrity at the protocol layer.
