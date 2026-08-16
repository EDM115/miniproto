---
title: "inputStickerSetEmojiChannelDefaultStatuses"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputStickerSetEmojiChannelDefaultStatuses"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x49748553"
---

# `inputStickerSetEmojiChannelDefaultStatuses`

No description provided by the pinned schema.

## Signature

```tl
inputStickerSetEmojiChannelDefaultStatuses#49748553 = InputStickerSet;
```

## Result type

`InputStickerSet`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputStickerSetEmojiChannelDefaultStatuses
```

Public access: `miniproto.raw.types.InputStickerSetEmojiChannelDefaultStatuses`.

## Safe usage shape

```python
from miniproto.raw.types import InputStickerSetEmojiChannelDefaultStatuses

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputStickerSetEmojiChannelDefaultStatuses
```

## Result family

[`InputStickerSet`](/reference/telegram/types/results/input-sticker-set/)

## Relationships

- Result family: [`InputStickerSet`](/reference/telegram/types/results/input-sticker-set/)
- Related constructors: [`inputStickerSetAnimatedEmoji`](/reference/telegram/types/base/input-sticker-set-animated-emoji/), [`inputStickerSetAnimatedEmojiAnimations`](/reference/telegram/types/base/input-sticker-set-animated-emoji-animations/), [`inputStickerSetDice`](/reference/telegram/types/base/input-sticker-set-dice/), [`inputStickerSetEmojiDefaultStatuses`](/reference/telegram/types/base/input-sticker-set-emoji-default-statuses/), [`inputStickerSetEmojiDefaultTopicIcons`](/reference/telegram/types/base/input-sticker-set-emoji-default-topic-icons/), [`inputStickerSetEmojiGenericAnimations`](/reference/telegram/types/base/input-sticker-set-emoji-generic-animations/), [`inputStickerSetEmpty`](/reference/telegram/types/base/input-sticker-set-empty/), [`inputStickerSetID`](/reference/telegram/types/base/input-sticker-set-id/), [`inputStickerSetPremiumGifts`](/reference/telegram/types/base/input-sticker-set-premium-gifts/), [`inputStickerSetShortName`](/reference/telegram/types/base/input-sticker-set-short-name/), [`inputStickerSetTonGifts`](/reference/telegram/types/base/input-sticker-set-ton-gifts/)
- Accepted by: [`channels.setEmojiStickers`](/reference/telegram/functions/channels/set-emoji-stickers/), [`channels.setStickers`](/reference/telegram/functions/channels/set-stickers/), [`messages.getStickerSet`](/reference/telegram/functions/messages/get-sticker-set/), [`messages.installStickerSet`](/reference/telegram/functions/messages/install-sticker-set/), [`messages.toggleStickerSets`](/reference/telegram/functions/messages/toggle-sticker-sets/), [`messages.uninstallStickerSet`](/reference/telegram/functions/messages/uninstall-sticker-set/), [`stickers.addStickerToSet`](/reference/telegram/functions/stickers/add-sticker-to-set/), [`stickers.deleteStickerSet`](/reference/telegram/functions/stickers/delete-sticker-set/), [`stickers.renameStickerSet`](/reference/telegram/functions/stickers/rename-sticker-set/), [`stickers.setStickerSetThumb`](/reference/telegram/functions/stickers/set-sticker-set-thumb/), [`channelAdminLogEventActionChangeEmojiStickerSet`](/reference/telegram/types/base/channel-admin-log-event-action-change-emoji-sticker-set/), [`channelAdminLogEventActionChangeStickerSet`](/reference/telegram/types/base/channel-admin-log-event-action-change-sticker-set/), [`documentAttributeCustomEmoji`](/reference/telegram/types/base/document-attribute-custom-emoji/), [`documentAttributeSticker`](/reference/telegram/types/base/document-attribute-sticker/), [`inputStickerSetThumb`](/reference/telegram/types/base/input-sticker-set-thumb/), [`inputStickerSetThumbLegacy`](/reference/telegram/types/base/input-sticker-set-thumb-legacy/), [`videoSizeStickerMarkup`](/reference/telegram/types/base/video-size-sticker-markup/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
