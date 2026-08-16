---
title: "miniproto.crypto.mtproto.encrypt_payload"
description: "Pad and AES-IGE-encrypt one MTProto payload."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.mtproto.encrypt_payload"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L106"
aliases: ["miniproto.crypto.encrypt_payload"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.encrypt_payload`

```python
encrypt_payload(auth_key: bytes, plaintext: BytesLike, *, client_to_server: bool = True, padding: bytes | None = None) -> EncryptedPayload
```

Pad and AES-IGE-encrypt one MTProto payload.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – Exactly 256 bytes of authorization-key material.
- **plaintext** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Unpadded MTProto payload bytes.
- **client_to_server** (<code>[bool](#bool)</code>) – Uses the client-to-server derivation direction by default.
- **padding** (<code>[bytes](#bytes) | None</code>) – Optional caller-provided random padding.  If omitted, this wrapper
obtains the minimum compliant length from ``os.urandom``.

**Returns:**

- <code>[EncryptedPayload](#miniproto.crypto.mtproto.EncryptedPayload)</code> – The key identifier, message key, and encrypted payload components.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If key length, padding length (12 through 1024 bytes), or final
AES block alignment is invalid.

The default only chooses a compliant padding length; callers who supply
``padding`` are responsible for its unpredictability.  Encryption backend
selection follows :mod:`miniproto.crypto.native` and does not change output
format.
