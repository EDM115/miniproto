---
title: "miniproto.file_id"
description: "Stable, local ``mpf1_`` file identifiers for reusable Telegram media references."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.file_id"
source_path: "src/miniproto/file_id.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/file_id.py"
module: "miniproto.file_id"
---

## `miniproto.file_id`

Stable, local ``mpf1_`` file identifiers for reusable Telegram media references.

## Public objects

- [`FILE_ID_PREFIX`](./file-id-prefix/) — Public attribute `miniproto.file_id.FILE_ID_PREFIX`.
- [`DecodedFileId`](./decodedfileid/) — Decoded local file-id fields used to recreate a media location or input media.
- [`is_file_id`](./is-file-id/) — Return whether a value has the miniproto file-id prefix.
- [`encode_file_id`](./encode-file-id/) — Encode supported Telegram media or input locations into a local file ID.
- [`try_encode_file_id`](./try-encode-file-id/) — Best-effort variant of :func:`encode_file_id`.
- [`decode_file_id`](./decode-file-id/) — Decode an ``mpf1_`` file ID without contacting Telegram.
- [`media_from_file_id`](./media-from-file-id/) — Decode a local file ID into a reusable ``Media`` value.
- [`input_media_from_file_id`](./input-media-from-file-id/) — Decode a file ID into Telegram input media.
