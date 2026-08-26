---
title: Event-loop ownership
description: Select a scoped asyncio loop integration without relying on deprecated process-global policies.
slug: /guides/event-loop-ownership
generated: false
---

# Event-loop ownership

The application that starts the process should own the event loop. For a command-line application with no loop already running in the current thread, `miniproto.event_loop.run(...)` creates an `asyncio.Runner`, runs one coroutine, closes its loop and clears the current-loop reference when it finishes.

```python
from miniproto import event_loop


async def main() -> None: ...


event_loop.run(main())
```

Do not call `event_loop.run(...)` from a thread that already has a running event loop. In an async web server, notebook, GUI, test runner or library callback, await the client work from the loop the host already owns instead of nesting a runner.

## Scoped optimized loops

On Windows, miniproto selects `winloop`; on other platforms it selects `uvloop`. If that selected package is absent, the helpers fall back to the standard asyncio event loop. A broken backend import is propagated rather than silently treated as unavailable, which helps distinguish an absent optional dependency from an installation problem.

For an application that owns a runner but needs explicit configuration, use the helper as its loop factory:

```python
import asyncio

from miniproto import event_loop


with asyncio.Runner(loop_factory=event_loop.new_event_loop) as runner:
    runner.run(main())
```

`new_event_loop()` registers the new loop as current for the calling thread. The caller owns its lifecycle when using it directly; `asyncio.Runner` closes the loop it receives from its factory.

Debug runners intentionally use the standard loop for the known debug-mode incompatibilities with uvloop through 0.22.1 and winloop through 0.6.3. This is a debugging trade-off, not evidence that the optimized backend is absent.

## Avoid the legacy installer

`event_loop.install()` attempts a deprecated process-global policy installation, always raises a `DeprecationWarning` and returns `False` when a backend/hook is unavailable, installation fails or Python 3.16+ does not support policy installation. It is race-unsafe with other tasks that create loops. Prefer `event_loop.run(...)` for a top-level command or `asyncio.Runner(loop_factory=event_loop.new_event_loop)` for an owned service boundary.

The package metadata requires Python 3.13 or newer. Its declared optimized-loop dependencies target Linux/Darwin (`uvloop`) and Windows/Cygwin (`winloop`); verify the actual interpreter and installed distribution in the environment that runs the service before assuming an optimized backend is active.
