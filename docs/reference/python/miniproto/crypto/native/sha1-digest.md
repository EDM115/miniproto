---
title: "miniproto.crypto.native.sha1_digest"
description: "Compute a SHA-1 digest for MTProto compatibility."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.sha1_digest"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L546"
aliases: ["miniproto.crypto.sha1_digest"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.sha1_digest`

```python
sha1_digest(data: bytes) -> bytes
```

Compute a SHA-1 digest for MTProto compatibility.

**Parameters:**

- **data** (<code>[bytes](#bytes)</code>) – Input bytes to hash.

**Returns:**

- <code>[bytes](#bytes)</code> – The 20-byte digest.

This public hot path deliberately uses the C-backed stdlib fallback even
when Rust is loaded because that is benchmarked faster for its small inputs.
SHA-1 is exposed for MTProto protocol derivations, not as a general-purpose
modern integrity recommendation.
