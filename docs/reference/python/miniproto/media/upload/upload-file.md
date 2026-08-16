---
title: "miniproto.media.upload.upload_file"
description: "Upload a source as MTProto file parts and return its input-file handle."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.upload.upload_file"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py#L105"
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
- **source** (<code>[FileSource](#miniproto.media.upload.FileSource)</code>) – Path, bytes, readable stream, or synchronous/asynchronous byte iterable. Paths are opened by this function; caller-owned readers are not closed.
- **file_name** (<code>[str](#str) | None</code>) – Optional override for the Telegram file name.
- **part_size** (<code>[int](#int)</code>) – KiB-aligned part size in bytes, at most 512 KiB.
- **concurrency** (<code>[int](#int)</code>) – Maximum in-flight save requests and bounded read-ahead queue slots.
- **progress** (<code>[ProgressCallback](#miniproto.media.upload.ProgressCallback) | None</code>) – Optional callback receiving ``(completed_bytes, total_bytes)`` after accepted parts, serialized in completion order rather than part-index order.
- **file_id** (<code>[int](#int) | None</code>) – Optional ID converted with ``int`` and used verbatim, including zero; absent IDs are generated non-zero.
- **max_retries** (<code>[int](#int)</code>) – Transient non-flood retry attempts per part.
- **max_buffer_size** (<code>[int](#int) | None</code>) – Required to cover the configured concurrency window when set.
- **request_timeout** (<code>[float](#float) | None</code>) – Per-part timeout; defaults to the upload-tail-safe timeout.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Largest server flood wait in seconds treated as retryable pacing; each part has a separate cap of 16 accepted flood retries.
- **max_file_parts** (<code>[int](#int) | None</code>) – Maximum accepted part count; size is increased when possible.

**Returns:**

- <code>[MediaUploadResult](#miniproto.media.upload.MediaUploadResult)</code> – The completed file metadata and a matching ``InputFile`` or ``InputFileBig``.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If options are invalid or the normalized source is empty.
- <code>[TypeError](#TypeError)</code> – If a streamed source yields a non-byte chunk.
- <code>[MediaUploadError](#miniproto.media.upload.MediaUploadError)</code> – If part-count constraints cannot be met or Telegram rejects a part.
- <code>[CancelledError](#asyncio.CancelledError)</code> – After cancelling producer and in-flight part tasks and cleaning up.

The checksum covers exactly the bytes read for small files. Seekable callers
are rewound to their initial offset before uploading and left at their final
read position; one-shot streams and iterables are consumed into an owned
temporary spool that is closed on success, failure, or cancellation.
