---
title: "inputStickerSetThumb"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputStickerSetThumb"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x9d84f3db"
---

# `inputStickerSetThumb`

No description provided by the pinned schema.

## Signature

```tl
inputStickerSetThumb#9d84f3db stickerset:InputStickerSet thumb_version:int = InputFileLocation;
```

## Result type

`InputFileLocation`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| stickerset | InputStickerSet | — | — | No description provided by the pinned schema. |
| thumb_version | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputStickerSetThumb
```

Public access: `miniproto.raw.types.InputStickerSetThumb`.

## Safe usage shape

```python
from miniproto.raw.types import InputStickerSetThumb

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputStickerSetThumb
```

## Result family

[`InputFileLocation`](/reference/telegram/types/results/input-file-location/)

## Relationships

- Result family: [`InputFileLocation`](/reference/telegram/types/results/input-file-location/)
- Related constructors: [`inputDocumentFileLocation`](/reference/telegram/types/base/input-document-file-location/), [`inputEncryptedFileLocation`](/reference/telegram/types/base/input-encrypted-file-location/), [`inputFileLocation`](/reference/telegram/types/base/input-file-location/), [`inputGroupCallStream`](/reference/telegram/types/base/input-group-call-stream/), [`inputPeerPhotoFileLocation`](/reference/telegram/types/base/input-peer-photo-file-location/), [`inputPeerPhotoFileLocationLegacy`](/reference/telegram/types/base/input-peer-photo-file-location-legacy/), [`inputPhotoFileLocation`](/reference/telegram/types/base/input-photo-file-location/), [`inputPhotoLegacyFileLocation`](/reference/telegram/types/base/input-photo-legacy-file-location/), [`inputSecureFileLocation`](/reference/telegram/types/base/input-secure-file-location/), [`inputStickerSetThumbLegacy`](/reference/telegram/types/base/input-sticker-set-thumb-legacy/), [`inputTakeoutFileLocation`](/reference/telegram/types/base/input-takeout-file-location/)
- Accepted by: [`upload.getFile`](/reference/telegram/functions/upload/get-file/), [`upload.getFileHashes`](/reference/telegram/functions/upload/get-file-hashes/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
