---
title: "miniproto.connection.framing.QuickAckFrame"
description: "A transport-level quick acknowledgement emitted by Telegram."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.framing.QuickAckFrame"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L39"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.QuickAckFrame`

```python
QuickAckFrame(token: int) -> None
```

A transport-level quick acknowledgement emitted by Telegram.

**Parameters:**

- **token** (<code>[int](#int)</code>) – The opaque acknowledgement token correlated by the sender with a
requested encrypted packet acknowledgement. It does not indicate an
RPC result or successful MTProto message processing.
