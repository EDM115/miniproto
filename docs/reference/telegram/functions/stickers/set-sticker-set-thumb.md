---
title: "stickers.setStickerSetThumb"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "stickers.setStickerSetThumb"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stickers"
layer: 228
schema_source: "tdlib"
constructor_id: "0xa76a5392"
---

# `stickers.setStickerSetThumb`

No description provided by the pinned schema.

## Signature

```tl
stickers.setStickerSetThumb#a76a5392 flags:# stickerset:InputStickerSet thumb:flags.0?InputDocument thumb_document_id:flags.1?long = messages.StickerSet;
```

## Result type

`messages.StickerSet`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| stickerset | InputStickerSet | — | — | No description provided by the pinned schema. |
| thumb | flags.0?InputDocument | flags.0 | — | No description provided by the pinned schema. |
| thumb_document_id | flags.1?long | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| thumb | 0 | Controlled by `flags`; present when this bit is set. |
| thumb_document_id | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import StickersSetStickerSetThumb
```

Public access: `miniproto.raw.functions.StickersSetStickerSetThumb`.

## Safe usage shape

```python
from miniproto.raw.functions import StickersSetStickerSetThumb

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = StickersSetStickerSetThumb
```

## Result family

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`STICKERSET_INVALID`](/reference/telegram/errors/stickerset-invalid/) | The provided sticker set is invalid. |
| 400 | [`STICKER_THUMB_PNG_NOPNG`](/reference/telegram/errors/sticker-thumb-png-nopng/) | Incorrect stickerset thumb file provided, PNG / WEBP expected. |
| 400 | [`STICKER_THUMB_TGS_NOTGS`](/reference/telegram/errors/sticker-thumb-tgs-notgs/) | Incorrect stickerset TGS thumb file provided. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputDocument`](/reference/telegram/types/results/input-document/), [`InputStickerSet`](/reference/telegram/types/results/input-sticker-set/)
Known selected constructors: [`inputDocument`](/reference/telegram/types/base/input-document/), [`inputDocumentEmpty`](/reference/telegram/types/base/input-document-empty/), [`inputStickerSetAnimatedEmoji`](/reference/telegram/types/base/input-sticker-set-animated-emoji/), [`inputStickerSetAnimatedEmojiAnimations`](/reference/telegram/types/base/input-sticker-set-animated-emoji-animations/), [`inputStickerSetDice`](/reference/telegram/types/base/input-sticker-set-dice/), [`inputStickerSetEmojiChannelDefaultStatuses`](/reference/telegram/types/base/input-sticker-set-emoji-channel-default-statuses/), [`inputStickerSetEmojiDefaultStatuses`](/reference/telegram/types/base/input-sticker-set-emoji-default-statuses/), [`inputStickerSetEmojiDefaultTopicIcons`](/reference/telegram/types/base/input-sticker-set-emoji-default-topic-icons/), [`inputStickerSetEmojiGenericAnimations`](/reference/telegram/types/base/input-sticker-set-emoji-generic-animations/), [`inputStickerSetEmpty`](/reference/telegram/types/base/input-sticker-set-empty/), [`inputStickerSetID`](/reference/telegram/types/base/input-sticker-set-id/), [`inputStickerSetPremiumGifts`](/reference/telegram/types/base/input-sticker-set-premium-gifts/), [`inputStickerSetShortName`](/reference/telegram/types/base/input-sticker-set-short-name/), [`inputStickerSetTonGifts`](/reference/telegram/types/base/input-sticker-set-ton-gifts/)

## Returned types

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)
Known selected constructors: [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/), [`messages.stickerSetNotModified`](/reference/telegram/types/messages/sticker-set-not-modified/)

## Related methods

[`account.createTheme`](/reference/telegram/functions/account/create-theme/), [`account.saveMusic`](/reference/telegram/functions/account/save-music/), [`account.saveRingtone`](/reference/telegram/functions/account/save-ringtone/), [`account.updateTheme`](/reference/telegram/functions/account/update-theme/), [`channels.setEmojiStickers`](/reference/telegram/functions/channels/set-emoji-stickers/), [`channels.setStickers`](/reference/telegram/functions/channels/set-stickers/), [`messages.faveSticker`](/reference/telegram/functions/messages/fave-sticker/), [`messages.getStickerSet`](/reference/telegram/functions/messages/get-sticker-set/), [`messages.installStickerSet`](/reference/telegram/functions/messages/install-sticker-set/), [`messages.reportMusicListen`](/reference/telegram/functions/messages/report-music-listen/), [`messages.saveGif`](/reference/telegram/functions/messages/save-gif/), [`messages.saveRecentSticker`](/reference/telegram/functions/messages/save-recent-sticker/), [`messages.toggleStickerSets`](/reference/telegram/functions/messages/toggle-sticker-sets/), [`messages.uninstallStickerSet`](/reference/telegram/functions/messages/uninstall-sticker-set/), [`stickers.addStickerToSet`](/reference/telegram/functions/stickers/add-sticker-to-set/), [`stickers.changeSticker`](/reference/telegram/functions/stickers/change-sticker/), [`stickers.changeStickerPosition`](/reference/telegram/functions/stickers/change-sticker-position/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stickers.deleteStickerSet`](/reference/telegram/functions/stickers/delete-sticker-set/), [`stickers.removeStickerFromSet`](/reference/telegram/functions/stickers/remove-sticker-from-set/), [`stickers.renameStickerSet`](/reference/telegram/functions/stickers/rename-sticker-set/), [`stickers.replaceSticker`](/reference/telegram/functions/stickers/replace-sticker/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`users.getSavedMusicByID`](/reference/telegram/functions/users/get-saved-music-by-id/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
