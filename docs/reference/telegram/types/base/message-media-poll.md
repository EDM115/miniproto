---
title: "messageMediaPoll"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageMediaPoll"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x773f4e66"
---

# `messageMediaPoll`

No description provided by the pinned schema.

## Signature

```tl
messageMediaPoll#773f4e66 flags:# poll:Poll results:PollResults attached_media:flags.0?MessageMedia = MessageMedia;
```

## Result type

`MessageMedia`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| poll | Poll | — | — | No description provided by the pinned schema. |
| results | PollResults | — | — | No description provided by the pinned schema. |
| attached_media | flags.0?MessageMedia | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| attached_media | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageMediaPoll
```

Public access: `miniproto.raw.types.MessageMediaPoll`.

## Safe usage shape

```python
from miniproto.raw.types import MessageMediaPoll

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageMediaPoll
```

## Result family

[`MessageMedia`](/reference/telegram/types/results/message-media/)

## Relationships

- Result family: [`MessageMedia`](/reference/telegram/types/results/message-media/)
- Related constructors: [`messageMediaContact`](/reference/telegram/types/base/message-media-contact/), [`messageMediaDice`](/reference/telegram/types/base/message-media-dice/), [`messageMediaDocument`](/reference/telegram/types/base/message-media-document/), [`messageMediaEmpty`](/reference/telegram/types/base/message-media-empty/), [`messageMediaGame`](/reference/telegram/types/base/message-media-game/), [`messageMediaGeo`](/reference/telegram/types/base/message-media-geo/), [`messageMediaGeoLive`](/reference/telegram/types/base/message-media-geo-live/), [`messageMediaGiveaway`](/reference/telegram/types/base/message-media-giveaway/), [`messageMediaGiveawayResults`](/reference/telegram/types/base/message-media-giveaway-results/), [`messageMediaInvoice`](/reference/telegram/types/base/message-media-invoice/), [`messageMediaPaidMedia`](/reference/telegram/types/base/message-media-paid-media/), [`messageMediaPhoto`](/reference/telegram/types/base/message-media-photo/), [`messageMediaStory`](/reference/telegram/types/base/message-media-story/), [`messageMediaToDo`](/reference/telegram/types/base/message-media-to-do/), [`messageMediaUnsupported`](/reference/telegram/types/base/message-media-unsupported/), [`messageMediaVenue`](/reference/telegram/types/base/message-media-venue/), [`messageMediaVideoStream`](/reference/telegram/types/base/message-media-video-stream/), [`messageMediaWebPage`](/reference/telegram/types/base/message-media-web-page/)
- Accepted by: [`botPreviewMedia`](/reference/telegram/types/base/bot-preview-media/), [`ephemeralMessage`](/reference/telegram/types/base/ephemeral-message/), [`message`](/reference/telegram/types/base/message/), [`messageExtendedMedia`](/reference/telegram/types/base/message-extended-media/), [`messageMediaPoll`](/reference/telegram/types/base/message-media-poll/), [`messageReplyHeader`](/reference/telegram/types/base/message-reply-header/), [`messages.webPagePreview`](/reference/telegram/types/messages/web-page-preview/), [`pollAnswer`](/reference/telegram/types/base/poll-answer/), [`pollResults`](/reference/telegram/types/base/poll-results/), [`sponsoredMessage`](/reference/telegram/types/base/sponsored-message/), [`starsTransaction`](/reference/telegram/types/base/stars-transaction/), [`storyItem`](/reference/telegram/types/base/story-item/), [`updateServiceNotification`](/reference/telegram/types/base/update-service-notification/), [`updateShortSentMessage`](/reference/telegram/types/base/update-short-sent-message/)
- Returned by: [`messages.uploadImportedMedia`](/reference/telegram/functions/messages/upload-imported-media/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
