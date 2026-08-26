---
title: "miniproto.messages.message_from_raw"
description: "Convert a raw Telegram message using ``fallback_peer`` for unknown peer forms."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.messages.message_from_raw"
source_path: "src/miniproto/messages.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/messages.py#L102"
module: "miniproto.messages"
---

## `miniproto.messages.message_from_raw`

```python
message_from_raw(raw: types.Message, *, fallback_peer: Peer) -> Message
```

Convert a raw Telegram message using ``fallback_peer`` for unknown peer forms.

**Parameters:**

- **raw** (<code>[Message](#miniproto.raw.types.Message)</code>) – Concrete Telegram message object.
- **fallback_peer** (<code>[Peer](#miniproto.types.Peer)</code>) – Destination peer retained when raw peer form is unknown or richer.
