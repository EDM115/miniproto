---
title: "miniproto.media.scheduler.MediaSchedulerRegistry"
description: "Own lazy per-DC schedulers and create lifecycle-managed media transfers."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.scheduler.MediaSchedulerRegistry"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py#L631"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler.MediaSchedulerRegistry`

```python
MediaSchedulerRegistry(*, download_max_bytes: int, upload_max_bytes: int, download_small_limit: int = DEFAULT_DOWNLOAD_SMALL_LIMIT, download_large_limit: int = DEFAULT_DOWNLOAD_LARGE_LIMIT) -> None
```

Own lazy per-DC schedulers and create lifecycle-managed media transfers.

Configure byte caps and download operation limits.

**Parameters:**

- **download_max_bytes** (<code>[int](#int)</code>) – Per-DC download charged-byte ceiling in bytes.
- **upload_max_bytes** (<code>[int](#int)</code>) – Per-DC upload charged-byte ceiling in bytes.
- **download_small_limit** (<code>[int](#int)</code>) – Concurrent small download-transfer cap.
- **download_large_limit** (<code>[int](#int)</code>) – Concurrent large download-transfer cap.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If a byte cap is below one scheduler unit or an
operation limit is not positive.
