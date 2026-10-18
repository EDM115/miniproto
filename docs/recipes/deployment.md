---
title: Deploy a Durable Client
description: Run a client with secret-managed credentials, encrypted session storage and deterministic cleanup.
slug: /recipes/deployment/
generated: false
---

Set a unique `session_path` for each account or deployment. Store API credentials and `MINIPROTO_SESSION_KEY` in the deployment platform's secret manager. The default backend encrypts sessions in SQLite. It cannot protect a process that logs or exports its own credentials.

```python
import os

from miniproto import Client, ClientConfig, event_loop


async def main() -> None:
    config = ClientConfig(
        api_id=int(os.environ["MINIPROTO_API_ID"]),
        api_hash=os.environ["MINIPROTO_API_HASH"],
        session_path=os.environ["MINIPROTO_SESSION_PATH"],
    )
    async with Client(config) as client:
        await client.sign_in_bot(os.environ["MINIPROTO_BOT_TOKEN"])
        await client.get_me()


event_loop.run(main())
```

The context manager disconnects the sender, update manager, media pools, scheduler, auxiliary download clients and selected storage. `disconnect()` closes the storage, so that client instance cannot be reused. Construct a new client to start another lifecycle.

Use one protected session per account or deployment. Keep the file private to the service identity. Do not log raw mappings, session strings, API hashes, bot tokens, phone numbers, credentialed proxies or the encryption key. See [Session Security](../session-security.md) for rotation, portable formats, storage transactions and conversion limits.
