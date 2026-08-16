---
title: "miniproto.invoke.wrap_raw_request"
description: "Wrap a raw request for transmission."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.wrap_raw_request"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L143"
module: "miniproto.invoke"
---

## `miniproto.invoke.wrap_raw_request`

```python
wrap_raw_request(raw_request: object, config: ClientConfig, *, needs_init: bool = True, without_updates: bool = False) -> object
```

Wrap a raw request for transmission.

``invokeWithLayer(initConnection(...))`` is only added when ``needs_init`` is true,
i.e. for the first request after a sender (re)connects. Media-lane senders
additionally wrap that first request in ``invokeWithoutUpdates`` so dedicated file
sessions never receive update traffic. Serialization happens exactly once, inside
the sender, when the message body is encoded.

**Parameters:**

- **raw_request** (<code>[object](#object)</code>) – Constructor-backed Telegram request or an existing invocation envelope.
- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client device and API configuration used to create ``initConnection``.
- **needs_init** (<code>[bool](#bool)</code>) – Whether this sender's next request still requires initialization wrapping.
- **without_updates** (<code>[bool](#bool)</code>) – Wrap a media-lane initialization in ``invokeWithoutUpdates``.
