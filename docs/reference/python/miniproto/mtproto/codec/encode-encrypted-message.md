---
title: "miniproto.mtproto.codec.encode_encrypted_message"
description: "Encrypt and frame one MTProto message using the configured authorization key."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.encode_encrypted_message"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L309"
aliases: ["miniproto.mtproto.encode_encrypted_message"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.encode_encrypted_message`

```python
encode_encrypted_message(auth_key: bytes, server_salt: int, session_id: int, msg_id: int, seq_no: int, body: bytes | object, *, client_to_server: bool = True, padding: bytes | None = None) -> bytes
```

Encrypt and frame one MTProto message using the configured authorization key.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – 256-byte MTProto authorization key.
- **server_salt** (<code>[int](#int)</code>) – Current 64-bit server salt.
- **session_id** (<code>[int](#int)</code>) – Current 64-bit session ID.
- **msg_id** (<code>[int](#int)</code>) – MTProto message identifier.
- **seq_no** (<code>[int](#int)</code>) – MTProto sequence number.
- **body** (<code>[bytes](#bytes) | [object](#object)</code>) – Raw or supported encoded body.
- **client_to_server** (<code>[bool](#bool)</code>) – Use client-to-server derivation, defaulting to ``True``.
- **padding** (<code>[bytes](#bytes) | None</code>) – Optional explicit padding; native codec chooses valid padding when omitted.

**Returns:**

- <code>[bytes](#bytes)</code> – Complete encrypted MTProto packet bytes.
