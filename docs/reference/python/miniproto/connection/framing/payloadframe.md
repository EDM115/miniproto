---
title: "miniproto.connection.framing.PayloadFrame"
description: "A decoded MTProto transport payload."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.framing.PayloadFrame"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L25"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.PayloadFrame`

```python
PayloadFrame(payload: bytes, quick_ack_requested: bool = False) -> None
```

A decoded MTProto transport payload.

**Parameters:**

- **payload** (<code>[bytes](#bytes)</code>) – Complete MTProto packet bytes with transport framing removed.
- **quick_ack_requested** (<code>[bool](#bool)</code>) – Whether a server-side decoder observed the peer's
request for a transport-level quick acknowledgement.
