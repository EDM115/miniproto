---
title: "starGiftUnique"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftUnique"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x85f0a9cd"
---

# `starGiftUnique`

No description provided by the pinned schema.

## Signature

```tl
starGiftUnique#85f0a9cd flags:# require_premium:flags.6?true resale_ton_only:flags.7?true theme_available:flags.9?true burned:flags.14?true crafted:flags.15?true id:long gift_id:long title:string slug:string num:int owner_id:flags.0?Peer owner_name:flags.1?string owner_address:flags.2?string attributes:Vector<StarGiftAttribute> availability_issued:int availability_total:int gift_address:flags.3?string resell_amount:flags.4?Vector<StarsAmount> released_by:flags.5?Peer value_amount:flags.8?long value_currency:flags.8?string value_usd_amount:flags.8?long theme_peer:flags.10?Peer peer_color:flags.11?PeerColor host_id:flags.12?Peer offer_min_stars:flags.13?int craft_chance_permille:flags.16?int = StarGift;
```

## Result type

`StarGift`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| require_premium | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| resale_ton_only | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| theme_available | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| burned | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| crafted | flags.15?true | flags.15 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| gift_id | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| slug | string | — | — | No description provided by the pinned schema. |
| num | int | — | — | No description provided by the pinned schema. |
| owner_id | flags.0?Peer | flags.0 | — | No description provided by the pinned schema. |
| owner_name | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| owner_address | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| attributes | Vector<StarGiftAttribute> | — | — | No description provided by the pinned schema. |
| availability_issued | int | — | — | No description provided by the pinned schema. |
| availability_total | int | — | — | No description provided by the pinned schema. |
| gift_address | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| resell_amount | flags.4?Vector<StarsAmount> | flags.4 | — | No description provided by the pinned schema. |
| released_by | flags.5?Peer | flags.5 | — | No description provided by the pinned schema. |
| value_amount | flags.8?long | flags.8 | — | No description provided by the pinned schema. |
| value_currency | flags.8?string | flags.8 | — | No description provided by the pinned schema. |
| value_usd_amount | flags.8?long | flags.8 | — | No description provided by the pinned schema. |
| theme_peer | flags.10?Peer | flags.10 | — | No description provided by the pinned schema. |
| peer_color | flags.11?PeerColor | flags.11 | — | No description provided by the pinned schema. |
| host_id | flags.12?Peer | flags.12 | — | No description provided by the pinned schema. |
| offer_min_stars | flags.13?int | flags.13 | — | No description provided by the pinned schema. |
| craft_chance_permille | flags.16?int | flags.16 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| require_premium | 6 | Controlled by `flags`; present when this bit is set. |
| resale_ton_only | 7 | Controlled by `flags`; present when this bit is set. |
| theme_available | 9 | Controlled by `flags`; present when this bit is set. |
| burned | 14 | Controlled by `flags`; present when this bit is set. |
| crafted | 15 | Controlled by `flags`; present when this bit is set. |
| owner_id | 0 | Controlled by `flags`; present when this bit is set. |
| owner_name | 1 | Controlled by `flags`; present when this bit is set. |
| owner_address | 2 | Controlled by `flags`; present when this bit is set. |
| gift_address | 3 | Controlled by `flags`; present when this bit is set. |
| resell_amount | 4 | Controlled by `flags`; present when this bit is set. |
| released_by | 5 | Controlled by `flags`; present when this bit is set. |
| value_amount | 8 | Controlled by `flags`; present when this bit is set. |
| value_currency | 8 | Controlled by `flags`; present when this bit is set. |
| value_usd_amount | 8 | Controlled by `flags`; present when this bit is set. |
| theme_peer | 10 | Controlled by `flags`; present when this bit is set. |
| peer_color | 11 | Controlled by `flags`; present when this bit is set. |
| host_id | 12 | Controlled by `flags`; present when this bit is set. |
| offer_min_stars | 13 | Controlled by `flags`; present when this bit is set. |
| craft_chance_permille | 16 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarGiftUnique
```

Public access: `miniproto.raw.types.StarGiftUnique`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftUnique

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftUnique
```

## Result family

[`StarGift`](/reference/telegram/types/results/star-gift/)

## Relationships

- Result family: [`StarGift`](/reference/telegram/types/results/star-gift/)
- Related constructors: [`starGift`](/reference/telegram/types/base/star-gift/)
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
