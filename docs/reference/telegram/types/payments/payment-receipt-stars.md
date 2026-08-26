---
title: "payments.paymentReceiptStars"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.paymentReceiptStars"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xdabbf83a"
---

# `payments.paymentReceiptStars`

No description provided by the pinned schema.

## Signature

```tl
payments.paymentReceiptStars#dabbf83a flags:# date:int bot_id:long title:string description:string photo:flags.2?WebDocument invoice:Invoice currency:string total_amount:long transaction_id:string users:Vector<User> = payments.PaymentReceipt;
```

## Result type

`payments.PaymentReceipt`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| description | string | — | — | No description provided by the pinned schema. |
| photo | flags.2?WebDocument | flags.2 | — | No description provided by the pinned schema. |
| invoice | Invoice | — | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| total_amount | long | — | — | No description provided by the pinned schema. |
| transaction_id | string | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| photo | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsPaymentReceiptStars
```

Public access: `miniproto.raw.types.PaymentsPaymentReceiptStars`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsPaymentReceiptStars

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsPaymentReceiptStars
```

## Result family

[`payments.PaymentReceipt`](/reference/telegram/types/results/payments-payment-receipt/)

## Relationships

- Result family: [`payments.PaymentReceipt`](/reference/telegram/types/results/payments-payment-receipt/)
- Related constructors: [`payments.paymentReceipt`](/reference/telegram/types/payments/payment-receipt/)
- Returned by: [`payments.getPaymentReceipt`](/reference/telegram/functions/payments/get-payment-receipt/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
