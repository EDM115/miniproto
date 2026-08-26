---
title: "photos.photos"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "photos.photos"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "photos"
schema_source: "tdlib"
constructor_id: "0x8dca6aa5"
---

# `photos.photos`

No description provided by the pinned schema.

## Signature

```tl
photos.photos#8dca6aa5 photos:Vector<Photo> users:Vector<User> = photos.Photos;
```

## Result type

`photos.Photos`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| photos | Vector<Photo> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PhotosPhotos
```

Public access: `miniproto.raw.types.PhotosPhotos`.

## Safe usage shape

```python
from miniproto.raw.types import PhotosPhotos

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhotosPhotos
```

## Result family

[`photos.Photos`](/reference/telegram/types/results/photos-photos/)

## Relationships

- Result family: [`photos.Photos`](/reference/telegram/types/results/photos-photos/)
- Related constructors: [`photos.photosSlice`](/reference/telegram/types/photos/photos-slice/)
- Returned by: [`photos.getUserPhotos`](/reference/telegram/functions/photos/get-user-photos/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
