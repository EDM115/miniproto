---
title: "miniproto.crypto.native.scrypt_derive_native"
description: "Derive Scrypt key material through explicit compiled Rust support."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.scrypt_derive_native"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L1022"
aliases: ["miniproto.crypto.scrypt_derive_native"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.scrypt_derive_native`

```python
scrypt_derive_native(password: bytes, salt: bytes, n: int, r: int, p: int, length: int) -> bytes
```

Derive Scrypt key material through explicit compiled Rust support.

**Parameters:**

- **password** (<code>[bytes](#bytes)</code>) – Secret input bytes.
- **salt** (<code>[bytes](#bytes)</code>) – Caller-selected salt bytes.
- **n** (<code>[int](#int)</code>) – Power-of-two CPU/memory cost greater than one.
- **r** (<code>[int](#int)</code>) – Block-size cost parameter.
- **p** (<code>[int](#int)</code>) – Parallelization cost parameter.
- **length** (<code>[int](#int)</code>) – Requested output length.

**Returns:**

- <code>[bytes](#bytes)</code> – Derived key bytes.

**Raises:**

- <code>[RuntimeError](#RuntimeError)</code> – If native Scrypt is unavailable.
- <code>[ValueError](#ValueError)</code> – If Scrypt parameters are invalid.

This no-fallback variant enforces the public resource limits before requiring
the compiled capability.
