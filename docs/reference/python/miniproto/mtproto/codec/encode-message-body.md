---
title: "miniproto.mtproto.codec.encode_message_body"
description: "Encode raw, generated or built-in MTProto service message bodies."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.encode_message_body"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L378"
aliases: ["miniproto.mtproto.encode_message_body"]
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.encode_message_body`

```python
encode_message_body(body: ByteBuffer | object) -> bytes
```

Encode raw, generated or built-in MTProto service message bodies.

**Parameters:**

- **body** (<code>[ByteBuffer](#miniproto.mtproto.codec.ByteBuffer) | [object](#object)</code>) – Bytes, generated TL object or supported service-body object.

**Returns:**

- <code>[bytes](#bytes)</code> – Constructor-prefixed MTProto body bytes where applicable.

**Raises:**

- <code>[TypeError](#TypeError)</code> – If the body is not supported by this codec.
