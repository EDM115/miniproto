---
title: "miniproto.media.scheduler.MediaTransfer"
description: "A caller-owned transfer registration that can acquire fair media permits."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.scheduler.MediaTransfer"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py#L563"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler.MediaTransfer`

```python
MediaTransfer(registry: MediaSchedulerRegistry, *, transfer_id: str, dc_id: int, direction: MediaDirection, total_size: int | None, priority: MediaPriority) -> None
```

A caller-owned transfer registration that can acquire fair media permits.

Register this transfer using its direction, priority, and size class.

**Parameters:**

- **registry** (<code>[MediaSchedulerRegistry](#miniproto.media.scheduler.MediaSchedulerRegistry)</code>) – Registry that owns the selected scheduler.
- **transfer_id** (<code>[str](#str)</code>) – Unique registry-generated transfer name.
- **dc_id** (<code>[int](#int)</code>) – Initial data-centre binding.
- **direction** (<code>[MediaDirection](#miniproto.media.scheduler.MediaDirection)</code>) – Upload or download scheduler direction.
- **total_size** (<code>[int](#int) | None</code>) – Known total bytes, or ``None`` to classify as large.
- **priority** (<code>[MediaPriority](#miniproto.media.scheduler.MediaPriority)</code>) – Default foreground or background request priority.
