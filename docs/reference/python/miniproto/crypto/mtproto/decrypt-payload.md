---
title: "miniproto.crypto.mtproto.decrypt_payload"
description: "Verify an MTProto message key and decrypt its AES-IGE payload."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.mtproto.decrypt_payload"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L138"
aliases: ["miniproto.crypto.decrypt_payload"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.decrypt_payload`

```python
decrypt_payload(auth_key: bytes, msg_key: bytes, ciphertext: BytesLike, *, client_to_server: bool = False) -> bytes
```

Verify an MTProto message key and decrypt its AES-IGE payload.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – Exactly 256 bytes of authorization-key material.
- **msg_key** (<code>[bytes](#bytes)</code>) – The 16-byte packet message key.
- **ciphertext** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Block-aligned AES-IGE ciphertext.
- **client_to_server** (<code>[bool](#bool)</code>) – Defaults to false because received packets normally use
the server-to-client derivation direction.

**Returns:**

- <code>[bytes](#bytes)</code> – The complete plaintext, including MTProto padding.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If lengths are invalid or the recomputed ``msg_key`` differs.

Message-key comparison occurs in the selected backend; this function does
not parse the plaintext envelope or authenticate arbitrary transport data.
