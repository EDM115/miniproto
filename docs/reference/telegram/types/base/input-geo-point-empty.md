---
title: "inputGeoPointEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputGeoPointEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe4c123d6"
---

# `inputGeoPointEmpty`

No description provided by the pinned schema.

## Signature

```tl
inputGeoPointEmpty#e4c123d6 = InputGeoPoint;
```

## Result type

`InputGeoPoint`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputGeoPointEmpty
```

Public access: `miniproto.raw.types.InputGeoPointEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import InputGeoPointEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputGeoPointEmpty
```

## Result family

[`InputGeoPoint`](/reference/telegram/types/results/input-geo-point/)

## Relationships

- Result family: [`InputGeoPoint`](/reference/telegram/types/results/input-geo-point/)
- Related constructors: [`inputGeoPoint`](/reference/telegram/types/base/input-geo-point/)
- Accepted by: [`account.updateBusinessLocation`](/reference/telegram/functions/account/update-business-location/), [`channels.createChannel`](/reference/telegram/functions/channels/create-channel/), [`channels.editLocation`](/reference/telegram/functions/channels/edit-location/), [`contacts.getLocated`](/reference/telegram/functions/contacts/get-located/), [`messages.getInlineBotResults`](/reference/telegram/functions/messages/get-inline-bot-results/), [`inputBotInlineMessageMediaGeo`](/reference/telegram/types/base/input-bot-inline-message-media-geo/), [`inputBotInlineMessageMediaVenue`](/reference/telegram/types/base/input-bot-inline-message-media-venue/), [`inputMediaGeoLive`](/reference/telegram/types/base/input-media-geo-live/), [`inputMediaGeoPoint`](/reference/telegram/types/base/input-media-geo-point/), [`inputMediaVenue`](/reference/telegram/types/base/input-media-venue/), [`inputPageBlockMap`](/reference/telegram/types/base/input-page-block-map/), [`inputWebFileGeoPointLocation`](/reference/telegram/types/base/input-web-file-geo-point-location/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
