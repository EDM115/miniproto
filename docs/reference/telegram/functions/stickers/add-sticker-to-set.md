---
title: "stickers.addStickerToSet"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "stickers.addStickerToSet"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stickers"
schema_source: "tdlib"
constructor_id: "0x8653febe"
---

# `stickers.addStickerToSet`

No description provided by the pinned schema.

## Signature

```tl
stickers.addStickerToSet#8653febe stickerset:InputStickerSet sticker:InputStickerSetItem = messages.StickerSet;
```

## Result type

`messages.StickerSet`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| stickerset | InputStickerSet | — | — | No description provided by the pinned schema. |
| sticker | InputStickerSetItem | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import StickersAddStickerToSet
```

Public access: `miniproto.raw.functions.StickersAddStickerToSet`.

## Safe usage shape

```python
from miniproto.raw.functions import StickersAddStickerToSet

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = StickersAddStickerToSet
```

## Result family

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`STICKERPACK_STICKERS_TOO_MUCH`](/reference/telegram/errors/stickerpack-stickers-too-much/) | There are too many stickers in this stickerpack, you can't add any more. |
| 400 | [`STICKERSET_INVALID`](/reference/telegram/errors/stickerset-invalid/) | The provided sticker set is invalid. |
| 400 | [`STICKERS_TOO_MUCH`](/reference/telegram/errors/stickers-too-much/) | There are too many stickers in this stickerpack, you can't add any more. |
| 400 | [`STICKER_PNG_NOPNG`](/reference/telegram/errors/sticker-png-nopng/) | One of the specified stickers is not a valid PNG file. |
| 400 | [`STICKER_TGS_NOTGS`](/reference/telegram/errors/sticker-tgs-notgs/) | Invalid TGS sticker provided. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 406 | [`STICKERSET_INVALID`](/reference/telegram/errors/stickerset-invalid-406/) | The provided sticker set is invalid. |

## Accepted types

[`InputStickerSet`](/reference/telegram/types/results/input-sticker-set/), [`InputStickerSetItem`](/reference/telegram/types/results/input-sticker-set-item/)
Known selected constructors: [`inputStickerSetAnimatedEmoji`](/reference/telegram/types/base/input-sticker-set-animated-emoji/), [`inputStickerSetAnimatedEmojiAnimations`](/reference/telegram/types/base/input-sticker-set-animated-emoji-animations/), [`inputStickerSetDice`](/reference/telegram/types/base/input-sticker-set-dice/), [`inputStickerSetEmojiChannelDefaultStatuses`](/reference/telegram/types/base/input-sticker-set-emoji-channel-default-statuses/), [`inputStickerSetEmojiDefaultStatuses`](/reference/telegram/types/base/input-sticker-set-emoji-default-statuses/), [`inputStickerSetEmojiDefaultTopicIcons`](/reference/telegram/types/base/input-sticker-set-emoji-default-topic-icons/), [`inputStickerSetEmojiGenericAnimations`](/reference/telegram/types/base/input-sticker-set-emoji-generic-animations/), [`inputStickerSetEmpty`](/reference/telegram/types/base/input-sticker-set-empty/), [`inputStickerSetID`](/reference/telegram/types/base/input-sticker-set-id/), [`inputStickerSetPremiumGifts`](/reference/telegram/types/base/input-sticker-set-premium-gifts/), [`inputStickerSetShortName`](/reference/telegram/types/base/input-sticker-set-short-name/), [`inputStickerSetTonGifts`](/reference/telegram/types/base/input-sticker-set-ton-gifts/), [`inputStickerSetItem`](/reference/telegram/types/base/input-sticker-set-item/)

## Returned types

[`messages.StickerSet`](/reference/telegram/types/results/messages-sticker-set/)
Known selected constructors: [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/), [`messages.stickerSetNotModified`](/reference/telegram/types/messages/sticker-set-not-modified/)

## Related methods

[`channels.setEmojiStickers`](/reference/telegram/functions/channels/set-emoji-stickers/), [`channels.setStickers`](/reference/telegram/functions/channels/set-stickers/), [`messages.getStickerSet`](/reference/telegram/functions/messages/get-sticker-set/), [`messages.installStickerSet`](/reference/telegram/functions/messages/install-sticker-set/), [`messages.toggleStickerSets`](/reference/telegram/functions/messages/toggle-sticker-sets/), [`messages.uninstallStickerSet`](/reference/telegram/functions/messages/uninstall-sticker-set/), [`stickers.changeSticker`](/reference/telegram/functions/stickers/change-sticker/), [`stickers.changeStickerPosition`](/reference/telegram/functions/stickers/change-sticker-position/), [`stickers.createStickerSet`](/reference/telegram/functions/stickers/create-sticker-set/), [`stickers.deleteStickerSet`](/reference/telegram/functions/stickers/delete-sticker-set/), [`stickers.removeStickerFromSet`](/reference/telegram/functions/stickers/remove-sticker-from-set/), [`stickers.renameStickerSet`](/reference/telegram/functions/stickers/rename-sticker-set/), [`stickers.replaceSticker`](/reference/telegram/functions/stickers/replace-sticker/), [`stickers.setStickerSetThumb`](/reference/telegram/functions/stickers/set-sticker-set-thumb/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
