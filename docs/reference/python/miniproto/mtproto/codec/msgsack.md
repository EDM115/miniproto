---
title: "miniproto.mtproto.codec.MsgsAck"
description: "MTProto ``msgs_ack`` body acknowledging received message IDs."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.MsgsAck"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L91"
aliases: ["miniproto.mtproto.MsgsAck"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.MsgsAck`

```python
MsgsAck(msg_ids: tuple[int, ...]) -> None
```

MTProto ``msgs_ack`` body acknowledging received message IDs.

**Attributes:**

- [**msg_ids**](#miniproto.mtproto.codec.MsgsAck.msg_ids) (<code>[tuple](#tuple)[[int](#int), ...]</code>) – Acknowledged MTProto message IDs.
