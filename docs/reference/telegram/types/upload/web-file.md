---
title: "upload.webFile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "upload.webFile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "upload"
layer: 228
schema_source: "tdlib"
constructor_id: "0x21e753bc"
---

# `upload.webFile`

No description provided by the pinned schema.

## Signature

```tl
upload.webFile#21e753bc size:int mime_type:string file_type:storage.FileType mtime:int bytes:bytes = upload.WebFile;
```

## Result type

`upload.WebFile`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| size | int | — | — | No description provided by the pinned schema. |
| mime_type | string | — | — | No description provided by the pinned schema. |
| file_type | storage.FileType | — | — | No description provided by the pinned schema. |
| mtime | int | — | — | No description provided by the pinned schema. |
| bytes | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UploadWebFile
```

Public access: `miniproto.raw.types.UploadWebFile`.

## Safe usage shape

```python
from miniproto.raw.types import UploadWebFile

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UploadWebFile
```

## Result family

[`upload.WebFile`](/reference/telegram/types/results/upload-web-file/)

## Relationships

- Result family: [`upload.WebFile`](/reference/telegram/types/results/upload-web-file/)
- Returned by: [`upload.getWebFile`](/reference/telegram/functions/upload/get-web-file/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
