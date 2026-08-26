---
title: "inputStorePaymentStarsTopup"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputStorePaymentStarsTopup"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf9a2a6cb"
---

# `inputStorePaymentStarsTopup`

No description provided by the pinned schema.

## Signature

```tl
inputStorePaymentStarsTopup#f9a2a6cb flags:# stars:long currency:string amount:long spend_purpose_peer:flags.0?InputPeer = InputStorePaymentPurpose;
```

## Result type

`InputStorePaymentPurpose`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| stars | long | — | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |
| spend_purpose_peer | flags.0?InputPeer | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| spend_purpose_peer | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputStorePaymentStarsTopup
```

Public access: `miniproto.raw.types.InputStorePaymentStarsTopup`.

## Safe usage shape

```python
from miniproto.raw.types import InputStorePaymentStarsTopup

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputStorePaymentStarsTopup
```

## Result family

[`InputStorePaymentPurpose`](/reference/telegram/types/results/input-store-payment-purpose/)

## Relationships

- Result family: [`InputStorePaymentPurpose`](/reference/telegram/types/results/input-store-payment-purpose/)
- Related constructors: [`inputStorePaymentAuthCode`](/reference/telegram/types/base/input-store-payment-auth-code/), [`inputStorePaymentGiftPremium`](/reference/telegram/types/base/input-store-payment-gift-premium/), [`inputStorePaymentPremiumGiftCode`](/reference/telegram/types/base/input-store-payment-premium-gift-code/), [`inputStorePaymentPremiumGiveaway`](/reference/telegram/types/base/input-store-payment-premium-giveaway/), [`inputStorePaymentPremiumSubscription`](/reference/telegram/types/base/input-store-payment-premium-subscription/), [`inputStorePaymentStarsGift`](/reference/telegram/types/base/input-store-payment-stars-gift/), [`inputStorePaymentStarsGiveaway`](/reference/telegram/types/base/input-store-payment-stars-giveaway/)
- Accepted by: [`payments.assignAppStoreTransaction`](/reference/telegram/functions/payments/assign-app-store-transaction/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.canPurchaseStore`](/reference/telegram/functions/payments/can-purchase-store/), [`payments.launchPrepaidGiveaway`](/reference/telegram/functions/payments/launch-prepaid-giveaway/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
