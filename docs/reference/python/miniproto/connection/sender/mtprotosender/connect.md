---
title: "miniproto.connection.sender.MTProtoSender.connect"
description: "Open the transport and start owned receive and keepalive tasks."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.sender.MTProtoSender.connect"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L269"
aliases: ["miniproto.connection.MTProtoSender.connect"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender.connect`

```python
connect() -> None
```

Open the transport and start owned receive and keepalive tasks.

Concurrent calls serialize on a lock; a call made while already healthy
is a no-op. A stored fatal receive-loop error is raised once and cleared
before a new connection is attempted.

**Raises:**

- <code>[BaseException](#BaseException)</code> – A remembered fatal receive-loop failure, or any error
raised while opening the configured transport.
