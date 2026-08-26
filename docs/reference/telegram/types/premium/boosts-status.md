---
title: "premium.boostsStatus"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "premium.boostsStatus"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "premium"
schema_source: "tdlib"
constructor_id: "0x4959427a"
---

# `premium.boostsStatus`

No description provided by the pinned schema.

## Signature

```tl
premium.boostsStatus#4959427a flags:# my_boost:flags.2?true level:int current_level_boosts:int boosts:int gift_boosts:flags.4?int next_level_boosts:flags.0?int premium_audience:flags.1?StatsPercentValue boost_url:string prepaid_giveaways:flags.3?Vector<PrepaidGiveaway> my_boost_slots:flags.2?Vector<int> = premium.BoostsStatus;
```

## Result type

`premium.BoostsStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| my_boost | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| level | int | — | — | No description provided by the pinned schema. |
| current_level_boosts | int | — | — | No description provided by the pinned schema. |
| boosts | int | — | — | No description provided by the pinned schema. |
| gift_boosts | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| next_level_boosts | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| premium_audience | flags.1?StatsPercentValue | flags.1 | — | No description provided by the pinned schema. |
| boost_url | string | — | — | No description provided by the pinned schema. |
| prepaid_giveaways | flags.3?Vector<PrepaidGiveaway> | flags.3 | — | No description provided by the pinned schema. |
| my_boost_slots | flags.2?Vector<int> | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| my_boost | 2 | Controlled by `flags`; present when this bit is set. |
| gift_boosts | 4 | Controlled by `flags`; present when this bit is set. |
| next_level_boosts | 0 | Controlled by `flags`; present when this bit is set. |
| premium_audience | 1 | Controlled by `flags`; present when this bit is set. |
| prepaid_giveaways | 3 | Controlled by `flags`; present when this bit is set. |
| my_boost_slots | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PremiumBoostsStatus
```

Public access: `miniproto.raw.types.PremiumBoostsStatus`.

## Safe usage shape

```python
from miniproto.raw.types import PremiumBoostsStatus

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PremiumBoostsStatus
```

## Result family

[`premium.BoostsStatus`](/reference/telegram/types/results/premium-boosts-status/)

## Relationships

- Result family: [`premium.BoostsStatus`](/reference/telegram/types/results/premium-boosts-status/)
- Returned by: [`premium.getBoostsStatus`](/reference/telegram/functions/premium/get-boosts-status/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
