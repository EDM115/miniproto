---
title: "miniproto.mtproto.codec.BadMsgNotification"
description: "MTProto notice that a message ID, sequence number or other field was invalid."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.BadMsgNotification"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L198"
aliases: ["miniproto.mtproto.BadMsgNotification"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.BadMsgNotification`

```python
BadMsgNotification(bad_msg_id: int, bad_msg_seq_no: int, error_code: int) -> None
```

MTProto notice that a message ID, sequence number or other field was invalid.

**Attributes:**

- [**bad_msg_id**](#miniproto.mtproto.codec.BadMsgNotification.bad_msg_id) (<code>[int](#int)</code>) – Rejected message ID.
- [**bad_msg_seq_no**](#miniproto.mtproto.codec.BadMsgNotification.bad_msg_seq_no) (<code>[int](#int)</code>) – Rejected sequence number.
- [**error_code**](#miniproto.mtproto.codec.BadMsgNotification.error_code) (<code>[int](#int)</code>) – MTProto validation error code.
