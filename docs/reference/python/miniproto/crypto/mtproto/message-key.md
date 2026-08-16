---
title: "miniproto.crypto.mtproto.message_key"
description: "Derive the 16-byte MTProto 2.0 message key."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.mtproto.message_key"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L64"
aliases: ["miniproto.crypto.message_key"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.message_key`

```python
message_key(auth_key: bytes, plaintext_with_padding: BytesLike, *, client_to_server: bool = True) -> bytes
```

Derive the 16-byte MTProto 2.0 message key.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – Exactly 256 bytes of authorization-key material.
- **plaintext_with_padding** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Complete plaintext including valid MTProto padding.
- **client_to_server** (<code>[bool](#bool)</code>) – Uses the client-to-server offset when true (the default);
false selects the server-to-client offset.

**Returns:**

- <code>[bytes](#bytes)</code> – The direction-bound message key used for AES key and IV derivation.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``auth_key`` has an invalid length.

This deterministic derivation does not validate the supplied padding; use
:func:`encrypt_payload` to create a complete encrypted payload.
