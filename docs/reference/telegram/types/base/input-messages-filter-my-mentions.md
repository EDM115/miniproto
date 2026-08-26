---
title: "inputMessagesFilterMyMentions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputMessagesFilterMyMentions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xc1f8e69a"
---

# `inputMessagesFilterMyMentions`

No description provided by the pinned schema.

## Signature

```tl
inputMessagesFilterMyMentions#c1f8e69a = MessagesFilter;
```

## Result type

`MessagesFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import InputMessagesFilterMyMentions
```

Public access: `miniproto.raw.types.InputMessagesFilterMyMentions`.

## Safe usage shape

```python
from miniproto.raw.types import InputMessagesFilterMyMentions

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputMessagesFilterMyMentions
```

## Result family

[`MessagesFilter`](/reference/telegram/types/results/messages-filter/)

## Relationships

- Result family: [`MessagesFilter`](/reference/telegram/types/results/messages-filter/)
- Related constructors: [`inputMessagesFilterChatPhotos`](/reference/telegram/types/base/input-messages-filter-chat-photos/), [`inputMessagesFilterContacts`](/reference/telegram/types/base/input-messages-filter-contacts/), [`inputMessagesFilterDocument`](/reference/telegram/types/base/input-messages-filter-document/), [`inputMessagesFilterEmpty`](/reference/telegram/types/base/input-messages-filter-empty/), [`inputMessagesFilterGeo`](/reference/telegram/types/base/input-messages-filter-geo/), [`inputMessagesFilterGif`](/reference/telegram/types/base/input-messages-filter-gif/), [`inputMessagesFilterMusic`](/reference/telegram/types/base/input-messages-filter-music/), [`inputMessagesFilterPhoneCalls`](/reference/telegram/types/base/input-messages-filter-phone-calls/), [`inputMessagesFilterPhotoVideo`](/reference/telegram/types/base/input-messages-filter-photo-video/), [`inputMessagesFilterPhotos`](/reference/telegram/types/base/input-messages-filter-photos/), [`inputMessagesFilterPinned`](/reference/telegram/types/base/input-messages-filter-pinned/), [`inputMessagesFilterPoll`](/reference/telegram/types/base/input-messages-filter-poll/), [`inputMessagesFilterRoundVideo`](/reference/telegram/types/base/input-messages-filter-round-video/), [`inputMessagesFilterRoundVoice`](/reference/telegram/types/base/input-messages-filter-round-voice/), [`inputMessagesFilterUrl`](/reference/telegram/types/base/input-messages-filter-url/), [`inputMessagesFilterVideo`](/reference/telegram/types/base/input-messages-filter-video/), [`inputMessagesFilterVoice`](/reference/telegram/types/base/input-messages-filter-voice/)
- Accepted by: [`messages.getSearchCounters`](/reference/telegram/functions/messages/get-search-counters/), [`messages.getSearchResultsCalendar`](/reference/telegram/functions/messages/get-search-results-calendar/), [`messages.getSearchResultsPositions`](/reference/telegram/functions/messages/get-search-results-positions/), [`messages.search`](/reference/telegram/functions/messages/search/), [`messages.searchGlobal`](/reference/telegram/functions/messages/search-global/), [`messages.searchSentMedia`](/reference/telegram/functions/messages/search-sent-media/), [`messages.searchCounter`](/reference/telegram/types/messages/search-counter/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
