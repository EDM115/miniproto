---
title: "miniproto.crypto.native.aes_256_ctr_crypt"
description: "Apply AES-256-CTR to bytes for encryption or decryption."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.aes_256_ctr_crypt"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L832"
aliases: ["miniproto.crypto.aes_256_ctr_crypt"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.aes_256_ctr_crypt`

```python
aes_256_ctr_crypt(data: BytesLike, key: bytes, iv: bytes) -> bytes
```

Apply AES-256-CTR to bytes for encryption or decryption.

**Parameters:**

- **data** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Input bytes of any length.
- **key** (<code>[bytes](#bytes)</code>) – Exactly 32 bytes of AES-256 key material.
- **iv** (<code>[bytes](#bytes)</code>) – Exactly 16 bytes of counter/initialization value.

**Returns:**

- <code>[bytes](#bytes)</code> – Transformed bytes of the same length.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the key or IV length is invalid.

CTR is symmetric and does not authenticate input.  Never reuse the same key
and IV for different plaintexts; this wrapper does not enforce uniqueness.
With ``cryptography`` installed, the benchmarked C-backed fallback is chosen.
