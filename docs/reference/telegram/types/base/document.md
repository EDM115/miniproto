---
title: "document"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "document"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x8fd4c4d8"
---

# `document`

No description provided by the pinned schema.

## Signature

```tl
document#8fd4c4d8 flags:# id:long access_hash:long file_reference:bytes date:int mime_type:string size:long thumbs:flags.0?Vector<PhotoSize> video_thumbs:flags.1?Vector<VideoSize> dc_id:int attributes:Vector<DocumentAttribute> = Document;
```

## Result type

`Document`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| file_reference | bytes | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| mime_type | string | — | — | No description provided by the pinned schema. |
| size | long | — | — | No description provided by the pinned schema. |
| thumbs | flags.0?Vector<PhotoSize> | flags.0 | — | No description provided by the pinned schema. |
| video_thumbs | flags.1?Vector<VideoSize> | flags.1 | — | No description provided by the pinned schema. |
| dc_id | int | — | — | No description provided by the pinned schema. |
| attributes | Vector<DocumentAttribute> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| thumbs | 0 | Controlled by `flags`; present when this bit is set. |
| video_thumbs | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Document
```

Public access: `miniproto.raw.types.Document`.

## Safe usage shape

```python
from miniproto.raw.types import Document

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Document
```

## Result family

[`Document`](/reference/telegram/types/results/document/)

## Relationships

- Result family: [`Document`](/reference/telegram/types/results/document/)
- Related constructors: [`documentEmpty`](/reference/telegram/types/base/document-empty/)
- Accepted by: [`account.savedRingtoneConverted`](/reference/telegram/types/account/saved-ringtone-converted/), [`account.savedRingtones`](/reference/telegram/types/account/saved-ringtones/), [`attachMenuBotIcon`](/reference/telegram/types/base/attach-menu-bot-icon/), [`availableReaction`](/reference/telegram/types/base/available-reaction/), [`botApp`](/reference/telegram/types/base/bot-app/), [`botInfo`](/reference/telegram/types/base/bot-info/), [`botInlineMediaResult`](/reference/telegram/types/base/bot-inline-media-result/), [`businessIntro`](/reference/telegram/types/base/business-intro/), [`game`](/reference/telegram/types/base/game/), [`help.appUpdate`](/reference/telegram/types/help/app-update/), [`help.premiumPromo`](/reference/telegram/types/help/premium-promo/), [`messageMediaDocument`](/reference/telegram/types/base/message-media-document/), [`messageMediaPhoto`](/reference/telegram/types/base/message-media-photo/), [`messages.availableEffects`](/reference/telegram/types/messages/available-effects/), [`messages.favedStickers`](/reference/telegram/types/messages/faved-stickers/), [`messages.foundStickers`](/reference/telegram/types/messages/found-stickers/), [`messages.recentStickers`](/reference/telegram/types/messages/recent-stickers/), [`messages.savedGifs`](/reference/telegram/types/messages/saved-gifs/), [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/), [`messages.stickers`](/reference/telegram/types/messages/stickers/), [`page`](/reference/telegram/types/base/page/), [`richMessage`](/reference/telegram/types/base/rich-message/), [`starGift`](/reference/telegram/types/base/star-gift/), [`starGiftAttributeModel`](/reference/telegram/types/base/star-gift-attribute-model/), [`starGiftAttributePattern`](/reference/telegram/types/base/star-gift-attribute-pattern/), [`starGiftCollection`](/reference/telegram/types/base/star-gift-collection/), [`stickerSetCovered`](/reference/telegram/types/base/sticker-set-covered/), [`stickerSetFullCovered`](/reference/telegram/types/base/sticker-set-full-covered/), [`stickerSetMultiCovered`](/reference/telegram/types/base/sticker-set-multi-covered/), [`storyAlbum`](/reference/telegram/types/base/story-album/), [`storyItem`](/reference/telegram/types/base/story-item/), [`theme`](/reference/telegram/types/base/theme/), [`userFull`](/reference/telegram/types/base/user-full/), [`users.savedMusic`](/reference/telegram/types/users/saved-music/), [`wallPaper`](/reference/telegram/types/base/wall-paper/), [`webPage`](/reference/telegram/types/base/web-page/), [`webPageAttributeStarGiftCollection`](/reference/telegram/types/base/web-page-attribute-star-gift-collection/), [`webPageAttributeStickerSet`](/reference/telegram/types/base/web-page-attribute-sticker-set/), [`webPageAttributeTheme`](/reference/telegram/types/base/web-page-attribute-theme/)
- Returned by: [`account.uploadRingtone`](/reference/telegram/functions/account/upload-ringtone/), [`account.uploadTheme`](/reference/telegram/functions/account/upload-theme/), [`messages.getCustomEmojiDocuments`](/reference/telegram/functions/messages/get-custom-emoji-documents/), [`messages.getDocumentByHash`](/reference/telegram/functions/messages/get-document-by-hash/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
