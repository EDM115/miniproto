---
title: "miniproto.mtproto.state.MTProtoState.pop_pending_acks"
description: "Remove the oldest queued acknowledgement IDs."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.pop_pending_acks"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L213"
aliases: ["miniproto.mtproto.MTProtoState.pop_pending_acks"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.pop_pending_acks`

```python
pop_pending_acks(*, limit: int | None = None) -> tuple[int, ...]
```

Remove the oldest queued acknowledgement IDs.

**Parameters:**

- **limit** (<code>[int](#int) | None</code>) – Maximum IDs to remove; ``None`` (default) removes all queued IDs.

**Returns:**

- <code>[tuple](#tuple)[[int](#int), ...]</code> – Removed IDs in acknowledgement order.
