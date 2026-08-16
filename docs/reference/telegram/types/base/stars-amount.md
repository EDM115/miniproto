---
title: "starsAmount"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starsAmount"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xbbb6b4a3"
---

# `starsAmount`

No description provided by the pinned schema.

## Signature

```tl
starsAmount#bbb6b4a3 amount:long nanos:int = StarsAmount;
```

## Result type

`StarsAmount`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| amount | long | — | — | No description provided by the pinned schema. |
| nanos | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarsAmount
```

Public access: `miniproto.raw.types.StarsAmount`.

## Safe usage shape

```python
from miniproto.raw.types import StarsAmount

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarsAmount
```

## Result family

[`StarsAmount`](/reference/telegram/types/results/stars-amount/)

## Relationships

- Result family: [`StarsAmount`](/reference/telegram/types/results/stars-amount/)
- Related constructors: [`starsTonAmount`](/reference/telegram/types/base/stars-ton-amount/)
- Accepted by: [`payments.sendStarGiftOffer`](/reference/telegram/functions/payments/send-star-gift-offer/), [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/), [`messageActionStarGiftPurchaseOffer`](/reference/telegram/types/base/message-action-star-gift-purchase-offer/), [`messageActionStarGiftPurchaseOfferDeclined`](/reference/telegram/types/base/message-action-star-gift-purchase-offer-declined/), [`messageActionStarGiftUnique`](/reference/telegram/types/base/message-action-star-gift-unique/), [`messageActionSuggestedPostApproval`](/reference/telegram/types/base/message-action-suggested-post-approval/), [`messageActionSuggestedPostSuccess`](/reference/telegram/types/base/message-action-suggested-post-success/), [`payments.starsStatus`](/reference/telegram/types/payments/stars-status/), [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/), [`starRefProgram`](/reference/telegram/types/base/star-ref-program/), [`starsRevenueStatus`](/reference/telegram/types/base/stars-revenue-status/), [`starsTransaction`](/reference/telegram/types/base/stars-transaction/), [`suggestedPost`](/reference/telegram/types/base/suggested-post/), [`updateStarsBalance`](/reference/telegram/types/base/update-stars-balance/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
