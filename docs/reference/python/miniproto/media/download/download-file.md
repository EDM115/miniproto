---
title: "miniproto.media.download.download_file"
description: "Download media into memory, a path or a caller-owned binary stream."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.download_file"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L1348"
aliases: ["miniproto.media.download_file"]
module: "miniproto.media.download"
---

## `miniproto.media.download.download_file`

```python
download_file(invoke: RawInvoker, location: object, destination: Destination = None, *, offset: int = 0, limit: int | None = None, part_size: int = DEFAULT_DOWNLOAD_PART_SIZE, resume: bool = False, progress: ProgressCallback | None = None, precise: bool = False, cdn_supported: bool = True, total_size: int | None = None, request_timeout: float | None = None, max_retries: int = 2, flood_sleep_threshold: int | None = 30, max_buffer_size: int | None = None, concurrency: int = DEFAULT_DOWNLOAD_CONCURRENCY, adaptive_concurrency: bool = True, launch_stagger: bool = True, max_in_flight_bytes: int | None = None, adaptive_part_size: bool = True, max_part_size: int = MAX_DOWNLOAD_CHUNK_SIZE, range_cache: DownloadRangeCache | bool | None = None, range_cache_key: str | None = None, range_cache_max_bytes: int = DEFAULT_RANGE_CACHE_BYTES, read_ahead_bytes: int = 0, verify_plain_hashes: bool = False, file_reference_refresher: FileReferenceRefresher | None = None) -> MediaDownloadResult
```

Download media into memory, a path or a caller-owned binary stream.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.download.RawInvoker)</code>) – Async raw-RPC invoker used for Telegram file requests.
- **location** (<code>[object](#object)</code>) – Telegram input file location to retrieve.
- **destination** (<code>[Destination](#miniproto.media.download.Destination)</code>) – ``None`` for in-memory bytes, a path to create/overwrite or an open binary stream written from its current position.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, a multiple of 1 KiB, defaults to ``0``.
- **limit** (<code>[int](#int) | None</code>) – Exact requested byte count or ``None`` to continue until EOF.
- **part_size** (<code>[int](#int)</code>) – Initial power-of-two request size from 1 KiB through one MiB, defaults to 512 KiB.
- **resume** (<code>[bool](#bool)</code>) – Retain an existing path's 1 KiB-aligned prefix and fetch from ``offset`` plus that length, defaults to ``False``. It does not verify the retained prefix.
- **progress** (<code>[ProgressCallback](#miniproto.media.upload.ProgressCallback) | None</code>) – Optional synchronous or async ``(current, total)`` callback. ``current`` counts acknowledged operation bytes including a retained resume prefix, ``total`` is the effective ``limit`` or otherwise ``total_size``.
- **precise** (<code>[bool](#bool)</code>) – Request Telegram's 1 KiB precise mode, enabled automatically when required.
- **cdn_supported** (<code>[bool](#bool)</code>) – Permit CDN redirects and their mandatory block verification.
- **total_size** (<code>[int](#int) | None</code>) – Known full file size used to preserve finite concurrent coverage.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional timeout in seconds passed to each raw request.
- **max_retries** (<code>[int](#int)</code>) – Non-flood transient retry budget per part, defaults to two.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Maximum retryable server flood wait in seconds, defaults to 30, ``None`` disables flood retries. Eligible waits retain their local slot and use a separate 16-retry cap per part.
- **max_buffer_size** (<code>[int](#int) | None</code>) – Legacy byte window alias used when ``max_in_flight_bytes`` is absent.
- **concurrency** (<code>[int](#int)</code>) – Maximum active part requests for finite ranges and queued destination writes, defaults to six. Unknown-length transfers use one part request at a time.
- **adaptive_concurrency** (<code>[bool](#bool)</code>) – Reduce new request slots on disconnects/timeouts, recover after clean completions, or keep one slot after a premium flood wait.
- **launch_stagger** (<code>[bool](#bool)</code>) – Pace start and flood-recovery request launches.
- **max_in_flight_bytes** (<code>[int](#int) | None</code>) – Local wire-byte window for part requests, separate from the writer queue and retained output. Defaults to 8 MiB, increased to ``part_size * concurrency`` for a larger finite-range window.
- **adaptive_part_size** (<code>[bool](#bool)</code>) – Probe larger legal parts for transfers of at least 8 MiB or unknown size.
- **max_part_size** (<code>[int](#int)</code>) – Upper bound for adaptive parts, no greater than one MiB.
- **range_cache** (<code>[DownloadRangeCache](#miniproto.media.download.DownloadRangeCache) | [bool](#bool) | None</code>) – Borrowed cache instance or ``True`` for shared cache. ``False`` disables caching, ``None`` selects the shared cache only when read-ahead is enabled.
- **range_cache_key** (<code>[str](#str) | None</code>) – Stable media identity required for caching and read-ahead, this raw-location API does not infer it.
- **range_cache_max_bytes** (<code>[int](#int)</code>) – Capacity used by an implicit shared cache.
- **read_ahead_bytes** (<code>[int](#int)</code>) – Speculative cache-fill distance ahead of consumed parts. Disabled for open-ended requests or finite ranges reaching the known EOF.
- **verify_plain_hashes** (<code>[bool](#bool)</code>) – Verify non-CDN data against complete SHA-256 hash intervals, fetching missing interval bytes before writing the requested slice. Retained resume bytes are not checked.
- **file_reference_refresher** (<code>[FileReferenceRefresher](#miniproto.media.download.FileReferenceRefresher) | None</code>) – Optional sync/async callback for one stale-reference refresh per part.

**Returns:**

- <code>[MediaDownloadResult](#miniproto.media.download.MediaDownloadResult)</code> – Metadata including the output path or stream. With ``destination=None``, ``data`` contains the downloaded bytes and ``destination`` holds the internal ``BytesIO``. Caller-provided streams remain open.

<details class="destination-ownership-and-rollback" open markdown="1">
<summary>Destination Ownership and Rollback</summary>

``None`` creates an internal ``BytesIO``. Paths create parent directories and overwrite existing non-resume contents. Resume truncates any non-1-KiB tail and retains at most the requested limit. Cleanup removes new paths, truncates existing paths to the retained prefix, clears internal buffers and restores caller ``BytesIO`` contents and position. Other caller streams remain open without rollback.
Failure cleanup joins owned part and writer tasks before restoring the destination, including under repeated cancellation. Secondary progress, write acknowledgement or cleanup errors do not replace the original failure. Progress callbacks remain cancellable during error reporting. Filesystem restoration errors are logged. Borrowed range-cache work remains cache-owned. Payload/key buffers are not explicitly zeroized. The local byte window excludes the writer queue, cached payloads, prefetch and extra hash-verification requests.

</details>

**Raises:**

- <code>[ValueError](#ValueError)</code> – An offset, limit, part/cache/window option is invalid.
- <code>[TypeError](#TypeError)</code> – ``verify_plain_hashes`` or ``launch_stagger`` is not boolean.
- <code>[MediaDownloadError](#miniproto.media.download.MediaDownloadError)</code> – A response, finite range or destination write is invalid.
- <code>[MediaIntegrityError](#miniproto.media.download.MediaIntegrityError)</code> – Optional plain-file integrity verification fails.
- <code>[CdnIntegrityError](#miniproto.media.cdn.CdnIntegrityError)</code> – CDN hash coverage or digest verification fails.
- <code>[OSError](#OSError)</code> – A path destination cannot be created, written, flushed or truncated.
- <code>[CancelledError](#asyncio.CancelledError)</code> – The transfer is cancelled after owned work settles and destination cleanup is attempted.
