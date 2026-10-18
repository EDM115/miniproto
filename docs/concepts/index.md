---
title: Concepts
description: The protocol, lifecycle, reliability, scheduling, schema and security boundaries behind miniproto.
slug: /concepts/
generated: false
---

`miniproto` is an async-first MTProto SDK. These pages describe its protocol, client lifecycle, update and session state, media scheduling and security rules. It does not replace Telegram's services or provide an application framework.

## Core model

- [MTProto and the Bot API](./mtproto-and-bot-api.md) explains which Telegram protocol miniproto implements and what it permits.
- [Architecture and data flow](./architecture.md) follows an application request through client coordination, storage, sender, transport, framing and Telegram.
- [High-level helpers and the raw API](./high-level-and-raw.md) separates the small convenience layer from generated TL requests.
- [Schema sources and layers](./schema-layers.md) records the Layer 230 canonical-source policy.

## Stateful operation

- [Session and update state](./session-update-state.md) covers encrypted persistence, cursors, duplicates, queues and gap recovery.
- [Transport, reliability and replay](./transport-reliability.md) explains framing, reconnects, quick acknowledgements and ambiguous requests.
- [Transfer scheduling](./transfer-scheduler.md) explains the per-DC byte budget and fairness model for media work.
- [Method FloodWait policy](./floodwait.md) explains cached waits, automatic sleep and when an error remains visible to the caller.

## Performance and security boundaries

- [Native Rust acceleration and fallback](./native-acceleration.md) explains capability detection and parity without treating native availability as a performance guarantee.
- [Security model](./security-model.md) explains credential, storage, validation and operational boundaries. For reporting a vulnerability, use the repository's [security and reporting page](../project/security.md).

## Alpha contract

Miniproto is pre-release Alpha software. Public APIs, defaults, storage formats, generated schemas and compatibility rules can change before a stable release. Local tests do not establish live Telegram behavior.
