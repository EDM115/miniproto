---
title: "miniproto.event_loop"
description: "Explicit optimized asyncio event-loop selection."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.event_loop"
source_path: "src/miniproto/event_loop.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/event_loop.py"
module: "miniproto.event_loop"
---

## `miniproto.event_loop`

Explicit optimized asyncio event-loop selection.

## Public objects

- [`backend_name`](./backend-name/) — Return the optimized event-loop package selected for this platform.
- [`backend`](./backend/) — Load and return the optimized backend module when it is available.
- [`backend_version`](./backend-version/) — Return the installed optimized backend version, if available.
- [`optimized_available`](./optimized-available/) — Return whether the platform's optimized event-loop backend can be loaded.
- [`installed`](./installed/) — Return whether :func:`install` last installed a legacy backend policy.
- [`install_error`](./install-error/) — Return the most recent explicit-install or backend-load error, if any.
- [`install`](./install/) — Install the backend's deprecated global policy on Python before 3.16.
- [`new_event_loop`](./new-event-loop/) — Create and register an optimized loop, falling back to asyncio's loop.
- [`run`](./run/) — Run one coroutine with an optimized ``asyncio.Runner`` when possible.
