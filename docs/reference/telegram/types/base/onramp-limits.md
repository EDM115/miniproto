---
title: "onrampLimits"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "onrampLimits"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x7be2677e"
---

# `onrampLimits`

No description provided by the pinned schema.

## Signature

```tl
onrampLimits#7be2677e base_currency:string base_min_amount:string base_max_amount:string crypto_min_amount:string crypto_max_amount:string payment_method:string = OnrampLimits;
```

## Result type

`OnrampLimits`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| base_currency | string | — | — | No description provided by the pinned schema. |
| base_min_amount | string | — | — | No description provided by the pinned schema. |
| base_max_amount | string | — | — | No description provided by the pinned schema. |
| crypto_min_amount | string | — | — | No description provided by the pinned schema. |
| crypto_max_amount | string | — | — | No description provided by the pinned schema. |
| payment_method | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import OnrampLimits
```

Public access: `miniproto.raw.types.OnrampLimits`.

## Class reference

```python
from miniproto.raw.types import OnrampLimits

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = OnrampLimits
```

## Result family

[`OnrampLimits`](/reference/telegram/types/results/onramp-limits/)

## Relationships

- Result family: [`OnrampLimits`](/reference/telegram/types/results/onramp-limits/)
- Returned by: [`payments.getOnrampLimits`](/reference/telegram/functions/payments/get-onramp-limits/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
