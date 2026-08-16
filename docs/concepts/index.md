---
title: Concepts
description: The protocol, lifecycle, reliability, scheduling, schema, and security boundaries behind miniproto.
slug: /concepts/
generated: false
---

`miniproto` is an async-first MTProto SDK, not a Telegram application framework or a replacement for Telegram's own rules and services. These pages explain the boundaries that matter when choosing APIs, operating a client, or reviewing a change.

## Core model

- [MTProto and the Bot API](./mtproto-and-bot-api.md) explains which Telegram surface miniproto speaks and what that does not authorize.
- [Architecture and data flow](./architecture.md) follows an application request through client coordination, storage, sender, transport, framing, and Telegram.
- [High-level helpers and the raw API](./high-level-and-raw.md) separates the small convenience layer from generated TL requests.
- [Schema sources and layers](./schema-layers.md) records the Layer 228 canonical-source policy.

## Stateful operation

- [Session and update state](./session-update-state.md) covers encrypted persistence, cursors, duplicates, queues, and gap recovery.
- [Transport, reliability, and replay](./transport-reliability.md) explains framing, reconnects, quick acknowledgements, and ambiguous requests.
- [Transfer scheduling](./transfer-scheduler.md) explains the per-DC byte budget and fairness model for media work.
- [Method FloodWait policy](./floodwait.md) explains cached waits, automatic sleep, and when an error remains visible to the caller.

## Performance and security boundaries

- [Native Rust acceleration and fallback](./native-acceleration.md) explains capability detection and parity without treating native availability as a performance guarantee.
- [Security model](./security-model.md) explains credential, storage, validation, and operational boundaries. For reporting a vulnerability, use the repository's [security and reporting page](../project/security.md).

## Alpha contract

This is pre-release documentation for an Alpha SDK. Public behavior, defaults, storage formats, generated schema surfaces, and compatibility policies can change before a stable release. Unit and fake-server evidence is valuable, but it is distinct from credentialed live Telegram acceptance; a feature is not live-accepted merely because it has deterministic coverage.
