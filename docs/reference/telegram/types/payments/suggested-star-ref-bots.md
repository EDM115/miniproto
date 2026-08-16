---
title: "payments.suggestedStarRefBots"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.suggestedStarRefBots"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb4d5d859"
---

# `payments.suggestedStarRefBots`

No description provided by the pinned schema.

## Signature

```tl
payments.suggestedStarRefBots#b4d5d859 flags:# count:int suggested_bots:Vector<StarRefProgram> users:Vector<User> next_offset:flags.0?string = payments.SuggestedStarRefBots;
```

## Result type

`payments.SuggestedStarRefBots`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| suggested_bots | Vector<StarRefProgram> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsSuggestedStarRefBots
```

Public access: `miniproto.raw.types.PaymentsSuggestedStarRefBots`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsSuggestedStarRefBots

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsSuggestedStarRefBots
```

## Result family

[`payments.SuggestedStarRefBots`](/reference/telegram/types/results/payments-suggested-star-ref-bots/)

## Relationships

- Result family: [`payments.SuggestedStarRefBots`](/reference/telegram/types/results/payments-suggested-star-ref-bots/)
- Returned by: [`payments.getSuggestedStarRefBots`](/reference/telegram/functions/payments/get-suggested-star-ref-bots/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
