---
title: "miniproto.mtproto.codec.encode_ping"
description: "Encode an MTProto ``ping`` service body."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.mtproto.codec.encode_ping"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py#L619"
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec.encode_ping`

```python
encode_ping(ping_id: int) -> bytes
```

Encode an MTProto ``ping`` service body.

**Parameters:**

- **ping_id** (<code>[int](#int)</code>) – Caller-chosen 64-bit ping correlation ID.

**Returns:**

- <code>[bytes](#bytes)</code> – Constructor-prefixed ``ping`` body bytes.
