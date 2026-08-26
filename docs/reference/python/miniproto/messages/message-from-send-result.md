---
title: "miniproto.messages.message_from_send_result"
description: "Normalize a send response, retaining supplied values when Telegram omits a message."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.messages.message_from_send_result"
source_path: "src/miniproto/messages.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/messages.py#L73"
module: "miniproto.messages"
---

## `miniproto.messages.message_from_send_result`

```python
message_from_send_result(result: object, *, peer: Peer, text: str, entities: Iterable[object] = ()) -> Message
```

Normalize a send response, retaining supplied values when Telegram omits a message.

**Parameters:**

- **result** (<code>[object](#object)</code>) – Raw send result or update container.
- **peer** (<code>[Peer](#miniproto.types.Peer)</code>) – Destination peer used as the fallback message peer.
- **text** (<code>[str](#str)</code>) – Submitted text used if no raw message is present.
- **entities** (<code>[Iterable](#collections.abc.Iterable)[[object](#object)]</code>) – Submitted entities used if Telegram did not return entities.

**Returns:**

- <code>[Message](#miniproto.types.Message)</code> – The sent message, with a zero ID and current UTC time only for incomplete responses.
