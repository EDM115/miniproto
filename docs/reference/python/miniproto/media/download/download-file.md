---
title: "miniproto.media.download.download_file"
description: "Download media into memory, a path, or a caller-owned binary stream."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.download_file"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L1354"
aliases: ["miniproto.media.download_file"]
module: "miniproto.media.download"
---

## `miniproto.media.download.download_file`

```python
download_file(invoke: RawInvoker, location: object, destination: Destination = None, *, offset: int = 0, limit: int | None = None, part_size: int = DEFAULT_DOWNLOAD_PART_SIZE, resume: bool = False, progress: ProgressCallback | None = None, precise: bool = False, cdn_supported: bool = True, total_size: int | None = None, request_timeout: float | None = None, max_retries: int = 2, flood_sleep_threshold: int | None = 30, max_buffer_size: int | None = None, concurrency: int = DEFAULT_DOWNLOAD_CONCURRENCY, adaptive_concurrency: bool = True, launch_stagger: bool = True, max_in_flight_bytes: int | None = None, adaptive_part_size: bool = True, max_part_size: int = MAX_DOWNLOAD_CHUNK_SIZE, range_cache: DownloadRangeCache | bool | None = None, range_cache_key: str | None = None, range_cache_max_bytes: int = DEFAULT_RANGE_CACHE_BYTES, read_ahead_bytes: int = 0, verify_plain_hashes: bool = False, file_reference_refresher: FileReferenceRefresher | None = None) -> MediaDownloadResult
```

Download media into memory, a path, or a caller-owned binary stream.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.download.RawInvoker)</code>) – Async raw-RPC invoker used for Telegram file requests.
- **location** (<code>[object](#object)</code>) – Telegram input file location to retrieve.
- **destination** (<code>[Destination](#miniproto.media.download.Destination)</code>) – ``None`` for in-memory bytes, a path to create/overwrite, or an open binary stream.
- **offset** (<code>[int](#int)</code>) – Starting byte offset; defaults to ``0``.
- **limit** (<code>[int](#int) | None</code>) – Exact requested byte count, or ``None`` to continue until EOF.
- **part_size** (<code>[int](#int)</code>) – Initial power-of-two request size; defaults to 512 KiB.
- **resume** (<code>[bool](#bool)</code>) – Append to an existing path from its 1 KiB-aligned size; defaults to ``False``.
- **progress** (<code>[ProgressCallback](#miniproto.media.upload.ProgressCallback) | None</code>) – Optional synchronous or async ``(current, total)`` callback;
``current`` is committed operation bytes and begins at any retained
resume prefix, while ``total`` is ``limit`` or otherwise ``total_size``.
- **precise** (<code>[bool](#bool)</code>) – Request Telegram's 1 KiB precise mode; enabled automatically when required.
- **cdn_supported** (<code>[bool](#bool)</code>) – Permit CDN redirects and their mandatory block verification.
- **total_size** (<code>[int](#int) | None</code>) – Known full file size used to preserve finite concurrent coverage.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional timeout passed to each raw request.
- **max_retries** (<code>[int](#int)</code>) – Non-flood transient retry budget per part; defaults to ``2``.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Retry eligible flood waits at or below this number of seconds; ``None`` disables them.
Eligible waits retain their slot and are separately capped at 16 per part.
- **max_buffer_size** (<code>[int](#int) | None</code>) – Legacy maximum in-flight byte window alias.
- **concurrency** (<code>[int](#int)</code>) – Maximum concurrent requests and queued writes.
- **adaptive_concurrency** (<code>[bool](#bool)</code>) – Adapt the active request window to connection failures.
- **launch_stagger** (<code>[bool](#bool)</code>) – Pace start and flood-recovery request launches.
- **max_in_flight_bytes** (<code>[int](#int) | None</code>) – Maximum requested bytes not yet released by the stream.
- **adaptive_part_size** (<code>[bool](#bool)</code>) – Probe larger legal part sizes for large transfers.
- **max_part_size** (<code>[int](#int)</code>) – Upper bound for adaptive parts, no greater than one MiB.
- **range_cache** (<code>[DownloadRangeCache](#miniproto.media.download.DownloadRangeCache) | [bool](#bool) | None</code>) – Exact-range cache instance, ``True`` for shared cache, or disabled value.
- **range_cache_key** (<code>[str](#str) | None</code>) – Stable media identity for range-cache sharing.
- **range_cache_max_bytes** (<code>[int](#int)</code>) – Capacity used by an implicit shared cache.
- **read_ahead_bytes** (<code>[int](#int)</code>) – Best-effort range prefetch budget; disabled for a full-file transfer.
- **verify_plain_hashes** (<code>[bool](#bool)</code>) – Verify non-CDN data with Telegram plain-file SHA-256 metadata.
- **file_reference_refresher** (<code>[FileReferenceRefresher](#miniproto.media.download.FileReferenceRefresher) | None</code>) – Optional sync/async callback for one stale-reference refresh per part.

**Returns:**

- <code>[MediaDownloadResult](#miniproto.media.download.MediaDownloadResult)</code> – Metadata including the resolved output. ``data`` is populated only for
- <code>[MediaDownloadResult](#miniproto.media.download.MediaDownloadResult)</code> – an in-memory destination; caller-provided streams remain open.

<details class="destination-ownership-and-rollback" open markdown="1">
<summary>Destination Ownership and Rollback</summary>

``None`` creates an internal ``BytesIO`` returned as ``data`` and clears it
on failure. A path creates parent directories; a new path is removed on
cancellation/failure, while an existing non-resume path is overwritten
rather than restored. A resumed path preserves its existing prefix after
truncating any non-1-KiB tail, and failure truncates it back to that
aligned prefix. A caller ``BytesIO`` is restored to its original contents
and position; arbitrary caller streams remain open and are not generally
restorable. Payload/key buffers are not explicitly zeroized.

</details>

**Raises:**

- <code>[ValueError](#ValueError)</code> – An offset, limit, part/cache/window option is invalid.
- <code>[TypeError](#TypeError)</code> – A boolean option has the wrong type.
- <code>[MediaDownloadError](#miniproto.media.download.MediaDownloadError)</code> – A response, finite range, or destination write is invalid.
- <code>[MediaIntegrityError](#miniproto.media.download.MediaIntegrityError)</code> – CDN or requested plain-file integrity verification fails.
- <code>[OSError](#OSError)</code> – A path destination cannot be created, written, or restored.
- <code>[CancelledError](#asyncio.CancelledError)</code> – The transfer is cancelled; created paths are removed and owned buffers restored.
