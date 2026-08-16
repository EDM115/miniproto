---
title: "payments.starsRevenueStats"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.starsRevenueStats"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0x6c207376"
---

# `payments.starsRevenueStats`

No description provided by the pinned schema.

## Signature

```tl
payments.starsRevenueStats#6c207376 flags:# top_hours_graph:flags.0?StatsGraph revenue_graph:StatsGraph status:StarsRevenueStatus usd_rate:double = payments.StarsRevenueStats;
```

## Result type

`payments.StarsRevenueStats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| top_hours_graph | flags.0?StatsGraph | flags.0 | — | No description provided by the pinned schema. |
| revenue_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| status | StarsRevenueStatus | — | — | No description provided by the pinned schema. |
| usd_rate | double | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| top_hours_graph | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsStarsRevenueStats
```

Public access: `miniproto.raw.types.PaymentsStarsRevenueStats`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsStarsRevenueStats

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsStarsRevenueStats
```

## Result family

[`payments.StarsRevenueStats`](/reference/telegram/types/results/payments-stars-revenue-stats/)

## Relationships

- Result family: [`payments.StarsRevenueStats`](/reference/telegram/types/results/payments-stars-revenue-stats/)
- Returned by: [`payments.getStarsRevenueStats`](/reference/telegram/functions/payments/get-stars-revenue-stats/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
