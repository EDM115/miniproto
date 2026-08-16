---
title: "paymentCharge"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "paymentCharge"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xea02c27e"
---

# `paymentCharge`

No description provided by the pinned schema.

## Signature

```tl
paymentCharge#ea02c27e id:string provider_charge_id:string = PaymentCharge;
```

## Result type

`PaymentCharge`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | string | — | — | No description provided by the pinned schema. |
| provider_charge_id | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentCharge
```

Public access: `miniproto.raw.types.PaymentCharge`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentCharge

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentCharge
```

## Result family

[`PaymentCharge`](/reference/telegram/types/results/payment-charge/)

## Relationships

- Result family: [`PaymentCharge`](/reference/telegram/types/results/payment-charge/)
- Accepted by: [`messageActionPaymentRefunded`](/reference/telegram/types/base/message-action-payment-refunded/), [`messageActionPaymentSentMe`](/reference/telegram/types/base/message-action-payment-sent-me/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
