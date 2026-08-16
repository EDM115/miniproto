---
title: "miniproto.mtproto.codec.MessageContainerItem"
description: "One message entry inside an MTProto message container."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.MessageContainerItem"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L137"
aliases: ["miniproto.mtproto.MessageContainerItem"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.MessageContainerItem`

```python
MessageContainerItem(msg_id: int, seq_no: int, body: ByteBuffer | object) -> None
```

One message entry inside an MTProto message container.

**Attributes:**

- [**msg_id**](#miniproto.mtproto.codec.MessageContainerItem.msg_id) (<code>[int](#int)</code>) – Contained MTProto message ID.
- [**seq_no**](#miniproto.mtproto.codec.MessageContainerItem.seq_no) (<code>[int](#int)</code>) – Contained MTProto sequence number.
- [**body**](#miniproto.mtproto.codec.MessageContainerItem.body) (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer) | [object](#object)</code>) – Raw or encodable contained message body.
