---
title: "upload.file"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "upload.file"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "upload"
layer: 228
schema_source: "tdlib"
constructor_id: "0x096a18d5"
---

# `upload.file`

No description provided by the pinned schema.

## Signature

```tl
upload.file#096a18d5 type:storage.FileType mtime:int bytes:bytes = upload.File;
```

## Result type

`upload.File`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| type | storage.FileType | — | — | No description provided by the pinned schema. |
| mtime | int | — | — | No description provided by the pinned schema. |
| bytes | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UploadFile
```

Public access: `miniproto.raw.types.UploadFile`.

## Safe usage shape

```python
from miniproto.raw.types import UploadFile

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UploadFile
```

## Result family

[`upload.File`](/reference/telegram/types/results/upload-file/)

## Relationships

- Result family: [`upload.File`](/reference/telegram/types/results/upload-file/)
- Related constructors: [`upload.fileCdnRedirect`](/reference/telegram/types/upload/file-cdn-redirect/)
- Returned by: [`upload.getFile`](/reference/telegram/functions/upload/get-file/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
