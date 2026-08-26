---
title: "inputMediaUploadedDocument"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputMediaUploadedDocument"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x037c9330"
---

# `inputMediaUploadedDocument`

No description provided by the pinned schema.

## Signature

```tl
inputMediaUploadedDocument#037c9330 flags:# nosound_video:flags.3?true force_file:flags.4?true spoiler:flags.5?true file:InputFile thumb:flags.2?InputFile mime_type:string attributes:Vector<DocumentAttribute> stickers:flags.0?Vector<InputDocument> video_cover:flags.6?InputPhoto video_timestamp:flags.7?int ttl_seconds:flags.1?int = InputMedia;
```

## Result type

`InputMedia`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| nosound_video | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| force_file | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| spoiler | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| file | InputFile | — | — | No description provided by the pinned schema. |
| thumb | flags.2?InputFile | flags.2 | — | No description provided by the pinned schema. |
| mime_type | string | — | — | No description provided by the pinned schema. |
| attributes | Vector<DocumentAttribute> | — | — | No description provided by the pinned schema. |
| stickers | flags.0?Vector<InputDocument> | flags.0 | — | No description provided by the pinned schema. |
| video_cover | flags.6?InputPhoto | flags.6 | — | No description provided by the pinned schema. |
| video_timestamp | flags.7?int | flags.7 | — | No description provided by the pinned schema. |
| ttl_seconds | flags.1?int | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| nosound_video | 3 | Controlled by `flags`; present when this bit is set. |
| force_file | 4 | Controlled by `flags`; present when this bit is set. |
| spoiler | 5 | Controlled by `flags`; present when this bit is set. |
| thumb | 2 | Controlled by `flags`; present when this bit is set. |
| stickers | 0 | Controlled by `flags`; present when this bit is set. |
| video_cover | 6 | Controlled by `flags`; present when this bit is set. |
| video_timestamp | 7 | Controlled by `flags`; present when this bit is set. |
| ttl_seconds | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputMediaUploadedDocument
```

Public access: `miniproto.raw.types.InputMediaUploadedDocument`.

## Safe usage shape

```python
from miniproto.raw.types import InputMediaUploadedDocument

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputMediaUploadedDocument
```

## Result family

[`InputMedia`](/reference/telegram/types/results/input-media/)

## Relationships

- Result family: [`InputMedia`](/reference/telegram/types/results/input-media/)
- Related constructors: [`inputMediaContact`](/reference/telegram/types/base/input-media-contact/), [`inputMediaDice`](/reference/telegram/types/base/input-media-dice/), [`inputMediaDocument`](/reference/telegram/types/base/input-media-document/), [`inputMediaDocumentExternal`](/reference/telegram/types/base/input-media-document-external/), [`inputMediaEmpty`](/reference/telegram/types/base/input-media-empty/), [`inputMediaGame`](/reference/telegram/types/base/input-media-game/), [`inputMediaGeoLive`](/reference/telegram/types/base/input-media-geo-live/), [`inputMediaGeoPoint`](/reference/telegram/types/base/input-media-geo-point/), [`inputMediaInvoice`](/reference/telegram/types/base/input-media-invoice/), [`inputMediaPaidMedia`](/reference/telegram/types/base/input-media-paid-media/), [`inputMediaPhoto`](/reference/telegram/types/base/input-media-photo/), [`inputMediaPhotoExternal`](/reference/telegram/types/base/input-media-photo-external/), [`inputMediaPoll`](/reference/telegram/types/base/input-media-poll/), [`inputMediaStakeDice`](/reference/telegram/types/base/input-media-stake-dice/), [`inputMediaStory`](/reference/telegram/types/base/input-media-story/), [`inputMediaTodo`](/reference/telegram/types/base/input-media-todo/), [`inputMediaUploadedPhoto`](/reference/telegram/types/base/input-media-uploaded-photo/), [`inputMediaVenue`](/reference/telegram/types/base/input-media-venue/), [`inputMediaWebPage`](/reference/telegram/types/base/input-media-web-page/)
- Accepted by: [`bots.addPreviewMedia`](/reference/telegram/functions/bots/add-preview-media/), [`bots.deletePreviewMedia`](/reference/telegram/functions/bots/delete-preview-media/), [`bots.editPreviewMedia`](/reference/telegram/functions/bots/edit-preview-media/), [`bots.reorderPreviewMedias`](/reference/telegram/functions/bots/reorder-preview-medias/), [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.uploadImportedMedia`](/reference/telegram/functions/messages/upload-imported-media/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/), [`payments.exportInvoice`](/reference/telegram/functions/payments/export-invoice/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`draftMessage`](/reference/telegram/types/base/draft-message/), [`inputMediaInvoice`](/reference/telegram/types/base/input-media-invoice/), [`inputMediaPaidMedia`](/reference/telegram/types/base/input-media-paid-media/), [`inputMediaPoll`](/reference/telegram/types/base/input-media-poll/), [`inputPollAnswer`](/reference/telegram/types/base/input-poll-answer/), [`inputSingleMedia`](/reference/telegram/types/base/input-single-media/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
