---
title: "messages.chatsSlice"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.chatsSlice"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x9cd81144"
---

# `messages.chatsSlice`

No description provided by the pinned schema.

## Signature

```tl
messages.chatsSlice#9cd81144 count:int chats:Vector<Chat> = messages.Chats;
```

## Result type

`messages.Chats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesChatsSlice
```

Public access: `miniproto.raw.types.MessagesChatsSlice`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesChatsSlice

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesChatsSlice
```

## Result family

[`messages.Chats`](/reference/telegram/types/results/messages-chats/)

## Relationships

- Result family: [`messages.Chats`](/reference/telegram/types/results/messages-chats/)
- Related constructors: [`messages.chats`](/reference/telegram/types/messages/chats/)
- Returned by: [`channels.getAdminedPublicChannels`](/reference/telegram/functions/channels/get-admined-public-channels/), [`channels.getChannelRecommendations`](/reference/telegram/functions/channels/get-channel-recommendations/), [`channels.getChannels`](/reference/telegram/functions/channels/get-channels/), [`channels.getGroupsForDiscussion`](/reference/telegram/functions/channels/get-groups-for-discussion/), [`channels.getLeftChannels`](/reference/telegram/functions/channels/get-left-channels/), [`communities.getJoinedCommunities`](/reference/telegram/functions/communities/get-joined-communities/), [`messages.getChats`](/reference/telegram/functions/messages/get-chats/), [`messages.getCommonChats`](/reference/telegram/functions/messages/get-common-chats/), [`stories.getChatsToSend`](/reference/telegram/functions/stories/get-chats-to-send/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
