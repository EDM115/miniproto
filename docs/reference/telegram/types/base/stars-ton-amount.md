---
title: "starsTonAmount"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starsTonAmount"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x74aee3e0"
---

# `starsTonAmount`

No description provided by the pinned schema.

## Signature

```tl
starsTonAmount#74aee3e0 amount:long = StarsAmount;
```

## Result type

`StarsAmount`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| amount | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarsTonAmount
```

Public access: `miniproto.raw.types.StarsTonAmount`.

## Safe usage shape

```python
from miniproto.raw.types import StarsTonAmount

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarsTonAmount
```

## Result family

[`StarsAmount`](/reference/telegram/types/results/stars-amount/)

## Relationships

- Result family: [`StarsAmount`](/reference/telegram/types/results/stars-amount/)
- Related constructors: [`starsAmount`](/reference/telegram/types/base/stars-amount/)
- Accepted by: [`payments.sendStarGiftOffer`](/reference/telegram/functions/payments/send-star-gift-offer/), [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/), [`messageActionStarGiftPurchaseOffer`](/reference/telegram/types/base/message-action-star-gift-purchase-offer/), [`messageActionStarGiftPurchaseOfferDeclined`](/reference/telegram/types/base/message-action-star-gift-purchase-offer-declined/), [`messageActionStarGiftUnique`](/reference/telegram/types/base/message-action-star-gift-unique/), [`messageActionSuggestedPostApproval`](/reference/telegram/types/base/message-action-suggested-post-approval/), [`messageActionSuggestedPostSuccess`](/reference/telegram/types/base/message-action-suggested-post-success/), [`payments.starsStatus`](/reference/telegram/types/payments/stars-status/), [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/), [`starRefProgram`](/reference/telegram/types/base/star-ref-program/), [`starsRevenueStatus`](/reference/telegram/types/base/stars-revenue-status/), [`starsTransaction`](/reference/telegram/types/base/stars-transaction/), [`suggestedPost`](/reference/telegram/types/base/suggested-post/), [`updateStarsBalance`](/reference/telegram/types/base/update-stars-balance/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
