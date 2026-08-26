---
title: "payments.paymentFormStars"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.paymentFormStars"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x7bf6b15c"
---

# `payments.paymentFormStars`

No description provided by the pinned schema.

## Signature

```tl
payments.paymentFormStars#7bf6b15c flags:# form_id:long bot_id:long title:string description:string photo:flags.5?WebDocument invoice:Invoice users:Vector<User> = payments.PaymentForm;
```

## Result type

`payments.PaymentForm`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| form_id | long | — | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| description | string | — | — | No description provided by the pinned schema. |
| photo | flags.5?WebDocument | flags.5 | — | No description provided by the pinned schema. |
| invoice | Invoice | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| photo | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsPaymentFormStars
```

Public access: `miniproto.raw.types.PaymentsPaymentFormStars`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsPaymentFormStars

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsPaymentFormStars
```

## Result family

[`payments.PaymentForm`](/reference/telegram/types/results/payments-payment-form/)

## Relationships

- Result family: [`payments.PaymentForm`](/reference/telegram/types/results/payments-payment-form/)
- Related constructors: [`payments.paymentForm`](/reference/telegram/types/payments/payment-form/), [`payments.paymentFormStarGift`](/reference/telegram/types/payments/payment-form-star-gift/)
- Returned by: [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
