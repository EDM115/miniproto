---
title: Task-oriented guides
description: Operational guidance for updates, sessions, event loops, observability, networking, native support, and benchmarks.
slug: /guides
generated: false
---

# Task-oriented guides

These guides connect the public API to the operating constraints that tend to matter after a prototype becomes a service. They describe the current `0.1.x` Alpha behavior; use the generated API reference for individual symbols and [development notes](../development.md) for the complete local command reference.

- [Updates and recovery](./updates.md) explains queue limits, persistent cursors, difference recovery, handler ordering, and cancellation.
- [String-session migration](./string-sessions.md) covers native, Telethon, and Pyrogram session strings and the import safety checks.
- [Production operation](./production-operation.md) covers ownership, shutdown, resources, and redaction.
- [Observability](./observability.md) covers logging, metrics, and resource snapshots.
- [Proxies and datacenters](./proxies-and-datacenters.md) explains transport proxy URLs and the separation between primary and media DC state.
- [Event-loop ownership](./event-loop-ownership.md) covers application-owned loops, runners, and the legacy installer.
- [Troubleshooting](./troubleshooting.md) gives targeted recovery paths for common startup, update, proxy, native, and test-gate failures.
- [Native extension diagnosis](./native-extension.md) explains the Rust extension probe and the Python fallback boundary.
- [Performance and benchmarks](./performance-and-benchmarks.md) explains what the benchmark commands measure and which results are comparable.

Security and media details remain in their canonical pages: [session storage and credentials](../session-security.md) and [media transfers](../media.md).
