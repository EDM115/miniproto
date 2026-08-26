---
title: "stats.messageStats"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stats.messageStats"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stats"
schema_source: "tdlib"
constructor_id: "0x7fe91c14"
---

# `stats.messageStats`

No description provided by the pinned schema.

## Signature

```tl
stats.messageStats#7fe91c14 views_graph:StatsGraph reactions_by_emotion_graph:StatsGraph = stats.MessageStats;
```

## Result type

`stats.MessageStats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| views_graph | StatsGraph | — | — | No description provided by the pinned schema. |
| reactions_by_emotion_graph | StatsGraph | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StatsMessageStats
```

Public access: `miniproto.raw.types.StatsMessageStats`.

## Safe usage shape

```python
from miniproto.raw.types import StatsMessageStats

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StatsMessageStats
```

## Result family

[`stats.MessageStats`](/reference/telegram/types/results/stats-message-stats/)

## Relationships

- Result family: [`stats.MessageStats`](/reference/telegram/types/results/stats-message-stats/)
- Returned by: [`stats.getMessageStats`](/reference/telegram/functions/stats/get-message-stats/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
