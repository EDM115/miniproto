---
title: "miniproto.media.scheduler.MediaTransfer.acquire"
description: "Acquire a charged byte reservation, optionally overriding request priority."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.scheduler.MediaTransfer.acquire"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py#L607"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler.MediaTransfer.acquire`

```python
acquire(requested_bytes: int, *, priority: MediaPriority | None = None) -> MediaPermit
```

Acquire a charged byte reservation, optionally overriding request priority.

**Parameters:**

- **requested_bytes** (<code>[int](#int)</code>) – Positive payload size charged in 64 KiB units.
- **priority** (<code>[MediaPriority](#miniproto.media.scheduler.MediaPriority) | None</code>) – Per-request foreground/background override, if needed.

**Raises:**

- <code>[RuntimeError](#RuntimeError)</code> – If this transfer has been closed.
- <code>[ValueError](#ValueError)</code> – If the request cannot fit its scheduler's byte limit.
