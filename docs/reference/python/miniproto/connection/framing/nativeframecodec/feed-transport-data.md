---
title: "miniproto.connection.framing.NativeFrameCodec.feed_transport_data"
description: "Decode native client-side transport events without payload wrappers."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.NativeFrameCodec.feed_transport_data"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L470"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.NativeFrameCodec.feed_transport_data`

```python
feed_transport_data(data: bytes | bytearray | memoryview) -> tuple[bytes | QuickAckFrame | TransportErrorFrame, ...]
```

Decode native client-side transport events without payload wrappers.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [bytearray](#bytearray) | [memoryview](#memoryview)</code>) – Client-side transport bytes that may end in an incomplete
frame.

**Raises:**

- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If the backend rejects invalid framing under the
same rules as the Python codec.
