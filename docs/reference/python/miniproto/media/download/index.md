---
title: "miniproto.media.download"
description: "Download ordered Telegram media ranges with retries, hash checks and range caching."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.media.download"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py"
module: "miniproto.media.download"
---

## `miniproto.media.download`

Download ordered Telegram media ranges with retries, hash checks and range caching.

## Public objects

- [`Destination`](./destination/) — Public type alias `miniproto.media.download.Destination`.
- [`MediaDownloadError`](./mediadownloaderror/) — Raised when a requested media range cannot be downloaded or materialized.
- [`MediaIntegrityError`](./mediaintegrityerror/) — Raised when declared file hashes or download-range invariants are violated.
- [`MAX_DOWNLOAD_CHUNK_SIZE`](./max-download-chunk-size/) — Public attribute `miniproto.media.download.MAX_DOWNLOAD_CHUNK_SIZE`.
- [`DEFAULT_DOWNLOAD_PART_SIZE`](./default-download-part-size/) — Public attribute `miniproto.media.download.DEFAULT_DOWNLOAD_PART_SIZE`.
- [`DEFAULT_DOWNLOAD_CONCURRENCY`](./default-download-concurrency/) — Public attribute `miniproto.media.download.DEFAULT_DOWNLOAD_CONCURRENCY`.
- [`DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES`](./default-download-in-flight-bytes/) — Public attribute `miniproto.media.download.DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES`.
- [`DEFAULT_RANGE_CACHE_BYTES`](./default-range-cache-bytes/) — Public attribute `miniproto.media.download.DEFAULT_RANGE_CACHE_BYTES`.
- [`MediaDownloadResult`](./mediadownloadresult/) — Completed materialized-download metadata and optional in-memory payload.
- [`DownloadRangeCache`](./downloadrangecache/) — Async LRU cache that shares exact media-range fetches and limits background prefetch tasks.
- [`iter_download`](./iter-download/) — Stream a media range in order through a bounded window of part requests.
- [`download_file`](./download-file/) — Download media into memory, a path or a caller-owned binary stream.
- [`iter_download_media`](./iter-download-media/) — Resolve a supported media object and stream it through :func:`iter_download`.
- [`download_media`](./download-media/) — Resolve media and materialize it through :func:`download_file`.
- [`download_location_from_media`](./download-location-from-media/) — Resolve a media model, raw Telegram object, file ID or input location for download.
- [`media_from_raw`](./media-from-raw/) — Normalize supported raw Telegram media shapes into a :class:`Media` record.
