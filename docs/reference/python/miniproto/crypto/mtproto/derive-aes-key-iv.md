---
title: "miniproto.crypto.mtproto.derive_aes_key_iv"
description: "Derive the AES-256 key and 32-byte IGE IV required by MTProto 2.0."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.mtproto.derive_aes_key_iv"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L85"
aliases: ["miniproto.crypto.derive_aes_key_iv"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.derive_aes_key_iv`

```python
derive_aes_key_iv(auth_key: bytes, msg_key: bytes, *, client_to_server: bool = True) -> tuple[bytes, bytes]
```

Derive the AES-256 key and 32-byte IGE IV required by MTProto 2.0.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – Exactly 256 bytes of authorization-key material.
- **msg_key** (<code>[bytes](#bytes)</code>) – Exactly 16 bytes produced for the same traffic direction.
- **client_to_server** (<code>[bool](#bool)</code>) – Selects the client-to-server offset by default; set false
for server-to-client traffic.

**Returns:**

- <code>[tuple](#tuple)[[bytes](#bytes), [bytes](#bytes)]</code> – A ``(key, iv)`` pair for AES-256-IGE.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the authorization key or message key has an invalid length.

Native and fallback implementations are output-compatible.  This only
derives material; it never transmits or clears the supplied key bytes.
