---
title: "miniproto.mtproto.codec.decode_encrypted_message"
description: "Authenticate, decrypt, and parse one MTProto encrypted envelope."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.decode_encrypted_message"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L348"
aliases: ["miniproto.mtproto.decode_encrypted_message"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.decode_encrypted_message`

```python
decode_encrypted_message(auth_key: bytes, packet: ByteBuffer, *, client_to_server: bool = False) -> DecodedEncryptedMessage
```

Authenticate, decrypt, and parse one MTProto encrypted envelope.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – 256-byte MTProto authorization key.
- **packet** (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer)</code>) – Complete encrypted packet bytes.
- **client_to_server** (<code>[bool](#bool)</code>) – Direction used for message-key derivation; defaults to server-to-client.

**Returns:**

- <code>[DecodedEncryptedMessage](#miniproto.mtproto.codec.DecodedEncryptedMessage)</code> – Decrypted envelope fields with body and padding views.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the native codec rejects framing, key, or integrity data.
