---
title: "starGiftAuctionUserState"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAuctionUserState"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2eeed1c4"
---

# `starGiftAuctionUserState`

No description provided by the pinned schema.

## Signature

```tl
starGiftAuctionUserState#2eeed1c4 flags:# returned:flags.1?true bid_amount:flags.0?long bid_date:flags.0?int min_bid_amount:flags.0?long bid_peer:flags.0?Peer acquired_count:int = StarGiftAuctionUserState;
```

## Result type

`StarGiftAuctionUserState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| returned | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| bid_amount | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| bid_date | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| min_bid_amount | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| bid_peer | flags.0?Peer | flags.0 | — | No description provided by the pinned schema. |
| acquired_count | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| returned | 1 | Controlled by `flags`; present when this bit is set. |
| bid_amount | 0 | Controlled by `flags`; present when this bit is set. |
| bid_date | 0 | Controlled by `flags`; present when this bit is set. |
| min_bid_amount | 0 | Controlled by `flags`; present when this bit is set. |
| bid_peer | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarGiftAuctionUserState
```

Public access: `miniproto.raw.types.StarGiftAuctionUserState`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAuctionUserState

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAuctionUserState
```

## Result family

[`StarGiftAuctionUserState`](/reference/telegram/types/results/star-gift-auction-user-state/)

## Relationships

- Result family: [`StarGiftAuctionUserState`](/reference/telegram/types/results/star-gift-auction-user-state/)
- Accepted by: [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/), [`starGiftActiveAuctionState`](/reference/telegram/types/base/star-gift-active-auction-state/), [`updateStarGiftAuctionUserState`](/reference/telegram/types/base/update-star-gift-auction-user-state/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
