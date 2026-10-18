---
title: Method FloodWait policy
description: How miniproto remembers method-scoped waits, decides whether to sleep and preserves caller control.
slug: /concepts/floodwait/
generated: false
---

## A FloodWait is Telegram's instruction to pause

Telegram's `FloodWait` gives the number of seconds to pause before retrying a method. Miniproto surfaces the typed error unless the caller has configured an automatic wait short enough to fit the threshold and retry budget. More concurrent requests do not bypass Telegram's wait.

`ClientConfig.flood_sleep_threshold` defaults to `None`, which disables automatic sleeping for ordinary invocation. A per-call threshold overrides the configuration. The client sleeps only when the wait is at or below that threshold and the configured request-retry budget still permits another attempt; otherwise it raises. Some media helpers have their own documented option defaults, so inspect the helper contract instead of assuming the general client default.

## Method-local remembered waits

Each client owns a bounded LRU `MethodFloodWaitCache`, with a default capacity of 512 entries and a monotonic deadline. Before invoking a request, the client checks the innermost Telegram method name. A remaining cached wait is treated just like a fresh server wait: it either sleeps under the same threshold/retry rules or is raised without sending another request.

The cache stores generic `FLOOD_WAIT` and `FLOOD_PREMIUM_WAIT` forms. It deliberately does not turn arbitrary method-specific error names into a global throttle and it never shortens an existing remembered deadline. Expiry is observed lazily on lookup.

## Operational guidance

Handle a surfaced `FloodWait` at the product layer when timing, cancellation, user feedback or queueing matters. Keep request concurrency bounded and preserve request identity when Telegram supports de-duplication. An automatic sleep does not guarantee that the next attempt will succeed. Record the wait and method in safe telemetry, never credentials or raw session material.

FloodWait behavior is Alpha API behavior: cache coverage, helper defaults and retry integration should be regression-tested against the version being deployed.
