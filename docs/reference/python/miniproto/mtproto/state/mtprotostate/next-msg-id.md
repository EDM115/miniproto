---
title: "miniproto.mtproto.state.MTProtoState.next_msg_id"
description: "Allocate a strictly increasing client MTProto message ID."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.next_msg_id"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L66"
aliases: ["miniproto.mtproto.MTProtoState.next_msg_id"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.next_msg_id`

```python
next_msg_id() -> int
```

Allocate a strictly increasing client MTProto message ID.

**Returns:**

- <code>[int](#int)</code> – Timestamp-derived, client-parity message ID advancing in steps of four.
