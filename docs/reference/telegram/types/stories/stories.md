---
title: "stories.stories"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stories.stories"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stories"
schema_source: "tdlib"
constructor_id: "0x63c3dd0a"
---

# `stories.stories`

No description provided by the pinned schema.

## Signature

```tl
stories.stories#63c3dd0a flags:# count:int stories:Vector<StoryItem> pinned_to_top:flags.0?Vector<int> chats:Vector<Chat> users:Vector<User> = stories.Stories;
```

## Result type

`stories.Stories`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| stories | Vector<StoryItem> | — | — | No description provided by the pinned schema. |
| pinned_to_top | flags.0?Vector<int> | flags.0 | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| pinned_to_top | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StoriesStories
```

Public access: `miniproto.raw.types.StoriesStories`.

## Safe usage shape

```python
from miniproto.raw.types import StoriesStories

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoriesStories
```

## Result family

[`stories.Stories`](/reference/telegram/types/results/stories-stories/)

## Relationships

- Result family: [`stories.Stories`](/reference/telegram/types/results/stories-stories/)
- Returned by: [`stories.getAlbumStories`](/reference/telegram/functions/stories/get-album-stories/), [`stories.getPinnedStories`](/reference/telegram/functions/stories/get-pinned-stories/), [`stories.getStoriesArchive`](/reference/telegram/functions/stories/get-stories-archive/), [`stories.getStoriesByID`](/reference/telegram/functions/stories/get-stories-by-id/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
