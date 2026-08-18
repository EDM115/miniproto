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
- [Changelog](https://github.com/EDM115/miniproto/blob/master/CHANGELOG.md) describes the complete `0.1.0` Alpha capability and limitation set without narrating private pre-release snapshots.
- [Migration](./migration.md) covers the current Alpha changes most likely to affect storage, session strings, custom backends, and generated raw imports.
- [Deployment](./deployment.md) covers lifecycle ownership, durable-session keys, secret handling, and the difference between deterministic and credentialed gates.
- [Security and reporting](./security.md) links to the canonical security policy and states what not to disclose publicly.
- [Brand assets](./brand.md) records the provisional Packet Loom identity, generated derivatives, and the intentionally swappable poll boundary.

## Codebase map

The contributor-oriented codebase map is source-grounded and deliberately separate from user API reference pages:

- [Technology stack](../codebase/STACK.md) maps runtimes, dependencies, tooling, commands, and environment constraints.
- [Structure](../codebase/STRUCTURE.md) maps entry points, directory ownership, generated boundaries, and naming.
- [Architecture](../codebase/ARCHITECTURE.md) traces request/response flow, module responsibilities, repeated patterns, and risks.
- [Conventions](../codebase/CONVENTIONS.md) records formatting, imports, public exports, errors, logs, docs, and test rules.
- [Integrations](../codebase/INTEGRATIONS.md) records Telegram, storage, proxy, schema, registry, and hosting boundaries.
- [Testing](../codebase/TESTING.md) maps the offline, fake-server, native, browser, live, stress, benchmark, and wheel gates.
- [Concerns](../codebase/CONCERNS.md) tracks current release evidence gaps, fragile areas, security/performance risks, and intent-versus-reality divergences.

The existing [development guide](../development.md) remains the authoritative command reference. The [faked-method ledger](../faked-methods.md) records where deterministic substitutions or credential-gated validation still limit an acceptance claim.
