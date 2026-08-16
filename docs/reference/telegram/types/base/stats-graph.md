---
title: "statsGraph"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "statsGraph"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x8ea464b6"
---

# `statsGraph`

No description provided by the pinned schema.

## Signature

```tl
statsGraph#8ea464b6 flags:# json:DataJSON zoom_token:flags.0?string = StatsGraph;
```

## Result type

`StatsGraph`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| json | DataJSON | — | — | No description provided by the pinned schema. |
| zoom_token | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| zoom_token | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StatsGraph
```

Public access: `miniproto.raw.types.StatsGraph`.

## Safe usage shape

```python
from miniproto.raw.types import StatsGraph

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StatsGraph
```

## Result family

[`StatsGraph`](/reference/telegram/types/results/stats-graph/)

## Relationships

- Result family: [`StatsGraph`](/reference/telegram/types/results/stats-graph/)
- Related constructors: [`statsGraphAsync`](/reference/telegram/types/base/stats-graph-async/), [`statsGraphError`](/reference/telegram/types/base/stats-graph-error/)
- Accepted by: [`payments.starsRevenueStats`](/reference/telegram/types/payments/stars-revenue-stats/), [`stats.broadcastStats`](/reference/telegram/types/stats/broadcast-stats/), [`stats.megagroupStats`](/reference/telegram/types/stats/megagroup-stats/), [`stats.messageStats`](/reference/telegram/types/stats/message-stats/), [`stats.pollStats`](/reference/telegram/types/stats/poll-stats/), [`stats.storyStats`](/reference/telegram/types/stats/story-stats/)
- Returned by: [`stats.loadAsyncGraph`](/reference/telegram/functions/stats/load-async-graph/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
