---
title: "starGift"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGift"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x313a9547"
---

# `starGift`

No description provided by the pinned schema.

## Signature

```tl
starGift#313a9547 flags:# limited:flags.0?true sold_out:flags.1?true birthday:flags.2?true require_premium:flags.7?true limited_per_user:flags.8?true peer_color_available:flags.10?true auction:flags.11?true id:long sticker:Document stars:long availability_remains:flags.0?int availability_total:flags.0?int availability_resale:flags.4?long convert_stars:long first_sale_date:flags.1?int last_sale_date:flags.1?int upgrade_stars:flags.3?long resell_min_stars:flags.4?long title:flags.5?string released_by:flags.6?Peer per_user_total:flags.8?int per_user_remains:flags.8?int locked_until_date:flags.9?int auction_slug:flags.11?string gifts_per_round:flags.11?int auction_start_date:flags.11?int upgrade_variants:flags.12?int background:flags.13?StarGiftBackground = StarGift;
```

## Result type

`StarGift`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| limited | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| sold_out | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| birthday | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| require_premium | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| limited_per_user | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| peer_color_available | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| auction | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| sticker | Document | — | — | No description provided by the pinned schema. |
| stars | long | — | — | No description provided by the pinned schema. |
| availability_remains | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| availability_total | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| availability_resale | flags.4?long | flags.4 | — | No description provided by the pinned schema. |
| convert_stars | long | — | — | No description provided by the pinned schema. |
| first_sale_date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| last_sale_date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| upgrade_stars | flags.3?long | flags.3 | — | No description provided by the pinned schema. |
| resell_min_stars | flags.4?long | flags.4 | — | No description provided by the pinned schema. |
| title | flags.5?string | flags.5 | — | No description provided by the pinned schema. |
| released_by | flags.6?Peer | flags.6 | — | No description provided by the pinned schema. |
| per_user_total | flags.8?int | flags.8 | — | No description provided by the pinned schema. |
| per_user_remains | flags.8?int | flags.8 | — | No description provided by the pinned schema. |
| locked_until_date | flags.9?int | flags.9 | — | No description provided by the pinned schema. |
| auction_slug | flags.11?string | flags.11 | — | No description provided by the pinned schema. |
| gifts_per_round | flags.11?int | flags.11 | — | No description provided by the pinned schema. |
| auction_start_date | flags.11?int | flags.11 | — | No description provided by the pinned schema. |
| upgrade_variants | flags.12?int | flags.12 | — | No description provided by the pinned schema. |
| background | flags.13?StarGiftBackground | flags.13 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| limited | 0 | Controlled by `flags`; present when this bit is set. |
| sold_out | 1 | Controlled by `flags`; present when this bit is set. |
| birthday | 2 | Controlled by `flags`; present when this bit is set. |
| require_premium | 7 | Controlled by `flags`; present when this bit is set. |
| limited_per_user | 8 | Controlled by `flags`; present when this bit is set. |
| peer_color_available | 10 | Controlled by `flags`; present when this bit is set. |
| auction | 11 | Controlled by `flags`; present when this bit is set. |
| availability_remains | 0 | Controlled by `flags`; present when this bit is set. |
| availability_total | 0 | Controlled by `flags`; present when this bit is set. |
| availability_resale | 4 | Controlled by `flags`; present when this bit is set. |
| first_sale_date | 1 | Controlled by `flags`; present when this bit is set. |
| last_sale_date | 1 | Controlled by `flags`; present when this bit is set. |
| upgrade_stars | 3 | Controlled by `flags`; present when this bit is set. |
| resell_min_stars | 4 | Controlled by `flags`; present when this bit is set. |
| title | 5 | Controlled by `flags`; present when this bit is set. |
| released_by | 6 | Controlled by `flags`; present when this bit is set. |
| per_user_total | 8 | Controlled by `flags`; present when this bit is set. |
| per_user_remains | 8 | Controlled by `flags`; present when this bit is set. |
| locked_until_date | 9 | Controlled by `flags`; present when this bit is set. |
| auction_slug | 11 | Controlled by `flags`; present when this bit is set. |
| gifts_per_round | 11 | Controlled by `flags`; present when this bit is set. |
| auction_start_date | 11 | Controlled by `flags`; present when this bit is set. |
| upgrade_variants | 12 | Controlled by `flags`; present when this bit is set. |
| background | 13 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarGift
```

Public access: `miniproto.raw.types.StarGift`.

## Safe usage shape

```python
from miniproto.raw.types import StarGift

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGift
```

## Result family

[`StarGift`](/reference/telegram/types/results/star-gift/)

## Relationships

- Result family: [`StarGift`](/reference/telegram/types/results/star-gift/)
- Related constructors: [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/)
- Accepted by: [`chatThemeUniqueGift`](/reference/telegram/types/base/chat-theme-unique-gift/), [`messageActionStarGift`](/reference/telegram/types/base/message-action-star-gift/), [`messageActionStarGiftPurchaseOffer`](/reference/telegram/types/base/message-action-star-gift-purchase-offer/), [`messageActionStarGiftPurchaseOfferDeclined`](/reference/telegram/types/base/message-action-star-gift-purchase-offer-declined/), [`messageActionStarGiftUnique`](/reference/telegram/types/base/message-action-star-gift-unique/), [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/), [`payments.starGifts`](/reference/telegram/types/payments/star-gifts/), [`payments.uniqueStarGift`](/reference/telegram/types/payments/unique-star-gift/), [`savedStarGift`](/reference/telegram/types/base/saved-star-gift/), [`starGiftActiveAuctionState`](/reference/telegram/types/base/star-gift-active-auction-state/), [`starsTransaction`](/reference/telegram/types/base/stars-transaction/), [`webPageAttributeStarGiftAuction`](/reference/telegram/types/base/web-page-attribute-star-gift-auction/), [`webPageAttributeUniqueStarGift`](/reference/telegram/types/base/web-page-attribute-unique-star-gift/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
