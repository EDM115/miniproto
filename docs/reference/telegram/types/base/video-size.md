---
title: "videoSize"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "videoSize"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xde33b094"
---

# `videoSize`

No description provided by the pinned schema.

## Signature

```tl
videoSize#de33b094 flags:# type:string w:int h:int size:int video_start_ts:flags.0?double = VideoSize;
```

## Result type

`VideoSize`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| type | string | — | — | No description provided by the pinned schema. |
| w | int | — | — | No description provided by the pinned schema. |
| h | int | — | — | No description provided by the pinned schema. |
| size | int | — | — | No description provided by the pinned schema. |
| video_start_ts | flags.0?double | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| video_start_ts | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import VideoSize
```

Public access: `miniproto.raw.types.VideoSize`.

## Safe usage shape

```python
from miniproto.raw.types import VideoSize

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = VideoSize
```

## Result family

[`VideoSize`](/reference/telegram/types/results/video-size/)

## Relationships

- Result family: [`VideoSize`](/reference/telegram/types/results/video-size/)
- Related constructors: [`videoSizeEmojiMarkup`](/reference/telegram/types/base/video-size-emoji-markup/), [`videoSizeStickerMarkup`](/reference/telegram/types/base/video-size-sticker-markup/)
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
