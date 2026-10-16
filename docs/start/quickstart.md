---
title: Five-Minute Quickstart
description: Authorize a throwaway bot session and inspect its identity with the public Client API.
slug: /start/quickstart/
generated: false
---

This example uses explicit in-memory storage so it does not create a session database. It still contacts Telegram, authorizes the supplied bot token and must be run only with an application and bot account you control.

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
        me = await client.get_me()
        print(f"authorized bot ID: {me.id}")


event_loop.run(main())
```

`async with Client(...)` calls `connect()` before entering the block and `disconnect()` on exit. Shutdown stops the sender, schedulers, update handling and storage. `connect()` is serialized and repeatable, so `sign_in_bot()` can call it again safely. The token remains in process memory while the client needs it. Never print it or include it in an exception message.

After authorization, `get_me()` returns the cached or refreshed normalized user identity. It raises `Unauthorized` when the session is not authorized. Use it as a first network check. It does not prove that message sending, media transfers or live limits will work for every account or data center.

For a durable account session, use the [authorization guide](./authentication.md) with a protected `MINIPROTO_SESSION_KEY`. For the next protocol-level step, continue with [First raw call](./raw-api.md).
