---
title: "photoPathSize"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "photoPathSize"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xd8214d41"
---

# `photoPathSize`

No description provided by the pinned schema.

## Signature

```tl
photoPathSize#d8214d41 type:string bytes:bytes = PhotoSize;
```

## Result type

`PhotoSize`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| type | string | — | — | No description provided by the pinned schema. |
| bytes | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PhotoPathSize
```

Public access: `miniproto.raw.types.PhotoPathSize`.

## Safe usage shape

```python
from miniproto.raw.types import PhotoPathSize

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhotoPathSize
```

## Result family

[`PhotoSize`](/reference/telegram/types/results/photo-size/)

## Relationships

- Result family: [`PhotoSize`](/reference/telegram/types/results/photo-size/)
- Related constructors: [`photoCachedSize`](/reference/telegram/types/base/photo-cached-size/), [`photoSize`](/reference/telegram/types/base/photo-size/), [`photoSizeEmpty`](/reference/telegram/types/base/photo-size-empty/), [`photoSizeProgressive`](/reference/telegram/types/base/photo-size-progressive/), [`photoStrippedSize`](/reference/telegram/types/base/photo-stripped-size/)
- Accepted by: [`document`](/reference/telegram/types/base/document/), [`messageExtendedMediaPreview`](/reference/telegram/types/base/message-extended-media-preview/), [`photo`](/reference/telegram/types/base/photo/), [`stickerSet`](/reference/telegram/types/base/sticker-set/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
