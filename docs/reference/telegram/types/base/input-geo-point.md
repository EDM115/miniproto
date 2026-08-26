---
title: "inputGeoPoint"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputGeoPoint"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x48222faf"
---

# `inputGeoPoint`

No description provided by the pinned schema.

## Signature

```tl
inputGeoPoint#48222faf flags:# lat:double long:double accuracy_radius:flags.0?int = InputGeoPoint;
```

## Result type

`InputGeoPoint`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| lat | double | — | — | No description provided by the pinned schema. |
| long | double | — | — | No description provided by the pinned schema. |
| accuracy_radius | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| accuracy_radius | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputGeoPoint
```

Public access: `miniproto.raw.types.InputGeoPoint`.

## Safe usage shape

```python
from miniproto.raw.types import InputGeoPoint

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputGeoPoint
```

## Result family

[`InputGeoPoint`](/reference/telegram/types/results/input-geo-point/)

## Relationships

- Result family: [`InputGeoPoint`](/reference/telegram/types/results/input-geo-point/)
- Related constructors: [`inputGeoPointEmpty`](/reference/telegram/types/base/input-geo-point-empty/)
- Accepted by: [`account.updateBusinessLocation`](/reference/telegram/functions/account/update-business-location/), [`channels.createChannel`](/reference/telegram/functions/channels/create-channel/), [`channels.editLocation`](/reference/telegram/functions/channels/edit-location/), [`contacts.getLocated`](/reference/telegram/functions/contacts/get-located/), [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/), [`inputBotInlineMessageMediaGeo`](/reference/telegram/types/base/input-bot-inline-message-media-geo/), [`inputBotInlineMessageMediaVenue`](/reference/telegram/types/base/input-bot-inline-message-media-venue/), [`inputMediaGeoLive`](/reference/telegram/types/base/input-media-geo-live/), [`inputMediaGeoPoint`](/reference/telegram/types/base/input-media-geo-point/), [`inputMediaVenue`](/reference/telegram/types/base/input-media-venue/), [`inputPageBlockMap`](/reference/telegram/types/base/input-page-block-map/), [`inputWebFileGeoPointLocation`](/reference/telegram/types/base/input-web-file-geo-point-location/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
