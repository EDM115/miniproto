---
title: "miniproto.connection.framing.NativeFrameCodec.encode_packet"
description: "Return native-encoded framing, normalizing validation errors."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.NativeFrameCodec.encode_packet"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L427"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.NativeFrameCodec.encode_packet`

```python
encode_packet(payload: bytes, *, quick_ack: bool = False) -> bytes
```

Return native-encoded framing, normalizing validation errors.

**Parameters:**

- **payload** (<code>[bytes](#bytes)</code>) – Unframed MTProto packet bytes to encode.
- **quick_ack** (<code>[bool](#bool)</code>) – Whether to request a mode-supported quick ACK.

**Raises:**

- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If the backend rejects the same payload/framing
validity rules as the Python codec.
