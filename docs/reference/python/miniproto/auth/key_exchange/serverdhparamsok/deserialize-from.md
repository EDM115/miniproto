---
title: "miniproto.auth.key_exchange.ServerDHParamsOk.deserialize_from"
description: "Decode fields following an already-consumed success constructor ID."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.key_exchange.ServerDHParamsOk.deserialize_from"
source_path: "src/miniproto/auth/key_exchange.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/key_exchange.py#L229"
aliases: ["miniproto.auth.ServerDHParamsOk.deserialize_from"]
module: "miniproto.auth.key_exchange"
---

## `miniproto.auth.key_exchange.ServerDHParamsOk.deserialize_from`

```python
deserialize_from(data: bytes | memoryview, offset: int) -> Self
```

Decode fields following an already-consumed success constructor ID.

**Parameters:**

- **data** (<code>[bytes](#bytes) | [memoryview](#memoryview)</code>) – Complete TL payload containing the response.
- **offset** (<code>[int](#int)</code>) – Byte offset immediately following the success constructor ID.
