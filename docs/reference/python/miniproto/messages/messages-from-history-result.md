---
title: "miniproto.messages.messages_from_history_result"
description: "Convert only concrete raw messages from a history result in source order."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.messages.messages_from_history_result"
source_path: "src/miniproto/messages.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/messages.py#L135"
module: "miniproto.messages"
---

## `miniproto.messages.messages_from_history_result`

```python
messages_from_history_result(result: object, *, fallback_peer: Peer) -> tuple[Message, ...]
```

Convert only concrete raw messages from a history result in source order.

**Parameters:**

- **result** (<code>[object](#object)</code>) – Raw history response with an optional ``messages`` sequence.
- **fallback_peer** (<code>[Peer](#miniproto.types.Peer)</code>) – Peer used for unknown raw peer representations.
