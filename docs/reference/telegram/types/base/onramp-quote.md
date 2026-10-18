---
title: "onrampQuote"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "onrampQuote"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x7a8011e9"
---

# `onrampQuote`

No description provided by the pinned schema.

## Signature

```tl
onrampQuote#7a8011e9 base_currency:string base_amount:string crypto_currency:string crypto_amount:string crypto_price:string fee_amount:string extra_fee_amount:string network_fee_amount:string total_amount:string payment_method:string expires_date:int = OnrampQuote;
```

## Result type

`OnrampQuote`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| base_currency | string | — | — | No description provided by the pinned schema. |
| base_amount | string | — | — | No description provided by the pinned schema. |
| crypto_currency | string | — | — | No description provided by the pinned schema. |
| crypto_amount | string | — | — | No description provided by the pinned schema. |
| crypto_price | string | — | — | No description provided by the pinned schema. |
| fee_amount | string | — | — | No description provided by the pinned schema. |
| extra_fee_amount | string | — | — | No description provided by the pinned schema. |
| network_fee_amount | string | — | — | No description provided by the pinned schema. |
| total_amount | string | — | — | No description provided by the pinned schema. |
| payment_method | string | — | — | No description provided by the pinned schema. |
| expires_date | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import OnrampQuote
```

Public access: `miniproto.raw.types.OnrampQuote`.

## Class reference

```python
from miniproto.raw.types import OnrampQuote

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = OnrampQuote
```

## Result family

[`OnrampQuote`](/reference/telegram/types/results/onramp-quote/)

## Relationships

- Result family: [`OnrampQuote`](/reference/telegram/types/results/onramp-quote/)
- Returned by: [`payments.getOnrampQuote`](/reference/telegram/functions/payments/get-onramp-quote/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
