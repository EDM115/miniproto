---
title: Stream and Schedule Downloads
description: Write ordered streamed chunks and run multiple bounded downloads without materializing each file.
slug: /recipes/transfers/
generated: false
---

`Client.iter_download()` yields ordered bytes and does not materialize the full file. It accepts normalized media, compatible raw media, or a miniproto file ID. The stream rejects `resume` and `multi_session`; use an explicit `offset` for a ranged continuation.

```python
from pathlib import Path

from miniproto import Client


async def stream_to_file(client: Client, file_id: str, destination: Path) -> None:
    with destination.open("wb") as output:
        async for chunk in client.iter_download(file_id, concurrency=2, max_in_flight_bytes=4 * 1024 * 1024):
            output.write(chunk)
```

The stream closes outstanding part tasks when the generator is closed or its caller is cancelled. Its `concurrency` is a bounded part-request window, not a promise of throughput; choose it alongside the byte budget and observe server flood waits, local memory, and connection health.

For separate known media objects, schedule top-level downloads concurrently and let the client-level media scheduler apply its configured per-DC budgets:

```python
import asyncio
from pathlib import Path

from miniproto import Client


async def download_pair(client: Client, first: object, second: object) -> None:
    async with asyncio.TaskGroup() as tasks:
        tasks.create_task(client.download_media(first, Path("first.bin"), concurrency=2))
        tasks.create_task(client.download_media(second, Path("second.bin"), concurrency=2))
```

`download_media()` can write to memory, a path, or a caller-owned destination; it may use multiple sessions only for complete, known-size bot downloads with sibling storage, and otherwise falls back to one session. See [Media Primitives](../media.md) for range alignment, integrity checks, CDN redirects, destinations, progress callbacks, file IDs, and cancellation semantics.
