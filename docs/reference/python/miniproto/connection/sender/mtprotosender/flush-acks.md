---
title: "miniproto.connection.sender.MTProtoSender.flush_acks"
description: "Send currently queued acknowledgements, or return ``None`` when empty."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.sender.MTProtoSender.flush_acks"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L583"
aliases: ["miniproto.connection.MTProtoSender.flush_acks"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.MTProtoSender.flush_acks`

```python
flush_acks() -> int | None
```

Send currently queued acknowledgements, or return ``None`` when empty.

**Returns:**

- <code>[int](#int) | None</code> – The outgoing acknowledgement message ID, or ``None`` if there were
- <code>[int](#int) | None</code> – no pending acknowledgements to flush.

**Raises:**

- <code>[BaseException](#BaseException)</code> – Any send failure after restoring popped
acknowledgements to the state queue.
