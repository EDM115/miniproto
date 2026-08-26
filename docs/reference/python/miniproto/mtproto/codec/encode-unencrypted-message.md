---
title: "miniproto.mtproto.codec.encode_unencrypted_message"
description: "Frame an unencrypted MTProto message with ``auth_key_id = 0``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.encode_unencrypted_message"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L271"
aliases: ["miniproto.mtproto.encode_unencrypted_message"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.encode_unencrypted_message`

```python
encode_unencrypted_message(msg_id: int, body: bytes | object) -> bytes
```

Frame an unencrypted MTProto message with ``auth_key_id = 0``.

**Parameters:**

- **msg_id** (<code>[int](#int)</code>) – MTProto message identifier.
- **body** (<code>[bytes](#bytes) | [object](#object)</code>) – Raw body bytes or a supported encodable body object.

**Returns:**

- <code>[bytes](#bytes)</code> – Complete unencrypted MTProto envelope bytes.
