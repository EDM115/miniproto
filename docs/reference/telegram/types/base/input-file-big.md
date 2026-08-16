---
title: "inputFileBig"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputFileBig"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfa4f0bb5"
---

# `inputFileBig`

No description provided by the pinned schema.

## Signature

```tl
inputFileBig#fa4f0bb5 id:long parts:int name:string = InputFile;
```

## Result type

`InputFile`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| parts | int | — | — | No description provided by the pinned schema. |
| name | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputFileBig
```

Public access: `miniproto.raw.types.InputFileBig`.

## Safe usage shape

```python
from miniproto.raw.types import InputFileBig

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputFileBig
```

## Result family

[`InputFile`](/reference/telegram/types/results/input-file/)

## Relationships

- Result family: [`InputFile`](/reference/telegram/types/results/input-file/)
- Related constructors: [`inputFile`](/reference/telegram/types/base/input-file/), [`inputFileStoryDocument`](/reference/telegram/types/base/input-file-story-document/)
- Accepted by: [`account.uploadRingtone`](/reference/telegram/functions/account/upload-ringtone/), [`account.uploadTheme`](/reference/telegram/functions/account/upload-theme/), [`account.uploadWallPaper`](/reference/telegram/functions/account/upload-wall-paper/), [`messages.initHistoryImport`](/reference/telegram/functions/messages/init-history-import/), [`phone.saveCallLog`](/reference/telegram/functions/phone/save-call-log/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/), [`inputChatUploadedPhoto`](/reference/telegram/types/base/input-chat-uploaded-photo/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputMediaUploadedPhoto`](/reference/telegram/types/base/input-media-uploaded-photo/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
