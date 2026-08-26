---
title: "shippingOption"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "shippingOption"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb6213cdf"
---

# `shippingOption`

No description provided by the pinned schema.

## Signature

```tl
shippingOption#b6213cdf id:string title:string prices:Vector<LabeledPrice> = ShippingOption;
```

## Result type

`ShippingOption`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | string | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| prices | Vector<LabeledPrice> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ShippingOption
```

Public access: `miniproto.raw.types.ShippingOption`.

## Safe usage shape

```python
from miniproto.raw.types import ShippingOption

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ShippingOption
```

## Result family

[`ShippingOption`](/reference/telegram/types/results/shipping-option/)

## Relationships

- Result family: [`ShippingOption`](/reference/telegram/types/results/shipping-option/)
- Accepted by: [`messages.setBotShippingResults`](/reference/telegram/functions/messages/set-bot-shipping-results/), [`payments.paymentReceipt`](/reference/telegram/types/payments/payment-receipt/), [`payments.validatedRequestedInfo`](/reference/telegram/types/payments/validated-requested-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
