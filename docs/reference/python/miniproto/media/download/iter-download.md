---
title: "miniproto.media.download.iter_download"
description: "Stream an exact media range as ordered, bounded byte chunks."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.download.iter_download"
source_path: "src/miniproto/media/download.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/download.py#L987"
aliases: ["miniproto.iter_download","miniproto.media.iter_download"]
module: "miniproto.media.download"
---

## `miniproto.media.download.iter_download`

```python
iter_download(invoke: RawInvoker, location: object, *, offset: int = 0, limit: int | None = None, part_size: int = DEFAULT_DOWNLOAD_PART_SIZE, progress: ProgressCallback | None = None, precise: bool = False, cdn_supported: bool = True, total_size: int | None = None, request_timeout: float | None = None, max_retries: int = 2, flood_sleep_threshold: int | None = 30, max_buffer_size: int | None = None, concurrency: int = DEFAULT_DOWNLOAD_CONCURRENCY, adaptive_concurrency: bool = True, launch_stagger: bool = True, max_in_flight_bytes: int | None = None, adaptive_part_size: bool = True, max_part_size: int = MAX_DOWNLOAD_CHUNK_SIZE, range_cache: DownloadRangeCache | bool | None = None, range_cache_key: str | None = None, range_cache_max_bytes: int = DEFAULT_RANGE_CACHE_BYTES, read_ahead_bytes: int = 0, verify_plain_hashes: bool = False, file_reference_refresher: FileReferenceRefresher | None = None) -> AsyncGenerator[bytes]
```

Stream an exact media range as ordered, bounded byte chunks.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.download.RawInvoker)</code>) – Async raw-RPC invoker used for Telegram file requests.
- **location** (<code>[object](#object)</code>) – Telegram input file location to retrieve.
- **offset** (<code>[int](#int)</code>) – Starting byte offset; defaults to ``0``.
- **limit** (<code>[int](#int) | None</code>) – Exact byte count to yield or ``None`` to stream until EOF.
- **part_size** (<code>[int](#int)</code>) – Initial power-of-two request size; defaults to 512 KiB.
- **progress** (<code>[ProgressCallback](#miniproto.media.upload.ProgressCallback) | None</code>) – Optional synchronous or async ``(current, total)`` callback;
``current`` is bytes yielded from this invocation, while ``total`` is
``limit`` for a finite range or ``total_size`` when streaming to EOF.
- **precise** (<code>[bool](#bool)</code>) – Request Telegram's 1 KiB precise mode; it is enabled automatically when needed.
- **cdn_supported** (<code>[bool](#bool)</code>) – Allow Telegram to redirect requests to its CDN; defaults to ``True``.
- **total_size** (<code>[int](#int) | None</code>) – Known full size, used for exact range completion and concurrency.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional timeout passed to each raw request.
- **max_retries** (<code>[int](#int)</code>) – Non-flood transient retry budget per part; defaults to ``2``.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Retry server flood waits at or below this number of seconds; ``None`` disables them.
Eligible waits do not consume ``max_retries`` but are capped at 16 per part.
- **max_buffer_size** (<code>[int](#int) | None</code>) – Legacy byte window alias used when ``max_in_flight_bytes`` is absent.
- **concurrency** (<code>[int](#int)</code>) – Maximum concurrent part requests; defaults to :data:`DEFAULT_DOWNLOAD_CONCURRENCY`.
- **adaptive_concurrency** (<code>[bool](#bool)</code>) – Reduce the active window on connection-health failures.
- **launch_stagger** (<code>[bool](#bool)</code>) – Pace launch bursts and flood recovery; defaults to ``True``.
- **max_in_flight_bytes** (<code>[int](#int) | None</code>) – Maximum requested but unyielded bytes.
- **adaptive_part_size** (<code>[bool](#bool)</code>) – Probe larger legal parts for sufficiently large transfers.
- **max_part_size** (<code>[int](#int)</code>) – Largest legal adaptive part size, at most one MiB.
- **range_cache** (<code>[DownloadRangeCache](#miniproto.media.download.DownloadRangeCache) | [bool](#bool) | None</code>) – Exact-range cache instance, ``True`` for the shared cache or ``False``/``None`` to disable it.
- **range_cache_key** (<code>[str](#str) | None</code>) – Stable identity used to share cached ranges.
- **range_cache_max_bytes** (<code>[int](#int)</code>) – Capacity for an implicitly created shared cache.
- **read_ahead_bytes** (<code>[int](#int)</code>) – Best-effort cached prefetch budget for ranged reads only.
- **verify_plain_hashes** (<code>[bool](#bool)</code>) – Validate non-CDN chunks against Telegram's file hashes.
- **file_reference_refresher** (<code>[FileReferenceRefresher](#miniproto.media.download.FileReferenceRefresher) | None</code>) – Optional sync/async callback to renew an expired file reference once per part.

**Yields:**

- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code> – Contiguous ``bytes`` in increasing offset order. A bounded request window
- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code> – limits in-flight resources; closing the generator cancels outstanding parts.
- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code> – Progress reports ``current`` bytes only after a chunk has been yielded,
- **unlike** (<code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code>) – func:`download_file`, which reports after destination-write
- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[bytes](#bytes)]</code> – acknowledgement and starts ``current`` at any retained resume prefix.

**Raises:**

- <code>[ValueError](#ValueError)</code> – A range, alignment, part size, retry or cache option is invalid.
- <code>[TypeError](#TypeError)</code> – ``verify_plain_hashes`` or ``launch_stagger`` is not boolean.
- <code>[MediaDownloadError](#miniproto.media.download.MediaDownloadError)</code> – Telegram ends a finite requested interval before full coverage.
- <code>[MediaIntegrityError](#miniproto.media.download.MediaIntegrityError)</code> – Optional plain-file verification finds missing or mismatched hashes.
- <code>[CancelledError](#asyncio.CancelledError)</code> – Iteration or an awaiting caller is cancelled.
