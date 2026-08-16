---
title: "miniproto.mtproto.state.MTProtoState.next_seq_no"
description: "Allocate the next MTProto sequence number."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.state.MTProtoState.next_seq_no"
source_path: "src/miniproto/mtproto/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/state.py#L78"
aliases: ["miniproto.mtproto.MTProtoState.next_seq_no"]
module: "miniproto.mtproto.state"
---

## `miniproto.mtproto.state.MTProtoState.next_seq_no`

```python
next_seq_no(*, content_related: bool) -> int
```

Allocate the next MTProto sequence number.

**Parameters:**

- **content_related** (<code>[bool](#bool)</code>) – Whether this message advances the content-related counter.

**Returns:**

- <code>[int](#int)</code> – Even non-content or odd content-related sequence number.
