---
title: "miniproto.mtproto.state.MTProtoState.oldest_pending_ack_age"
description: "Return the age of the oldest queued acknowledgement."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.oldest_pending_ack_age"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L199"
aliases: ["miniproto.mtproto.MTProtoState.oldest_pending_ack_age"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.oldest_pending_ack_age`

```python
oldest_pending_ack_age(now: float | None = None) -> float
```

Return the age of the oldest queued acknowledgement.

**Parameters:**

- **now** (<code>[float](#float) | None</code>) – Optional monotonic timestamp for deterministic measurement.

**Returns:**

- <code>[float](#float)</code> – Nonnegative age in seconds or ``0.0`` when the queue is empty.
