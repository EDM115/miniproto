---
title: "miniproto.connection.sender.MTProtoSender.acked"
description: "Return whether Telegram has sent a ``msgs_ack`` containing ``msg_id``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.sender.MTProtoSender.acked"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L575"
aliases: ["miniproto.connection.MTProtoSender.acked"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender.acked`

```python
acked(msg_id: int) -> bool
```

Return whether Telegram has sent a ``msgs_ack`` containing ``msg_id``.

**Parameters:**

- **msg_id** (<code>[int](#int)</code>) – Outgoing MTProto message ID to look up in received ACKs.
