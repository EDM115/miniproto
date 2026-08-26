---
title: "miniproto.media.scheduler.MediaSchedulerRegistry.open_transfer"
description: "Open a transfer with foreground priority by default."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.scheduler.MediaSchedulerRegistry.open_transfer"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py#L700"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler.MediaSchedulerRegistry.open_transfer`

```python
open_transfer(*, dc_id: int, direction: MediaDirection, total_size: int | None, priority: MediaPriority = 'foreground') -> MediaTransfer
```

Open a transfer with foreground priority by default.

**Parameters:**

- **dc_id** (<code>[int](#int)</code>) – Positive Telegram data-centre identifier.
- **direction** (<code>[MediaDirection](#miniproto.media.scheduler.MediaDirection)</code>) – Whether requests upload or download.
- **total_size** (<code>[int](#int) | None</code>) – Known size or ``None`` to conservatively classify it as large.
- **priority** (<code>[MediaPriority](#miniproto.media.scheduler.MediaPriority)</code>) – ``foreground`` by default; background still receives periodic grants.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the DC, direction, size or priority is invalid.
