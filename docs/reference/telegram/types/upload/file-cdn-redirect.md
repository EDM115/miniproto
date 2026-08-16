---
title: "upload.fileCdnRedirect"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "upload.fileCdnRedirect"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "upload"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf18cda44"
---

# `upload.fileCdnRedirect`

No description provided by the pinned schema.

## Signature

```tl
upload.fileCdnRedirect#f18cda44 dc_id:int file_token:bytes encryption_key:bytes encryption_iv:bytes file_hashes:Vector<FileHash> = upload.File;
```

## Result type

`upload.File`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| dc_id | int | — | — | No description provided by the pinned schema. |
| file_token | bytes | — | — | No description provided by the pinned schema. |
| encryption_key | bytes | — | — | No description provided by the pinned schema. |
| encryption_iv | bytes | — | — | No description provided by the pinned schema. |
| file_hashes | Vector<FileHash> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UploadFileCdnRedirect
```

Public access: `miniproto.raw.types.UploadFileCdnRedirect`.

## Safe usage shape

```python
from miniproto.raw.types import UploadFileCdnRedirect

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UploadFileCdnRedirect
```

## Result family

[`upload.File`](/reference/telegram/types/results/upload-file/)

## Relationships

- Result family: [`upload.File`](/reference/telegram/types/results/upload-file/)
- Related constructors: [`upload.file`](/reference/telegram/types/upload/file/)
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
