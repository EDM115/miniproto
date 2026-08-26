---
title: "miniproto.media.scheduler.MediaSchedulerRegistry.configure_download_limits"
description: "Update limits for future and existing download schedulers."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.scheduler.MediaSchedulerRegistry.configure_download_limits"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py#L727"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler.MediaSchedulerRegistry.configure_download_limits`

```python
configure_download_limits(*, small_limit: int, large_limit: int) -> None
```

Update limits for future and existing download schedulers.

**Parameters:**

- **small_limit** (<code>[int](#int)</code>) – Positive concurrent small-download transfer cap.
- **large_limit** (<code>[int](#int)</code>) – Positive concurrent large-download transfer cap.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If either concurrent-transfer limit is not positive.
