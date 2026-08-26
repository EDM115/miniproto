---
title: "storage.fileUnknown"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "storage.fileUnknown"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "storage"
schema_source: "tdlib"
constructor_id: "0xaa963b05"
---

# `storage.fileUnknown`

No description provided by the pinned schema.

## Signature

```tl
storage.fileUnknown#aa963b05 = storage.FileType;
```

## Result type

`storage.FileType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import StorageFileUnknown
```

Public access: `miniproto.raw.types.StorageFileUnknown`.

## Safe usage shape

```python
from miniproto.raw.types import StorageFileUnknown

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StorageFileUnknown
```

## Result family

[`storage.FileType`](/reference/telegram/types/results/storage-file-type/)

## Relationships

- Result family: [`storage.FileType`](/reference/telegram/types/results/storage-file-type/)
- Related constructors: [`storage.fileGif`](/reference/telegram/types/storage/file-gif/), [`storage.fileJpeg`](/reference/telegram/types/storage/file-jpeg/), [`storage.fileMov`](/reference/telegram/types/storage/file-mov/), [`storage.fileMp3`](/reference/telegram/types/storage/file-mp3/), [`storage.fileMp4`](/reference/telegram/types/storage/file-mp4/), [`storage.filePartial`](/reference/telegram/types/storage/file-partial/), [`storage.filePdf`](/reference/telegram/types/storage/file-pdf/), [`storage.filePng`](/reference/telegram/types/storage/file-png/), [`storage.fileWebp`](/reference/telegram/types/storage/file-webp/)
- Accepted by: [`upload.file`](/reference/telegram/types/upload/file/), [`upload.webFile`](/reference/telegram/types/upload/web-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
