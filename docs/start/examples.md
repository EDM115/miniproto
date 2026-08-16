---
title: Runnable Examples
description: Small environment-driven scripts for bot identity, raw invocation, and controlled message sending.
slug: /start/examples/
generated: false
---

The following program is a complete bot identity check. It has no command-line credential arguments: provide `MINIPROTO_API_ID`, `MINIPROTO_API_HASH`, and `MINIPROTO_BOT_TOKEN` through a protected environment or secret manager before running it. It makes a live Telegram connection, so it is not an offline verification command.

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

For a first low-level request, substitute the body of `main()` with the [raw-call example](./raw-api.md). For a controlled send, use the [high-level-operation example](./high-level-operation.md) and a chat where the bot has permission to post. For a durable account, replace in-memory storage only after following [Phone, Bot, and 2FA Authorization](./authentication.md) and [Session Security](../session-security.md).

These examples establish an expected shape for applications; they do not guarantee a particular Telegram response, rate, peer permission, account state, or live test outcome.
