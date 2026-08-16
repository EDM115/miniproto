---
title: "payments.paymentForm"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.paymentForm"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0xa0058751"
---

# `payments.paymentForm`

No description provided by the pinned schema.

## Signature

```tl
payments.paymentForm#a0058751 flags:# can_save_credentials:flags.2?true password_missing:flags.3?true form_id:long bot_id:long title:string description:string photo:flags.5?WebDocument invoice:Invoice provider_id:long url:string native_provider:flags.4?string native_params:flags.4?DataJSON additional_methods:flags.6?Vector<PaymentFormMethod> saved_info:flags.0?PaymentRequestedInfo saved_credentials:flags.1?Vector<PaymentSavedCredentials> users:Vector<User> = payments.PaymentForm;
```

## Result type

`payments.PaymentForm`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| can_save_credentials | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| password_missing | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| form_id | long | — | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| description | string | — | — | No description provided by the pinned schema. |
| photo | flags.5?WebDocument | flags.5 | — | No description provided by the pinned schema. |
| invoice | Invoice | — | — | No description provided by the pinned schema. |
| provider_id | long | — | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| native_provider | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| native_params | flags.4?DataJSON | flags.4 | — | No description provided by the pinned schema. |
| additional_methods | flags.6?Vector<PaymentFormMethod> | flags.6 | — | No description provided by the pinned schema. |
| saved_info | flags.0?PaymentRequestedInfo | flags.0 | — | No description provided by the pinned schema. |
| saved_credentials | flags.1?Vector<PaymentSavedCredentials> | flags.1 | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| can_save_credentials | 2 | Controlled by `flags`; present when this bit is set. |
| password_missing | 3 | Controlled by `flags`; present when this bit is set. |
| photo | 5 | Controlled by `flags`; present when this bit is set. |
| native_provider | 4 | Controlled by `flags`; present when this bit is set. |
| native_params | 4 | Controlled by `flags`; present when this bit is set. |
| additional_methods | 6 | Controlled by `flags`; present when this bit is set. |
| saved_info | 0 | Controlled by `flags`; present when this bit is set. |
| saved_credentials | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsPaymentForm
```

Public access: `miniproto.raw.types.PaymentsPaymentForm`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsPaymentForm

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsPaymentForm
```

## Result family

[`payments.PaymentForm`](/reference/telegram/types/results/payments-payment-form/)

## Relationships

- Result family: [`payments.PaymentForm`](/reference/telegram/types/results/payments-payment-form/)
- Related constructors: [`payments.paymentFormStarGift`](/reference/telegram/types/payments/payment-form-star-gift/), [`payments.paymentFormStars`](/reference/telegram/types/payments/payment-form-stars/)
- Returned by: [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
