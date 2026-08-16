---
title: "miniproto.mtproto.state.MTProtoState.validate_incoming"
description: "Validate an incoming envelope before permanently recording it."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.validate_incoming"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L107"
aliases: ["miniproto.mtproto.MTProtoState.validate_incoming"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.validate_incoming`

```python
validate_incoming(msg_id: int, *, session_id: int, now: float | None = None, provisional_time_offset: float | None = None, provisional_seen_msg_ids: Collection[int] = ()) -> None
```

Validate an incoming envelope before permanently recording it.

**Parameters:**

- **msg_id** (<code>[int](#int)</code>) – Server-generated message ID to validate.
- **session_id** (<code>[int](#int)</code>) – Envelope session ID, which must match this state.
- **now** (<code>[float](#float) | None</code>) – Optional wall-clock time for deterministic validation.
- **provisional_time_offset** (<code>[float](#float) | None</code>) – Optional transactional offset to use for time-window checks.
- **provisional_seen_msg_ids** (<code>[Collection](#collections.abc.Collection)[[int](#int)]</code>) – Additional IDs already staged in the current transaction.

**Raises:**

- <code>[ProtocolValidationError](#miniproto.errors.ProtocolValidationError)</code> – If session, parity, duplicate, replay-window, or trusted time checks fail.
