---
title: Recipes
description: Focused patterns for authorization, raw requests, sends, transfers, offline tests, benchmarks, and deployment.
slug: /recipes/
generated: false
---

These recipes are small adaptations of the public SDK surface, not a second API reference. They assume application credentials are protected and a client is managed with `async with` or equivalent explicit cleanup.

- [Authorize without logging secrets](./authentication.md)
- [Invoke a raw Telegram function](./raw-invocation.md)
- [Send text with result semantics](./sending.md)
- [Stream and schedule downloads](./transfers.md)
- [Run fake-server tests](./fake-server-tests.md)
- [Run deterministic benchmarks](./benchmarks.md)
- [Deploy a durable client](./deployment.md)

For detailed transfer behavior, destinations, integrity verification, and CDN handling, see [Media Primitives](../media.md). For session material and redaction, see [Session Security](../session-security.md). For Layer provenance and generated names, see [Raw API](../raw-api.md).
