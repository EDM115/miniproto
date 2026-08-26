---
title: "stats.megagroupStats"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stats.megagroupStats"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stats"
schema_source: "tdlib"
constructor_id: "0xef7ff916"
---

# `stats.megagroupStats`

No description provided by the pinned schema.

## Signature

```tl
stats.megagroupStats#ef7ff916 period:StatsDateRangeDays members:StatsAbsValueAndPrev messages:StatsAbsValueAndPrev viewers:StatsAbsValueAndPrev posters:StatsAbsValueAndPrev growth_graph:StatsGraph members_graph:StatsGraph new_members_by_source_graph:StatsGraph languages_graph:StatsGraph messages_graph:StatsGraph actions_graph:StatsGraph top_hours_graph:StatsGraph weekdays_graph:StatsGraph top_posters:Vector<StatsGroupTopPoster> top_admins:Vector<StatsGroupTopAdmin> top_inviters:Vector<StatsGroupTopInviter> users:Vector<User> = stats.MegagroupStats;
```

## Result type

`stats.MegagroupStats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| period | StatsDateRangeDays | — | — | No description provided by the pinned schema. |
| members | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| messages | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| viewers | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| posters | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| growth_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| members_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| new_members_by_source_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| languages_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| messages_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| actions_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| top_hours_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| weekdays_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| top_posters | Vector<StatsGroupTopPoster> | — | — | No description provided by the pinned schema. |
| top_admins | Vector<StatsGroupTopAdmin> | — | — | No description provided by the pinned schema. |
| top_inviters | Vector<StatsGroupTopInviter> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StatsMegagroupStats
```

Public access: `miniproto.raw.types.StatsMegagroupStats`.

## Safe usage shape

```python
from miniproto.raw.types import StatsMegagroupStats

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StatsMegagroupStats
```

## Result family

[`stats.MegagroupStats`](/reference/telegram/types/results/stats-megagroup-stats/)

## Relationships

- Result family: [`stats.MegagroupStats`](/reference/telegram/types/results/stats-megagroup-stats/)
- Returned by: [`stats.getMegagroupStats`](/reference/telegram/functions/stats/get-megagroup-stats/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
