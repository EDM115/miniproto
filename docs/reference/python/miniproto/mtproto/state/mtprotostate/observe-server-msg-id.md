---
title: "miniproto.mtproto.state.MTProtoState.observe_server_msg_id"
description: "Update the time offset from the timestamp carried by a server message ID."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.observe_server_msg_id"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L92"
aliases: ["miniproto.mtproto.MTProtoState.observe_server_msg_id"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.observe_server_msg_id`

```python
observe_server_msg_id(msg_id: int) -> None
```

Update the time offset from the timestamp carried by a server message ID.

**Parameters:**

- **msg_id** (<code>[int](#int)</code>) – Server-generated MTProto message ID.
