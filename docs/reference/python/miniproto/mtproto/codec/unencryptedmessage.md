---
title: "miniproto.mtproto.codec.UnencryptedMessage"
description: "Unencrypted MTProto envelope carrying a message ID and raw body."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.mtproto.codec.UnencryptedMessage"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L78"
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.UnencryptedMessage`

```python
UnencryptedMessage(msg_id: int, body: ByteBuffer) -> None
```

Unencrypted MTProto envelope carrying a message ID and raw body.

**Attributes:**

- [**msg_id**](#miniproto.mtproto.codec.UnencryptedMessage.msg_id) (<code>[int](#int)</code>) – MTProto message ID.
- [**body**](#miniproto.mtproto.codec.UnencryptedMessage.body) (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer)</code>) – Raw unencrypted message-body view.
