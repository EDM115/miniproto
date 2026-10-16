---
title: Runnable Examples
description: Small environment-driven scripts for bot identity, raw invocation and controlled message sending.
slug: /start/examples/
generated: false
---

This complete bot identity check takes credentials from `MINIPROTO_API_ID`, `MINIPROTO_API_HASH` and `MINIPROTO_BOT_TOKEN`. Set them in a protected environment or secret manager. The program connects to Telegram, so it cannot verify the package offline.

```python
import os

from miniproto import Client, ClientConfig, InMemorySessionStorage, event_loop


async def main() -> None:
    client = Client(
        ClientConfig(
            api_id=int(os.environ["MINIPROTO_API_ID"]),
            api_hash=os.environ["MINIPROTO_API_HASH"],
            session_storage=InMemorySessionStorage(),
        )
    )
    async with client:
        await client.sign_in_bot(os.environ["MINIPROTO_BOT_TOKEN"])
        me = await client.get_me()
        print({"id": me.id, "is_bot": me.is_bot})


event_loop.run(main())
```

To make a raw request, use the [raw-call example](./raw-api.md) inside `main()`. To send a message, use the [high-level-operation example](./high-level-operation.md) and choose a chat where the bot can post. For a durable account, follow [Phone, Bot and 2FA Authorization](./authentication.md) and [Session Security](../session-security.md) before replacing in-memory storage.

These examples show how to structure application calls. Telegram controls responses, rate limits, peer permissions and account state, so an example cannot guarantee a live test outcome.
