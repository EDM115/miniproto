---
title: "miniproto.connection.framing.NativeFrameCodec.feed_data"
description: "Decode native frame-pump events into the portable event types."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.NativeFrameCodec.feed_data"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L443"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.NativeFrameCodec.feed_data`

```python
feed_data(data: bytes | bytearray | memoryview) -> tuple[FrameEvent, ...]
```

Decode native frame-pump events into the portable event types.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [bytearray](#bytearray) | [memoryview](#memoryview)</code>) – Transport bytes that may contain any number of partial frames.

**Raises:**

- <code>[TransportError](#miniproto.connection.transport.TransportError)</code> – If the backend rejects invalid framing under the
same rules as the Python codec.
- <code>[RuntimeError](#RuntimeError)</code> – If the backend emits an unknown event kind.
