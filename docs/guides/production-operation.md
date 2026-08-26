---
title: Production operation
description: Own client lifecycle, bounded resources, orderly shutdown and credential redaction in a service.
slug: /guides/production-operation
generated: false
---

# Production operation

Make one application component responsible for each `Client` instance. The client owns its connection, update machinery, media pools and schedulers, auxiliary download clients and session storage. The narrowest reliable lifecycle is an async context manager:

```python
from miniproto import Client, ClientConfig


async def serve(config: ClientConfig) -> None:
    async with Client(config) as client:
        await run_application_work(client)
```

`connect()` is serialized with `disconnect()` and is repeat-safe while the client remains usable. If update startup fails, connection startup rolls back its state and closes the sender it created. `disconnect()` stops updates and receive dispatch, flushes salt state, releases transport and media resources, closes schedulers and auxiliary download clients, then closes session storage. It continues cleanup after an individual cleanup failure and re-raises the first failure it captured.

Closing storage is a terminal lifecycle boundary: do not attempt to reconnect and reuse the same client after `disconnect()`. Construct a new client for a new lifecycle. This matters during service restarts, test fixtures and supervisor retries.

## Shutdown sequence

1. Stop accepting application work that would start new RPCs or transfers.
2. Cancel application-owned tasks consuming `client.iter_updates()`; the iterator is not closed by update-manager shutdown.
3. Exit the client context manager or await `client.disconnect()` from the component that owns it.
4. Let cancellation propagate to the service supervisor after cleanup. Do not replace cancellation with a broad exception handler that leaves the client alive.

The update drainer itself is cancellable, so a shutdown can interrupt raw update processing. Durable update cursor state may already be ahead of a side effect exposed to your application; use idempotent processing and follow the [updates guide](./updates.md) for the recovery model.

## Set bounds from workload evidence

The defaults are intentionally finite in a few high-impact places:

- update queues hold 1,000 entries and raise on overflow;
- the primary request timeout is 30 seconds, with two retry attempts by default;
- the default transport connects in 10 seconds, reads and writes in 30 seconds and backs off reconnects from 0.25 seconds to at most 5 seconds;
- maximum transport payload size is 16 MiB;
- media download and upload byte budgets default to 16 MiB and 8 MiB and an idle media connection closes after 120 seconds.

These values are limits and retry controls, not service-level guarantees. Derive production queue capacity, concurrency, timeouts and budget settings from observed update rate, handler time, message sizes and an explicit failure budget. The [media guide](../media.md) owns transfer API and scheduling details; the [benchmark guide](./performance-and-benchmarks.md) explains how to compare changes without mistaking a local result for a general capacity claim.

## Credentials and diagnostic data

The default session storage path is `miniproto.session.sqlite`; durable storage needs an encryption key configured at client construction. The full key-source, rotation, export and test-storage model is documented in [session storage and credential handling](../session-security.md).

Logging and metric fields pass through miniproto's redaction helpers for recognized sensitive keys, including session/auth-key material, API hash, bot token, password, proxy credentials and proxy URL. That is a safety net for predictable fields, not a license to emit arbitrary credentials. In particular, redacting text only recognizes key/value-like assignments and cannot infer that an arbitrary message, exception, URL fragment or serialized object contains a secret. Keep secrets out of diagnostic values at the call site.

Use credentialed integration tests and live benchmarks only in a deliberately isolated environment. They require explicit environment gates and real Telegram credentials; do not run them as a routine local test command or against an account whose state cannot be changed. [Development notes](../development.md) list the current gated commands and variables.
