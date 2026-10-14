---
title: "miniproto.media"
description: "Public download, upload, CDN decryption and range-cache APIs."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.media"
source_path: "src/miniproto/media/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/__init__.py"
module: "miniproto.media"
---

## `miniproto.media`

Public download, upload, CDN decryption and range-cache APIs.

## Public objects

- [`CdnError`](./cdn/cdnerror/) — Base exception for unsupported CDN responses and integrity failures.
- [`CdnIntegrityError`](./cdn/cdnintegrityerror/) — Raised when a CDN range lacks valid ``FileHash`` coverage or verification fails.
- [`CdnRedirect`](./cdn/cdnredirect/) — Metadata supplied by Telegram when it redirects a file to its CDN.
- [`decrypt_cdn_chunk`](./cdn/decrypt-cdn-chunk/) — Decrypt a CDN ciphertext range with the counter aligned to its file offset.
- [`DEFAULT_DOWNLOAD_CONCURRENCY`](./download/default-download-concurrency/) — Public attribute `miniproto.media.download.DEFAULT_DOWNLOAD_CONCURRENCY`.
- [`DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES`](./download/default-download-in-flight-bytes/) — Public attribute `miniproto.media.download.DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES`.
- [`DEFAULT_DOWNLOAD_PART_SIZE`](./download/default-download-part-size/) — Public attribute `miniproto.media.download.DEFAULT_DOWNLOAD_PART_SIZE`.
- [`DEFAULT_RANGE_CACHE_BYTES`](./download/default-range-cache-bytes/) — Public attribute `miniproto.media.download.DEFAULT_RANGE_CACHE_BYTES`.
- [`Destination`](./download/destination/) — Public type alias `miniproto.media.download.Destination`.
- [`DownloadRangeCache`](./download/downloadrangecache/) — Async LRU cache that shares exact media-range fetches and limits background prefetch tasks.
- [`MAX_DOWNLOAD_CHUNK_SIZE`](./download/max-download-chunk-size/) — Public attribute `miniproto.media.download.MAX_DOWNLOAD_CHUNK_SIZE`.
- [`MediaDownloadError`](./download/mediadownloaderror/) — Raised when a requested media range cannot be downloaded or materialized.
- [`MediaDownloadResult`](./download/mediadownloadresult/) — Completed materialized-download metadata and optional in-memory payload.
- [`MediaIntegrityError`](./download/mediaintegrityerror/) — Raised when declared file hashes or download-range invariants are violated.
- [`download_file`](./download/download-file/) — Download media into memory, a path or a caller-owned binary stream.
- [`download_location_from_media`](./download/download-location-from-media/) — Resolve a media model, raw Telegram object, file ID or input location for download.
- [`download_media`](./download/download-media/) — Resolve media and materialize it through :func:`download_file`.
- [`iter_download`](./download/iter-download/) — Stream a media range in order through a bounded window of part requests.
- [`iter_download_media`](./download/iter-download-media/) — Resolve a supported media object and stream it through :func:`iter_download`.
- [`media_from_raw`](./download/media-from-raw/) — Normalize supported raw Telegram media shapes into a :class:`Media` record.
- [`BIG_FILE_THRESHOLD`](./upload/big-file-threshold/) — Public attribute `miniproto.media.upload.BIG_FILE_THRESHOLD`.
- [`DEFAULT_CHUNK_SIZE`](./upload/default-chunk-size/) — Public attribute `miniproto.media.upload.DEFAULT_CHUNK_SIZE`.
- [`FileSource`](./upload/filesource/) — Public type alias `miniproto.media.upload.FileSource`.
- [`MediaUploadError`](./upload/mediauploaderror/) — Raised for part-cap, source-length or exhausted non-true save failures.
- [`MediaUploadResult`](./upload/mediauploadresult/) — Upload metadata and the MTProto input-file reference to reuse.
- [`ProgressCallback`](./upload/progresscallback/) — Public type alias `miniproto.media.upload.ProgressCallback`.
- [`upload_file`](./upload/upload-file/) — Upload a source as MTProto file parts and return its input-file handle.
