---
title: "miniproto.connection.sender.MTProtoSender.disconnect"
description: "Stop background tasks, close the transport, and fail unresolved requests."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.sender.MTProtoSender.disconnect"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L300"
aliases: ["miniproto.connection.MTProtoSender.disconnect"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender.disconnect`

```python
disconnect() -> None
```

Stop background tasks, close the transport, and fail unresolved requests.

This is the terminal lifecycle action for this connection instance until
a later :meth:`connect` call. Pending request futures receive
:class:`TransportClosed`; cancellation of owned tasks is awaited.
