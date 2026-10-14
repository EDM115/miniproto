---
title: First High-Level Operation
description: Send a text message through Client.send_message() after bot authorization.
slug: /start/high-level-operation/
generated: false
---

The convenience API is small. `Client.send_message()` resolves a peer, converts the result into a normalized `Message` and exposes timeout, flood-wait, retry and quick-ack controls.

```python
import os

from miniproto import Client, ClientConfig, InMemorySessionStorage, event_loop


async def main() -> None:
    config = ClientConfig(
        api_id=int(os.environ["MINIPROTO_API_ID"]),
        api_hash=os.environ["MINIPROTO_API_HASH"],
        session_storage=InMemorySessionStorage(),
    )
    async with Client(config) as client:
        await client.sign_in_bot(os.environ["MINIPROTO_BOT_TOKEN"])
        message = await client.send_message("@your_test_chat", "Hello from miniproto")
        print(f"sent message {message.id}")


event_loop.run(main())
```

Use a chat where the bot can post and replace `@your_test_chat` before running the program. You can pass a username, numeric ID or normalized `Peer`. A numeric ID may lack the access data Telegram requires. The client can resolve usernames through its peer cache. A returned `Message` confirms that miniproto decoded Telegram's RPC result, not that other clients displayed it.

Leave `quick_ack=False` unless you need an early transport receipt. It does not replace waiting for `send_message()` to return or raise. Use the [Raw API guide](./raw-api.md) for Telegram options that `send_message()` does not expose.
