---
title: Updates and recovery
description: Operate update consumption with explicit queue, recovery, ordering and cancellation expectations.
slug: /guides/updates
generated: false
---

# Updates and recovery

`Client.connect()` starts the update manager when updates are enabled. The manager restores its persisted cursor before it accepts new raw updates; `async with Client(...)` connects before the body and disconnects after it. The manager commits cursor state before it exposes an update to `iter_updates()` or a handler. A crash after that commit but before handler delivery can leave the cursor ahead of application work, and miniproto may not deliver that update again. Idempotency helps when an update repeats, but it cannot recover missed work. Applications that cannot accept missed effects need a separate reconciliation strategy. Miniproto does not promise exactly-once or at-least-once delivery to application code.

```python
from miniproto import Client, ClientConfig, Update


async def consume(config: ClientConfig) -> None:
    async with Client(config) as client:
        async for update in client.iter_updates():
            await process_update(update)


async def process_update(update: Update) -> None:
    # Use application state to deduplicate repeats and reconcile missed work.
    ...
```

The stream is FIFO for the normalized updates it emits. An iterator becomes active on its first `anext()` and stays active while the consumer processes each yielded event. Close a retained iterator with `await iterator.aclose()` or `contextlib.aclosing()` when stopping between events. Multiple iterators compete for the same queue.  
The stream is deliberately open-ended: stopping the update manager does not close the public queue or insert a sentinel. A consumer blocked in `iter_updates()` remains blocked until it is cancelled or a later event arrives. Arrange shutdown so the task consuming the iterator is cancelled, then let the client context manager disconnect.

## Queue pressure is a policy choice

`ClientConfig.update_queue_size` defaults to `1000`; both the raw intake queue and the public normalized-update queue use that bound. `ClientConfig.update_queue_overflow` defaults to `"raise"`:

- `"raise"` raises `asyncio.QueueFull` when a full queue receives another item. Treat it as backpressure or a capacity incident rather than silently losing state.
- `"drop_newest"` discards the incoming item.
- `"drop_oldest"` removes the oldest queued item before accepting the incoming item.

When handlers are registered and no iterator is active, updates go directly to handlers without filling an unused iterator queue. A later iterator does not receive that callback-only history. With no registered handlers, the bounded pre-iteration backlog remains available. When callbacks and an active iterator share delivery, queue admission still precedes callbacks: either dropping policy also skips handlers for the rejected event. Raising a queue size or choosing a loss policy does not create delivery guarantees, it changes which overload failure your application must handle.

Measure handler latency and queue pressure before increasing the bound. Handlers registered with `client.on(...)` are awaited sequentially in registration-mapping order for matching types. One slow handler delays later matching handlers and the next public delivery work. Keep handler work short, hand durable jobs to an application-owned worker and retain enough application state to make a recovered update safe to replay.

## Gaps and recovery

The manager detects gaps in global PTS, QTS or update-container sequence state and uses `updates.getDifference` to restore global cursor state. It uses `updates.getChannelDifference` for a channel PTS gap when it has that channel's cached access hash. Both recovery loops stop after ten non-final rounds. Events in a difference response are processed by date; this does not order independent network inputs or application workers.

The raw drainer is a cancellable background task. Call `await client.wait_for_updates()` after connection to observe its current run: processing failures propagate promptly and normal shutdown completes the wait. Cancelling the waiter leaves the drainer running. A restarted manager needs a new wait, and this method does not supervise the separate network receive-dispatch task. Later raw intake also raises an already-failed drainer's error. During `stop()`, cancellation can interrupt raw processing, shutdown re-raises an existing failure. Plan a supervised task boundary around the client and log the failure context without logging session credentials. The [production-operation guide](./production-operation.md) covers the wider shutdown order and [observability guide](./observability.md) covers the structured logging hooks.

## Practical checklist

- Make externally visible effects idempotent or deduplicate them with application-owned durable state.
- Choose `"raise"` when loss must surface and catch `asyncio.QueueFull` at the ownership boundary.
- Choose a dropping policy only when the discarded update class is acceptable for the application.
- Cancel the iterator task during shutdown; waiting for an end-of-stream signal will wait indefinitely.
- Run recovery tests through a fake or controlled invoker before enabling a live account. Credentialed integration runs are opt-in and must not be treated as ordinary unit tests; see [development notes](../development.md).
