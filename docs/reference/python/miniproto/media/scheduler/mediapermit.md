---
title: "miniproto.media.scheduler.MediaPermit"
description: "A charged scheduler reservation that must eventually be released."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.scheduler.MediaPermit"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py#L89"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler.MediaPermit`

```python
MediaPermit(scheduler: _MediaScheduler, state: _TransferState, charged_bytes: int) -> None
```

A charged scheduler reservation that must eventually be released.

Use as an async context manager or call :meth:`release`. The first release
returns capacity; repeated releases are harmless and return capacity at most
once. Holding a permit keeps its charged bytes and transfer operation slot
active, even after transfer closure, until it is released.

Bind a newly granted charge to its scheduler and transfer state.

**Parameters:**

- **scheduler** (<code>[_MediaScheduler](#miniproto.media.scheduler._MediaScheduler)</code>) – Private owner that accounts for release capacity.
- **state** (<code>[_TransferState](#miniproto.media.scheduler._TransferState)</code>) – Registered transfer state whose live-permit count is updated.
- **charged_bytes** (<code>[int](#int)</code>) – Already rounded reservation size in bytes.
