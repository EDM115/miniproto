---
title: "miniproto.media.scheduler"
description: "Coordinate fair, byte-bounded media transfers per data centre and direction."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.media.scheduler"
source_path: "src/miniproto/media/scheduler.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/scheduler.py"
module: "miniproto.media.scheduler"
---

## `miniproto.media.scheduler`

Coordinate fair, byte-bounded media transfers per data centre and direction.

## Public objects

- [`MediaDirection`](./mediadirection/) — Public type alias `miniproto.media.scheduler.MediaDirection`.
- [`MediaPriority`](./mediapriority/) — Public type alias `miniproto.media.scheduler.MediaPriority`.
- [`MediaSizeClass`](./mediasizeclass/) — Public type alias `miniproto.media.scheduler.MediaSizeClass`.
- [`MEDIA_SCHEDULER_UNIT`](./media-scheduler-unit/) — Public attribute `miniproto.media.scheduler.MEDIA_SCHEDULER_UNIT`.
- [`MEDIA_LARGE_FILE_THRESHOLD`](./media-large-file-threshold/) — Public attribute `miniproto.media.scheduler.MEDIA_LARGE_FILE_THRESHOLD`.
- [`DEFAULT_DOWNLOAD_SMALL_LIMIT`](./default-download-small-limit/) — Public attribute `miniproto.media.scheduler.DEFAULT_DOWNLOAD_SMALL_LIMIT`.
- [`DEFAULT_DOWNLOAD_LARGE_LIMIT`](./default-download-large-limit/) — Public attribute `miniproto.media.scheduler.DEFAULT_DOWNLOAD_LARGE_LIMIT`.
- [`MediaSchedulerSnapshot`](./mediaschedulersnapshot/) — Immutable byte and operation measurements for one DC/direction scheduler.
- [`MediaPermit`](./mediapermit/) — A charged scheduler reservation that must eventually be released.
- [`MediaTransfer`](./mediatransfer/) — A caller-owned transfer registration that can acquire fair media permits.
- [`MediaSchedulerRegistry`](./mediaschedulerregistry/) — Own lazy per-DC schedulers and create lifecycle-managed media transfers.
