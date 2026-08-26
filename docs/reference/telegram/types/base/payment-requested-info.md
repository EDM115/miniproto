---
title: "paymentRequestedInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "paymentRequestedInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x909c3f94"
---

# `paymentRequestedInfo`

No description provided by the pinned schema.

## Signature

```tl
paymentRequestedInfo#909c3f94 flags:# name:flags.0?string phone:flags.1?string email:flags.2?string shipping_address:flags.3?PostAddress = PaymentRequestedInfo;
```

## Result type

`PaymentRequestedInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| name | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| phone | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| email | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| shipping_address | flags.3?PostAddress | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| name | 0 | Controlled by `flags`; present when this bit is set. |
| phone | 1 | Controlled by `flags`; present when this bit is set. |
| email | 2 | Controlled by `flags`; present when this bit is set. |
| shipping_address | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentRequestedInfo
```

Public access: `miniproto.raw.types.PaymentRequestedInfo`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentRequestedInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentRequestedInfo
```

## Result family

[`PaymentRequestedInfo`](/reference/telegram/types/results/payment-requested-info/)

## Relationships

- Result family: [`PaymentRequestedInfo`](/reference/telegram/types/results/payment-requested-info/)
- Accepted by: [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/), [`messageActionPaymentSentMe`](/reference/telegram/types/base/message-action-payment-sent-me/), [`payments.paymentForm`](/reference/telegram/types/payments/payment-form/), [`payments.paymentReceipt`](/reference/telegram/types/payments/payment-receipt/), [`payments.savedInfo`](/reference/telegram/types/payments/saved-info/), [`updateBotPrecheckoutQuery`](/reference/telegram/types/base/update-bot-precheckout-query/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
