---
title: "account.updateTheme"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.updateTheme"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x2bf40ccc"
---

# `account.updateTheme`

No description provided by the pinned schema.

## Signature

```tl
account.updateTheme#2bf40ccc flags:# format:string theme:InputTheme slug:flags.0?string title:flags.1?string document:flags.2?InputDocument settings:flags.3?Vector<InputThemeSettings> = Theme;
```

## Result type

`Theme`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| format | string | — | — | No description provided by the pinned schema. |
| theme | InputTheme | — | — | No description provided by the pinned schema. |
| slug | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| title | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| document | flags.2?InputDocument | flags.2 | — | No description provided by the pinned schema. |
| settings | flags.3?Vector<InputThemeSettings> | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| slug | 0 | Controlled by `flags`; present when this bit is set. |
| title | 1 | Controlled by `flags`; present when this bit is set. |
| document | 2 | Controlled by `flags`; present when this bit is set. |
| settings | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AccountUpdateTheme
```

Public access: `miniproto.raw.functions.AccountUpdateTheme`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountUpdateTheme

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountUpdateTheme
```

## Result family

[`Theme`](/reference/telegram/types/results/theme/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`THEME_INVALID`](/reference/telegram/errors/theme-invalid/) | Invalid theme provided. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputDocument`](/reference/telegram/types/results/input-document/), [`InputTheme`](/reference/telegram/types/results/input-theme/), [`InputThemeSettings`](/reference/telegram/types/results/input-theme-settings/)
Known selected constructors: [`inputDocument`](/reference/telegram/types/base/input-document/), [`inputDocumentEmpty`](/reference/telegram/types/base/input-document-empty/), [`inputTheme`](/reference/telegram/types/base/input-theme/), [`inputThemeSlug`](/reference/telegram/types/base/input-theme-slug/), [`inputThemeSettings`](/reference/telegram/types/base/input-theme-settings/)

## Returned types

[`Theme`](/reference/telegram/types/results/theme/)
Known selected constructors: [`theme`](/reference/telegram/types/base/theme/)

## Related methods

[`account.createTheme`](/reference/telegram/functions/account/create-theme/), [`account.getTheme`](/reference/telegram/functions/account/get-theme/), [`account.installTheme`](/reference/telegram/functions/account/install-theme/), [`account.saveMusic`](/reference/telegram/functions/account/save-music/), [`account.saveRingtone`](/reference/telegram/functions/account/save-ringtone/), [`account.saveTheme`](/reference/telegram/functions/account/save-theme/), [`messages.faveSticker`](/reference/telegram/functions/messages/fave-sticker/), [`messages.reportMusicListen`](/reference/telegram/functions/messages/report-music-listen/), [`messages.saveGif`](/reference/telegram/functions/messages/save-gif/), [`messages.saveRecentSticker`](/reference/telegram/functions/messages/save-recent-sticker/), [`stickers.changeSticker`](/reference/telegram/functions/stickers/change-sticker/), [`stickers.changeStickerPosition`](/reference/telegram/functions/stickers/change-sticker-position/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stickers.removeStickerFromSet`](/reference/telegram/functions/stickers/remove-sticker-from-set/), [`stickers.replaceSticker`](/reference/telegram/functions/stickers/replace-sticker/), [`stickers.setStickerSetThumb`](/reference/telegram/functions/stickers/set-sticker-set-thumb/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
