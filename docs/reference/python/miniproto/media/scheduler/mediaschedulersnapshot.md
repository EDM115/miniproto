---
title: "miniproto.media.scheduler.MediaSchedulerSnapshot"
description: "Immutable byte and operation measurements for one DC/direction scheduler."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.scheduler.MediaSchedulerSnapshot"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py#L26"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler.MediaSchedulerSnapshot`

```python
MediaSchedulerSnapshot(max_bytes: int, active_bytes: int, queued_bytes: int, active_transfers: int, queued_transfers: int, grants: int, grants_by_transfer: dict[str, int]) -> None
```

Immutable byte and operation measurements for one DC/direction scheduler.

**Attributes:**

- [**max_bytes**](#miniproto.media.scheduler.MediaSchedulerSnapshot.max_bytes) (<code>[int](#int)</code>) – Per-data-centre and direction byte ceiling in bytes.
- [**active_bytes**](#miniproto.media.scheduler.MediaSchedulerSnapshot.active_bytes) (<code>[int](#int)</code>) – Charged bytes reserved by unreleased permits.
- [**queued_bytes**](#miniproto.media.scheduler.MediaSchedulerSnapshot.queued_bytes) (<code>[int](#int)</code>) – Charged bytes waiting for a permit.
- [**active_transfers**](#miniproto.media.scheduler.MediaSchedulerSnapshot.active_transfers) (<code>[int](#int)</code>) – Transfers with at least one live permit.
- [**queued_transfers**](#miniproto.media.scheduler.MediaSchedulerSnapshot.queued_transfers) (<code>[int](#int)</code>) – Transfers with at least one queued acquire.
- [**grants**](#miniproto.media.scheduler.MediaSchedulerSnapshot.grants) (<code>[int](#int)</code>) – Total permits granted by this scheduler since creation.
- [**grants_by_transfer**](#miniproto.media.scheduler.MediaSchedulerSnapshot.grants_by_transfer) (<code>[dict](#dict)[[str](#str), [int](#int)]</code>) – Copy of total grants keyed by transfer identifier.
