---
title: "miniproto.crypto.native.mtproto_encode_message"
description: "Build, pad and encrypt a complete MTProto encrypted message."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.mtproto_encode_message"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L672"
aliases: ["miniproto.crypto.mtproto_encode_message"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.mtproto_encode_message`

```python
mtproto_encode_message(auth_key: bytes, server_salt: int, session_id: int, msg_id: int, seq_no: int, body: BytesLike, *, client_to_server: bool = True, padding: bytes | None = None) -> bytes
```

Build, pad and encrypt a complete MTProto encrypted message.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – Exactly 256 bytes of authorization-key material.
- **server_salt** (<code>[int](#int)</code>) – Unsigned 64-bit salt.
- **session_id** (<code>[int](#int)</code>) – Unsigned 64-bit session identifier.
- **msg_id** (<code>[int](#int)</code>) – Signed 64-bit MTProto message identifier.
- **seq_no** (<code>[int](#int)</code>) – Signed 32-bit message sequence number.
- **body** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Four-byte-aligned TL body bytes no larger than the signed 32-bit protocol limit.
- **client_to_server** (<code>[bool](#bool)</code>) – Uses the client-to-server direction by default.
- **padding** (<code>[bytes](#bytes) | None</code>) – Optional compliant padding; when omitted the backend generates
random padding.

**Returns:**

- <code>[bytes](#bytes)</code> – The encrypted wire packet: auth-key ID, message key and ciphertext.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If key, body, padding or encrypted-layout constraints fail.
- <code>[OverflowError](#OverflowError)</code> – If ``msg_id`` or ``seq_no`` cannot be encoded, or native argument conversion rejects an out-of-range salt or session ID.

The selected backend supplies the random padding when omitted.
