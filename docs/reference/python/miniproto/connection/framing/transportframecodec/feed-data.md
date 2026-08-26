---
title: "miniproto.connection.framing.TransportFrameCodec.feed_data"
description: "Consume a byte fragment and return every complete decoded event."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.TransportFrameCodec.feed_data"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L79"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.TransportFrameCodec.feed_data`

```python
feed_data(data: bytes | bytearray | memoryview) -> tuple[FrameEvent, ...]
```

Consume a byte fragment and return every complete decoded event.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [bytearray](#bytearray) | [memoryview](#memoryview)</code>) – Newly received transport bytes, which may end mid-frame.
