---
title: "messageService"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageService"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x7a800e0a"
---

# `messageService`

No description provided by the pinned schema.

## Signature

```tl
messageService#7a800e0a flags:# out:flags.1?true mentioned:flags.4?true media_unread:flags.5?true reactions_are_possible:flags.9?true silent:flags.13?true post:flags.14?true legacy:flags.19?true id:int from_id:flags.8?Peer peer_id:Peer saved_peer_id:flags.28?Peer reply_to:flags.3?MessageReplyHeader date:int action:MessageAction reactions:flags.20?MessageReactions ttl_period:flags.25?int = Message;
```

## Result type

`Message`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| out | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| mentioned | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| media_unread | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| reactions_are_possible | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| silent | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| post | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| legacy | flags.19?true | flags.19 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| from_id | flags.8?Peer | flags.8 | — | No description provided by the pinned schema. |
| peer_id | Peer | — | — | No description provided by the pinned schema. |
| saved_peer_id | flags.28?Peer | flags.28 | — | No description provided by the pinned schema. |
| reply_to | flags.3?MessageReplyHeader | flags.3 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| action | MessageAction | — | — | No description provided by the pinned schema. |
| reactions | flags.20?MessageReactions | flags.20 | — | No description provided by the pinned schema. |
| ttl_period | flags.25?int | flags.25 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| out | 1 | Controlled by `flags`; present when this bit is set. |
| mentioned | 4 | Controlled by `flags`; present when this bit is set. |
| media_unread | 5 | Controlled by `flags`; present when this bit is set. |
| reactions_are_possible | 9 | Controlled by `flags`; present when this bit is set. |
| silent | 13 | Controlled by `flags`; present when this bit is set. |
| post | 14 | Controlled by `flags`; present when this bit is set. |
| legacy | 19 | Controlled by `flags`; present when this bit is set. |
| from_id | 8 | Controlled by `flags`; present when this bit is set. |
| saved_peer_id | 28 | Controlled by `flags`; present when this bit is set. |
| reply_to | 3 | Controlled by `flags`; present when this bit is set. |
| reactions | 20 | Controlled by `flags`; present when this bit is set. |
| ttl_period | 25 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageService
```

Public access: `miniproto.raw.types.MessageService`.

## Safe usage shape

```python
from miniproto.raw.types import MessageService

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageService
```

## Result family

[`Message`](/reference/telegram/types/results/message/)

## Relationships

- Result family: [`Message`](/reference/telegram/types/results/message/)
- Related constructors: [`message`](/reference/telegram/types/base/message/), [`messageEmpty`](/reference/telegram/types/base/message-empty/)
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
