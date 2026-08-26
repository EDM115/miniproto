---
title: "messages.searchSentMedia"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.searchSentMedia"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x107e31a0"
---

# `messages.searchSentMedia`

No description provided by the pinned schema.

## Signature

```tl
messages.searchSentMedia#107e31a0 q:string filter:MessagesFilter limit:int = messages.Messages;
```

## Result type

`messages.Messages`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| q | string | — | — | No description provided by the pinned schema. |
| filter | MessagesFilter | — | — | No description provided by the pinned schema. |
| limit | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesSearchSentMedia
```

Public access: `miniproto.raw.functions.MessagesSearchSentMedia`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesSearchSentMedia

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesSearchSentMedia
```

## Result family

[`messages.Messages`](/reference/telegram/types/results/messages-messages/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`FILTER_NOT_SUPPORTED`](/reference/telegram/errors/filter-not-supported/) | The specified filter cannot be used in this context. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`MessagesFilter`](/reference/telegram/types/results/messages-filter/)
Known selected constructors: [`inputMessagesFilterChatPhotos`](/reference/telegram/types/base/input-messages-filter-chat-photos/), [`inputMessagesFilterContacts`](/reference/telegram/types/base/input-messages-filter-contacts/), [`inputMessagesFilterDocument`](/reference/telegram/types/base/input-messages-filter-document/), [`inputMessagesFilterEmpty`](/reference/telegram/types/base/input-messages-filter-empty/), [`inputMessagesFilterGeo`](/reference/telegram/types/base/input-messages-filter-geo/), [`inputMessagesFilterGif`](/reference/telegram/types/base/input-messages-filter-gif/), [`inputMessagesFilterMusic`](/reference/telegram/types/base/input-messages-filter-music/), [`inputMessagesFilterMyMentions`](/reference/telegram/types/base/input-messages-filter-my-mentions/), [`inputMessagesFilterPhoneCalls`](/reference/telegram/types/base/input-messages-filter-phone-calls/), [`inputMessagesFilterPhotoVideo`](/reference/telegram/types/base/input-messages-filter-photo-video/), [`inputMessagesFilterPhotos`](/reference/telegram/types/base/input-messages-filter-photos/), [`inputMessagesFilterPinned`](/reference/telegram/types/base/input-messages-filter-pinned/), [`inputMessagesFilterPoll`](/reference/telegram/types/base/input-messages-filter-poll/), [`inputMessagesFilterRoundVideo`](/reference/telegram/types/base/input-messages-filter-round-video/), [`inputMessagesFilterRoundVoice`](/reference/telegram/types/base/input-messages-filter-round-voice/), [`inputMessagesFilterUrl`](/reference/telegram/types/base/input-messages-filter-url/), [`inputMessagesFilterVideo`](/reference/telegram/types/base/input-messages-filter-video/), [`inputMessagesFilterVoice`](/reference/telegram/types/base/input-messages-filter-voice/)

## Returned types

[`messages.Messages`](/reference/telegram/types/results/messages-messages/)
Known selected constructors: [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesNotModified`](/reference/telegram/types/messages/messages-not-modified/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/)

## Related methods

[`channels.getMessages`](/reference/telegram/functions/channels/get-messages/), [`channels.searchPosts`](/reference/telegram/functions/channels/search-posts/), [`messages.getHistory`](/reference/telegram/functions/messages/get-history/), [`messages.getMessages`](/reference/telegram/functions/messages/get-messages/), [`messages.getPersonalChannelHistory`](/reference/telegram/functions/messages/get-personal-channel-history/), [`messages.getQuickReplyMessages`](/reference/telegram/functions/messages/get-quick-reply-messages/), [`messages.getRecentLocations`](/reference/telegram/functions/messages/get-recent-locations/), [`messages.getReplies`](/reference/telegram/functions/messages/get-replies/), [`messages.getRichMessage`](/reference/telegram/functions/messages/get-rich-message/), [`messages.getSavedHistory`](/reference/telegram/functions/messages/get-saved-history/), [`messages.getScheduledHistory`](/reference/telegram/functions/messages/get-scheduled-history/), [`messages.getScheduledMessages`](/reference/telegram/functions/messages/get-scheduled-messages/), [`messages.getSearchCounters`](/reference/telegram/functions/messages/get-search-counters/), [`messages.getSearchResultsCalendar`](/reference/telegram/functions/messages/get-search-results-calendar/), [`messages.getSearchResultsPositions`](/reference/telegram/functions/messages/get-search-results-positions/), [`messages.getUnreadMentions`](/reference/telegram/functions/messages/get-unread-mentions/), [`messages.getUnreadPollVotes`](/reference/telegram/functions/messages/get-unread-poll-votes/), [`messages.getUnreadReactions`](/reference/telegram/functions/messages/get-unread-reactions/), [`messages.search`](/reference/telegram/functions/messages/search/), [`messages.searchGlobal`](/reference/telegram/functions/messages/search-global/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
