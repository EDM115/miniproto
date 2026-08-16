---
title: "miniproto.auth.key_exchange.ResPQ.deserialize"
description: "Decode a complete ``resPQ`` payload."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.ResPQ.deserialize"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L116"
aliases: ["miniproto.auth.ResPQ.deserialize"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ResPQ.deserialize`

```python
deserialize(data: bytes | memoryview) -> Self
```

Decode a complete ``resPQ`` payload.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – Constructor-prefixed TL bytes returned by Telegram for ``req_pq_multi``.

**Raises:**

- <code>[TLCodecError](#miniproto.tl.codec.TLCodecError)</code> – If the constructor ID is not ``resPQ`` or trailing bytes remain.
