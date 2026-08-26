---
title: "mediaAreaStarGift"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "mediaAreaStarGift"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x5787686d"
---

# `mediaAreaStarGift`

No description provided by the pinned schema.

## Signature

```tl
mediaAreaStarGift#5787686d coordinates:MediaAreaCoordinates slug:string = MediaArea;
```

## Result type

`MediaArea`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| coordinates | MediaAreaCoordinates | — | — | No description provided by the pinned schema. |
| slug | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MediaAreaStarGift
```

Public access: `miniproto.raw.types.MediaAreaStarGift`.

## Safe usage shape

```python
from miniproto.raw.types import MediaAreaStarGift

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MediaAreaStarGift
```

## Result family

[`MediaArea`](/reference/telegram/types/results/media-area/)

## Relationships

- Result family: [`MediaArea`](/reference/telegram/types/results/media-area/)
- Related constructors: [`inputMediaAreaChannelPost`](/reference/telegram/types/base/input-media-area-channel-post/), [`inputMediaAreaVenue`](/reference/telegram/types/base/input-media-area-venue/), [`mediaAreaChannelPost`](/reference/telegram/types/base/media-area-channel-post/), [`mediaAreaGeoPoint`](/reference/telegram/types/base/media-area-geo-point/), [`mediaAreaSuggestedReaction`](/reference/telegram/types/base/media-area-suggested-reaction/), [`mediaAreaUrl`](/reference/telegram/types/base/media-area-url/), [`mediaAreaVenue`](/reference/telegram/types/base/media-area-venue/), [`mediaAreaWeather`](/reference/telegram/types/base/media-area-weather/)
- Accepted by: [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.searchPosts`](/reference/telegram/functions/stories/search-posts/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`storyItem`](/reference/telegram/types/base/story-item/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
