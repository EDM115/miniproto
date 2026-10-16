---
title: "payments.starGiftWithdrawalUrl"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.starGiftWithdrawalUrl"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x84aa3a9c"
---

# `payments.starGiftWithdrawalUrl`

No description provided by the pinned schema.

## Signature

```tl
payments.starGiftWithdrawalUrl#84aa3a9c url:string = payments.StarGiftWithdrawalUrl;
```

## Result type

`payments.StarGiftWithdrawalUrl`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentsStarGiftWithdrawalUrl
```

Public access: `miniproto.raw.types.PaymentsStarGiftWithdrawalUrl`.

## Class reference

```python
from miniproto.raw.types import PaymentsStarGiftWithdrawalUrl

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = PaymentsStarGiftWithdrawalUrl
```

## Result family

[`payments.StarGiftWithdrawalUrl`](/reference/telegram/types/results/payments-star-gift-withdrawal-url/)

## Relationships

- Result family: [`payments.StarGiftWithdrawalUrl`](/reference/telegram/types/results/payments-star-gift-withdrawal-url/)
- Returned by: [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
