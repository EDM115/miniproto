---
title: "photoStrippedSize"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "photoStrippedSize"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe0b0bc2e"
---

# `photoStrippedSize`

No description provided by the pinned schema.

## Signature

```tl
photoStrippedSize#e0b0bc2e type:string bytes:bytes = PhotoSize;
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
from miniproto.raw.types import PhotoStrippedSize
```

Public access: `miniproto.raw.types.PhotoStrippedSize`.

## Safe usage shape

```python
from miniproto.raw.types import PhotoStrippedSize

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhotoStrippedSize
```

## Result family

[`PhotoSize`](/reference/telegram/types/results/photo-size/)

## Relationships

- Result family: [`PhotoSize`](/reference/telegram/types/results/photo-size/)
- Related constructors: [`photoCachedSize`](/reference/telegram/types/base/photo-cached-size/), [`photoPathSize`](/reference/telegram/types/base/photo-path-size/), [`photoSize`](/reference/telegram/types/base/photo-size/), [`photoSizeEmpty`](/reference/telegram/types/base/photo-size-empty/), [`photoSizeProgressive`](/reference/telegram/types/base/photo-size-progressive/)
- Accepted by: [`document`](/reference/telegram/types/base/document/), [`messageExtendedMediaPreview`](/reference/telegram/types/base/message-extended-media-preview/), [`photo`](/reference/telegram/types/base/photo/), [`stickerSet`](/reference/telegram/types/base/sticker-set/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
