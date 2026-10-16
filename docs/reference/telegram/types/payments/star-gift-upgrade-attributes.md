---
title: "payments.starGiftUpgradeAttributes"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.starGiftUpgradeAttributes"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x46c6e36f"
---

# `payments.starGiftUpgradeAttributes`

No description provided by the pinned schema.

## Signature

```tl
payments.starGiftUpgradeAttributes#46c6e36f attributes:Vector<StarGiftAttribute> = payments.StarGiftUpgradeAttributes;
```

## Result type

`payments.StarGiftUpgradeAttributes`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| attributes | Vector<StarGiftAttribute> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentsStarGiftUpgradeAttributes
```

Public access: `miniproto.raw.types.PaymentsStarGiftUpgradeAttributes`.

## Class reference

```python
from miniproto.raw.types import PaymentsStarGiftUpgradeAttributes

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = PaymentsStarGiftUpgradeAttributes
```

## Result family

[`payments.StarGiftUpgradeAttributes`](/reference/telegram/types/results/payments-star-gift-upgrade-attributes/)

## Relationships

- Result family: [`payments.StarGiftUpgradeAttributes`](/reference/telegram/types/results/payments-star-gift-upgrade-attributes/)
- Returned by: [`payments.getStarGiftUpgradeAttributes`](/reference/telegram/functions/payments/get-star-gift-upgrade-attributes/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
