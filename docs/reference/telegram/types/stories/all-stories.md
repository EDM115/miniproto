---
title: "stories.allStories"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stories.allStories"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stories"
schema_source: "tdlib"
constructor_id: "0x6efc5e81"
---

# `stories.allStories`

No description provided by the pinned schema.

## Signature

```tl
stories.allStories#6efc5e81 flags:# has_more:flags.0?true count:int state:string peer_stories:Vector<PeerStories> chats:Vector<Chat> users:Vector<User> stealth_mode:StoriesStealthMode = stories.AllStories;
```

## Result type

`stories.AllStories`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_more | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| state | string | — | — | No description provided by the pinned schema. |
| peer_stories | Vector<PeerStories> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| stealth_mode | StoriesStealthMode | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_more | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StoriesAllStories
```

Public access: `miniproto.raw.types.StoriesAllStories`.

## Safe usage shape

```python
from miniproto.raw.types import StoriesAllStories

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoriesAllStories
```

## Result family

[`stories.AllStories`](/reference/telegram/types/results/stories-all-stories/)

## Relationships

- Result family: [`stories.AllStories`](/reference/telegram/types/results/stories-all-stories/)
- Related constructors: [`stories.allStoriesNotModified`](/reference/telegram/types/stories/all-stories-not-modified/)
- Returned by: [`stories.getAllStories`](/reference/telegram/functions/stories/get-all-stories/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
