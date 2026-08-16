---
title: "videoSizeStickerMarkup"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "videoSizeStickerMarkup"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0da082fe"
---

# `videoSizeStickerMarkup`

No description provided by the pinned schema.

## Signature

```tl
videoSizeStickerMarkup#0da082fe stickerset:InputStickerSet sticker_id:long background_colors:Vector<int> = VideoSize;
```

## Result type

`VideoSize`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| stickerset | InputStickerSet | — | — | No description provided by the pinned schema. |
| sticker_id | long | — | — | No description provided by the pinned schema. |
| background_colors | Vector<int> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import VideoSizeStickerMarkup
```

Public access: `miniproto.raw.types.VideoSizeStickerMarkup`.

## Safe usage shape

```python
from miniproto.raw.types import VideoSizeStickerMarkup

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = VideoSizeStickerMarkup
```

## Result family

[`VideoSize`](/reference/telegram/types/results/video-size/)

## Relationships

- Result family: [`VideoSize`](/reference/telegram/types/results/video-size/)
- Related constructors: [`videoSize`](/reference/telegram/types/base/video-size/), [`videoSizeEmojiMarkup`](/reference/telegram/types/base/video-size-emoji-markup/)
- Accepted by: [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/), [`document`](/reference/telegram/types/base/document/), [`inputChatUploadedPhoto`](/reference/telegram/types/base/input-chat-uploaded-photo/), [`photo`](/reference/telegram/types/base/photo/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
