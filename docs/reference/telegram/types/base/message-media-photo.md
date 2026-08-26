---
title: "messageMediaPhoto"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageMediaPhoto"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xe216eb63"
---

# `messageMediaPhoto`

No description provided by the pinned schema.

## Signature

```tl
messageMediaPhoto#e216eb63 flags:# spoiler:flags.3?true live_photo:flags.4?true photo:flags.0?Photo ttl_seconds:flags.2?int video:flags.4?Document = MessageMedia;
```

## Result type

`MessageMedia`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| spoiler | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| live_photo | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| photo | flags.0?Photo | flags.0 | — | No description provided by the pinned schema. |
| ttl_seconds | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| video | flags.4?Document | flags.4 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| spoiler | 3 | Controlled by `flags`; present when this bit is set. |
| live_photo | 4 | Controlled by `flags`; present when this bit is set. |
| photo | 0 | Controlled by `flags`; present when this bit is set. |
| ttl_seconds | 2 | Controlled by `flags`; present when this bit is set. |
| video | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageMediaPhoto
```

Public access: `miniproto.raw.types.MessageMediaPhoto`.

## Safe usage shape

```python
from miniproto.raw.types import MessageMediaPhoto

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageMediaPhoto
```

## Result family

[`MessageMedia`](/reference/telegram/types/results/message-media/)

## Relationships

- Result family: [`MessageMedia`](/reference/telegram/types/results/message-media/)
- Related constructors: [`messageMediaContact`](/reference/telegram/types/base/message-media-contact/), [`messageMediaDice`](/reference/telegram/types/base/message-media-dice/), [`messageMediaDocument`](/reference/telegram/types/base/message-media-document/), [`messageMediaEmpty`](/reference/telegram/types/base/message-media-empty/), [`messageMediaGame`](/reference/telegram/types/base/message-media-game/), [`messageMediaGeo`](/reference/telegram/types/base/message-media-geo/), [`messageMediaGeoLive`](/reference/telegram/types/base/message-media-geo-live/), [`messageMediaGiveaway`](/reference/telegram/types/base/message-media-giveaway/), [`messageMediaGiveawayResults`](/reference/telegram/types/base/message-media-giveaway-results/), [`messageMediaInvoice`](/reference/telegram/types/base/message-media-invoice/), [`messageMediaPaidMedia`](/reference/telegram/types/base/message-media-paid-media/), [`messageMediaPoll`](/reference/telegram/types/base/message-media-poll/), [`messageMediaStory`](/reference/telegram/types/base/message-media-story/), [`messageMediaToDo`](/reference/telegram/types/base/message-media-to-do/), [`messageMediaUnsupported`](/reference/telegram/types/base/message-media-unsupported/), [`messageMediaVenue`](/reference/telegram/types/base/message-media-venue/), [`messageMediaVideoStream`](/reference/telegram/types/base/message-media-video-stream/), [`messageMediaWebPage`](/reference/telegram/types/base/message-media-web-page/)
- Accepted by: [`botPreviewMedia`](/reference/telegram/types/base/bot-preview-media/), [`ephemeralMessage`](/reference/telegram/types/base/ephemeral-message/), [`message`](/reference/telegram/types/base/message/), [`messageExtendedMedia`](/reference/telegram/types/base/message-extended-media/), [`messageMediaPoll`](/reference/telegram/types/base/message-media-poll/), [`messageReplyHeader`](/reference/telegram/types/base/message-reply-header/), [`messages.webPagePreview`](/reference/telegram/types/messages/web-page-preview/), [`pollAnswer`](/reference/telegram/types/base/poll-answer/), [`pollResults`](/reference/telegram/types/base/poll-results/), [`sponsoredMessage`](/reference/telegram/types/base/sponsored-message/), [`starsTransaction`](/reference/telegram/types/base/stars-transaction/), [`storyItem`](/reference/telegram/types/base/story-item/), [`updateServiceNotification`](/reference/telegram/types/base/update-service-notification/), [`updateShortSentMessage`](/reference/telegram/types/base/update-short-sent-message/)
- Returned by: [`messages.uploadImportedMedia`](/reference/telegram/functions/messages/upload-imported-media/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
