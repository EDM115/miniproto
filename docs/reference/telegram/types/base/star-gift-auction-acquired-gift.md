---
title: "starGiftAuctionAcquiredGift"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAuctionAcquiredGift"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x42b00348"
---

# `starGiftAuctionAcquiredGift`

No description provided by the pinned schema.

## Signature

```tl
starGiftAuctionAcquiredGift#42b00348 flags:# name_hidden:flags.0?true peer:Peer date:int bid_amount:long round:int pos:int message:flags.1?TextWithEntities gift_num:flags.2?int = StarGiftAuctionAcquiredGift;
```

## Result type

`StarGiftAuctionAcquiredGift`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| name_hidden | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| bid_amount | long | — | — | No description provided by the pinned schema. |
| round | int | — | — | No description provided by the pinned schema. |
| pos | int | — | — | No description provided by the pinned schema. |
| message | flags.1?TextWithEntities | flags.1 | — | No description provided by the pinned schema. |
| gift_num | flags.2?int | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| name_hidden | 0 | Controlled by `flags`; present when this bit is set. |
| message | 1 | Controlled by `flags`; present when this bit is set. |
| gift_num | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarGiftAuctionAcquiredGift
```

Public access: `miniproto.raw.types.StarGiftAuctionAcquiredGift`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAuctionAcquiredGift

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAuctionAcquiredGift
```

## Result family

[`StarGiftAuctionAcquiredGift`](/reference/telegram/types/results/star-gift-auction-acquired-gift/)

## Relationships

- Result family: [`StarGiftAuctionAcquiredGift`](/reference/telegram/types/results/star-gift-auction-acquired-gift/)
- Accepted by: [`payments.starGiftAuctionAcquiredGifts`](/reference/telegram/types/payments/star-gift-auction-acquired-gifts/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
