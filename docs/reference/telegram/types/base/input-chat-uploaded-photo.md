---
title: "inputChatUploadedPhoto"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputChatUploadedPhoto"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xbdcdaec0"
---

# `inputChatUploadedPhoto`

No description provided by the pinned schema.

## Signature

```tl
inputChatUploadedPhoto#bdcdaec0 flags:# file:flags.0?InputFile video:flags.1?InputFile video_start_ts:flags.2?double video_emoji_markup:flags.3?VideoSize = InputChatPhoto;
```

## Result type

`InputChatPhoto`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| file | flags.0?InputFile | flags.0 | — | No description provided by the pinned schema. |
| video | flags.1?InputFile | flags.1 | — | No description provided by the pinned schema. |
| video_start_ts | flags.2?double | flags.2 | — | No description provided by the pinned schema. |
| video_emoji_markup | flags.3?VideoSize | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| file | 0 | Controlled by `flags`; present when this bit is set. |
| video | 1 | Controlled by `flags`; present when this bit is set. |
| video_start_ts | 2 | Controlled by `flags`; present when this bit is set. |
| video_emoji_markup | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputChatUploadedPhoto
```

Public access: `miniproto.raw.types.InputChatUploadedPhoto`.

## Safe usage shape

```python
from miniproto.raw.types import InputChatUploadedPhoto

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputChatUploadedPhoto
```

## Result family

[`InputChatPhoto`](/reference/telegram/types/results/input-chat-photo/)

## Relationships

- Result family: [`InputChatPhoto`](/reference/telegram/types/results/input-chat-photo/)
- Related constructors: [`inputChatPhoto`](/reference/telegram/types/base/input-chat-photo/), [`inputChatPhotoEmpty`](/reference/telegram/types/base/input-chat-photo-empty/)
- Accepted by: [`channels.editPhoto`](/reference/telegram/functions/channels/edit-photo/), [`messages.editChatPhoto`](/reference/telegram/functions/messages/edit-chat-photo/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
