---
title: "mediaAreaCoordinates"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "mediaAreaCoordinates"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xcfc9e002"
---

# `mediaAreaCoordinates`

No description provided by the pinned schema.

## Signature

```tl
mediaAreaCoordinates#cfc9e002 flags:# x:double y:double w:double h:double rotation:double radius:flags.0?double = MediaAreaCoordinates;
```

## Result type

`MediaAreaCoordinates`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| x | double | — | — | No description provided by the pinned schema. |
| y | double | — | — | No description provided by the pinned schema. |
| w | double | — | — | No description provided by the pinned schema. |
| h | double | — | — | No description provided by the pinned schema. |
| rotation | double | — | — | No description provided by the pinned schema. |
| radius | flags.0?double | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| radius | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MediaAreaCoordinates
```

Public access: `miniproto.raw.types.MediaAreaCoordinates`.

## Safe usage shape

```python
from miniproto.raw.types import MediaAreaCoordinates

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MediaAreaCoordinates
```

## Result family

[`MediaAreaCoordinates`](/reference/telegram/types/results/media-area-coordinates/)

## Relationships

- Result family: [`MediaAreaCoordinates`](/reference/telegram/types/results/media-area-coordinates/)
- Accepted by: [`inputMediaAreaChannelPost`](/reference/telegram/types/base/input-media-area-channel-post/), [`inputMediaAreaVenue`](/reference/telegram/types/base/input-media-area-venue/), [`mediaAreaChannelPost`](/reference/telegram/types/base/media-area-channel-post/), [`mediaAreaGeoPoint`](/reference/telegram/types/base/media-area-geo-point/), [`mediaAreaStarGift`](/reference/telegram/types/base/media-area-star-gift/), [`mediaAreaSuggestedReaction`](/reference/telegram/types/base/media-area-suggested-reaction/), [`mediaAreaUrl`](/reference/telegram/types/base/media-area-url/), [`mediaAreaVenue`](/reference/telegram/types/base/media-area-venue/), [`mediaAreaWeather`](/reference/telegram/types/base/media-area-weather/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
