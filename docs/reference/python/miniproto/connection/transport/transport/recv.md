---
title: "miniproto.connection.transport.Transport.recv"
description: "Return the next payload or quick acknowledgement in wire order."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.transport.Transport.recv"
source_path: "src/miniproto/connection/transport.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/transport.py#L86"
aliases: ["miniproto.connection.Transport.recv"]
module: "miniproto.connection.transport"
---

## `miniproto.connection.transport.Transport.recv`

```python
recv() -> bytes | QuickAckFrame
```

Return the next payload or quick acknowledgement in wire order.

One task must own receiving: ``asyncio.StreamReader`` rejects concurrent
reads on the same stream, so implementations cannot safely multiplex
simultaneous ``recv`` calls.
