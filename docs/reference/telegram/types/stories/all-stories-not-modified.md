---
title: "stories.allStoriesNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stories.allStoriesNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stories"
schema_source: "tdlib"
constructor_id: "0x1158fe3e"
---

# `stories.allStoriesNotModified`

No description provided by the pinned schema.

## Signature

```tl
stories.allStoriesNotModified#1158fe3e flags:# state:string stealth_mode:StoriesStealthMode = stories.AllStories;
```

## Result type

`stories.AllStories`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| state | string | — | — | No description provided by the pinned schema. |
| stealth_mode | StoriesStealthMode | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StoriesAllStoriesNotModified
```

Public access: `miniproto.raw.types.StoriesAllStoriesNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import StoriesAllStoriesNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoriesAllStoriesNotModified
```

## Result family

[`stories.AllStories`](/reference/telegram/types/results/stories-all-stories/)

## Relationships

- Result family: [`stories.AllStories`](/reference/telegram/types/results/stories-all-stories/)
- Related constructors: [`stories.allStories`](/reference/telegram/types/stories/all-stories/)
- Returned by: [`stories.getAllStories`](/reference/telegram/functions/stories/get-all-stories/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
