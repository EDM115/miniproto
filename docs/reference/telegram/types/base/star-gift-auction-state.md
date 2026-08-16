---
title: "starGiftAuctionState"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAuctionState"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x771a4e66"
---

# `starGiftAuctionState`

No description provided by the pinned schema.

## Signature

```tl
starGiftAuctionState#771a4e66 version:int start_date:int end_date:int min_bid_amount:long bid_levels:Vector<AuctionBidLevel> top_bidders:Vector<long> next_round_at:int last_gift_num:int gifts_left:int current_round:int total_rounds:int rounds:Vector<StarGiftAuctionRound> = StarGiftAuctionState;
```

## Result type

`StarGiftAuctionState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| version | int | — | — | No description provided by the pinned schema. |
| start_date | int | — | — | No description provided by the pinned schema. |
| end_date | int | — | — | No description provided by the pinned schema. |
| min_bid_amount | long | — | — | No description provided by the pinned schema. |
| bid_levels | Vector<AuctionBidLevel> | — | — | No description provided by the pinned schema. |
| top_bidders | Vector<long> | — | — | No description provided by the pinned schema. |
| next_round_at | int | — | — | No description provided by the pinned schema. |
| last_gift_num | int | — | — | No description provided by the pinned schema. |
| gifts_left | int | — | — | No description provided by the pinned schema. |
| current_round | int | — | — | No description provided by the pinned schema. |
| total_rounds | int | — | — | No description provided by the pinned schema. |
| rounds | Vector<StarGiftAuctionRound> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarGiftAuctionState
```

Public access: `miniproto.raw.types.StarGiftAuctionState`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAuctionState

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAuctionState
```

## Result family

[`StarGiftAuctionState`](/reference/telegram/types/results/star-gift-auction-state/)

## Relationships

- Result family: [`StarGiftAuctionState`](/reference/telegram/types/results/star-gift-auction-state/)
- Related constructors: [`starGiftAuctionStateFinished`](/reference/telegram/types/base/star-gift-auction-state-finished/), [`starGiftAuctionStateNotModified`](/reference/telegram/types/base/star-gift-auction-state-not-modified/)
- Accepted by: [`payments.starGiftAuctionState`](/reference/telegram/types/payments/star-gift-auction-state/), [`starGiftActiveAuctionState`](/reference/telegram/types/base/star-gift-active-auction-state/), [`updateStarGiftAuctionState`](/reference/telegram/types/base/update-star-gift-auction-state/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
