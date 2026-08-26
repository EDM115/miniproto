---
title: "miniproto.mtproto.state.MTProtoState.requeue_acks"
description: "Restore acknowledgement IDs after an unsent batch fails."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.requeue_acks"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L230"
aliases: ["miniproto.mtproto.MTProtoState.requeue_acks"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.requeue_acks`

```python
requeue_acks(msg_ids: tuple[int, ...]) -> None
```

Restore acknowledgement IDs after an unsent batch fails.

**Parameters:**

- **msg_ids** (<code>[tuple](#tuple)[[int](#int), ...]</code>) – IDs to queue unless already pending.
