---
title: "messageEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x90a6ca84"
---

# `messageEmpty`

No description provided by the pinned schema.

## Signature

```tl
messageEmpty#90a6ca84 flags:# id:int peer_id:flags.0?Peer = Message;
```

## Result type

`Message`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| peer_id | flags.0?Peer | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| peer_id | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageEmpty
```

Public access: `miniproto.raw.types.MessageEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import MessageEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageEmpty
```

## Result family

[`Message`](/reference/telegram/types/results/message/)

## Relationships

- Result family: [`Message`](/reference/telegram/types/results/message/)
- Related constructors: [`message`](/reference/telegram/types/base/message/), [`messageService`](/reference/telegram/types/base/message-service/)
- Accepted by: [`channelAdminLogEventActionDeleteMessage`](/reference/telegram/types/base/channel-admin-log-event-action-delete-message/), [`channelAdminLogEventActionEditMessage`](/reference/telegram/types/base/channel-admin-log-event-action-edit-message/), [`channelAdminLogEventActionSendMessage`](/reference/telegram/types/base/channel-admin-log-event-action-send-message/), [`channelAdminLogEventActionStopPoll`](/reference/telegram/types/base/channel-admin-log-event-action-stop-poll/), [`channelAdminLogEventActionUpdatePinned`](/reference/telegram/types/base/channel-admin-log-event-action-update-pinned/), [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.dialogs`](/reference/telegram/types/messages/dialogs/), [`messages.dialogsSlice`](/reference/telegram/types/messages/dialogs-slice/), [`messages.discussionMessage`](/reference/telegram/types/messages/discussion-message/), [`messages.forumTopics`](/reference/telegram/types/messages/forum-topics/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/), [`messages.peerDialogs`](/reference/telegram/types/messages/peer-dialogs/), [`messages.quickReplies`](/reference/telegram/types/messages/quick-replies/), [`messages.savedDialogs`](/reference/telegram/types/messages/saved-dialogs/), [`messages.savedDialogsSlice`](/reference/telegram/types/messages/saved-dialogs-slice/), [`messages.searchResultsCalendar`](/reference/telegram/types/messages/search-results-calendar/), [`publicForwardMessage`](/reference/telegram/types/base/public-forward-message/), [`storyReactionPublicForward`](/reference/telegram/types/base/story-reaction-public-forward/), [`storyViewPublicForward`](/reference/telegram/types/base/story-view-public-forward/), [`updateBotEditBusinessMessage`](/reference/telegram/types/base/update-bot-edit-business-message/), [`updateBotGuestChatQuery`](/reference/telegram/types/base/update-bot-guest-chat-query/), [`updateBotNewBusinessMessage`](/reference/telegram/types/base/update-bot-new-business-message/), [`updateBusinessBotCallbackQuery`](/reference/telegram/types/base/update-business-bot-callback-query/), [`updateEditChannelMessage`](/reference/telegram/types/base/update-edit-channel-message/), [`updateEditMessage`](/reference/telegram/types/base/update-edit-message/), [`updateNewChannelMessage`](/reference/telegram/types/base/update-new-channel-message/), [`updateNewMessage`](/reference/telegram/types/base/update-new-message/), [`updateNewScheduledMessage`](/reference/telegram/types/base/update-new-scheduled-message/), [`updateQuickReplyMessage`](/reference/telegram/types/base/update-quick-reply-message/), [`updates.channelDifference`](/reference/telegram/types/updates/channel-difference/), [`updates.channelDifferenceTooLong`](/reference/telegram/types/updates/channel-difference-too-long/), [`updates.difference`](/reference/telegram/types/updates/difference/), [`updates.differenceSlice`](/reference/telegram/types/updates/difference-slice/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
