---
title: "payments.currencyRates"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.currencyRates"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xbbcce4c2"
---

# `payments.currencyRates`

No description provided by the pinned schema.

## Signature

```tl
payments.currencyRates#bbcce4c2 rates:Vector<CurrencyRate> = payments.CurrencyRates;
```

## Result type

`payments.CurrencyRates`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| rates | Vector<CurrencyRate> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentsCurrencyRates
```

Public access: `miniproto.raw.types.PaymentsCurrencyRates`.

## Class reference

```python
from miniproto.raw.types import PaymentsCurrencyRates

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = PaymentsCurrencyRates
```

## Result family

[`payments.CurrencyRates`](/reference/telegram/types/results/payments-currency-rates/)

## Relationships

- Result family: [`payments.CurrencyRates`](/reference/telegram/types/results/payments-currency-rates/)
- Returned by: [`payments.getCurrencyRates`](/reference/telegram/functions/payments/get-currency-rates/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
