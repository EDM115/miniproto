---
title: "miniproto.mtproto.state.MTProtoState.message_statuses"
description: "Describe received IDs and unknown IDs relative to the bounded receive window."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.message_statuses"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L271"
aliases: ["miniproto.mtproto.MTProtoState.message_statuses"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.message_statuses`

```python
message_statuses(msg_ids: tuple[int, ...]) -> bytes
```

Describe received IDs and unknown IDs relative to the bounded receive window.

**Parameters:**

- **msg_ids** (<code>[tuple](#tuple)[[int](#int), ...]</code>) – IDs in the order required by a ``msgs_state_info`` reply.

**Returns:**

- <code>[bytes](#bytes)</code> – One status byte per ID: unknown below the window (1), missing within it (2), above it (3), or received (4) with acknowledged (8) and no-ack-required (16) flags when known. An empty receive window returns 1 for every queried ID.
