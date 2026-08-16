---
title: Deployment
description: Lifecycle, event-loop, storage-key, credential, and acceptance boundaries for running miniproto in a service.
slug: /project/deployment/
generated: false
---

## Own the application lifecycle

Create a `Client` in the component that owns its lifecycle, connect it before invoking raw requests, and disconnect it during orderly shutdown. An async context manager is the simplest shape when the service startup/shutdown scope maps to one client. Disconnect stops updates, senders, media schedulers and pools, auxiliary clients, and storage; callers should still handle cleanup errors according to their service policy.

Do not let a library import replace the host application's asyncio policy. Scripts that own their top-level coroutine can use `miniproto.event_loop.run()`. Embedded applications retain their own running loop; advanced standalone integrations can supply `miniproto.event_loop.new_event_loop` to `asyncio.Runner`. The legacy global policy installer is deprecated and unsuitable for coordinated service startup.

## Provision durable state deliberately

Production clients use encrypted SQLite by default and require `MINIPROTO_SESSION_KEY` or constructor key material. Obtain it from the platform secret manager, never from a committed environment file or command-line argument. Use an absolute, private, per-account session path when a working-directory-relative default would be ambiguous. Keep bot tokens, API hashes, phone/2FA values, auth keys, proxy credentials, and session strings out of logs and artifacts.

`InMemorySessionStorage()` is for tests and intentionally ephemeral work. It is not a durable production substitute. Portable session strings are bearer credentials and require the same access controls as an active session database.

## Operate within Telegram and local resource limits

Telegram controls authorization, FloodWaits, and transport behavior. Bound work at the application layer, use the SDK's pending-RPC, queue, payload, and scheduler limits, and handle `FloodWait`/ambiguous requests as product events rather than trying to bypass them. A successful quick acknowledgement does not confirm an RPC result.

## Acceptance boundary

Ordinary CI disables real integration credentials. Live tests and live benchmarks are explicitly guarded and require secrets plus Telegram-side prerequisites. When those are unavailable, report the gate as not run or externally blocked; do not claim that deterministic fake coverage proves a production deployment against Telegram.
