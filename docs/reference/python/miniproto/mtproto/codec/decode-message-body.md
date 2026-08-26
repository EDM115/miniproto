---
title: "miniproto.mtproto.codec.decode_message_body"
description: "Decode recognized MTProto service bodies, preserving unknown data as a view."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.decode_message_body"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L474"
aliases: ["miniproto.mtproto.decode_message_body"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.decode_message_body`

```python
decode_message_body(data: ByteBuffer) -> ByteBuffer | object
```

Decode recognized MTProto service bodies, preserving unknown data as a view.

**Parameters:**

- **data** (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer)</code>) – Exactly one MTProto body.

**Returns:**

- <code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer) | [object](#object)</code> – Service-body dataclass, ping tuple, RPC error/result or the original ``ByteBuffer`` input for an unknown constructor.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If a recognized body is truncated, malformed or has trailing bytes.
