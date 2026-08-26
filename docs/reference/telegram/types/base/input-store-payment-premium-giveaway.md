---
title: "inputStorePaymentPremiumGiveaway"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputStorePaymentPremiumGiveaway"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x160544ca"
---

# `inputStorePaymentPremiumGiveaway`

No description provided by the pinned schema.

## Signature

```tl
inputStorePaymentPremiumGiveaway#160544ca flags:# only_new_subscribers:flags.0?true winners_are_visible:flags.3?true boost_peer:InputPeer additional_peers:flags.1?Vector<InputPeer> countries_iso2:flags.2?Vector<string> prize_description:flags.4?string random_id:long until_date:int currency:string amount:long = InputStorePaymentPurpose;
```

## Result type

`InputStorePaymentPurpose`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| only_new_subscribers | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| winners_are_visible | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| boost_peer | InputPeer | — | — | No description provided by the pinned schema. |
| additional_peers | flags.1?Vector<InputPeer> | flags.1 | — | No description provided by the pinned schema. |
| countries_iso2 | flags.2?Vector<string> | flags.2 | — | No description provided by the pinned schema. |
| prize_description | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| random_id | long | — | — | No description provided by the pinned schema. |
| until_date | int | — | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| only_new_subscribers | 0 | Controlled by `flags`; present when this bit is set. |
| winners_are_visible | 3 | Controlled by `flags`; present when this bit is set. |
| additional_peers | 1 | Controlled by `flags`; present when this bit is set. |
| countries_iso2 | 2 | Controlled by `flags`; present when this bit is set. |
| prize_description | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputStorePaymentPremiumGiveaway
```

Public access: `miniproto.raw.types.InputStorePaymentPremiumGiveaway`.

## Safe usage shape

```python
from miniproto.raw.types import InputStorePaymentPremiumGiveaway

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputStorePaymentPremiumGiveaway
```

## Result family

[`InputStorePaymentPurpose`](/reference/telegram/types/results/input-store-payment-purpose/)

## Relationships

- Result family: [`InputStorePaymentPurpose`](/reference/telegram/types/results/input-store-payment-purpose/)
- Related constructors: [`inputStorePaymentAuthCode`](/reference/telegram/types/base/input-store-payment-auth-code/), [`inputStorePaymentGiftPremium`](/reference/telegram/types/base/input-store-payment-gift-premium/), [`inputStorePaymentPremiumGiftCode`](/reference/telegram/types/base/input-store-payment-premium-gift-code/), [`inputStorePaymentPremiumSubscription`](/reference/telegram/types/base/input-store-payment-premium-subscription/), [`inputStorePaymentStarsGift`](/reference/telegram/types/base/input-store-payment-stars-gift/), [`inputStorePaymentStarsGiveaway`](/reference/telegram/types/base/input-store-payment-stars-giveaway/), [`inputStorePaymentStarsTopup`](/reference/telegram/types/base/input-store-payment-stars-topup/)
- Accepted by: [`payments.assignAppStoreTransaction`](/reference/telegram/functions/payments/assign-app-store-transaction/), [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/), [`payments.canPurchaseStore`](/reference/telegram/functions/payments/can-purchase-store/), [`payments.launchPrepaidGiveaway`](/reference/telegram/functions/payments/launch-prepaid-giveaway/), [`inputInvoicePremiumAuthCode`](/reference/telegram/types/base/input-invoice-premium-auth-code/), [`inputInvoicePremiumGiftCode`](/reference/telegram/types/base/input-invoice-premium-gift-code/), [`inputInvoiceStars`](/reference/telegram/types/base/input-invoice-stars/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
