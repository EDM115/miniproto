---
title: "miniproto.media.upload.upload_file"
description: "Upload a source as MTProto file parts and return its input-file handle."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.upload.upload_file"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py#L100"
aliases: ["miniproto.media.upload_file"]
module: "miniproto.media.upload"
---

## `miniproto.media.upload.upload_file`

```python
upload_file(invoke: RawInvoker, source: FileSource, *, file_name: str | None = None, part_size: int = DEFAULT_CHUNK_SIZE, concurrency: int = DEFAULT_UPLOAD_CONCURRENCY, progress: ProgressCallback | None = None, file_id: int | None = None, max_retries: int = 2, max_buffer_size: int | None = None, request_timeout: float | None = None, flood_sleep_threshold: int | None = DEFAULT_UPLOAD_FLOOD_SLEEP_THRESHOLD, max_file_parts: int | None = 4000) -> MediaUploadResult
```

Upload a source as MTProto file parts and return its input-file handle.

**Parameters:**

- **invoke** (<code>[RawInvoker](#miniproto.media.upload.RawInvoker)</code>) – Raw request callable used to save each part.
- **source** (<code>[FileSource](#miniproto.media.upload.FileSource)</code>) – Path, bytes, readable stream or synchronous/asynchronous byte iterable. This function opens paths and leaves caller-owned readers open.
- **file_name** (<code>[str](#str) | None</code>) – Optional override for the Telegram file name.
- **part_size** (<code>[int](#int)</code>) – KiB-aligned divisor of 512 KiB, in bytes, defaults to 512 KiB. The function increases it when needed to meet ``max_file_parts``.
- **concurrency** (<code>[int](#int)</code>) – Maximum active save tasks, defaults to eight. The read-ahead queue holds up to ``max(2, concurrency)`` more parts.
- **progress** (<code>[ProgressCallback](#miniproto.media.upload.ProgressCallback) | None</code>) – Optional callback receiving ``(completed_bytes, total_bytes)`` after accepted parts, serialized in completion order rather than part-index order.
- **file_id** (<code>[int](#int) | None</code>) – Optional ID converted with ``int`` and used verbatim, including zero. Absent IDs are generated non-zero.
- **max_retries** (<code>[int](#int)</code>) – Shared retry budget per part for transient non-flood failures and non-true save results, defaults to two.
- **max_buffer_size** (<code>[int](#int) | None</code>) – Optional validation threshold for the initial ``part_size * concurrency``. It does not cap queued payloads or account for later part-size growth.
- **request_timeout** (<code>[float](#float) | None</code>) – Per-part timeout in seconds, ``None`` selects 45 seconds.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Largest retryable server flood wait in seconds, defaults to 30, ``None`` disables flood retries. Each part allows up to 16 eligible flood retries outside ``max_retries``.
- **max_file_parts** (<code>[int](#int) | None</code>) – Maximum part count, defaults to 4000, ``None`` disables the cap. Parts grow to the next supported size up to 512 KiB when needed.

**Returns:**

- <code>[MediaUploadResult](#miniproto.media.upload.MediaUploadResult)</code> – The completed file metadata and a matching ``InputFile`` or ``InputFileBig``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If options are invalid or the normalized source is empty.
- <code>[TypeError](#TypeError)</code> – If a streamed source yields an unsupported chunk type.
- <code>[MediaUploadError](#miniproto.media.upload.MediaUploadError)</code> – If part-count constraints cannot be met, the source cannot fill its measured length or Telegram rejects a part.
- <code>[CancelledError](#asyncio.CancelledError)</code> – The upload is cancelled, active producer and part tasks are cancelled and joined once part-transfer execution has started.

The small-file checksum covers all uploaded bytes. Short nonempty reads are combined into complete parts, with a partial final part when needed. An EOF before the measured length fails the upload. Seekable readers start at their initial offset and remain at their final read position. One-shot streams and iterables are consumed into an owned temporary spool before any part is sent. Cleanup closes the spool on success, setup or transfer failure, or cancellation, preserving an existing failure if spool closure also fails.
