---
title: "miniproto.mtproto.state.MTProtoState.correct_time_offset_from_msg_id"
description: "Refresh the server-time offset and restart client message-ID monotonicity."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.correct_time_offset_from_msg_id"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L249"
aliases: ["miniproto.mtproto.MTProtoState.correct_time_offset_from_msg_id"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.correct_time_offset_from_msg_id`

```python
correct_time_offset_from_msg_id(msg_id: int) -> None
```

Refresh the server-time offset and restart client message-ID monotonicity.

**Parameters:**

- **msg_id** (<code>[int](#int)</code>) – Server message ID supplying the authoritative timestamp.
