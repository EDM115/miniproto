---
title: "miniproto.media.cdn"
description: "Telegram CDN retrieval, AES-CTR decryption and ``FileHash``-bounded integrity checks."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.media.cdn"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py"
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn`

Telegram CDN retrieval, AES-CTR decryption and ``FileHash``-bounded integrity checks.

The module accepts and returns ordinary immutable ``bytes``. Ciphertext,
plaintext, redirect keys, IVs and temporary counter buffers are not explicitly
zeroized; callers that require memory sanitization must manage their own process
and buffer-lifetime boundary.

## Public objects

- [`CDN_HASH_BLOCK_SIZE`](./cdn-hash-block-size/) — Public attribute `miniproto.media.cdn.CDN_HASH_BLOCK_SIZE`.
- [`CdnError`](./cdnerror/) — Raised when a CDN response cannot be reuploaded, decrypted or interpreted.
- [`CdnIntegrityError`](./cdnintegrityerror/) — Raised when a CDN range lacks valid ``FileHash`` coverage or verification fails.
- [`CdnRedirect`](./cdnredirect/) — Validated information supplied by Telegram when a file moves to its CDN.
- [`get_cdn_file_part`](./get-cdn-file-part/) — Fetch, decrypt and hash-verify one CDN file range.
- [`verify_cdn_part`](./verify-cdn-part/) — Verify a decrypted CDN chunk against Telegram's 128 KiB SHA-256 file hashes.
- [`cdn_redirect_from_raw`](./cdn-redirect-from-raw/) — Convert a raw CDN redirect response to stable transfer metadata.
- [`decrypt_cdn_chunk`](./decrypt-cdn-chunk/) — Decrypt a CDN ciphertext range with the counter aligned to its file offset.
