---
title: "miniproto.updates"
description: "Update-stream management, persistent cursors, duplicate tracking, and handler registration."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.updates"
source_path: "src/miniproto/updates/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/__init__.py"
module: "miniproto.updates"
---

## `miniproto.updates`

Update-stream management, persistent cursors, duplicate tracking, and handler registration.

## Public objects

- [`UpdateHandler`](./manager/updatehandler/) — Public attribute `miniproto.updates.manager.UpdateHandler`.
- [`UpdateInvoker`](./manager/updateinvoker/) — Public attribute `miniproto.updates.manager.UpdateInvoker`.
- [`UpdateManager`](./manager/updatemanager/) — Process Telegram updates into public events while persisting recovery state.
- [`UpdateQueueOverflowPolicy`](./manager/updatequeueoverflowpolicy/) — Public attribute `miniproto.updates.manager.UpdateQueueOverflowPolicy`.
- [`DuplicateTracker`](./state/duplicatetracker/) — Bounded insertion-ordered set for duplicate suppression across persisted update state.
- [`EntityReference`](./state/entityreference/) — Persistent, normalized peer data learned while processing updates.
- [`UpdateCursor`](./state/updatecursor/) — Immutable global and per-channel update state persisted in a session record.
