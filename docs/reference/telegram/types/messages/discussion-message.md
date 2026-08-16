---
title: "messages.discussionMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.discussionMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xa6341782"
---

# `messages.discussionMessage`

No description provided by the pinned schema.

## Signature

```tl
messages.discussionMessage#a6341782 flags:# messages:Vector<Message> max_id:flags.0?int read_inbox_max_id:flags.1?int read_outbox_max_id:flags.2?int unread_count:int chats:Vector<Chat> users:Vector<User> = messages.DiscussionMessage;
```

## Result type

`messages.DiscussionMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| messages | Vector<Message> | — | — | No description provided by the pinned schema. |
| max_id | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| read_inbox_max_id | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| read_outbox_max_id | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| unread_count | int | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| max_id | 0 | Controlled by `flags`; present when this bit is set. |
| read_inbox_max_id | 1 | Controlled by `flags`; present when this bit is set. |
| read_outbox_max_id | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesDiscussionMessage
```

Public access: `miniproto.raw.types.MessagesDiscussionMessage`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesDiscussionMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesDiscussionMessage
```

## Result family

[`messages.DiscussionMessage`](/reference/telegram/types/results/messages-discussion-message/)

## Relationships

- Result family: [`messages.DiscussionMessage`](/reference/telegram/types/results/messages-discussion-message/)
- Returned by: [`messages.getDiscussionMessage`](/reference/telegram/functions/messages/get-discussion-message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
