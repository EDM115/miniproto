---
title: "miniproto.connection.framing.PythonFrameCodec.feed_data"
description: "Consume an arbitrary transport fragment and drain complete events."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.PythonFrameCodec.feed_data"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L144"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.PythonFrameCodec.feed_data`

```python
feed_data(data: bytes | bytearray | memoryview) -> tuple[FrameEvent, ...]
```

Consume an arbitrary transport fragment and drain complete events.

Incomplete trailing bytes remain buffered for the next call, so callers
may pass ordinary socket-read fragments without preserving boundaries.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [bytearray](#bytearray) | [memoryview](#memoryview)</code>) – Newly received wire bytes.

**Returns:**

- <code>[FrameEvent](#miniproto.connection.framing.FrameEvent)</code> – Every complete payload, quick-ACK or transport-error event decoded
- <code>...</code> – from the accumulated input, in wire order.

**Raises:**

- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If a complete header or frame is malformed or
exceeds the configured size bound.
