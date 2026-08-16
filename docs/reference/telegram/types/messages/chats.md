---
title: "messages.chats"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.chats"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x64ff9fd5"
---

# `messages.chats`

No description provided by the pinned schema.

## Signature

```tl
messages.chats#64ff9fd5 chats:Vector<Chat> = messages.Chats;
```

## Result type

`messages.Chats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesChats
```

Public access: `miniproto.raw.types.MessagesChats`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesChats

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesChats
```

## Result family

[`messages.Chats`](/reference/telegram/types/results/messages-chats/)

## Relationships

- Result family: [`messages.Chats`](/reference/telegram/types/results/messages-chats/)
- Related constructors: [`messages.chatsSlice`](/reference/telegram/types/messages/chats-slice/)
- Returned by: [`channels.getAdminedPublicChannels`](/reference/telegram/functions/channels/get-admined-public-channels/), [`channels.getChannelRecommendations`](/reference/telegram/functions/channels/get-channel-recommendations/), [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getGroupsForDiscussion`](/reference/telegram/functions/channels/get-groups-for-discussion/), [`channels.getLeftChannels`](/reference/telegram/functions/channels/get-left-channels/), [`communities.getJoinedCommunities`](/reference/telegram/functions/communities/get-joined-communities/), [`messages.getChats`](/reference/telegram/functions/messages/get-chats/), [`messages.getCommonChats`](/reference/telegram/functions/messages/get-common-chats/), [`stories.getChatsToSend`](/reference/telegram/functions/stories/get-chats-to-send/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
