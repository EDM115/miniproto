---
title: "inputFileStoryDocument"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputFileStoryDocument"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x62dc8b48"
---

# `inputFileStoryDocument`

No description provided by the pinned schema.

## Signature

```tl
inputFileStoryDocument#62dc8b48 id:InputDocument = InputFile;
```

## Result type

`InputFile`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | InputDocument | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputFileStoryDocument
```

Public access: `miniproto.raw.types.InputFileStoryDocument`.

## Safe usage shape

```python
from miniproto.raw.types import InputFileStoryDocument

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputFileStoryDocument
```

## Result family

[`InputFile`](/reference/telegram/types/results/input-file/)

## Relationships

- Result family: [`InputFile`](/reference/telegram/types/results/input-file/)
- Related constructors: [`inputFile`](/reference/telegram/types/base/input-file/), [`inputFileBig`](/reference/telegram/types/base/input-file-big/)
- Accepted by: [`account.uploadRingtone`](/reference/telegram/functions/account/upload-ringtone/), [`account.uploadTheme`](/reference/telegram/functions/account/upload-theme/), [`account.uploadWallPaper`](/reference/telegram/functions/account/upload-wall-paper/), [`messages.initHistoryImport`](/reference/telegram/functions/messages/init-history-import/), [`phone.saveCallLog`](/reference/telegram/functions/phone/save-call-log/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/), [`inputChatUploadedPhoto`](/reference/telegram/types/base/input-chat-uploaded-photo/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputMediaUploadedPhoto`](/reference/telegram/types/base/input-media-uploaded-photo/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
