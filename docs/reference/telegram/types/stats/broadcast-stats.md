---
title: "stats.broadcastStats"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stats.broadcastStats"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stats"
schema_source: "tdlib"
constructor_id: "0x396ca5fc"
---

# `stats.broadcastStats`

No description provided by the pinned schema.

## Signature

```tl
stats.broadcastStats#396ca5fc period:StatsDateRangeDays followers:StatsAbsValueAndPrev views_per_post:StatsAbsValueAndPrev shares_per_post:StatsAbsValueAndPrev reactions_per_post:StatsAbsValueAndPrev views_per_story:StatsAbsValueAndPrev shares_per_story:StatsAbsValueAndPrev reactions_per_story:StatsAbsValueAndPrev enabled_notifications:StatsPercentValue growth_graph:StatsGraph followers_graph:StatsGraph mute_graph:StatsGraph top_hours_graph:StatsGraph interactions_graph:StatsGraph iv_interactions_graph:StatsGraph views_by_source_graph:StatsGraph new_followers_by_source_graph:StatsGraph languages_graph:StatsGraph reactions_by_emotion_graph:StatsGraph story_interactions_graph:StatsGraph story_reactions_by_emotion_graph:StatsGraph recent_posts_interactions:Vector<PostInteractionCounters> = stats.BroadcastStats;
```

## Result type

`stats.BroadcastStats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| period | StatsDateRangeDays | — | — | No description provided by the pinned schema. |
| followers | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| views_per_post | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| shares_per_post | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| reactions_per_post | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| views_per_story | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| shares_per_story | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| reactions_per_story | StatsAbsValueAndPrev | — | — | No description provided by the pinned schema. |
| enabled_notifications | StatsPercentValue | — | — | No description provided by the pinned schema. |
| growth_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| followers_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| mute_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| top_hours_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| interactions_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| iv_interactions_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| views_by_source_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| new_followers_by_source_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| languages_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| reactions_by_emotion_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| story_interactions_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| story_reactions_by_emotion_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| recent_posts_interactions | Vector<PostInteractionCounters> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StatsBroadcastStats
```

Public access: `miniproto.raw.types.StatsBroadcastStats`.

## Safe usage shape

```python
from miniproto.raw.types import StatsBroadcastStats

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StatsBroadcastStats
```

## Result family

[`stats.BroadcastStats`](/reference/telegram/types/results/stats-broadcast-stats/)

## Relationships

- Result family: [`stats.BroadcastStats`](/reference/telegram/types/results/stats-broadcast-stats/)
- Returned by: [`stats.getBroadcastStats`](/reference/telegram/functions/stats/get-broadcast-stats/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
