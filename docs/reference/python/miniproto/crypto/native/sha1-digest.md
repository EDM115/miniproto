---
title: "miniproto.crypto.native.sha1_digest"
description: "Compute a SHA-1 digest for MTProto compatibility."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.sha1_digest"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L534"
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

Uses the C-backed stdlib fallback even when Rust is loaded. SHA-1 is required by MTProto's protocol derivations.
