---
title: Migration
description: Current Alpha migration boundaries for session storage, portable sessions, custom backends and generated raw API changes.
slug: /project/migration/
generated: false
---

## Expect Alpha breaking changes

Before a stable release, `miniproto` may make intentional breaking changes. Pin the deployed version, read its changelog and test a migration with a copied non-production account/session before applying it to a durable deployment. Do not assume that a pre-1.0 helper, generated import, serialized session or default remains source-compatible indefinitely.

## Durable session storage is now the default

`Client(ClientConfig(...))` uses encrypted SQLite at `miniproto.session.sqlite` when `session_storage` is omitted. It requires a constructor key or `MINIPROTO_SESSION_KEY`; callers that previously expected an ephemeral default must explicitly pass `InMemorySessionStorage()` for tests or throwaway use. `session_storage` takes precedence over `session_path`.

Use a distinct session path for each account/deployment. Do not point multiple unrelated accounts at the same default relative file. See [Session Security](../session-security.md) for authenticated storage, key material and operational handling.

## Custom storage and portable sessions

Custom `SessionStorage` implementations must provide atomic synchronous `mutate()` and `domain_revisions()` behavior. An unlocked `load()` followed by `save()` can lose concurrent authorization, peer, update, salt or media-DC changes and is not conformant.

Portable string import is deliberately guarded: it requires a disconnected client and refuses to replace nonempty storage unless `replace=True` is explicit. Telethon and Pyrogram formats preserve less state than a full miniproto record; configure original API credentials and allow the documented one-time update-state bootstrap. Treat every imported string and passphrase as a bearer secret.

## Generated raw API changes

The raw surface follows the pinned Layer 229 schema policy. A schema update can add/remove generated classes or fields, change available imports and remove a constructor that was present in an earlier snapshot. Regenerate and review the raw diff rather than carrying handwritten patches in generated files. The [schema and layer concept](../concepts/schema-layers.md) describes the source policy; the [development guide](../development.md) gives the authoritative commands.
