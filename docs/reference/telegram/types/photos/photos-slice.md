---
title: "photos.photosSlice"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "photos.photosSlice"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "photos"
layer: 228
schema_source: "tdlib"
constructor_id: "0x15051f54"
---

# `photos.photosSlice`

No description provided by the pinned schema.

## Signature

```tl
photos.photosSlice#15051f54 count:int photos:Vector<Photo> users:Vector<User> = photos.Photos;
```

## Result type

`photos.Photos`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| photos | Vector<Photo> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PhotosPhotosSlice
```

Public access: `miniproto.raw.types.PhotosPhotosSlice`.

## Safe usage shape

```python
from miniproto.raw.types import PhotosPhotosSlice

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhotosPhotosSlice
```

## Result family

[`photos.Photos`](/reference/telegram/types/results/photos-photos/)

## Relationships

- Result family: [`photos.Photos`](/reference/telegram/types/results/photos-photos/)
- Related constructors: [`photos.photos`](/reference/telegram/types/photos/photos/)
- Returned by: [`photos.getUserPhotos`](/reference/telegram/functions/photos/get-user-photos/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
