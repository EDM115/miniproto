---
title: First Raw Call
description: Construct a generated TL request and send it through Client.invoke().
slug: /start/raw-api/
generated: false
---

The generated raw API exposes Telegram constructors and functions as Python classes. `Client.invoke()` accepts one of those request objects, establishes its sender lazily after the client has connected and returns the decoded raw response.

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

`invoke()` applies the configured request timeout, retry policy, eligible flood-wait handling and data-center migration behavior. It can raise `RpcError` variants, `FloodWait`, `TimeoutError` or `ConnectionError`; forcing `retry=True` is appropriate only for an idempotent request or an operation Telegram will deduplicate. A transport quick acknowledgement, when requested, confirms packet receipt rather than the RPC result.

For the complete Layer 229 provenance, lazy facade behavior, generated names and current runtime boundaries, use [Raw API](../raw-api.md). The generated [Telegram function reference](../reference/telegram/functions/index.md) contains every pinned per-symbol page; this guide intentionally does not duplicate that reference surface.
