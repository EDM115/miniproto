---
title: "payments.paymentVerificationNeeded"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.paymentVerificationNeeded"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xd8411139"
---

# `payments.paymentVerificationNeeded`

No description provided by the pinned schema.

## Signature

```tl
payments.paymentVerificationNeeded#d8411139 url:string = payments.PaymentResult;
```

## Result type

`payments.PaymentResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentsPaymentVerificationNeeded
```

Public access: `miniproto.raw.types.PaymentsPaymentVerificationNeeded`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsPaymentVerificationNeeded

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsPaymentVerificationNeeded
```

## Result family

[`payments.PaymentResult`](/reference/telegram/types/results/payments-payment-result/)

## Relationships

- Result family: [`payments.PaymentResult`](/reference/telegram/types/results/payments-payment-result/)
- Related constructors: [`payments.paymentResult`](/reference/telegram/types/payments/payment-result/)
- Returned by: [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/), [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
