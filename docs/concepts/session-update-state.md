---
title: Session and update state
description: Persisted session domains, update cursors, duplicate suppression, queues and gap recovery.
slug: /concepts/session-update-state/
generated: false
---

## Session state is durable by default

Unless an explicit `session_storage` is provided, `ClientConfig` uses encrypted SQLite at `miniproto.session.sqlite`. Construction requires a constructor key or `MINIPROTO_SESSION_KEY`; it fails before connecting when key material is absent or too short. `InMemorySessionStorage()` is intentionally explicit for tests and throwaway clients.

The durable record separates logical `auth`, `peers`, `update_state` and `metadata` domains. Built-in storage makes `load`, `save`, `mutate`, `clear` and `close` serialized operations. Read-modify-write changes must use the synchronous `mutate()` transform: do awaited work first, then atomically apply a detached change. That prevents a cursor, salt, peer or authorization update from erasing an unrelated concurrent change.

## Cursor commits can precede application delivery

`UpdateManager` restores global PTS, QTS and sequence values plus independent per-channel PTS cursors. It drains raw updates, suppresses duplicate or stale units, and commits cursor and entity changes before it queues normalized updates or calls handlers. If the process stops between that commit and handler delivery, the stored cursor may have passed an update the application did not process, and miniproto may not offer it again after restart. Idempotent handlers help with duplicate effects, but they do not recover a missed update. Applications that cannot accept that gap need their own reconciliation strategy. Miniproto does not provide exactly-once application processing.

The public update queue is bounded. Its configured overflow policy either raises, drops the newest item or replaces the oldest one. Dropped updates are not delivered to handlers. Stopping the manager cancels its raw drainer but does not close the public queue or end an already waiting `iter_updates()` consumer; application shutdown should cancel or otherwise coordinate that consumer.

## Gap recovery and imported state

When global PTS, QTS or container sequence state indicates a gap, the manager requests `updates.getDifference` with the stored global PTS, QTS and date, for at most ten non-final rounds. A per-channel PTS gap or `updateChannelTooLong` triggers `updates.getChannelDifference` when the session has that channel's access hash, also for at most ten rounds. Without the access hash, miniproto cannot recover that channel gap and leaves the gapped update unapplied. Recovered events are ordered by date within a difference response; that order does not extend across independent inputs or application workers.

Portable-session imports can mark the record for one `updates.getState` bootstrap after connection because external string formats do not preserve the complete miniproto update cursor. See [Session Security](../session-security.md) for storage keys and portable-session credential handling.
