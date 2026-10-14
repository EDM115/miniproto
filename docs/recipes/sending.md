---
title: Send Text With Result Semantics
description: Send a text message to a resolved peer and distinguish transport acknowledgement from RPC completion.
slug: /recipes/sending/
generated: false
---

`Client.send_message()` accepts a normalized `Peer`, a numeric ID or a username. Resolve and cache peer data through the client rather than constructing an incomplete raw input peer yourself.

```python
from miniproto import Client


async def send_notice(client: Client) -> int:
    message = await client.send_message("@your_test_chat", "Maintenance begins soon.")
    return message.id
```

The `await` completes when miniproto receives and normalizes Telegram's RPC result. A bot still needs permission to post in the target chat and a numeric peer may lack access data; neither condition is inferred from the Python type.

`quick_ack=True` or `quick_ack_callback=` requests a transport acknowledgement for the final encrypted request. The receipt confirms transport acceptance, not message delivery. Still await `send_message()` for its RPC result. Supply `random_id` only when your application manages deduplication. Otherwise, miniproto generates one.

For raw send options beyond this small convenience method, use [Invoke a Raw Telegram Function](./raw-invocation.md) and the generated [Raw API](../raw-api.md).
