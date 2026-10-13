---
title: "payments.getCurrencyRates"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.getCurrencyRates"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xd35983e8"
---

# `payments.getCurrencyRates`

No description provided by the pinned schema.

## Signature

```tl
payments.getCurrencyRates#d35983e8 = payments.CurrencyRates;
```

## Result type

`payments.CurrencyRates`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.functions import PaymentsGetCurrencyRates
```

Public access: `miniproto.raw.functions.PaymentsGetCurrencyRates`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsGetCurrencyRates

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsGetCurrencyRates
```

## Result family

[`payments.CurrencyRates`](/reference/telegram/types/results/payments-currency-rates/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`payments.CurrencyRates`](/reference/telegram/types/results/payments-currency-rates/)
Known selected constructors: [`payments.currencyRates`](/reference/telegram/types/payments/currency-rates/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
