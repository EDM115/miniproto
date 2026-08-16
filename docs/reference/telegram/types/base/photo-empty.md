---
title: "photoEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "photoEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2331b22d"
---

# `photoEmpty`

No description provided by the pinned schema.

## Signature

```tl
photoEmpty#2331b22d id:long = Photo;
```

## Result type

`Photo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PhotoEmpty
```

Public access: `miniproto.raw.types.PhotoEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import PhotoEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhotoEmpty
```

## Result family

[`Photo`](/reference/telegram/types/results/photo/)

## Relationships

- Result family: [`Photo`](/reference/telegram/types/results/photo/)
- Related constructors: [`photo`](/reference/telegram/types/base/photo/)
- Accepted by: [`botApp`](/reference/telegram/types/base/bot-app/), [`botInfo`](/reference/telegram/types/base/bot-info/), [`botInlineMediaResult`](/reference/telegram/types/base/bot-inline-media-result/), [`channelAdminLogEventActionChangePhoto`](/reference/telegram/types/base/channel-admin-log-event-action-change-photo/), [`channelFull`](/reference/telegram/types/base/channel-full/), [`chatFull`](/reference/telegram/types/base/chat-full/), [`chatInvite`](/reference/telegram/types/base/chat-invite/), [`communityFull`](/reference/telegram/types/base/community-full/), [`game`](/reference/telegram/types/base/game/), [`messageActionChatEditPhoto`](/reference/telegram/types/base/message-action-chat-edit-photo/), [`messageActionSuggestProfilePhoto`](/reference/telegram/types/base/message-action-suggest-profile-photo/), [`messageMediaDocument`](/reference/telegram/types/base/message-media-document/), [`messageMediaPhoto`](/reference/telegram/types/base/message-media-photo/), [`page`](/reference/telegram/types/base/page/), [`photos.photo`](/reference/telegram/types/photos/photo/), [`photos.photos`](/reference/telegram/types/photos/photos/), [`photos.photosSlice`](/reference/telegram/types/photos/photos-slice/), [`requestedPeerChannel`](/reference/telegram/types/base/requested-peer-channel/), [`requestedPeerChat`](/reference/telegram/types/base/requested-peer-chat/), [`requestedPeerUser`](/reference/telegram/types/base/requested-peer-user/), [`richMessage`](/reference/telegram/types/base/rich-message/), [`sponsoredMessage`](/reference/telegram/types/base/sponsored-message/), [`storyAlbum`](/reference/telegram/types/base/story-album/), [`userFull`](/reference/telegram/types/base/user-full/), [`webPage`](/reference/telegram/types/base/web-page/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
