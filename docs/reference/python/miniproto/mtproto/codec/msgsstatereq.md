---
title: "miniproto.mtproto.codec.MsgsStateReq"
description: "MTProto ``msgs_state_req`` body requesting message states."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.MsgsStateReq"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L102"
aliases: ["miniproto.mtproto.MsgsStateReq"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.MsgsStateReq`

```python
MsgsStateReq(msg_ids: tuple[int, ...]) -> None
```

MTProto ``msgs_state_req`` body requesting message states.

**Attributes:**

- [**msg_ids**](#miniproto.mtproto.codec.MsgsStateReq.msg_ids) (<code>[tuple](#tuple)[[int](#int), ...]</code>) – Message IDs whose states are requested.
