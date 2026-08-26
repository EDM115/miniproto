---
title: "miniproto.connection.framing.PythonFrameCodec.encode_packet"
description: "Return one complete framed packet."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.PythonFrameCodec.encode_packet"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L117"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.PythonFrameCodec.encode_packet`

```python
encode_packet(payload: bytes, *, quick_ack: bool = False) -> bytes
```

Return one complete framed packet.

**Parameters:**

- **payload** (<code>[bytes](#bytes)</code>) – Unframed MTProto packet bytes, bounded by the configured
maximum.
- **quick_ack** (<code>[bool](#bool)</code>) – Set the protocol quick-ACK-request bit where the chosen
transport mode permits it.

**Returns:**

- <code>[bytes](#bytes)</code> – Wire-ready framing bytes. Padded intermediate frames include zero to
- <code>[bytes](#bytes)</code> – fifteen random transport-padding bytes.

**Raises:**

- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If the payload is oversized or violates the mode's
alignment or encoding limits.
