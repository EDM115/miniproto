---
title: "sendMessageTextDraftAction"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "sendMessageTextDraftAction"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x376d975c"
---

# `sendMessageTextDraftAction`

No description provided by the pinned schema.

## Signature

```tl
sendMessageTextDraftAction#376d975c random_id:long text:TextWithEntities = SendMessageAction;
```

## Result type

`SendMessageAction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| random_id | long | — | — | No description provided by the pinned schema. |
| text | TextWithEntities | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import SendMessageTextDraftAction
```

Public access: `miniproto.raw.types.SendMessageTextDraftAction`.

## Safe usage shape

```python
from miniproto.raw.types import SendMessageTextDraftAction

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SendMessageTextDraftAction
```

## Result family

[`SendMessageAction`](/reference/telegram/types/results/send-message-action/)

## Relationships

- Result family: [`SendMessageAction`](/reference/telegram/types/results/send-message-action/)
- Related constructors: [`inputSendMessageRichMessageDraftAction`](/reference/telegram/types/base/input-send-message-rich-message-draft-action/), [`sendMessageCancelAction`](/reference/telegram/types/base/send-message-cancel-action/), [`sendMessageChooseContactAction`](/reference/telegram/types/base/send-message-choose-contact-action/), [`sendMessageChooseStickerAction`](/reference/telegram/types/base/send-message-choose-sticker-action/), [`sendMessageEmojiInteraction`](/reference/telegram/types/base/send-message-emoji-interaction/), [`sendMessageEmojiInteractionSeen`](/reference/telegram/types/base/send-message-emoji-interaction-seen/), [`sendMessageGamePlayAction`](/reference/telegram/types/base/send-message-game-play-action/), [`sendMessageGeoLocationAction`](/reference/telegram/types/base/send-message-geo-location-action/), [`sendMessageHistoryImportAction`](/reference/telegram/types/base/send-message-history-import-action/), [`sendMessageRecordAudioAction`](/reference/telegram/types/base/send-message-record-audio-action/), [`sendMessageRecordRoundAction`](/reference/telegram/types/base/send-message-record-round-action/), [`sendMessageRecordVideoAction`](/reference/telegram/types/base/send-message-record-video-action/), [`sendMessageRichMessageDraftAction`](/reference/telegram/types/base/send-message-rich-message-draft-action/), [`sendMessageTypingAction`](/reference/telegram/types/base/send-message-typing-action/), [`sendMessageUploadAudioAction`](/reference/telegram/types/base/send-message-upload-audio-action/), [`sendMessageUploadDocumentAction`](/reference/telegram/types/base/send-message-upload-document-action/), [`sendMessageUploadPhotoAction`](/reference/telegram/types/base/send-message-upload-photo-action/), [`sendMessageUploadRoundAction`](/reference/telegram/types/base/send-message-upload-round-action/), [`sendMessageUploadVideoAction`](/reference/telegram/types/base/send-message-upload-video-action/), [`speakingInGroupCallAction`](/reference/telegram/types/base/speaking-in-group-call-action/)
- Accepted by: [`messages.setTyping`](/reference/telegram/functions/messages/set-typing/), [`updateChannelUserTyping`](/reference/telegram/types/base/update-channel-user-typing/), [`updateChatUserTyping`](/reference/telegram/types/base/update-chat-user-typing/), [`updateUserTyping`](/reference/telegram/types/base/update-user-typing/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
