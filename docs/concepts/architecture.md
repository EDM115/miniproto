---
title: Architecture and data flow
description: How application work moves through the client, state, raw invocation, transport, and Telegram.
slug: /concepts/architecture/
generated: false
---

## The request path

`Client` is the application-facing coordinator. It owns configuration, session storage, peer and update coordination, sender lifecycle, media pools, and per-data-centre schedulers. A connected client accepts either a small set of convenience calls or a generated raw request through `Client.invoke()`.

```text
application
  -> Client helper or Client.invoke(raw request)
  -> peer/update/media coordination and session state
  -> MTProtoSender: message IDs, pending RPCs, acknowledgements, reconnect policy
  -> TCP transport and frame codec
  -> MTProto encryption/TL serialization
  -> Telegram data centre
```

The response travels back through the sender's single receive loop. It is validated and matched to a pending request, delivered as an unsolicited message, or passed to the update dispatcher. A quick acknowledgement is only an early transport receipt; it is not a completed RPC result.

## State beside the request path

Session storage persists authorization, DC options, user identity, peer data, update cursor state, salts, and metadata. The default client backend is encrypted SQLite; an explicit in-memory backend is available for tests and throwaway work. Updates and peer/cache changes use atomic storage mutation rather than an unlocked load-edit-save sequence.

Media work has a related but separate path. A `Client` creates scheduler registrations by data centre and direction, then media sender lanes perform raw upload/download requests. This keeps byte capacity and fairness accounting local to the relevant DC rather than treating every transfer as one global queue.

## Lifecycle ownership

`async with Client(...)` connects on entry and disconnects on exit. `connect()` starts update handling when enabled; raw sender construction is lazy when a request needs it. `disconnect()` stops updates, dispatch, media pools and schedulers, auxiliary clients, and storage, then re-raises the first cleanup failure after attempting the remaining cleanup.

Applications embedded in another async runtime retain their event-loop ownership. `miniproto.event_loop.run()` is for scripts that own the top-level coroutine; the deprecated global-policy installer is not the normal integration path.

## What this diagram does not promise

The diagram describes local control flow, not a guarantee that Telegram has accepted a request, that an update will be delivered exactly once to application code, or that a live network path is available. See [transport reliability](./transport-reliability.md) and [session and update state](./session-update-state.md) for those contracts.
