---
title: "payments.validatedRequestedInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.validatedRequestedInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xd1451883"
---

# `payments.validatedRequestedInfo`

No description provided by the pinned schema.

## Signature

```tl
payments.validatedRequestedInfo#d1451883 flags:# id:flags.0?string shipping_options:flags.1?Vector<ShippingOption> = payments.ValidatedRequestedInfo;
```

## Result type

`payments.ValidatedRequestedInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| id | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| shipping_options | flags.1?Vector<ShippingOption> | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| id | 0 | Controlled by `flags`; present when this bit is set. |
| shipping_options | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsValidatedRequestedInfo
```

Public access: `miniproto.raw.types.PaymentsValidatedRequestedInfo`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsValidatedRequestedInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsValidatedRequestedInfo
```

## Result family

[`payments.ValidatedRequestedInfo`](/reference/telegram/types/results/payments-validated-requested-info/)

## Relationships

- Result family: [`payments.ValidatedRequestedInfo`](/reference/telegram/types/results/payments-validated-requested-info/)
- Returned by: [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
