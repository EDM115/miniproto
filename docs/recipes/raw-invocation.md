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

Call this while `client` is connected, normally inside `async with Client(config)`. `invoke()` returns the decoded result and applies the configured timeout and retry policy. It also handles eligible flood waits, sender reconnection and main-session migration. It can raise `RpcError`, `FloodWait`, `TimeoutError` or `ConnectionError`.

Setting `retry=True` forces retry eligibility. After an ambiguous transport failure, that can replay a non-idempotent operation. Use it only when the operation is idempotent or Telegram deduplicates it. See [First Raw Call](../start/raw-api.md) and [Raw API](../raw-api.md) for generated requests and schema provenance.
