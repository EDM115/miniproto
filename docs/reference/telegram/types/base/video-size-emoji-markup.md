---
title: "videoSizeEmojiMarkup"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "videoSizeEmojiMarkup"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf85c413c"
---

# `videoSizeEmojiMarkup`

No description provided by the pinned schema.

## Signature

```tl
videoSizeEmojiMarkup#f85c413c emoji_id:long background_colors:Vector<int> = VideoSize;
```

## Result type

`VideoSize`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| emoji_id | long | — | — | No description provided by the pinned schema. |
| background_colors | Vector<int> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import VideoSizeEmojiMarkup
```

Public access: `miniproto.raw.types.VideoSizeEmojiMarkup`.

## Safe usage shape

```python
from miniproto.raw.types import VideoSizeEmojiMarkup

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = VideoSizeEmojiMarkup
```

## Result family

[`VideoSize`](/reference/telegram/types/results/video-size/)

## Relationships

- Result family: [`VideoSize`](/reference/telegram/types/results/video-size/)
- Related constructors: [`videoSize`](/reference/telegram/types/base/video-size/), [`videoSizeStickerMarkup`](/reference/telegram/types/base/video-size-sticker-markup/)
- Accepted by: [`photos.uploadContactProfilePhoto`](/reference/telegram/functions/photos/upload-contact-profile-photo/), [`photos.uploadProfilePhoto`](/reference/telegram/functions/photos/upload-profile-photo/), [`document`](/reference/telegram/types/base/document/), [`inputChatUploadedPhoto`](/reference/telegram/types/base/input-chat-uploaded-photo/), [`photo`](/reference/telegram/types/base/photo/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
