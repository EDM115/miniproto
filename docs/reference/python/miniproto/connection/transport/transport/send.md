---
title: "miniproto.connection.transport.Transport.send"
description: "Frame and send a payload, optionally requesting a quick acknowledgement."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.transport.Transport.send"
source_path: "src/miniproto/connection/transport.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/transport.py#L77"
aliases: ["miniproto.connection.Transport.send"]
module: "miniproto.connection.transport"
---

## `miniproto.connection.transport.Transport.send`

```python
send(payload: bytes, *, quick_ack: bool = False) -> None
```

Frame and send a payload, optionally requesting a quick acknowledgement.

**Parameters:**

- **payload** (<code>[bytes](#bytes)</code>) – Unframed bounded MTProto packet bytes to transmit.
- **quick_ack** (<code>[bool](#bool)</code>) – Whether to request a transport quick ACK for this packet.
