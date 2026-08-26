---
title: Transfer scheduler
description: Fair, byte-bounded media scheduling by Telegram data centre and transfer direction.
slug: /concepts/transfer-scheduler/
generated: false
---

## What is being scheduled

Media requests are not controlled only by a count of coroutines. `MediaSchedulerRegistry` owns lazy schedulers keyed by `(data centre, direction)`, where direction is upload or download. A transfer opens a registration, then acquires a permit before a chunk request. Each permit charges the request rounded up to a 64 KiB unit and returns capacity exactly once when released.

The default `ClientConfig` byte budgets are 16 MiB per DC for downloads and 8 MiB per DC for uploads. Download schedulers also default to five active small transfers and two active large transfers. A known transfer at or above 20 MiB and any unknown-size transfer, is classified as large. These are local resource limits, not claims about Telegram's own throughput or rate limits.

## Fairness and priority

Within one scheduler, grants use deficit round robin over logical transfers. A foreground request is preferred, but a queued background transfer receives a periodic grant rather than being allowed to starve indefinitely. Queue and active-byte measurements are exposed through `MediaSchedulerSnapshot` for observability and deterministic tests.

The fairness scope is intentional: two different data centres and uploads versus downloads, do not contend through one global budget. This isolates unrelated workload while still ensuring that transfers aimed at the same DC and direction share capacity fairly.

## Cancellation, migration and closure

Cancelling a queued acquire removes it; cancelling immediately after grant releases the just-granted capacity. Closing a transfer rejects new acquires and cancels still-pending work, while a live permit remains charged until its owner releases it. This prevents cancellation and shutdown from leaking scheduler capacity.

When Telegram redirects future work to another DC, a transfer can rebind. Pending future work moves to the new scheduler; already granted permits drain at the old binding. Schedulers are evicted only after complete drain and client disconnect closes the registry. Use `async with` for a permit whenever practical so exceptional control flow returns capacity.
