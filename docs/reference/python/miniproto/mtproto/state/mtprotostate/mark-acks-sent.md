---
title: "miniproto.mtproto.state.MTProtoState.mark_acks_sent"
description: "Mark retained messages acknowledged only after their receipt reply was written."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.mark_acks_sent"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L218"
aliases: ["miniproto.mtproto.MTProtoState.mark_acks_sent"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.mark_acks_sent`

```python
mark_acks_sent(msg_ids: tuple[int, ...]) -> None
```

Mark retained messages acknowledged only after their receipt reply was written.

**Parameters:**

- **msg_ids** (<code>[tuple](#tuple)[[int](#int), ...]</code>) – IDs covered by a successfully sent acknowledgement or state reply.
