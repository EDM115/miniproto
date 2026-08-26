---
title: "payments.paymentReceipt"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.paymentReceipt"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x70c4fe03"
---

# `payments.paymentReceipt`

No description provided by the pinned schema.

## Signature

```tl
payments.paymentReceipt#70c4fe03 flags:# date:int bot_id:long provider_id:long title:string description:string photo:flags.2?WebDocument invoice:Invoice info:flags.0?PaymentRequestedInfo shipping:flags.1?ShippingOption tip_amount:flags.3?long currency:string total_amount:long credentials_title:string users:Vector<User> = payments.PaymentReceipt;
```

## Result type

`payments.PaymentReceipt`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| provider_id | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| description | string | — | — | No description provided by the pinned schema. |
| photo | flags.2?WebDocument | flags.2 | — | No description provided by the pinned schema. |
| invoice | Invoice | — | — | No description provided by the pinned schema. |
| info | flags.0?PaymentRequestedInfo | flags.0 | — | No description provided by the pinned schema. |
| shipping | flags.1?ShippingOption | flags.1 | — | No description provided by the pinned schema. |
| tip_amount | flags.3?long | flags.3 | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| total_amount | long | — | — | No description provided by the pinned schema. |
| credentials_title | string | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| photo | 2 | Controlled by `flags`; present when this bit is set. |
| info | 0 | Controlled by `flags`; present when this bit is set. |
| shipping | 1 | Controlled by `flags`; present when this bit is set. |
| tip_amount | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsPaymentReceipt
```

Public access: `miniproto.raw.types.PaymentsPaymentReceipt`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsPaymentReceipt

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsPaymentReceipt
```

## Result family

[`payments.PaymentReceipt`](/reference/telegram/types/results/payments-payment-receipt/)

## Relationships

- Result family: [`payments.PaymentReceipt`](/reference/telegram/types/results/payments-payment-receipt/)
- Related constructors: [`payments.paymentReceiptStars`](/reference/telegram/types/payments/payment-receipt-stars/)
- Returned by: [`payments.getPaymentReceipt`](/reference/telegram/functions/payments/get-payment-receipt/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
