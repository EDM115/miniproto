---
title: "messages.forumTopics"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.forumTopics"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x367617d3"
---

# `messages.forumTopics`

No description provided by the pinned schema.

## Signature

```tl
messages.forumTopics#367617d3 flags:# order_by_create_date:flags.0?true count:int topics:Vector<ForumTopic> messages:Vector<Message> chats:Vector<Chat> users:Vector<User> pts:int = messages.ForumTopics;
```

## Result type

`messages.ForumTopics`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| order_by_create_date | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| topics | Vector<ForumTopic> | — | — | No description provided by the pinned schema. |
| messages | Vector<Message> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| pts | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| order_by_create_date | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesForumTopics
```

Public access: `miniproto.raw.types.MessagesForumTopics`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesForumTopics

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesForumTopics
```

## Result family

[`messages.ForumTopics`](/reference/telegram/types/results/messages-forum-topics/)

## Relationships

- Result family: [`messages.ForumTopics`](/reference/telegram/types/results/messages-forum-topics/)
- Returned by: [`messages.getForumTopics`](/reference/telegram/functions/messages/get-forum-topics/), [`messages.getForumTopicsByID`](/reference/telegram/functions/messages/get-forum-topics-by-id/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
