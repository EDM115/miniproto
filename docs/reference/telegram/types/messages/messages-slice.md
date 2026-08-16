---
title: "messages.messagesSlice"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.messagesSlice"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5f206716"
---

# `messages.messagesSlice`

No description provided by the pinned schema.

## Signature

```tl
messages.messagesSlice#5f206716 flags:# inexact:flags.1?true count:int next_rate:flags.0?int offset_id_offset:flags.2?int search_flood:flags.3?SearchPostsFlood messages:Vector<Message> topics:Vector<ForumTopic> chats:Vector<Chat> users:Vector<User> = messages.Messages;
```

## Result type

`messages.Messages`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| inexact | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| next_rate | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| offset_id_offset | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| search_flood | flags.3?SearchPostsFlood | flags.3 | — | No description provided by the pinned schema. |
| messages | Vector<Message> | — | — | No description provided by the pinned schema. |
| topics | Vector<ForumTopic> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| inexact | 1 | Controlled by `flags`; present when this bit is set. |
| next_rate | 0 | Controlled by `flags`; present when this bit is set. |
| offset_id_offset | 2 | Controlled by `flags`; present when this bit is set. |
| search_flood | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesMessagesSlice
```

Public access: `miniproto.raw.types.MessagesMessagesSlice`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesMessagesSlice

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesMessagesSlice
```

## Result family

[`messages.Messages`](/reference/telegram/types/results/messages-messages/)

## Relationships

- Result family: [`messages.Messages`](/reference/telegram/types/results/messages-messages/)
- Related constructors: [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesNotModified`](/reference/telegram/types/messages/messages-not-modified/)
- Returned by: [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.searchPosts`](/reference/telegram/functions/channels/search-posts/), [`messages.getHistory`](/reference/telegram/functions/messages/get-history/), [`messages.getMessages`](/reference/telegram/functions/messages/get-messages/), [`messages.getPersonalChannelHistory`](/reference/telegram/functions/messages/get-personal-channel-history/), [`messages.getQuickReplyMessages`](/reference/telegram/functions/messages/get-quick-reply-messages/), [`messages.getRecentLocations`](/reference/telegram/functions/messages/get-recent-locations/), [`messages.getReplies`](/reference/telegram/functions/messages/get-replies/), [`messages.getRichMessage`](/reference/telegram/functions/messages/get-rich-message/), [`messages.getSavedHistory`](/reference/telegram/functions/messages/get-saved-history/), [`messages.getScheduledHistory`](/reference/telegram/functions/messages/get-scheduled-history/), [`messages.getScheduledMessages`](/reference/telegram/functions/messages/get-scheduled-messages/), [`messages.getUnreadMentions`](/reference/telegram/functions/messages/get-unread-mentions/), [`messages.getUnreadPollVotes`](/reference/telegram/functions/messages/get-unread-poll-votes/), [`messages.getUnreadReactions`](/reference/telegram/functions/messages/get-unread-reactions/), [`messages.search`](/reference/telegram/functions/messages/search/), [`messages.searchGlobal`](/reference/telegram/functions/messages/search-global/), [`messages.searchSentMedia`](/reference/telegram/functions/messages/search-sent-media/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
