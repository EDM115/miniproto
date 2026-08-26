---
title: "miniproto.auth.key_exchange.ServerDHInnerData.deserialize"
description: "Decode a complete ``server_DH_inner_data`` payload."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.ServerDHInnerData.deserialize"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L311"
aliases: ["miniproto.auth.ServerDHInnerData.deserialize"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ServerDHInnerData.deserialize`

```python
deserialize(data: bytes | memoryview) -> Self
```

Decode a complete ``server_DH_inner_data`` payload.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – Constructor-prefixed TL bytes for the inner DH payload.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If the constructor is unexpected or bytes remain after decoding.
