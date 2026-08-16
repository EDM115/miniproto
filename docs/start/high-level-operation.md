---
title: First High-Level Operation
description: Send a text message through Client.send_message() after bot authorization.
slug: /start/high-level-operation/
generated: false
---

The public convenience surface is intentionally small. `Client.send_message()` resolves a peer, converts the message result into a normalized `Message`, and still exposes timeout, flood-wait, retry, and quick-ack controls when a caller needs them.

```python
import os

from miniproto import Client, ClientConfig, event_loop


async def main() -> None:
    config = ClientConfig(api_id=int(os.environ["MINIPROTO_API_ID"]), api_hash=os.environ["MINIPROTO_API_HASH"])
    async with Client(config) as client:
        await client.sign_in_bot(os.environ["MINIPROTO_BOT_TOKEN"])
        message = await client.send_message("@your_test_chat", "Hello from miniproto")
        print(f"sent message {message.id}")


event_loop.run(main())
```

Use a chat where the bot is allowed to send and replace `@your_test_chat` before running the program. A username, numeric ID, or normalized `Peer` is accepted, but a numeric peer can still lack the access data required by Telegram. The client may resolve a username through its peer cache; a returned `Message` means the RPC result was decoded, not that every downstream client has displayed it.

Leave `quick_ack=False` unless you specifically need a transport-receipt signal. When enabled, it does not replace waiting for `send_message()` to return or raise. Use the [Raw API guide](./raw-api.md) when the small convenience surface does not expose the Telegram option you need.
