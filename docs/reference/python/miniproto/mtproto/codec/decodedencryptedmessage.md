---
title: "miniproto.mtproto.codec.DecodedEncryptedMessage"
description: "Authenticated encrypted MTProto envelope with decrypted body and padding."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.DecodedEncryptedMessage"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L55"
aliases: ["miniproto.mtproto.DecodedEncryptedMessage"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.DecodedEncryptedMessage`

```python
DecodedEncryptedMessage(auth_key_id: bytes, server_salt: int, session_id: int, msg_id: int, seq_no: int, body: ByteBuffer, padding: ByteBuffer) -> None
```

Authenticated encrypted MTProto envelope with decrypted body and padding.

**Attributes:**

- [**auth_key_id**](#miniproto.mtproto.codec.DecodedEncryptedMessage.auth_key_id) (<code>[bytes](#bytes)</code>) – Eight-byte authorization-key identifier from the envelope.
- [**server_salt**](#miniproto.mtproto.codec.DecodedEncryptedMessage.server_salt) (<code>[int](#int)</code>) – Decrypted 64-bit server salt.
- [**session_id**](#miniproto.mtproto.codec.DecodedEncryptedMessage.session_id) (<code>[int](#int)</code>) – Decrypted 64-bit session ID.
- [**msg_id**](#miniproto.mtproto.codec.DecodedEncryptedMessage.msg_id) (<code>[int](#int)</code>) – MTProto message ID.
- [**seq_no**](#miniproto.mtproto.codec.DecodedEncryptedMessage.seq_no) (<code>[int](#int)</code>) – MTProto sequence number.
- [**body**](#miniproto.mtproto.codec.DecodedEncryptedMessage.body) (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer)</code>) – Decrypted message body view.
- [**padding**](#miniproto.mtproto.codec.DecodedEncryptedMessage.padding) (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer)</code>) – Decrypted trailing padding view.
