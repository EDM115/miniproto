---
title: "miniproto.mtproto.state.MTProtoState.commit_incoming"
description: "Permanently record an already validated incoming message."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.commit_incoming"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L146"
aliases: ["miniproto.mtproto.MTProtoState.commit_incoming"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.commit_incoming`

```python
commit_incoming(msg_id: int, *, content_related: bool = True, now: float | None = None) -> None
```

Permanently record an already validated incoming message.

**Parameters:**

- **msg_id** (<code>[int](#int)</code>) – Validated server message ID.
- **content_related** (<code>[bool](#bool)</code>) – Queue an acknowledgement when ``True`` (the default).
- **now** (<code>[float](#float) | None</code>) – Optional wall-clock time used when initially trusting the server clock.
