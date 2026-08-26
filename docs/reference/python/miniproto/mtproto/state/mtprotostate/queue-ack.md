---
title: "miniproto.mtproto.state.MTProtoState.queue_ack"
description: "Queue one message ID for a future ``msgs_ack`` body."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.queue_ack"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L186"
aliases: ["miniproto.mtproto.MTProtoState.queue_ack"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.queue_ack`

```python
queue_ack(msg_id: int) -> None
```

Queue one message ID for a future ``msgs_ack`` body.

**Parameters:**

- **msg_id** (<code>[int](#int)</code>) – Server message ID to acknowledge.
