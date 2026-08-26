---
title: "miniproto.crypto.native.sha256_digest"
description: "Compute a SHA-256 digest."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.sha256_digest"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L566"
aliases: ["miniproto.crypto.sha256_digest"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.sha256_digest`

```python
sha256_digest(data: bytes) -> bytes
```

Compute a SHA-256 digest.

**Parameters:**

- **data** (<code>[bytes](#bytes)</code>) – Input bytes to hash.

**Returns:**

- <code>[bytes](#bytes)</code> – The 32-byte digest.

This public helper uses the Python stdlib fallback so its behavior and
performance do not imply Rust dispatch.
