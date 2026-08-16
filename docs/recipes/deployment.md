---
title: Deploy a Durable Client
description: Run a client with secret-managed credentials, encrypted session storage, and deterministic cleanup.
slug: /recipes/deployment/
generated: false
---

Provision API credentials, a unique session path, and `MINIPROTO_SESSION_KEY` through the deployment platform's secret manager. The default storage backend is encrypted SQLite, but it cannot protect a process that deliberately logs or exports its own credentials.

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

The context manager disconnects the sender, update machinery, media pools, scheduler, auxiliary download clients, and selected storage. After `disconnect()`, client storage is closed and that client instance is not reusable; construct a new client for a new lifecycle.

Use one protected session per account/deployment and keep the file private to the service identity. Do not log raw mappings, session strings, API hashes, bot tokens, phone numbers, proxies with credentials, or the encryption key. For rotation, portable-session formats, storage transactions, and cross-library conversion limits, follow [Session Security](../session-security.md).
