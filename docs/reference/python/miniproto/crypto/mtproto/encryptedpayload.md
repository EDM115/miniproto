---
title: "miniproto.crypto.mtproto.EncryptedPayload"
description: "MTProto payload components produced by :func:`encrypt_payload`."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.crypto.mtproto.EncryptedPayload"
source_path: "src/miniproto/crypto/mtproto.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/mtproto.py#L31"
aliases: ["miniproto.crypto.EncryptedPayload"]
module: "miniproto.crypto.mtproto"
---

## `miniproto.crypto.mtproto.EncryptedPayload`

```python
EncryptedPayload(auth_key_id: bytes, msg_key: bytes, ciphertext: bytes) -> None
```

MTProto payload components produced by :func:`encrypt_payload`.

**Attributes:**

- [**auth_key_id**](#miniproto.crypto.mtproto.EncryptedPayload.auth_key_id) (<code>[bytes](#bytes)</code>) – The trailing eight bytes of SHA-1 over the 256-byte auth key.
- [**msg_key**](#miniproto.crypto.mtproto.EncryptedPayload.msg_key) (<code>[bytes](#bytes)</code>) – The 16-byte direction-dependent MTProto message key.
- [**ciphertext**](#miniproto.crypto.mtproto.EncryptedPayload.ciphertext) (<code>[bytes](#bytes)</code>) – AES-256-IGE ciphertext for the padded plaintext.
