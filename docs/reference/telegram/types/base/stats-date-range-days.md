---
title: "statsDateRangeDays"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "statsDateRangeDays"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb637edaf"
---

# `statsDateRangeDays`

No description provided by the pinned schema.

## Signature

```tl
statsDateRangeDays#b637edaf min_date:int max_date:int = StatsDateRangeDays;
```

## Result type

`StatsDateRangeDays`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| min_date | int | — | — | No description provided by the pinned schema. |
| max_date | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StatsDateRangeDays
```

Public access: `miniproto.raw.types.StatsDateRangeDays`.

## Class reference

```python
from miniproto.raw.types import StatsDateRangeDays

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = StatsDateRangeDays
```

## Result family

[`StatsDateRangeDays`](/reference/telegram/types/results/stats-date-range-days/)

## Relationships

- Result family: [`StatsDateRangeDays`](/reference/telegram/types/results/stats-date-range-days/)
- Accepted by: [`stats.broadcastStats`](/reference/telegram/types/stats/broadcast-stats/), [`stats.megagroupStats`](/reference/telegram/types/stats/megagroup-stats/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
