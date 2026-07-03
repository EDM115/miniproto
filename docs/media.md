# Media Primitives

Status: Phase 10 primitive implementation, fake-backed tests passing, live Telegram upload/download still gated.

## Scope

`miniproto` owns protocol-core media movement: chunked upload, `messages.sendMedia`, `upload.getFile`, CDN redirects, CDN reupload tokens, AES-CTR CDN chunk decryption, resumable destinations, and progress callbacks. Rich media convenience wrappers, bound message helpers, album helpers, thumbnail generation, and framework ergonomics remain future `mpgram` responsibilities.

## Upload

Use `Client.send_file(peer, file, caption="...")` for the thin high-level path. It uploads the file with 512 KiB default parts, chooses `upload.saveFilePart` for small files and `upload.saveBigFilePart` for files over 10 MiB, then sends `messages.sendMedia` with `inputMediaUploadedDocument` by default. High-level media transfers use dedicated MTProto sender lanes by default: the lane count follows transfer `concurrency`, so a socket reset on one media lane does not poison unrelated requests on the main client sender or every other in-flight part. Pass `media_lanes=0` to force the legacy single-sender path, or pass an explicit positive `media_lanes` count to decouple socket count from part concurrency. Low-level callers can use `miniproto.media.upload_file()` directly to get the generated `InputFile` or `InputFileBig` object.

Uploaded or received document-like media and photos expose `media.file_id`, a miniproto-owned opaque ID that can be decoded later with `decode_file_id()` / `media_from_file_id()`. Passing that ID back to `Client.send_file(peer, file_id, caption="...")` sends `inputMediaDocument` or `inputMediaPhoto` and skips reuploading the bytes. Telegram represents videos, GIFs, audio, voice notes, stickers, and ordinary files as document media with different `DocumentAttribute` values, so miniproto file IDs use a `document` family for all of those and a separate `photo` family for photos.

Supported upload inputs are paths, bytes-like objects, seekable binary file objects, sync iterables of byte chunks, and async iterables of byte chunks. Unknown-size sources are spooled to a temporary file before upload because Telegram's big-file method requires the total part count.

## Download

Use `Client.download_media(media, destination=None)` for the thin high-level path. It resolves public `Media`, miniproto file IDs, raw `MessageMediaDocument`, raw `MessageMediaPhoto`, raw `Document`, raw `Photo`, or generated `InputFileLocation` objects into `upload.getFile` requests. Passing no destination returns downloaded bytes in `MediaDownloadResult.data`; passing a path writes to disk; `resume=True` appends to an existing path and starts requests after the existing byte count. High-level downloads use the same dedicated media-lane pool as uploads, with `media_lanes=0` available for reproducing the old main-sender path. Downloads accept up to 1 MiB `upload.getFile` requests while uploads stay capped at 512 KiB parts; the live benchmark defaults to 512 KiB download chunks because flood behavior is easier to compare there, and 1 MiB remains an explicit performance experiment. Large known-size downloads can use bounded `concurrency`; transient chunk failures and short `FloodWait` responses are retried at the media layer with `max_retries` while non-transient RPC errors still fail immediately. Concurrent downloads use adaptive throttling by default: the first active window is intentionally below the requested maximum, short flood waits cut the active request window, successful chunks slowly ramp it back up toward the requested concurrency, and `adaptive_concurrency=False` disables that behavior for controlled experiments. Set `flood_sleep_threshold=None` to fail download chunks on flood waits instead of sleeping and retrying them.

## CDN

When `upload.getFile` returns `upload.fileCdnRedirect`, Phase 10 follows `upload.getCdnFile`, handles `upload.cdnFileReuploadNeeded` with `upload.reuploadCdnFile`, and decrypts returned CDN chunks with AES-CTR using the redirect key and IV. Real CDN DC authorization and live edge cases still need gated integration coverage.

## Live Tests

The live scaffold is `tests/integration/test_media_live.py`. It requires `MINIPROTO_INTEGRATION=1`, API credentials, a test phone or bot token, `MINIPROTO_TEST_UPLOAD_FILE`, and optionally `MINIPROTO_TEST_DOWNLOAD_PATH`; it intentionally skips until maintainers provide test-DC credentials and validate the real transport path.
