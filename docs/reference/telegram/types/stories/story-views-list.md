---
title: "stories.storyViewsList"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stories.storyViewsList"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stories"
layer: 228
schema_source: "tdlib"
constructor_id: "0x59d78fc5"
---

# `stories.storyViewsList`

No description provided by the pinned schema.

## Signature

```tl
stories.storyViewsList#59d78fc5 flags:# count:int views_count:int forwards_count:int reactions_count:int views:Vector<StoryView> chats:Vector<Chat> users:Vector<User> next_offset:flags.0?string = stories.StoryViewsList;
```

## Result type

`stories.StoryViewsList`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| views_count | int | — | — | No description provided by the pinned schema. |
| forwards_count | int | — | — | No description provided by the pinned schema. |
| reactions_count | int | — | — | No description provided by the pinned schema. |
| views | Vector<StoryView> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StoriesStoryViewsList
```

Public access: `miniproto.raw.types.StoriesStoryViewsList`.

## Safe usage shape

```python
from miniproto.raw.types import StoriesStoryViewsList

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoriesStoryViewsList
```

## Result family

[`stories.StoryViewsList`](/reference/telegram/types/results/stories-story-views-list/)

## Relationships

- Result family: [`stories.StoryViewsList`](/reference/telegram/types/results/stories-story-views-list/)
- Returned by: [`stories.getStoryViewsList`](/reference/telegram/functions/stories/get-story-views-list/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
