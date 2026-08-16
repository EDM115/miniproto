---
title: "miniproto.connection.framing.TransportFrameCodec.encode_packet"
description: "Frame a bounded payload, optionally marking it for a quick ACK."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.TransportFrameCodec.encode_packet"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L70"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.TransportFrameCodec.encode_packet`

```python
encode_packet(payload: bytes, *, quick_ack: bool = False) -> bytes
```

Frame a bounded payload, optionally marking it for a quick ACK.

**Parameters:**

- **payload** (<code>[bytes](#bytes)</code>) – Unframed MTProto packet bytes to place on the wire.
- **quick_ack** (<code>[bool](#bool)</code>) – Whether to set the mode-specific quick-ACK request flag.
