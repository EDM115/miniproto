---
title: "miniproto.mtproto.quick_ack.quick_ack_token"
description: "Derive Telegram's high-bit-set quick-ACK token for an encrypted packet."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.quick_ack.quick_ack_token"
source_path: "src/miniproto/mtproto/quick_ack.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/quick_ack.py#L10"
module: "miniproto.mtproto.quick_ack"
---

## `miniproto.mtproto.quick_ack.quick_ack_token`

```python
quick_ack_token(auth_key: bytes, encrypted_packet: bytes) -> int
```

Derive Telegram's high-bit-set quick-ACK token for an encrypted packet.

**Parameters:**

- **auth_key** (<code>[bytes](#bytes)</code>) – MTProto authorization key used for the packet.
- **encrypted_packet** (<code>[bytes](#bytes)</code>) – Complete encrypted MTProto packet bytes.

**Returns:**

- <code>[int](#int)</code> – The 32-bit quick-ACK token computed by the available native or fallback codec.

**Raises:**

- <code>[ValueError](#ValueError)</code> – The selected native or fallback codec rejects the authorization key or packet framing.
