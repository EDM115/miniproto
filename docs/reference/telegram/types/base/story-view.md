---
title: "storyView"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "storyView"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb0bdeac5"
---

# `storyView`

No description provided by the pinned schema.

## Signature

```tl
storyView#b0bdeac5 flags:# blocked:flags.0?true blocked_my_stories_from:flags.1?true user_id:long date:int reaction:flags.2?Reaction = StoryView;
```

## Result type

`StoryView`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| blocked | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| blocked_my_stories_from | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| reaction | flags.2?Reaction | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| blocked | 0 | Controlled by `flags`; present when this bit is set. |
| blocked_my_stories_from | 1 | Controlled by `flags`; present when this bit is set. |
| reaction | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StoryView
```

Public access: `miniproto.raw.types.StoryView`.

## Safe usage shape

```python
from miniproto.raw.types import StoryView

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoryView
```

## Result family

[`StoryView`](/reference/telegram/types/results/story-view/)

## Relationships

- Result family: [`StoryView`](/reference/telegram/types/results/story-view/)
- Related constructors: [`storyViewPublicForward`](/reference/telegram/types/base/story-view-public-forward/), [`storyViewPublicRepost`](/reference/telegram/types/base/story-view-public-repost/)
- Accepted by: [`stories.storyViewsList`](/reference/telegram/types/stories/story-views-list/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
