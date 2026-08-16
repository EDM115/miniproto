---
title: "geoPoint"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "geoPoint"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb2a2f663"
---

# `geoPoint`

No description provided by the pinned schema.

## Signature

```tl
geoPoint#b2a2f663 flags:# long:double lat:double access_hash:long accuracy_radius:flags.0?int = GeoPoint;
```

## Result type

`GeoPoint`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| long | double | — | — | No description provided by the pinned schema. |
| lat | double | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| accuracy_radius | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| accuracy_radius | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import GeoPoint
```

Public access: `miniproto.raw.types.GeoPoint`.

## Safe usage shape

```python
from miniproto.raw.types import GeoPoint

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = GeoPoint
```

## Result family

[`GeoPoint`](/reference/telegram/types/results/geo-point/)

## Relationships

- Result family: [`GeoPoint`](/reference/telegram/types/results/geo-point/)
- Related constructors: [`geoPointEmpty`](/reference/telegram/types/base/geo-point-empty/)
- Accepted by: [`botInlineMessageMediaGeo`](/reference/telegram/types/base/bot-inline-message-media-geo/), [`botInlineMessageMediaVenue`](/reference/telegram/types/base/bot-inline-message-media-venue/), [`businessLocation`](/reference/telegram/types/base/business-location/), [`channelLocation`](/reference/telegram/types/base/channel-location/), [`mediaAreaGeoPoint`](/reference/telegram/types/base/media-area-geo-point/), [`mediaAreaVenue`](/reference/telegram/types/base/media-area-venue/), [`messageMediaGeo`](/reference/telegram/types/base/message-media-geo/), [`messageMediaGeoLive`](/reference/telegram/types/base/message-media-geo-live/), [`messageMediaVenue`](/reference/telegram/types/base/message-media-venue/), [`pageBlockMap`](/reference/telegram/types/base/page-block-map/), [`updateBotInlineQuery`](/reference/telegram/types/base/update-bot-inline-query/), [`updateBotInlineSend`](/reference/telegram/types/base/update-bot-inline-send/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
