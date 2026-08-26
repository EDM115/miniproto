---
title: "miniproto.connection.framing.TransportErrorFrame"
description: "A negative MTProto transport error code decoded from a frame."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.framing.TransportErrorFrame"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L52"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.TransportErrorFrame`

```python
TransportErrorFrame(code: int) -> None
```

A negative MTProto transport error code decoded from a frame.

**Parameters:**

- **code** (<code>[int](#int)</code>) – Signed protocol error code. The transport converts this to a
domain exception before exposing a received payload to callers.
