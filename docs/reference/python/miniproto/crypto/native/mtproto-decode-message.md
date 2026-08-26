---
title: "miniproto.crypto.native.mtproto_decode_message"
description: "Decrypt, authenticate and parse an MTProto encrypted message."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.crypto.native.mtproto_decode_message"
source_path: "src/miniproto/crypto/native.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/crypto/native.py#L736"
aliases: ["miniproto.crypto.mtproto_decode_message"]
module: "miniproto.crypto.native"
---

## `miniproto.crypto.native.mtproto_decode_message`

```python
mtproto_decode_message(auth_key: bytes, packet: BytesLike, *, client_to_server: bool = False) -> tuple[bytes, int, int, int, int, bytes, bytes]
```

Decrypt, authenticate and parse an MTProto encrypted message.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – Exactly 256 bytes of authorization-key material.
- **packet** (<code>[BytesLike](#miniproto.crypto.native.BytesLike)</code>) – Packet containing the 8-byte auth-key ID, 16-byte message key,
and block-aligned ciphertext.
- **client_to_server** (<code>[bool](#bool)</code>) – Defaults to false for inbound server-to-client packets.

**Returns:**

- <code>[tuple](#tuple)[[bytes](#bytes), [int](#int), [int](#int), [int](#int), [int](#int), [bytes](#bytes), [bytes](#bytes)]</code> – ``(auth_key_id, server_salt, session_id, msg_id, seq_no, body, padding)``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the packet is malformed, keys mismatch, lengths are
invalid or padding violates MTProto 2.0 constraints.

This checks the packet's auth-key identifier and message key, but transport
ordering, replay handling and message semantics remain the caller's job.
