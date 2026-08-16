---
title: "stickerSet"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stickerSet"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2dd14edc"
---

# `stickerSet`

No description provided by the pinned schema.

## Signature

```tl
stickerSet#2dd14edc flags:# archived:flags.1?true official:flags.2?true masks:flags.3?true emojis:flags.7?true text_color:flags.9?true channel_emoji_status:flags.10?true creator:flags.11?true installed_date:flags.0?int id:long access_hash:long title:string short_name:string thumbs:flags.4?Vector<PhotoSize> thumb_dc_id:flags.4?int thumb_version:flags.4?int thumb_document_id:flags.8?long count:int hash:int = StickerSet;
```

## Result type

`StickerSet`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| archived | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| official | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| masks | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| emojis | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| text_color | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| channel_emoji_status | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| creator | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| installed_date | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| short_name | string | — | — | No description provided by the pinned schema. |
| thumbs | flags.4?Vector<PhotoSize> | flags.4 | — | No description provided by the pinned schema. |
| thumb_dc_id | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| thumb_version | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| thumb_document_id | flags.8?long | flags.8 | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| hash | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| archived | 1 | Controlled by `flags`; present when this bit is set. |
| official | 2 | Controlled by `flags`; present when this bit is set. |
| masks | 3 | Controlled by `flags`; present when this bit is set. |
| emojis | 7 | Controlled by `flags`; present when this bit is set. |
| text_color | 9 | Controlled by `flags`; present when this bit is set. |
| channel_emoji_status | 10 | Controlled by `flags`; present when this bit is set. |
| creator | 11 | Controlled by `flags`; present when this bit is set. |
| installed_date | 0 | Controlled by `flags`; present when this bit is set. |
| thumbs | 4 | Controlled by `flags`; present when this bit is set. |
| thumb_dc_id | 4 | Controlled by `flags`; present when this bit is set. |
| thumb_version | 4 | Controlled by `flags`; present when this bit is set. |
| thumb_document_id | 8 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StickerSet
```

Public access: `miniproto.raw.types.StickerSet`.

## Safe usage shape

```python
from miniproto.raw.types import StickerSet

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StickerSet
```

## Result family

[`StickerSet`](/reference/telegram/types/results/sticker-set/)

## Relationships

- Result family: [`StickerSet`](/reference/telegram/types/results/sticker-set/)
- Accepted by: [`channelFull`](/reference/telegram/types/base/channel-full/), [`messages.allStickers`](/reference/telegram/types/messages/all-stickers/), [`messages.stickerSet`](/reference/telegram/types/messages/sticker-set/), [`stickerSetCovered`](/reference/telegram/types/base/sticker-set-covered/), [`stickerSetFullCovered`](/reference/telegram/types/base/sticker-set-full-covered/), [`stickerSetMultiCovered`](/reference/telegram/types/base/sticker-set-multi-covered/), [`stickerSetNoCovered`](/reference/telegram/types/base/sticker-set-no-covered/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
