---
title: "miniproto.crypto.native.scrypt_derive"
description: "Derive key material with Scrypt through the available session backend."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.scrypt_derive"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L948"
aliases: ["miniproto.crypto.scrypt_derive"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.scrypt_derive`

```python
scrypt_derive(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes
```

Derive key material with Scrypt through the available session backend.

**Parameters:**

- **password** (<code>[bytes](#bytes)</code>) – Secret input bytes.
- **salt** (<code>[bytes](#bytes)</code>) – Caller-selected salt bytes.
- **n** (<code>[int](#int)</code>) – CPU/memory cost, which must be a power of two greater than one.
- **r** (<code>[int](#int)</code>) – Block-size cost parameter.
- **p** (<code>[int](#int)</code>) – Parallelization cost parameter.
- **length** (<code>[int](#int)</code>) – Requested output length.

**Returns:**

- <code>[bytes](#bytes)</code> – The derived key bytes.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If Scrypt parameters or output length are rejected.

Uses native Scrypt only when the optional symbol exists, otherwise
``cryptography``. Every route enforces the same 256 MiB memory estimate and
1 GiB aggregate work estimate before entering either backend.
