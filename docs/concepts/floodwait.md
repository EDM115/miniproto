---
title: Method FloodWait policy
description: How miniproto remembers method-scoped waits, decides whether to sleep, and preserves caller control.
slug: /concepts/floodwait/
generated: false
---

## A FloodWait is Telegram's instruction to pause

Telegram can return a `FloodWait` with a number of seconds. It is not a transport retry and it is not an error that a client should bypass by making more concurrent requests. `miniproto` surfaces the typed error unless the caller has explicitly configured a short-enough automatic wait.

`ClientConfig.flood_sleep_threshold` defaults to `None`, which disables automatic sleeping for ordinary invocation. A per-call threshold overrides the configuration. The client sleeps only when the wait is at or below that threshold and the configured request-retry budget still permits another attempt; otherwise it raises. Some media helpers have their own documented option defaults, so inspect the helper contract instead of assuming the general client default.

## Method-local remembered waits

Each client owns a bounded LRU `MethodFloodWaitCache`, with a default capacity of 512 entries and a monotonic deadline. Before invoking a request, the client checks the innermost Telegram method name. A remaining cached wait is treated just like a fresh server wait: it either sleeps under the same threshold/retry rules or is raised without sending another request.

The cache stores generic `FLOOD_WAIT` and `FLOOD_PREMIUM_WAIT` forms. It deliberately does not turn arbitrary method-specific error names into a global throttle, and it never shortens an existing remembered deadline. Expiry is observed lazily on lookup.

## Operational guidance

Handle a surfaced `FloodWait` at the product layer when the operation's timing, cancellation, user feedback, or queueing policy matters. Keep request concurrency bounded, preserve request identity where Telegram supports de-duplication, and do not treat automatic sleep as a guarantee that the next attempt will succeed. Record the wait and method in safe telemetry, but do not log credentials or raw session material.

FloodWait behavior is Alpha API behavior: cache coverage, helper defaults, and retry integration should be regression-tested against the version being deployed.
