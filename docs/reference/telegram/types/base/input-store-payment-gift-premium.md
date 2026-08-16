---
title: "inputStorePaymentGiftPremium"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputStorePaymentGiftPremium"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x616f7fe8"
---

# `inputStorePaymentGiftPremium`

No description provided by the pinned schema.

## Signature

```tl
inputStorePaymentGiftPremium#616f7fe8 user_id:InputUser currency:string amount:long = InputStorePaymentPurpose;
```

## Result type

`InputStorePaymentPurpose`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| user_id | InputUser | — | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputStorePaymentGiftPremium
```

Public access: `miniproto.raw.types.InputStorePaymentGiftPremium`.

## Safe usage shape

```python
from miniproto.raw.types import InputStorePaymentGiftPremium

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputStorePaymentGiftPremium
```

## Result family

[`InputStorePaymentPurpose`](/reference/telegram/types/results/input-store-payment-purpose/)

## Relationships

- Result family: [`InputStorePaymentPurpose`](/reference/telegram/types/results/input-store-payment-purpose/)
- Related constructors: [`inputStorePaymentAuthCode`](/reference/telegram/types/base/input-store-payment-auth-code/), [`inputStorePaymentPremiumGiftCode`](/reference/telegram/types/base/input-store-payment-premium-gift-code/), [`inputStorePaymentPremiumGiveaway`](/reference/telegram/types/base/input-store-payment-premium-giveaway/), [`inputStorePaymentPremiumSubscription`](/reference/telegram/types/base/input-store-payment-premium-subscription/), [`inputStorePaymentStarsGift`](/reference/telegram/types/base/input-store-payment-stars-gift/), [`inputStorePaymentStarsGiveaway`](/reference/telegram/types/base/input-store-payment-stars-giveaway/), [`inputStorePaymentStarsTopup`](/reference/telegram/types/base/input-store-payment-stars-topup/)
- Accepted by: [`payments.assignAppStoreTransaction`](/reference/telegram/functions/payments/assign-app-store-transaction/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.canPurchaseStore`](/reference/telegram/functions/payments/can-purchase-store/), [`payments.launchPrepaidGiveaway`](/reference/telegram/functions/payments/launch-prepaid-giveaway/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
