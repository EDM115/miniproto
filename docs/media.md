# Media Primitives

Status: Phase 10 primitive implementation, fake-backed tests passing, live Telegram upload/download still gated.

## Scope

`miniproto` owns protocol-core media movement: chunked upload, `messages.sendMedia`, `upload.getFile`, CDN redirects, CDN reupload tokens, AES-CTR CDN chunk decryption, resumable destinations, and progress callbacks. Rich media convenience wrappers, bound message helpers, album helpers, thumbnail generation, and framework ergonomics remain future `mpgram` responsibilities.

## Upload

Use `Client.send_file(peer, file, caption="...")` for the thin high-level path. It uploads the file with 512 KiB default parts, chooses `upload.saveFilePart` for small files and `upload.saveBigFilePart` for files over 10 MiB, then sends `messages.sendMedia` with `inputMediaUploadedDocument` by default. Low-level callers can use `miniproto.media.upload_file()` directly to get the generated `InputFile` or `InputFileBig` object.

Supported upload inputs are paths, bytes-like objects, seekable binary file objects, sync iterables of byte chunks, and async iterables of byte chunks. Unknown-size sources are spooled to a temporary file before upload because Telegram's big-file method requires the total part count.

## Download

Use `Client.download_media(media, destination=None)` for the thin high-level path. It resolves public `Media`, raw `MessageMediaDocument`, raw `MessageMediaPhoto`, raw `Document`, raw `Photo`, or generated `InputFileLocation` objects into `upload.getFile` requests. Passing no destination returns downloaded bytes in `MediaDownloadResult.data`; passing a path writes to disk; `resume=True` appends to an existing path and starts requests after the existing byte count.

## CDN

When `upload.getFile` returns `upload.fileCdnRedirect`, Phase 10 follows `upload.getCdnFile`, handles `upload.cdnFileReuploadNeeded` with `upload.reuploadCdnFile`, and decrypts returned CDN chunks with AES-CTR using the redirect key and IV. Real CDN DC authorization and live edge cases still need gated integration coverage.

## Live Tests

The live scaffold is `tests/integration/test_media_live.py`. It requires `MINIPROTO_INTEGRATION=1`, API credentials, a test phone or bot token, `MINIPROTO_TEST_UPLOAD_FILE`, and optionally `MINIPROTO_TEST_DOWNLOAD_PATH`; it intentionally skips until maintainers provide test-DC credentials and validate the real transport path.
