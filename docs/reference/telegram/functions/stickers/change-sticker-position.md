---
title: "stickers.changeStickerPosition"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "stickers.changeStickerPosition"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stickers"
layer: 228
schema_source: "tdlib"
constructor_id: "0xffb6d4ca"
---

# `stickers.changeStickerPosition`

No description provided by the pinned schema.

## Signature

```tl
stickers.changeStickerPosition#ffb6d4ca sticker:InputDocument position:int = messages.StickerSet;
```

## Result type

`messages.StickerSet`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| sticker | InputDocument | — | — | No description provided by the pinned schema. |
| position | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import StickersChangeStickerPosition
```

Public access: `miniproto.raw.functions.StickersChangeStickerPosition`.

## Safe usage shape

```python
from miniproto.raw.functions import StickersChangeStickerPosition

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = StickersChangeStickerPosition
```

## Result family

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`STICKER_INVALID`](/reference/telegram/errors/sticker-invalid/) | The provided sticker is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputDocument`](/reference/telegram/types/results/input-document/)
Known selected constructors: [`inputDocument`](/reference/telegram/types/base/input-document/), [`inputDocumentEmpty`](/reference/telegram/types/base/input-document-empty/)

## Returned types

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)
Known selected constructors: [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/), [`messages.stickerSetNotModified`](/reference/telegram/types/messages/sticker-set-not-modified/)

## Related methods

[`account.createTheme`](/reference/telegram/functions/account/create-theme/), [`account.saveMusic`](/reference/telegram/functions/account/save-music/), [`account.saveRingtone`](/reference/telegram/functions/account/save-ringtone/), [`account.updateTheme`](/reference/telegram/functions/account/update-theme/), [`messages.faveSticker`](/reference/telegram/functions/messages/fave-sticker/), [`messages.getStickerSet`](/reference/telegram/functions/messages/get-sticker-set/), [`messages.reportMusicListen`](/reference/telegram/functions/messages/report-music-listen/), [`messages.saveGif`](/reference/telegram/functions/messages/save-gif/), [`messages.saveRecentSticker`](/reference/telegram/functions/messages/save-recent-sticker/), [`stickers.addStickerToSet`](/reference/telegram/functions/stickers/add-sticker-to-set/), [`stickers.changeSticker`](/reference/telegram/functions/stickers/change-sticker/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stickers.removeStickerFromSet`](/reference/telegram/functions/stickers/remove-sticker-from-set/), [`stickers.renameStickerSet`](/reference/telegram/functions/stickers/rename-sticker-set/), [`stickers.replaceSticker`](/reference/telegram/functions/stickers/replace-sticker/), [`stickers.setStickerSetThumb`](/reference/telegram/functions/stickers/set-sticker-set-thumb/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
