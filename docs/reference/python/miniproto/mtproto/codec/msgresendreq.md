---
title: "miniproto.mtproto.codec.MsgResendReq"
description: "MTProto ``msg_resend_req`` body requesting retransmission of message IDs."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.MsgResendReq"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L126"
aliases: ["miniproto.mtproto.MsgResendReq"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.MsgResendReq`

```python
MsgResendReq(msg_ids: tuple[int, ...]) -> None
```

MTProto ``msg_resend_req`` body requesting retransmission of message IDs.

**Attributes:**

- [**msg_ids**](#miniproto.mtproto.codec.MsgResendReq.msg_ids) (<code>[tuple](#tuple)[[int](#int), ...]</code>) – Message IDs requested for retransmission.
