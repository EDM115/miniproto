---
title: First Raw Call
description: Construct a generated TL request and send it through Client.invoke().
slug: /start/raw-api/
generated: false
---

The generated raw API exposes Telegram constructors and functions as Python classes. `Client.invoke()` requires a connected client, creates its sender lazily and returns the decoded raw response.

```python
from miniproto import Client, ClientConfig, InMemorySessionStorage, event_loop
from miniproto.raw import functions


async def main() -> None:
    config = ClientConfig(
        api_id=12345, api_hash="read this from a secret manager", session_storage=InMemorySessionStorage()
    )
    async with Client(config) as client:
        result = await client.invoke(functions.HelpGetConfig())
        print(result.this_dc)


event_loop.run(main())
```

Replace the placeholder credentials before running it. The sample is syntactically complete but deliberately not executed by the offline documentation checks because it contacts Telegram and performs an MTProto key exchange.

`invoke()` applies the configured timeout and retry policy, handles eligible flood waits and follows data-center migrations. It can raise `RpcError`, `FloodWait`, `TimeoutError` or `ConnectionError`. Set `retry=True` only for idempotent requests or operations Telegram deduplicates. A quick acknowledgement confirms packet receipt, not the RPC result.

See [Raw API](../raw-api.md) for Layer 230 provenance, lazy loading and runtime limits. The generated [Telegram function reference](../reference/telegram/functions/index.md) has a page for each pinned function.
