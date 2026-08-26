---
title: "storyViews"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "storyViews"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x8d595cd6"
---

# `storyViews`

No description provided by the pinned schema.

## Signature

```tl
storyViews#8d595cd6 flags:# has_viewers:flags.1?true views_count:int forwards_count:flags.2?int reactions:flags.3?Vector<ReactionCount> reactions_count:flags.4?int recent_viewers:flags.0?Vector<long> = StoryViews;
```

## Result type

`StoryViews`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_viewers | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| views_count | int | — | — | No description provided by the pinned schema. |
| forwards_count | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| reactions | flags.3?Vector<ReactionCount> | flags.3 | — | No description provided by the pinned schema. |
| reactions_count | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| recent_viewers | flags.0?Vector<long> | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_viewers | 1 | Controlled by `flags`; present when this bit is set. |
| forwards_count | 2 | Controlled by `flags`; present when this bit is set. |
| reactions | 3 | Controlled by `flags`; present when this bit is set. |
| reactions_count | 4 | Controlled by `flags`; present when this bit is set. |
| recent_viewers | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StoryViews
```

Public access: `miniproto.raw.types.StoryViews`.

## Safe usage shape

```python
from miniproto.raw.types import StoryViews

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoryViews
```

## Result family

[`StoryViews`](/reference/telegram/types/results/story-views/)

## Relationships

- Result family: [`StoryViews`](/reference/telegram/types/results/story-views/)
- Accepted by: [`stories.storyViews`](/reference/telegram/types/stories/story-views/), [`storyItem`](/reference/telegram/types/base/story-item/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
