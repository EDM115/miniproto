---
title: Invoke a Raw Telegram Function
description: Build a generated raw request and send it through the connected Client invocation policy.
slug: /recipes/raw-invocation/
generated: false
---

Build the generated request explicitly, then give it to `Client.invoke()`. Keep the client lifecycle outside the helper so connection ownership and authorization remain visible at the call site.

```python
from miniproto import Client
from miniproto.raw import functions


async def current_datacenter(client: Client) -> int:
    result = await client.invoke(functions.HelpGetConfig())
    return result.this_dc
```

Call this only while `client` is connected, normally inside `async with Client(config)`. `invoke()` returns the decoded raw result and owns the configured timeout, retry, eligible flood-wait, sender reconnect, and main-session migration behavior. It can still raise `RpcError`, `FloodWait`, `TimeoutError`, or `ConnectionError`.

Do not set `retry=True` merely to make a failed write look successful: it forces retry eligibility and can replay a non-idempotent operation after an ambiguous transport failure. Use that override only when the operation is idempotent or Telegram de-duplicates it. See [First Raw Call](../start/raw-api.md) and [Raw API](../raw-api.md) for the generated surface and provenance.
