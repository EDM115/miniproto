---
title: "invoice"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "invoice"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x049ee584"
---

# `invoice`

No description provided by the pinned schema.

## Signature

```tl
invoice#049ee584 flags:# test:flags.0?true name_requested:flags.1?true phone_requested:flags.2?true email_requested:flags.3?true shipping_address_requested:flags.4?true flexible:flags.5?true phone_to_provider:flags.6?true email_to_provider:flags.7?true recurring:flags.9?true currency:string prices:Vector<LabeledPrice> max_tip_amount:flags.8?long suggested_tip_amounts:flags.8?Vector<long> terms_url:flags.10?string subscription_period:flags.11?int = Invoice;
```

## Result type

`Invoice`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| test | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| name_requested | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| phone_requested | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| email_requested | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| shipping_address_requested | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| flexible | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| phone_to_provider | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| email_to_provider | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| recurring | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| prices | Vector<LabeledPrice> | — | — | No description provided by the pinned schema. |
| max_tip_amount | flags.8?long | flags.8 | — | No description provided by the pinned schema. |
| suggested_tip_amounts | flags.8?Vector<long> | flags.8 | — | No description provided by the pinned schema. |
| terms_url | flags.10?string | flags.10 | — | No description provided by the pinned schema. |
| subscription_period | flags.11?int | flags.11 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| test | 0 | Controlled by `flags`; present when this bit is set. |
| name_requested | 1 | Controlled by `flags`; present when this bit is set. |
| phone_requested | 2 | Controlled by `flags`; present when this bit is set. |
| email_requested | 3 | Controlled by `flags`; present when this bit is set. |
| shipping_address_requested | 4 | Controlled by `flags`; present when this bit is set. |
| flexible | 5 | Controlled by `flags`; present when this bit is set. |
| phone_to_provider | 6 | Controlled by `flags`; present when this bit is set. |
| email_to_provider | 7 | Controlled by `flags`; present when this bit is set. |
| recurring | 9 | Controlled by `flags`; present when this bit is set. |
| max_tip_amount | 8 | Controlled by `flags`; present when this bit is set. |
| suggested_tip_amounts | 8 | Controlled by `flags`; present when this bit is set. |
| terms_url | 10 | Controlled by `flags`; present when this bit is set. |
| subscription_period | 11 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Invoice
```

Public access: `miniproto.raw.types.Invoice`.

## Safe usage shape

```python
from miniproto.raw.types import Invoice

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Invoice
```

## Result family

[`Invoice`](/reference/telegram/types/results/invoice/)

## Relationships

- Result family: [`Invoice`](/reference/telegram/types/results/invoice/)
- Accepted by: [`inputBotInlineMessageMediaInvoice`](/reference/telegram/types/base/input-bot-inline-message-media-invoice/), [`inputMediaInvoice`](/reference/telegram/types/base/input-media-invoice/), [`payments.paymentForm`](/reference/telegram/types/payments/payment-form/), [`payments.paymentFormStarGift`](/reference/telegram/types/payments/payment-form-star-gift/), [`payments.paymentFormStars`](/reference/telegram/types/payments/payment-form-stars/), [`payments.paymentReceipt`](/reference/telegram/types/payments/payment-receipt/), [`payments.paymentReceiptStars`](/reference/telegram/types/payments/payment-receipt-stars/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
