---
title: "miniproto.media.download.iter_download"
description: "Stream a media range in order through a bounded window of part requests."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.iter_download"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L962"
aliases: ["miniproto.iter_download","miniproto.media.iter_download"]
module: "miniproto.media.download"
---

## `miniproto.media.download.iter_download`

```python
iter_download(invoke: RawInvoker, location: object, *, offset: int = 0, limit: int | None = None, part_size: int = DEFAULT_DOWNLOAD_PART_SIZE, progress: ProgressCallback | None = None, precise: bool = False, cdn_supported: bool = True, total_size: int | None = None, request_timeout: float | None = None, max_retries: int = 2, flood_sleep_threshold: int | None = 30, max_buffer_size: int | None = None, concurrency: int = DEFAULT_DOWNLOAD_CONCURRENCY, adaptive_concurrency: bool = True, launch_stagger: bool = True, max_in_flight_bytes: int | None = None, adaptive_part_size: bool = True, max_part_size: int = MAX_DOWNLOAD_CHUNK_SIZE, range_cache: DownloadRangeCache | bool | None = None, range_cache_key: str | None = None, range_cache_max_bytes: int = DEFAULT_RANGE_CACHE_BYTES, read_ahead_bytes: int = 0, verify_plain_hashes: bool = False, file_reference_refresher: FileReferenceRefresher | None = None) -> AsyncGenerator[bytes]
```

Stream a media range in order through a bounded window of part requests.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.download.RawInvoker)</code>) – Async raw-RPC invoker used for Telegram file requests.
- **location** (<code>[object](#object)</code>) – Telegram input file location to retrieve.
- **offset** (<code>[int](#int)</code>) – Starting byte offset, a multiple of 1 KiB, defaults to ``0``.
- **limit** (<code>[int](#int) | None</code>) – Exact byte count to yield. ``None`` uses ``total_size - offset`` when known, otherwise streams until EOF.
- **part_size** (<code>[int](#int)</code>) – Initial power-of-two request size from 1 KiB through one MiB, defaults to 512 KiB.
- **progress** (<code>[ProgressCallback](#miniproto.media.upload.ProgressCallback) | None</code>) – Optional synchronous or async ``(current, total)`` callback. ``current`` counts yielded bytes from this invocation, ``total`` is the effective finite range length or ``None`` for unknown EOF.
- **precise** (<code>[bool](#bool)</code>) – Request Telegram's 1 KiB precise mode, enabled automatically for offsets or parts that need it.
- **cdn_supported** (<code>[bool](#bool)</code>) – Allow Telegram to redirect requests to its CDN, defaults to ``True``. CDN hash verification is mandatory.
- **total_size** (<code>[int](#int) | None</code>) – Known full size, used for exact range completion and concurrency.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional timeout in seconds passed to each raw request.
- **max_retries** (<code>[int](#int)</code>) – Non-flood transient retry budget per part, defaults to two.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Maximum retryable server flood wait in seconds, defaults to 30, ``None`` disables flood retries. Eligible waits retain their local slot and use a separate 16-retry cap per part.
- **max_buffer_size** (<code>[int](#int) | None</code>) – Legacy byte window alias used when ``max_in_flight_bytes`` is absent.
- **concurrency** (<code>[int](#int)</code>) – Maximum active part requests for a finite range, defaults to six. Unknown-length streams use one request at a time.
- **adaptive_concurrency** (<code>[bool](#bool)</code>) – Reduce new request slots on disconnects/timeouts, recover after clean completions, or keep one slot for the rest of the transfer after a premium flood wait.
- **launch_stagger** (<code>[bool](#bool)</code>) – Pace launch bursts and flood recovery, defaults to ``True``.
- **max_in_flight_bytes** (<code>[int](#int) | None</code>) – Local wire-byte window for parts until the consumer resumes after each yield. Defaults to 8 MiB, increased to ``part_size * concurrency`` for a larger finite-range window.
- **adaptive_part_size** (<code>[bool](#bool)</code>) – Probe larger legal parts for transfers of at least 8 MiB or unknown size.
- **max_part_size** (<code>[int](#int)</code>) – Largest legal adaptive part size, at most one MiB.
- **range_cache** (<code>[DownloadRangeCache](#miniproto.media.download.DownloadRangeCache) | [bool](#bool) | None</code>) – Borrowed cache instance or ``True`` for the shared cache. ``False`` disables caching, ``None`` selects the shared cache only when read-ahead is enabled.
- **range_cache_key** (<code>[str](#str) | None</code>) – Stable media identity required for caching and read-ahead, this raw-location API does not infer it.
- **range_cache_max_bytes** (<code>[int](#int)</code>) – Capacity for an implicitly created shared cache.
- **read_ahead_bytes** (<code>[int](#int)</code>) – Speculative cache-fill distance ahead of the consumer. Disabled for open-ended requests or finite ranges reaching the known EOF.
- **verify_plain_hashes** (<code>[bool](#bool)</code>) – Validate non-CDN chunks against complete Telegram hash intervals, fetching any missing bytes before yielding the requested slice.
- **file_reference_refresher** (<code>[FileReferenceRefresher](#miniproto.media.download.FileReferenceRefresher) | None</code>) – Optional sync/async callback to renew an expired file reference once per part.

**Yields:**

- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code> – Contiguous ``bytes`` in increasing offset order. Progress advances when the consumer resumes after a yield. :func:`download_file` reports acknowledged writes and includes any retained resume prefix.

<details class="resource-lifetime" open markdown="1">
<summary>Resource Lifetime</summary>

Close an iterator with ``await iterator.aclose()`` when stopping early. Closure cancels and joins its own part tasks. Shared cache producers and prefetch tasks remain cache-owned until completion or ``clear()``.
The local byte window excludes cached payloads, background prefetch, extra CDN/plain-hash verification requests and any output the consumer retains.

</details>

**Raises:**

- <code>[ValueError](#ValueError)</code> – A range, alignment, part size, retry or cache option is invalid.
- <code>[TypeError](#TypeError)</code> – ``verify_plain_hashes`` or ``launch_stagger`` is not boolean.
- <code>[MediaDownloadError](#miniproto.media.download.MediaDownloadError)</code> – Telegram ends a finite requested interval before full coverage.
- <code>[MediaIntegrityError](#miniproto.media.download.MediaIntegrityError)</code> – Optional plain-file verification finds missing or mismatched hashes.
- <code>[CdnIntegrityError](#miniproto.media.cdn.CdnIntegrityError)</code> – CDN hash coverage or digest verification fails.
- <code>[CancelledError](#asyncio.CancelledError)</code> – Iteration or an awaiting caller is cancelled.
