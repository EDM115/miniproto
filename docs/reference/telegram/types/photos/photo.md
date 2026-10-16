---
title: "photos.photo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "photos.photo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "photos"
schema_source: "tdlib"
constructor_id: "0x20212ca8"
---

# `photos.photo`

No description provided by the pinned schema.

## Signature

```tl
photos.photo#20212ca8 photo:Photo users:Vector<User> = photos.Photo;
```

## Result type

`photos.Photo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| photo | Photo | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PhotosPhoto
```

Public access: `miniproto.raw.types.PhotosPhoto`.

## Class reference

```python
from miniproto.raw.types import PhotosPhoto

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = PhotosPhoto
```

## Result family

[`photos.Photo`](/reference/telegram/types/results/photos-photo/)

## Relationships

- Result family: [`photos.Photo`](/reference/telegram/types/results/photos-photo/)
- Returned by: [`photos.updateProfilePhoto`](/reference/telegram/functions/photos/update-profile-photo/), [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
