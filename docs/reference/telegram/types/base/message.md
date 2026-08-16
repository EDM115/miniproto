---
title: "message"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "message"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x7600b9d3"
---

# `message`

No description provided by the pinned schema.

## Signature

```tl
message#7600b9d3 flags:# out:flags.1?true mentioned:flags.4?true media_unread:flags.5?true silent:flags.13?true post:flags.14?true from_scheduled:flags.18?true legacy:flags.19?true edit_hide:flags.21?true pinned:flags.24?true noforwards:flags.26?true invert_media:flags.27?true flags2:# offline:flags2.1?true video_processing_pending:flags2.4?true paid_suggested_post_stars:flags2.8?true paid_suggested_post_ton:flags2.9?true id:int from_id:flags.8?Peer from_boosts_applied:flags.29?int from_rank:flags2.12?string peer_id:Peer saved_peer_id:flags.28?Peer fwd_from:flags.2?MessageFwdHeader via_bot_id:flags.11?long via_business_bot_id:flags2.0?long guestchat_via_from:flags2.19?Peer reply_to:flags.3?MessageReplyHeader date:int message:string media:flags.9?MessageMedia reply_markup:flags.6?ReplyMarkup entities:flags.7?Vector<MessageEntity> views:flags.10?int forwards:flags.10?int replies:flags.23?MessageReplies edit_date:flags.15?int post_author:flags.16?string grouped_id:flags.17?long reactions:flags.20?MessageReactions restriction_reason:flags.22?Vector<RestrictionReason> ttl_period:flags.25?int quick_reply_shortcut_id:flags.30?int effect:flags2.2?long factcheck:flags2.3?FactCheck report_delivery_until_date:flags2.5?int paid_message_stars:flags2.6?long suggested_post:flags2.7?SuggestedPost schedule_repeat_period:flags2.10?int summary_from_language:flags2.11?string rich_message:flags2.13?RichMessage = Message;
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
| silent | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| post | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| from_scheduled | flags.18?true | flags.18 | — | No description provided by the pinned schema. |
| legacy | flags.19?true | flags.19 | — | No description provided by the pinned schema. |
| edit_hide | flags.21?true | flags.21 | — | No description provided by the pinned schema. |
| pinned | flags.24?true | flags.24 | — | No description provided by the pinned schema. |
| noforwards | flags.26?true | flags.26 | — | No description provided by the pinned schema. |
| invert_media | flags.27?true | flags.27 | — | No description provided by the pinned schema. |
| flags2 | # | flag word | — | No description provided by the pinned schema. |
| offline | flags2.1?true | flags2.1 | — | No description provided by the pinned schema. |
| video_processing_pending | flags2.4?true | flags2.4 | — | No description provided by the pinned schema. |
| paid_suggested_post_stars | flags2.8?true | flags2.8 | — | No description provided by the pinned schema. |
| paid_suggested_post_ton | flags2.9?true | flags2.9 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| from_id | flags.8?Peer | flags.8 | — | No description provided by the pinned schema. |
| from_boosts_applied | flags.29?int | flags.29 | — | No description provided by the pinned schema. |
| from_rank | flags2.12?string | flags2.12 | — | No description provided by the pinned schema. |
| peer_id | Peer | — | — | No description provided by the pinned schema. |
| saved_peer_id | flags.28?Peer | flags.28 | — | No description provided by the pinned schema. |
| fwd_from | flags.2?MessageFwdHeader | flags.2 | — | No description provided by the pinned schema. |
| via_bot_id | flags.11?long | flags.11 | — | No description provided by the pinned schema. |
| via_business_bot_id | flags2.0?long | flags2.0 | — | No description provided by the pinned schema. |
| guestchat_via_from | flags2.19?Peer | flags2.19 | — | No description provided by the pinned schema. |
| reply_to | flags.3?MessageReplyHeader | flags.3 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| media | flags.9?MessageMedia | flags.9 | — | No description provided by the pinned schema. |
| reply_markup | flags.6?ReplyMarkup | flags.6 | — | No description provided by the pinned schema. |
| entities | flags.7?Vector<MessageEntity> | flags.7 | — | No description provided by the pinned schema. |
| views | flags.10?int | flags.10 | — | No description provided by the pinned schema. |
| forwards | flags.10?int | flags.10 | — | No description provided by the pinned schema. |
| replies | flags.23?MessageReplies | flags.23 | — | No description provided by the pinned schema. |
| edit_date | flags.15?int | flags.15 | — | No description provided by the pinned schema. |
| post_author | flags.16?string | flags.16 | — | No description provided by the pinned schema. |
| grouped_id | flags.17?long | flags.17 | — | No description provided by the pinned schema. |
| reactions | flags.20?MessageReactions | flags.20 | — | No description provided by the pinned schema. |
| restriction_reason | flags.22?Vector<RestrictionReason> | flags.22 | — | No description provided by the pinned schema. |
| ttl_period | flags.25?int | flags.25 | — | No description provided by the pinned schema. |
| quick_reply_shortcut_id | flags.30?int | flags.30 | — | No description provided by the pinned schema. |
| effect | flags2.2?long | flags2.2 | — | No description provided by the pinned schema. |
| factcheck | flags2.3?FactCheck | flags2.3 | — | No description provided by the pinned schema. |
| report_delivery_until_date | flags2.5?int | flags2.5 | — | No description provided by the pinned schema. |
| paid_message_stars | flags2.6?long | flags2.6 | — | No description provided by the pinned schema. |
| suggested_post | flags2.7?SuggestedPost | flags2.7 | — | No description provided by the pinned schema. |
| schedule_repeat_period | flags2.10?int | flags2.10 | — | No description provided by the pinned schema. |
| summary_from_language | flags2.11?string | flags2.11 | — | No description provided by the pinned schema. |
| rich_message | flags2.13?RichMessage | flags2.13 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| out | 1 | Controlled by `flags`; present when this bit is set. |
| mentioned | 4 | Controlled by `flags`; present when this bit is set. |
| media_unread | 5 | Controlled by `flags`; present when this bit is set. |
| silent | 13 | Controlled by `flags`; present when this bit is set. |
| post | 14 | Controlled by `flags`; present when this bit is set. |
| from_scheduled | 18 | Controlled by `flags`; present when this bit is set. |
| legacy | 19 | Controlled by `flags`; present when this bit is set. |
| edit_hide | 21 | Controlled by `flags`; present when this bit is set. |
| pinned | 24 | Controlled by `flags`; present when this bit is set. |
| noforwards | 26 | Controlled by `flags`; present when this bit is set. |
| invert_media | 27 | Controlled by `flags`; present when this bit is set. |
| offline | 1 | Controlled by `flags2`; present when this bit is set. |
| video_processing_pending | 4 | Controlled by `flags2`; present when this bit is set. |
| paid_suggested_post_stars | 8 | Controlled by `flags2`; present when this bit is set. |
| paid_suggested_post_ton | 9 | Controlled by `flags2`; present when this bit is set. |
| from_id | 8 | Controlled by `flags`; present when this bit is set. |
| from_boosts_applied | 29 | Controlled by `flags`; present when this bit is set. |
| from_rank | 12 | Controlled by `flags2`; present when this bit is set. |
| saved_peer_id | 28 | Controlled by `flags`; present when this bit is set. |
| fwd_from | 2 | Controlled by `flags`; present when this bit is set. |
| via_bot_id | 11 | Controlled by `flags`; present when this bit is set. |
| via_business_bot_id | 0 | Controlled by `flags2`; present when this bit is set. |
| guestchat_via_from | 19 | Controlled by `flags2`; present when this bit is set. |
| reply_to | 3 | Controlled by `flags`; present when this bit is set. |
| media | 9 | Controlled by `flags`; present when this bit is set. |
| reply_markup | 6 | Controlled by `flags`; present when this bit is set. |
| entities | 7 | Controlled by `flags`; present when this bit is set. |
| views | 10 | Controlled by `flags`; present when this bit is set. |
| forwards | 10 | Controlled by `flags`; present when this bit is set. |
| replies | 23 | Controlled by `flags`; present when this bit is set. |
| edit_date | 15 | Controlled by `flags`; present when this bit is set. |
| post_author | 16 | Controlled by `flags`; present when this bit is set. |
| grouped_id | 17 | Controlled by `flags`; present when this bit is set. |
| reactions | 20 | Controlled by `flags`; present when this bit is set. |
| restriction_reason | 22 | Controlled by `flags`; present when this bit is set. |
| ttl_period | 25 | Controlled by `flags`; present when this bit is set. |
| quick_reply_shortcut_id | 30 | Controlled by `flags`; present when this bit is set. |
| effect | 2 | Controlled by `flags2`; present when this bit is set. |
| factcheck | 3 | Controlled by `flags2`; present when this bit is set. |
| report_delivery_until_date | 5 | Controlled by `flags2`; present when this bit is set. |
| paid_message_stars | 6 | Controlled by `flags2`; present when this bit is set. |
| suggested_post | 7 | Controlled by `flags2`; present when this bit is set. |
| schedule_repeat_period | 10 | Controlled by `flags2`; present when this bit is set. |
| summary_from_language | 11 | Controlled by `flags2`; present when this bit is set. |
| rich_message | 13 | Controlled by `flags2`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Message
```

Public access: `miniproto.raw.types.Message`.

## Safe usage shape

```python
from miniproto.raw.types import Message

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Message
```

## Result family

[`Message`](/reference/telegram/types/results/message/)

## Relationships

- Result family: [`Message`](/reference/telegram/types/results/message/)
- Related constructors: [`messageEmpty`](/reference/telegram/types/base/message-empty/), [`messageService`](/reference/telegram/types/base/message-service/)
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
