---
title: "inputMediaPaidMedia"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputMediaPaidMedia"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc4103386"
---

# `inputMediaPaidMedia`

No description provided by the pinned schema.

## Signature

```tl
inputMediaPaidMedia#c4103386 flags:# stars_amount:long extended_media:Vector<InputMedia> payload:flags.0?string = InputMedia;
```

## Result type

`InputMedia`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| stars_amount | long | — | — | No description provided by the pinned schema. |
| extended_media | Vector<InputMedia> | — | — | No description provided by the pinned schema. |
| payload | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| payload | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputMediaPaidMedia
```

Public access: `miniproto.raw.types.InputMediaPaidMedia`.

## Safe usage shape

```python
from miniproto.raw.types import InputMediaPaidMedia

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputMediaPaidMedia
```

## Result family

[`InputMedia`](/reference/telegram/types/results/input-media/)

## Relationships

- Result family: [`InputMedia`](/reference/telegram/types/results/input-media/)
- Related constructors: [`inputMediaContact`](/reference/telegram/types/base/input-media-contact/), [`inputMediaDice`](/reference/telegram/types/base/input-media-dice/), [`inputMediaDocument`](/reference/telegram/types/base/input-media-document/), [`inputMediaDocumentExternal`](/reference/telegram/types/base/input-media-document-external/), [`inputMediaEmpty`](/reference/telegram/types/base/input-media-empty/), [`inputMediaGame`](/reference/telegram/types/base/input-media-game/), [`inputMediaGeoLive`](/reference/telegram/types/base/input-media-geo-live/), [`inputMediaGeoPoint`](/reference/telegram/types/base/input-media-geo-point/), [`inputMediaInvoice`](/reference/telegram/types/base/input-media-invoice/), [`inputMediaPhoto`](/reference/telegram/types/base/input-media-photo/), [`inputMediaPhotoExternal`](/reference/telegram/types/base/input-media-photo-external/), [`inputMediaPoll`](/reference/telegram/types/base/input-media-poll/), [`inputMediaStakeDice`](/reference/telegram/types/base/input-media-stake-dice/), [`inputMediaStory`](/reference/telegram/types/base/input-media-story/), [`inputMediaTodo`](/reference/telegram/types/base/input-media-todo/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputMediaUploadedPhoto`](/reference/telegram/types/base/input-media-uploaded-photo/), [`inputMediaVenue`](/reference/telegram/types/base/input-media-venue/), [`inputMediaWebPage`](/reference/telegram/types/base/input-media-web-page/)
- Accepted by: [`bots.addPreviewMedia`](/reference/telegram/functions/bots/add-preview-media/), [`bots.deletePreviewMedia`](/reference/telegram/functions/bots/delete-preview-media/), [`bots.editPreviewMedia`](/reference/telegram/functions/bots/edit-preview-media/), [`bots.reorderPreviewMedias`](/reference/telegram/functions/bots/reorder-preview-medias/), [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.uploadImportedMedia`](/reference/telegram/functions/messages/upload-imported-media/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/), [`payments.exportInvoice`](/reference/telegram/functions/payments/export-invoice/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/), [`draftMessage`](/reference/telegram/types/base/draft-message/), [`inputMediaInvoice`](/reference/telegram/types/base/input-media-invoice/), [`inputMediaPaidMedia`](/reference/telegram/types/base/input-media-paid-media/), [`inputMediaPoll`](/reference/telegram/types/base/input-media-poll/), [`inputPollAnswer`](/reference/telegram/types/base/input-poll-answer/), [`inputSingleMedia`](/reference/telegram/types/base/input-single-media/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
