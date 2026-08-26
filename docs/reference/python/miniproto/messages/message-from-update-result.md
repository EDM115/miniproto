---
title: "miniproto.messages.message_from_update_result"
description: "Normalize an update response or create a fallback message when none is present."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.messages.message_from_update_result"
source_path: "src/miniproto/messages.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/messages.py#L112"
module: "miniproto.messages"
---

## `miniproto.messages.message_from_update_result`

```python
message_from_update_result(result: object, *, fallback_peer: Peer, fallback_text: str, entities: Iterable[object] = ()) -> Message
```

Normalize an update response or create a fallback message when none is present.

The fallback has ID ``0`` and the current UTC time, preserving submitted text
and entities for response forms that do not carry a message object.

**Parameters:**

- **result** (<code>[object](#object)</code>) – Raw update or response container to inspect.
- **fallback_peer** (<code>[Peer](#miniproto.types.Peer)</code>) – Peer used when no concrete message is found.
- **fallback_text** (<code>[str](#str)</code>) – Submitted text used by the synthetic fallback.
- **entities** (<code>[Iterable](#collections.abc.Iterable)[[object](#object)]</code>) – Submitted entities used when a concrete message omits entities.
