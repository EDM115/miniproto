---
title: "miniproto.media.scheduler.MediaTransfer.rebind"
description: "Move future queued work to ``dc_id`` while live permits drain in place."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.scheduler.MediaTransfer.rebind"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py#L594"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler.MediaTransfer.rebind`

```python
rebind(dc_id: int) -> None
```

Move future queued work to ``dc_id`` while live permits drain in place.

**Parameters:**

- **dc_id** (<code>[int](#int)</code>) – Destination data-centre identifier.

**Raises:**

- <code>[RuntimeError](#RuntimeError)</code> – If this transfer has been closed.
