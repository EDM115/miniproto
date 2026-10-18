---
title: "stats.storyStats"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stats.storyStats"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stats"
schema_source: "tdlib"
constructor_id: "0x50cd067c"
---

# `stats.storyStats`

No description provided by the pinned schema.

## Signature

```tl
stats.storyStats#50cd067c views_graph:StatsGraph reactions_by_emotion_graph:StatsGraph = stats.StoryStats;
```

## Result type

`stats.StoryStats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| views_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| reactions_by_emotion_graph | StatsGraph | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StatsStoryStats
```

Public access: `miniproto.raw.types.StatsStoryStats`.

## Class reference

```python
from miniproto.raw.types import StatsStoryStats

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = StatsStoryStats
```

## Result family

[`stats.StoryStats`](/reference/telegram/types/results/stats-story-stats/)

## Relationships

- Result family: [`stats.StoryStats`](/reference/telegram/types/results/stats-story-stats/)
- Returned by: [`stats.getStoryStats`](/reference/telegram/functions/stats/get-story-stats/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
