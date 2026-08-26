---
title: "miniproto.crypto.mtproto.auth_key_id"
description: "Return the MTProto auth-key identifier."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.mtproto.auth_key_id"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L46"
aliases: ["miniproto.crypto.auth_key_id"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.auth_key_id`

```python
auth_key_id(auth_key: bytes) -> bytes
```

Return the MTProto auth-key identifier.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – Exactly 256 bytes of MTProto authorization-key material.

**Returns:**

- <code>[bytes](#bytes)</code> – The eight-byte SHA-1-derived key identifier.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``auth_key`` is not exactly 256 bytes.

The selected backend preserves this result; this wrapper intentionally has
no distinct cryptographic state or GIL behavior.
