---
title: "miniproto.connection.sender.SenderState"
description: "Snapshot of sender liveness and pending RPC capacity."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.sender.SenderState"
source_path: "src/miniproto/connection/sender.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/sender.py#L137"
aliases: ["miniproto.connection.SenderState"]
module: "miniproto.connection.sender"
---

## `miniproto.connection.sender.SenderState`

```python
SenderState(pending_count: int, connected: bool, receive_task_done: bool) -> None
```

Snapshot of sender liveness and pending RPC capacity.

**Parameters:**

- **pending_count** (<code>[int](#int)</code>) – Reserved request slots, including requests awaiting send.
- **connected** (<code>[bool](#bool)</code>) – Whether transport and receive-loop tasks are both live.
- **receive_task_done** (<code>[bool](#bool)</code>) – Whether no receive loop exists or the current one has
finished.
