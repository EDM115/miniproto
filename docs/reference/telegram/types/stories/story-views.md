---
title: "stories.storyViews"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stories.storyViews"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stories"
layer: 228
schema_source: "tdlib"
constructor_id: "0xde9eed1d"
---

# `stories.storyViews`

No description provided by the pinned schema.

## Signature

```tl
stories.storyViews#de9eed1d views:Vector<StoryViews> users:Vector<User> = stories.StoryViews;
```

## Result type

`stories.StoryViews`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| views | Vector<StoryViews> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StoriesStoryViews
```

Public access: `miniproto.raw.types.StoriesStoryViews`.

## Safe usage shape

```python
from miniproto.raw.types import StoriesStoryViews

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StoriesStoryViews
```

## Result family

[`stories.StoryViews`](/reference/telegram/types/results/stories-story-views/)

## Relationships

- Result family: [`stories.StoryViews`](/reference/telegram/types/results/stories-story-views/)
- Returned by: [`stories.getStoriesViews`](/reference/telegram/functions/stories/get-stories-views/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
