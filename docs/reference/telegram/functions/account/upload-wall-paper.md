---
title: "account.uploadWallPaper"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.uploadWallPaper"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe39a8f03"
---

# `account.uploadWallPaper`

No description provided by the pinned schema.

## Signature

```tl
account.uploadWallPaper#e39a8f03 flags:# for_chat:flags.0?true file:InputFile mime_type:string settings:WallPaperSettings = WallPaper;
```

## Result type

`WallPaper`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| for_chat | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| file | InputFile | — | — | No description provided by the pinned schema. |
| mime_type | string | — | — | No description provided by the pinned schema. |
| settings | WallPaperSettings | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| for_chat | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AccountUploadWallPaper
```

Public access: `miniproto.raw.functions.AccountUploadWallPaper`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountUploadWallPaper

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountUploadWallPaper
```

## Result family

[`WallPaper`](/reference/telegram/types/results/wall-paper/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`WALLPAPER_FILE_INVALID`](/reference/telegram/errors/wallpaper-file-invalid/) | The specified wallpaper file is invalid. |
| 400 | [`WALLPAPER_MIME_INVALID`](/reference/telegram/errors/wallpaper-mime-invalid/) | The specified wallpaper MIME type is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputFile`](/reference/telegram/types/results/input-file/), [`WallPaperSettings`](/reference/telegram/types/results/wall-paper-settings/)
Known selected constructors: [`inputFile`](/reference/telegram/types/base/input-file/), [`inputFileBig`](/reference/telegram/types/base/input-file-big/), [`inputFileStoryDocument`](/reference/telegram/types/base/input-file-story-document/), [`wallPaperSettings`](/reference/telegram/types/base/wall-paper-settings/)

## Returned types

[`WallPaper`](/reference/telegram/types/results/wall-paper/)
Known selected constructors: [`wallPaper`](/reference/telegram/types/base/wall-paper/), [`wallPaperNoFile`](/reference/telegram/types/base/wall-paper-no-file/)

## Related methods

[`account.getMultiWallPapers`](/reference/telegram/functions/account/get-multi-wall-papers/), [`account.getWallPaper`](/reference/telegram/functions/account/get-wall-paper/), [`account.installWallPaper`](/reference/telegram/functions/account/install-wall-paper/), [`account.saveWallPaper`](/reference/telegram/functions/account/save-wall-paper/), [`account.uploadRingtone`](/reference/telegram/functions/account/upload-ringtone/), [`account.uploadTheme`](/reference/telegram/functions/account/upload-theme/), [`messages.initHistoryImport`](/reference/telegram/functions/messages/init-history-import/), [`messages.setChatWallPaper`](/reference/telegram/functions/messages/set-chat-wall-paper/), [`phone.saveCallLog`](/reference/telegram/functions/phone/save-call-log/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/)

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
