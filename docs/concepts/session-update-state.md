---
title: Session and update state
description: Persisted session domains, update cursors, duplicate suppression, queues and gap recovery.
slug: /concepts/session-update-state/
generated: false
---

## Session state is durable by default

Unless an explicit `session_storage` is provided, `ClientConfig` uses encrypted SQLite at `miniproto.session.sqlite`. Construction requires a constructor key or `MINIPROTO_SESSION_KEY`; it fails before connecting when key material is absent or too short. `InMemorySessionStorage()` is intentionally explicit for tests and throwaway clients.

The durable record separates logical `auth`, `peers`, `update_state` and `metadata` domains. Built-in storage makes `load`, `save`, `mutate`, `clear` and `close` serialized operations. Read-modify-write changes must use the synchronous `mutate()` transform: do awaited work first, then atomically apply a detached change. That prevents a cursor, salt, peer or authorization update from erasing an unrelated concurrent change.

## Update delivery is stateful, not exactly once

`UpdateManager` restores persisted cursor state, drains raw updates in the background, suppresses duplicate or stale units, persists cursor/entity changes and only then queues normalized public updates and runs handlers. This means persisted state is ahead of or equal to observable application delivery. It does not provide application-level exactly-once processing; handlers should be idempotent when the product needs stronger delivery semantics.

The public update queue is bounded. Its configured overflow policy either raises, drops the newest item or replaces the oldest one. Dropped updates are not delivered to handlers. Stopping the manager cancels its raw drainer but does not close the public queue or end an already waiting `iter_updates()` consumer; application shutdown should cancel or otherwise coordinate that consumer.

## Gap recovery and imported state

When PTS or sequence state indicates a gap, the manager requests `updates.getDifference` for global recovery, with a bounded number of rounds. Channel recovery requires a cached access hash and has its own bounded difference loop. Recovered events are date-ordered within one difference response, but this is not a global ordering promise across independent inputs.

Portable-session imports can mark the record for one `updates.getState` bootstrap after connection because external string formats do not preserve the complete miniproto update cursor. See [Session Security](../session-security.md) for storage keys and portable-session credential handling.
