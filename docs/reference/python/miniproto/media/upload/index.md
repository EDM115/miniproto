---
title: "miniproto.media.upload"
description: "Upload sources as concurrent Telegram file parts with bounded read-ahead."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.media.upload"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py"
module: "miniproto.media.upload"
---

## `miniproto.media.upload`

Upload sources as concurrent Telegram file parts with bounded read-ahead.

## Public objects

- [`DEFAULT_CHUNK_SIZE`](./default-chunk-size/) — Public attribute `miniproto.media.upload.DEFAULT_CHUNK_SIZE`.
- [`BIG_FILE_THRESHOLD`](./big-file-threshold/) — Public attribute `miniproto.media.upload.BIG_FILE_THRESHOLD`.
- [`DEFAULT_UPLOAD_FLOOD_SLEEP_THRESHOLD`](./default-upload-flood-sleep-threshold/) — Public attribute `miniproto.media.upload.DEFAULT_UPLOAD_FLOOD_SLEEP_THRESHOLD`.
- [`DEFAULT_UPLOAD_PART_TIMEOUT`](./default-upload-part-timeout/) — Public attribute `miniproto.media.upload.DEFAULT_UPLOAD_PART_TIMEOUT`.
- [`DEFAULT_UPLOAD_CONCURRENCY`](./default-upload-concurrency/) — Public attribute `miniproto.media.upload.DEFAULT_UPLOAD_CONCURRENCY`.
- [`ProgressCallback`](./progresscallback/) — Public type alias `miniproto.media.upload.ProgressCallback`.
- [`FileSource`](./filesource/) — Public type alias `miniproto.media.upload.FileSource`.
- [`MediaUploadError`](./mediauploaderror/) — Raised for part-cap, source-length or exhausted non-true save failures.
- [`RawInvoker`](./rawinvoker/) — Public type alias `miniproto.media.upload.RawInvoker`.
- [`MediaUploadResult`](./mediauploadresult/) — Upload metadata and the MTProto input-file reference to reuse.
- [`upload_file`](./upload-file/) — Upload a source as MTProto file parts and return its input-file handle.
