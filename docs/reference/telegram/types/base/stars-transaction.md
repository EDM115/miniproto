---
title: "starsTransaction"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starsTransaction"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x13659eb0"
---

# `starsTransaction`

No description provided by the pinned schema.

## Signature

```tl
starsTransaction#13659eb0 flags:# refund:flags.3?true pending:flags.4?true failed:flags.6?true gift:flags.10?true reaction:flags.11?true stargift_upgrade:flags.18?true business_transfer:flags.21?true stargift_resale:flags.22?true posts_search:flags.24?true stargift_prepaid_upgrade:flags.25?true stargift_drop_original_details:flags.26?true phonegroup_message:flags.27?true stargift_auction_bid:flags.28?true offer:flags.29?true id:string amount:StarsAmount date:int peer:StarsTransactionPeer title:flags.0?string description:flags.1?string photo:flags.2?WebDocument transaction_date:flags.5?int transaction_url:flags.5?string bot_payload:flags.7?bytes msg_id:flags.8?int extended_media:flags.9?Vector<MessageMedia> subscription_period:flags.12?int giveaway_post_id:flags.13?int stargift:flags.14?StarGift floodskip_number:flags.15?int starref_commission_permille:flags.16?int starref_peer:flags.17?Peer starref_amount:flags.17?StarsAmount paid_messages:flags.19?int premium_gift_months:flags.20?int ads_proceeds_from_date:flags.23?int ads_proceeds_to_date:flags.23?int = StarsTransaction;
```

## Result type

`StarsTransaction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| refund | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| pending | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| failed | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| gift | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| reaction | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| stargift_upgrade | flags.18?true | flags.18 | — | No description provided by the pinned schema. |
| business_transfer | flags.21?true | flags.21 | — | No description provided by the pinned schema. |
| stargift_resale | flags.22?true | flags.22 | — | No description provided by the pinned schema. |
| posts_search | flags.24?true | flags.24 | — | No description provided by the pinned schema. |
| stargift_prepaid_upgrade | flags.25?true | flags.25 | — | No description provided by the pinned schema. |
| stargift_drop_original_details | flags.26?true | flags.26 | — | No description provided by the pinned schema. |
| phonegroup_message | flags.27?true | flags.27 | — | No description provided by the pinned schema. |
| stargift_auction_bid | flags.28?true | flags.28 | — | No description provided by the pinned schema. |
| offer | flags.29?true | flags.29 | — | No description provided by the pinned schema. |
| id | string | — | — | No description provided by the pinned schema. |
| amount | StarsAmount | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| peer | StarsTransactionPeer | — | — | No description provided by the pinned schema. |
| title | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| description | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| photo | flags.2?WebDocument | flags.2 | — | No description provided by the pinned schema. |
| transaction_date | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| transaction_url | flags.5?string | flags.5 | — | No description provided by the pinned schema. |
| bot_payload | flags.7?bytes | flags.7 | — | No description provided by the pinned schema. |
| msg_id | flags.8?int | flags.8 | — | No description provided by the pinned schema. |
| extended_media | flags.9?Vector<MessageMedia> | flags.9 | — | No description provided by the pinned schema. |
| subscription_period | flags.12?int | flags.12 | — | No description provided by the pinned schema. |
| giveaway_post_id | flags.13?int | flags.13 | — | No description provided by the pinned schema. |
| stargift | flags.14?StarGift | flags.14 | — | No description provided by the pinned schema. |
| floodskip_number | flags.15?int | flags.15 | — | No description provided by the pinned schema. |
| starref_commission_permille | flags.16?int | flags.16 | — | No description provided by the pinned schema. |
| starref_peer | flags.17?Peer | flags.17 | — | No description provided by the pinned schema. |
| starref_amount | flags.17?StarsAmount | flags.17 | — | No description provided by the pinned schema. |
| paid_messages | flags.19?int | flags.19 | — | No description provided by the pinned schema. |
| premium_gift_months | flags.20?int | flags.20 | — | No description provided by the pinned schema. |
| ads_proceeds_from_date | flags.23?int | flags.23 | — | No description provided by the pinned schema. |
| ads_proceeds_to_date | flags.23?int | flags.23 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| refund | 3 | Controlled by `flags`; present when this bit is set. |
| pending | 4 | Controlled by `flags`; present when this bit is set. |
| failed | 6 | Controlled by `flags`; present when this bit is set. |
| gift | 10 | Controlled by `flags`; present when this bit is set. |
| reaction | 11 | Controlled by `flags`; present when this bit is set. |
| stargift_upgrade | 18 | Controlled by `flags`; present when this bit is set. |
| business_transfer | 21 | Controlled by `flags`; present when this bit is set. |
| stargift_resale | 22 | Controlled by `flags`; present when this bit is set. |
| posts_search | 24 | Controlled by `flags`; present when this bit is set. |
| stargift_prepaid_upgrade | 25 | Controlled by `flags`; present when this bit is set. |
| stargift_drop_original_details | 26 | Controlled by `flags`; present when this bit is set. |
| phonegroup_message | 27 | Controlled by `flags`; present when this bit is set. |
| stargift_auction_bid | 28 | Controlled by `flags`; present when this bit is set. |
| offer | 29 | Controlled by `flags`; present when this bit is set. |
| title | 0 | Controlled by `flags`; present when this bit is set. |
| description | 1 | Controlled by `flags`; present when this bit is set. |
| photo | 2 | Controlled by `flags`; present when this bit is set. |
| transaction_date | 5 | Controlled by `flags`; present when this bit is set. |
| transaction_url | 5 | Controlled by `flags`; present when this bit is set. |
| bot_payload | 7 | Controlled by `flags`; present when this bit is set. |
| msg_id | 8 | Controlled by `flags`; present when this bit is set. |
| extended_media | 9 | Controlled by `flags`; present when this bit is set. |
| subscription_period | 12 | Controlled by `flags`; present when this bit is set. |
| giveaway_post_id | 13 | Controlled by `flags`; present when this bit is set. |
| stargift | 14 | Controlled by `flags`; present when this bit is set. |
| floodskip_number | 15 | Controlled by `flags`; present when this bit is set. |
| starref_commission_permille | 16 | Controlled by `flags`; present when this bit is set. |
| starref_peer | 17 | Controlled by `flags`; present when this bit is set. |
| starref_amount | 17 | Controlled by `flags`; present when this bit is set. |
| paid_messages | 19 | Controlled by `flags`; present when this bit is set. |
| premium_gift_months | 20 | Controlled by `flags`; present when this bit is set. |
| ads_proceeds_from_date | 23 | Controlled by `flags`; present when this bit is set. |
| ads_proceeds_to_date | 23 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarsTransaction
```

Public access: `miniproto.raw.types.StarsTransaction`.

## Safe usage shape

```python
from miniproto.raw.types import StarsTransaction

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarsTransaction
```

## Result family

[`StarsTransaction`](/reference/telegram/types/results/stars-transaction/)

## Relationships

- Result family: [`StarsTransaction`](/reference/telegram/types/results/stars-transaction/)
- Accepted by: [`payments.starsStatus`](/reference/telegram/types/payments/stars-status/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
