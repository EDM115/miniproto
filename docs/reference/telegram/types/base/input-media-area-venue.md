---
title: "inputMediaAreaVenue"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputMediaAreaVenue"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb282217f"
---

# `inputMediaAreaVenue`

No description provided by the pinned schema.

## Signature

```tl
inputMediaAreaVenue#b282217f coordinates:MediaAreaCoordinates query_id:long result_id:string = MediaArea;
```

## Result type

`MediaArea`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| coordinates | MediaAreaCoordinates | — | — | No description provided by the pinned schema. |
| query_id | long | — | — | No description provided by the pinned schema. |
| result_id | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputMediaAreaVenue
```

Public access: `miniproto.raw.types.InputMediaAreaVenue`.

## Safe usage shape

```python
from miniproto.raw.types import InputMediaAreaVenue

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputMediaAreaVenue
```

## Result family

[`MediaArea`](/reference/telegram/types/results/media-area/)

## Relationships

- Result family: [`MediaArea`](/reference/telegram/types/results/media-area/)
- Related constructors: [`inputMediaAreaChannelPost`](/reference/telegram/types/base/input-media-area-channel-post/), [`mediaAreaChannelPost`](/reference/telegram/types/base/media-area-channel-post/), [`mediaAreaGeoPoint`](/reference/telegram/types/base/media-area-geo-point/), [`mediaAreaStarGift`](/reference/telegram/types/base/media-area-star-gift/), [`mediaAreaSuggestedReaction`](/reference/telegram/types/base/media-area-suggested-reaction/), [`mediaAreaUrl`](/reference/telegram/types/base/media-area-url/), [`mediaAreaVenue`](/reference/telegram/types/base/media-area-venue/), [`mediaAreaWeather`](/reference/telegram/types/base/media-area-weather/)
- Accepted by: [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.searchPosts`](/reference/telegram/functions/stories/search-posts/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`storyItem`](/reference/telegram/types/base/story-item/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
