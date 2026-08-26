---
title: "miniproto.mtproto.state.MTProtoState.record_incoming"
description: "Record a server message unless it is already known."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.record_incoming"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L165"
aliases: ["miniproto.mtproto.MTProtoState.record_incoming"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.record_incoming`

```python
record_incoming(msg_id: int, *, content_related: bool = True) -> bool
```

Record a server message unless it is already known.

**Parameters:**

- **msg_id** (<code>[int](#int)</code>) – Server message ID.
- **content_related** (<code>[bool](#bool)</code>) – Queue an acknowledgement when ``True`` (the default).

**Returns:**

- <code>[bool](#bool)</code> – ``True`` for a newly recorded ID, otherwise ``False``.
