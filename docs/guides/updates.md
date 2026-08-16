---
title: Updates and recovery
description: Operate update consumption with explicit queue, recovery, ordering, and cancellation expectations.
slug: /guides/updates
generated: false
---

# Updates and recovery

`Client.connect()` starts the update manager when updates are enabled. The manager restores its persisted cursor before it accepts new raw updates, and `async with Client(...)` connects and disconnects around the consumer. Keep application side effects idempotent: the persisted recovery state is written before an update becomes visible to `iter_updates()` or to registered handlers, so a crash can leave recovery state ahead of the last side effect your application observed. This is not an application-level exactly-once delivery contract.

```python
from miniproto import Client, ClientConfig, Update


async def consume(config: ClientConfig) -> None:
    async with Client(config) as client:
        async for update in client.iter_updates():
            await process_update(update)


async def process_update(update: Update) -> None:
    # Persist an application idempotency key before a non-idempotent side effect.
    ...
```

The stream is FIFO for the normalized updates it emits. It is deliberately open-ended: stopping the update manager does not close the public queue or insert a sentinel. A consumer blocked in `iter_updates()` remains blocked until it is cancelled or a later event arrives. Arrange shutdown so the task consuming the iterator is cancelled, then let the client context manager disconnect.

## Queue pressure is a policy choice

`ClientConfig.update_queue_size` defaults to `1000`; both the raw intake queue and the public normalized-update queue use that bound. `ClientConfig.update_queue_overflow` defaults to `"raise"`:

- `"raise"` raises `asyncio.QueueFull` when a full queue receives another item. Treat it as backpressure or a capacity incident rather than silently losing state.
- `"drop_newest"` discards the incoming item.
- `"drop_oldest"` removes the oldest queued item before accepting the incoming item.

For either dropping policy, an update that is not put on the public queue is not passed to handlers. Raising a queue size or choosing a loss policy does not create delivery guarantees; it changes which overload failure your application must handle.

Measure handler latency and queue pressure before increasing the bound. Handlers registered with `client.on(...)` are awaited sequentially in registration-mapping order for matching types. One slow handler delays later matching handlers and the next public delivery work. Keep handler work short, hand durable jobs to an application-owned worker, and retain enough application state to make a recovered update safe to replay.

## Gaps and recovery

When the manager detects a gap, it uses Telegram update-state and difference requests through its configured invoker to restore cursor state. Events returned by one difference response are processed in that response's date order. That local ordering does not establish a global total order across independent input calls, network timing, or your own background workers.

The raw drainer is a cancellable background task. During `stop()`, cancellation can interrupt raw processing; if the task had already failed, shutdown re-raises its exception. Plan a supervised task boundary around the client and log the failure context without logging session credentials. The [production-operation guide](./production-operation.md) covers the wider shutdown order and [observability guide](./observability.md) covers the structured logging hooks.

## Practical checklist

- Make externally visible effects idempotent or deduplicate them with application-owned durable state.
- Choose `"raise"` when loss must surface, and catch `asyncio.QueueFull` at the ownership boundary.
- Choose a dropping policy only when the discarded update class is acceptable for the application.
- Cancel the iterator task during shutdown; waiting for an end-of-stream signal will wait indefinitely.
- Run recovery tests through a fake or controlled invoker before enabling a live account. Credentialed integration runs are opt-in and must not be treated as ordinary unit tests; see [development notes](../development.md).
