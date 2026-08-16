---
title: "miniproto.mtproto.codec.encode_ping_delay_disconnect"
description: "Encode an MTProto ``ping_delay_disconnect`` service body."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.encode_ping_delay_disconnect"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L631"
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.encode_ping_delay_disconnect`

```python
encode_ping_delay_disconnect(ping_id: int, disconnect_delay: int) -> bytes
```

Encode an MTProto ``ping_delay_disconnect`` service body.

**Parameters:**

- **ping_id** (<code>[int](#int)</code>) – Caller-chosen 64-bit ping correlation ID.
- **disconnect_delay** (<code>[int](#int)</code>) – Requested disconnect-delay seconds.

**Returns:**

- <code>[bytes](#bytes)</code> – Constructor-prefixed service-body bytes.
