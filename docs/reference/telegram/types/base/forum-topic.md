---
title: "forumTopic"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "forumTopic"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfcdad815"
---

# `forumTopic`

No description provided by the pinned schema.

## Signature

```tl
forumTopic#fcdad815 flags:# my:flags.1?true closed:flags.2?true pinned:flags.3?true short:flags.5?true hidden:flags.6?true title_missing:flags.7?true id:int date:int peer:Peer title:string icon_color:int icon_emoji_id:flags.0?long top_message:int read_inbox_max_id:int read_outbox_max_id:int unread_count:int unread_mentions_count:int unread_reactions_count:int unread_poll_votes_count:int from_id:Peer notify_settings:PeerNotifySettings draft:flags.4?DraftMessage = ForumTopic;
```

## Result type

`ForumTopic`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| my | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| closed | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| pinned | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| short | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| hidden | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| title_missing | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| icon_color | int | — | — | No description provided by the pinned schema. |
| icon_emoji_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| top_message | int | — | — | No description provided by the pinned schema. |
| read_inbox_max_id | int | — | — | No description provided by the pinned schema. |
| read_outbox_max_id | int | — | — | No description provided by the pinned schema. |
| unread_count | int | — | — | No description provided by the pinned schema. |
| unread_mentions_count | int | — | — | No description provided by the pinned schema. |
| unread_reactions_count | int | — | — | No description provided by the pinned schema. |
| unread_poll_votes_count | int | — | — | No description provided by the pinned schema. |
| from_id | Peer | — | — | No description provided by the pinned schema. |
| notify_settings | PeerNotifySettings | — | — | No description provided by the pinned schema. |
| draft | flags.4?DraftMessage | flags.4 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| my | 1 | Controlled by `flags`; present when this bit is set. |
| closed | 2 | Controlled by `flags`; present when this bit is set. |
| pinned | 3 | Controlled by `flags`; present when this bit is set. |
| short | 5 | Controlled by `flags`; present when this bit is set. |
| hidden | 6 | Controlled by `flags`; present when this bit is set. |
| title_missing | 7 | Controlled by `flags`; present when this bit is set. |
| icon_emoji_id | 0 | Controlled by `flags`; present when this bit is set. |
| draft | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ForumTopic
```

Public access: `miniproto.raw.types.ForumTopic`.

## Safe usage shape

```python
from miniproto.raw.types import ForumTopic

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ForumTopic
```

## Result family

[`ForumTopic`](/reference/telegram/types/results/forum-topic/)

## Relationships

- Result family: [`ForumTopic`](/reference/telegram/types/results/forum-topic/)
- Related constructors: [`forumTopicDeleted`](/reference/telegram/types/base/forum-topic-deleted/)
- Accepted by: [`channelAdminLogEventActionCreateTopic`](/reference/telegram/types/base/channel-admin-log-event-action-create-topic/), [`channelAdminLogEventActionDeleteTopic`](/reference/telegram/types/base/channel-admin-log-event-action-delete-topic/), [`channelAdminLogEventActionEditTopic`](/reference/telegram/types/base/channel-admin-log-event-action-edit-topic/), [`channelAdminLogEventActionPinTopic`](/reference/telegram/types/base/channel-admin-log-event-action-pin-topic/), [`messages.channelMessages`](/reference/telegram/types/messages/channel-messages/), [`messages.forumTopics`](/reference/telegram/types/messages/forum-topics/), [`messages.messages`](/reference/telegram/types/messages/messages/), [`messages.messagesSlice`](/reference/telegram/types/messages/messages-slice/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
