---
title: Project
description: Contribution, release, migration, deployment, and security-reporting entry points for miniproto.
slug: /project/
generated: false
---

## Working on an Alpha SDK

`miniproto` is in active Alpha development. Its public protocol surface, schema layer, storage behavior, native capability routing, and operational defaults can change before a stable release. Treat planned work and deterministic tests as evidence of local implementation, not as a substitute for completed release or live Telegram acceptance.

## Project operations

- [Contributing](./contributing.md) points to the repository contribution policy and canonical developer command reference.
- [Release](./release.md) explains the non-mutating release gate and the boundary between checks and user-controlled publishing.
- [Migration](./migration.md) covers the current Alpha changes most likely to affect storage, session strings, custom backends, and generated raw imports.
- [Deployment](./deployment.md) covers lifecycle ownership, durable-session keys, secret handling, and the difference between deterministic and credentialed gates.
- [Security and reporting](./security.md) links to the canonical security policy and states what not to disclose publicly.

The existing [development guide](../development.md) remains the authoritative command reference. The [faked-method ledger](../faked-methods.md) records where deterministic substitutions or credential-gated validation still limit an acceptance claim.
