---
title: "starRefProgram"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starRefProgram"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xdd0c66f2"
---

# `starRefProgram`

No description provided by the pinned schema.

## Signature

```tl
starRefProgram#dd0c66f2 flags:# bot_id:long commission_permille:int duration_months:flags.0?int end_date:flags.1?int daily_revenue_per_user:flags.2?StarsAmount = StarRefProgram;
```

## Result type

`StarRefProgram`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| commission_permille | int | — | — | No description provided by the pinned schema. |
| duration_months | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| end_date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| daily_revenue_per_user | flags.2?StarsAmount | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| duration_months | 0 | Controlled by `flags`; present when this bit is set. |
| end_date | 1 | Controlled by `flags`; present when this bit is set. |
| daily_revenue_per_user | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarRefProgram
```

Public access: `miniproto.raw.types.StarRefProgram`.

## Safe usage shape

```python
from miniproto.raw.types import StarRefProgram

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarRefProgram
```

## Result family

[`StarRefProgram`](/reference/telegram/types/results/star-ref-program/)

## Relationships

- Result family: [`StarRefProgram`](/reference/telegram/types/results/star-ref-program/)
- Accepted by: [`payments.suggestedStarRefBots`](/reference/telegram/types/payments/suggested-star-ref-bots/), [`userFull`](/reference/telegram/types/base/user-full/)
- Returned by: [`bots.updateStarRefProgram`](/reference/telegram/functions/bots/update-star-ref-program/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
