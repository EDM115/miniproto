---
title: "miniproto.crypto.mtproto.media_ctr_crypt"
description: "Apply AES-256-CTR to CDN/media bytes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.mtproto.media_ctr_crypt"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L160"
aliases: ["miniproto.crypto.media_ctr_crypt"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.media_ctr_crypt`

```python
media_ctr_crypt(data: BytesLike, key: bytes, iv: bytes) -> bytes
```

Apply AES-256-CTR to CDN/media bytes.

**Parameters:**

- **data** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Bytes to encrypt or decrypt; CTR uses the same operation both ways.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 16 bytes of counter/initialization value.

**Returns:**

- <code>[bytes](#bytes)</code> – Transformed bytes of the same length as ``data``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the key or IV length is invalid.

Reusing a key/IV pair across distinct plaintexts is unsafe; this wrapper does
not track nonce reuse.  Dispatch can prefer the C-backed fallback when
``cryptography`` is installed for the benchmarked media path.
