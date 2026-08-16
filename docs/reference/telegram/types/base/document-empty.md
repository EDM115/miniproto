---
title: "documentEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "documentEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x36f8c871"
---

# `documentEmpty`

No description provided by the pinned schema.

## Signature

```tl
documentEmpty#36f8c871 id:long = Document;
```

## Result type

`Document`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import DocumentEmpty
```

Public access: `miniproto.raw.types.DocumentEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import DocumentEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DocumentEmpty
```

## Result family

[`Document`](/reference/telegram/types/results/document/)

## Relationships

- Result family: [`Document`](/reference/telegram/types/results/document/)
- Related constructors: [`document`](/reference/telegram/types/base/document/)
- Accepted by: [`account.savedRingtoneConverted`](/reference/telegram/types/account/saved-ringtone-converted/), [`account.savedRingtones`](/reference/telegram/types/account/saved-ringtones/), [`attachMenuBotIcon`](/reference/telegram/types/base/attach-menu-bot-icon/), [`availableReaction`](/reference/telegram/types/base/available-reaction/), [`botApp`](/reference/telegram/types/base/bot-app/), [`botInfo`](/reference/telegram/types/base/bot-info/), [`botInlineMediaResult`](/reference/telegram/types/base/bot-inline-media-result/), [`businessIntro`](/reference/telegram/types/base/business-intro/), [`game`](/reference/telegram/types/base/game/), [`help.appUpdate`](/reference/telegram/types/help/app-update/), [`help.premiumPromo`](/reference/telegram/types/help/premium-promo/), [`messageMediaDocument`](/reference/telegram/types/base/message-media-document/), [`messageMediaPhoto`](/reference/telegram/types/base/message-media-photo/), [`messages.availableEffects`](/reference/telegram/types/messages/available-effects/), [`messages.favedStickers`](/reference/telegram/types/messages/faved-stickers/), [`messages.foundStickers`](/reference/telegram/types/messages/found-stickers/), [`messages.recentStickers`](/reference/telegram/types/messages/recent-stickers/), [`messages.savedGifs`](/reference/telegram/types/messages/saved-gifs/), [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/), [`messages.stickers`](/reference/telegram/types/messages/stickers/), [`page`](/reference/telegram/types/base/page/), [`richMessage`](/reference/telegram/types/base/rich-message/), [`starGift`](/reference/telegram/types/base/star-gift/), [`starGiftAttributeModel`](/reference/telegram/types/base/star-gift-attribute-model/), [`starGiftAttributePattern`](/reference/telegram/types/base/star-gift-attribute-pattern/), [`starGiftCollection`](/reference/telegram/types/base/star-gift-collection/), [`stickerSetCovered`](/reference/telegram/types/base/sticker-set-covered/), [`stickerSetFullCovered`](/reference/telegram/types/base/sticker-set-full-covered/), [`stickerSetMultiCovered`](/reference/telegram/types/base/sticker-set-multi-covered/), [`storyAlbum`](/reference/telegram/types/base/story-album/), [`storyItem`](/reference/telegram/types/base/story-item/), [`theme`](/reference/telegram/types/base/theme/), [`userFull`](/reference/telegram/types/base/user-full/), [`users.savedMusic`](/reference/telegram/types/users/saved-music/), [`wallPaper`](/reference/telegram/types/base/wall-paper/), [`webPage`](/reference/telegram/types/base/web-page/), [`webPageAttributeStarGiftCollection`](/reference/telegram/types/base/web-page-attribute-star-gift-collection/), [`webPageAttributeStickerSet`](/reference/telegram/types/base/web-page-attribute-sticker-set/), [`webPageAttributeTheme`](/reference/telegram/types/base/web-page-attribute-theme/)
- Returned by: [`account.uploadRingtone`](/reference/telegram/functions/account/upload-ringtone/), [`account.uploadTheme`](/reference/telegram/functions/account/upload-theme/), [`messages.getCustomEmojiDocuments`](/reference/telegram/functions/messages/get-custom-emoji-documents/), [`messages.getDocumentByHash`](/reference/telegram/functions/messages/get-document-by-hash/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
