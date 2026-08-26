---
title: "miniproto.mtproto.codec.decode_unencrypted_message"
description: "Validate and decode an unencrypted MTProto envelope."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.decode_unencrypted_message"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L285"
aliases: ["miniproto.mtproto.decode_unencrypted_message"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.decode_unencrypted_message`

```python
decode_unencrypted_message(packet: ByteBuffer) -> UnencryptedMessage
```

Validate and decode an unencrypted MTProto envelope.

**Parameters:**

- **packet** (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer)</code>) – Complete unencrypted packet bytes.

**Returns:**

- <code>[UnencryptedMessage](#miniproto.mtproto.codec.UnencryptedMessage)</code> – Message identifier and a body memoryview.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the packet is too short, nonzero-authenticated or malformed.
