---
title: "payments.savedInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.savedInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfb8fe43c"
---

# `payments.savedInfo`

No description provided by the pinned schema.

## Signature

```tl
payments.savedInfo#fb8fe43c flags:# has_saved_credentials:flags.1?true saved_info:flags.0?PaymentRequestedInfo = payments.SavedInfo;
```

## Result type

`payments.SavedInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_saved_credentials | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| saved_info | flags.0?PaymentRequestedInfo | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_saved_credentials | 1 | Controlled by `flags`; present when this bit is set. |
| saved_info | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsSavedInfo
```

Public access: `miniproto.raw.types.PaymentsSavedInfo`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsSavedInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsSavedInfo
```

## Result family

[`payments.SavedInfo`](/reference/telegram/types/results/payments-saved-info/)

## Relationships

- Result family: [`payments.SavedInfo`](/reference/telegram/types/results/payments-saved-info/)
- Returned by: [`payments.getSavedInfo`](/reference/telegram/functions/payments/get-saved-info/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
