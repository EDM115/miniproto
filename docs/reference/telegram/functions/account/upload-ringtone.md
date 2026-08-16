---
title: "account.uploadRingtone"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.uploadRingtone"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x831a83a2"
---

# `account.uploadRingtone`

No description provided by the pinned schema.

## Signature

```tl
account.uploadRingtone#831a83a2 file:InputFile file_name:string mime_type:string = Document;
```

## Result type

`Document`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| file | InputFile | — | — | No description provided by the pinned schema. |
| file_name | string | — | — | No description provided by the pinned schema. |
| mime_type | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountUploadRingtone
```

Public access: `miniproto.raw.functions.AccountUploadRingtone`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountUploadRingtone

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountUploadRingtone
```

## Result family

[`Document`](/reference/telegram/types/results/document/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`RINGTONE_MIME_INVALID`](/reference/telegram/errors/ringtone-mime-invalid/) | The MIME type for the ringtone is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputFile`](/reference/telegram/types/results/input-file/)
Known selected constructors: [`inputFile`](/reference/telegram/types/base/input-file/), [`inputFileBig`](/reference/telegram/types/base/input-file-big/), [`inputFileStoryDocument`](/reference/telegram/types/base/input-file-story-document/)

## Returned types

[`Document`](/reference/telegram/types/results/document/)
Known selected constructors: [`document`](/reference/telegram/types/base/document/), [`documentEmpty`](/reference/telegram/types/base/document-empty/)

## Related methods

[`account.uploadTheme`](/reference/telegram/functions/account/upload-theme/), [`account.uploadWallPaper`](/reference/telegram/functions/account/upload-wall-paper/), [`messages.getCustomEmojiDocuments`](/reference/telegram/functions/messages/get-custom-emoji-documents/), [`messages.getDocumentByHash`](/reference/telegram/functions/messages/get-document-by-hash/), [`messages.initHistoryImport`](/reference/telegram/functions/messages/init-history-import/), [`phone.saveCallLog`](/reference/telegram/functions/phone/save-call-log/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/)

## Availability evidence

- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
