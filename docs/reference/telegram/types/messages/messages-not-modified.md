---
title: "messages.messagesNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.messagesNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x74535f21"
---

# `messages.messagesNotModified`

No description provided by the pinned schema.

## Signature

```tl
messages.messagesNotModified#74535f21 count:int = messages.Messages;
```

## Result type

`messages.Messages`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesMessagesNotModified
```

Public access: `miniproto.raw.types.MessagesMessagesNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesMessagesNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesMessagesNotModified
```

## Result family

[`messages.Messages`](/reference/telegram/types/results/messages-messages/)

## Relationships

- Result family: [`messages.Messages`](/reference/telegram/types/results/messages-messages/)
- Related constructors: [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/)
- Returned by: [`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.searchPosts`](/reference/telegram/functions/channels/search-posts/), [`messages.getHistory`](/reference/telegram/functions/messages/get-history/), [`messages.getMessages`](/reference/telegram/functions/messages/get-messages/), [`messages.getPersonalChannelHistory`](/reference/telegram/functions/messages/get-personal-channel-history/), [`messages.getQuickReplyMessages`](/reference/telegram/functions/messages/get-quick-reply-messages/), [`messages.getRecentLocations`](/reference/telegram/functions/messages/get-recent-locations/), [`messages.getReplies`](/reference/telegram/functions/messages/get-replies/), [`messages.getRichMessage`](/reference/telegram/functions/messages/get-rich-message/), [`messages.getSavedHistory`](/reference/telegram/functions/messages/get-saved-history/), [`messages.getScheduledHistory`](/reference/telegram/functions/messages/get-scheduled-history/), [`messages.getScheduledMessages`](/reference/telegram/functions/messages/get-scheduled-messages/), [`messages.getUnreadMentions`](/reference/telegram/functions/messages/get-unread-mentions/), [`messages.getUnreadPollVotes`](/reference/telegram/functions/messages/get-unread-poll-votes/), [`messages.getUnreadReactions`](/reference/telegram/functions/messages/get-unread-reactions/), [`messages.search`](/reference/telegram/functions/messages/search/), [`messages.searchGlobal`](/reference/telegram/functions/messages/search-global/), [`messages.searchSentMedia`](/reference/telegram/functions/messages/search-sent-media/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
