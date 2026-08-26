---
title: "messageReplyHeader"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageReplyHeader"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x1b97dd66"
---

# `messageReplyHeader`

No description provided by the pinned schema.

## Signature

```tl
messageReplyHeader#1b97dd66 flags:# reply_to_scheduled:flags.2?true forum_topic:flags.3?true quote:flags.9?true reply_to_ephemeral:flags.13?true reply_to_msg_id:flags.4?int reply_to_peer_id:flags.0?Peer reply_from:flags.5?MessageFwdHeader reply_media:flags.8?MessageMedia reply_to_top_id:flags.1?int quote_text:flags.6?string quote_entities:flags.7?Vector<MessageEntity> quote_offset:flags.10?int todo_item_id:flags.11?int poll_option:flags.12?bytes = MessageReplyHeader;
```

## Result type

`MessageReplyHeader`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| reply_to_scheduled | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| forum_topic | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| quote | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| reply_to_ephemeral | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| reply_to_msg_id | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| reply_to_peer_id | flags.0?Peer | flags.0 | — | No description provided by the pinned schema. |
| reply_from | flags.5?MessageFwdHeader | flags.5 | — | No description provided by the pinned schema. |
| reply_media | flags.8?MessageMedia | flags.8 | — | No description provided by the pinned schema. |
| reply_to_top_id | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| quote_text | flags.6?string | flags.6 | — | No description provided by the pinned schema. |
| quote_entities | flags.7?Vector<MessageEntity> | flags.7 | — | No description provided by the pinned schema. |
| quote_offset | flags.10?int | flags.10 | — | No description provided by the pinned schema. |
| todo_item_id | flags.11?int | flags.11 | — | No description provided by the pinned schema. |
| poll_option | flags.12?bytes | flags.12 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| reply_to_scheduled | 2 | Controlled by `flags`; present when this bit is set. |
| forum_topic | 3 | Controlled by `flags`; present when this bit is set. |
| quote | 9 | Controlled by `flags`; present when this bit is set. |
| reply_to_ephemeral | 13 | Controlled by `flags`; present when this bit is set. |
| reply_to_msg_id | 4 | Controlled by `flags`; present when this bit is set. |
| reply_to_peer_id | 0 | Controlled by `flags`; present when this bit is set. |
| reply_from | 5 | Controlled by `flags`; present when this bit is set. |
| reply_media | 8 | Controlled by `flags`; present when this bit is set. |
| reply_to_top_id | 1 | Controlled by `flags`; present when this bit is set. |
| quote_text | 6 | Controlled by `flags`; present when this bit is set. |
| quote_entities | 7 | Controlled by `flags`; present when this bit is set. |
| quote_offset | 10 | Controlled by `flags`; present when this bit is set. |
| todo_item_id | 11 | Controlled by `flags`; present when this bit is set. |
| poll_option | 12 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageReplyHeader
```

Public access: `miniproto.raw.types.MessageReplyHeader`.

## Safe usage shape

```python
from miniproto.raw.types import MessageReplyHeader

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageReplyHeader
```

## Result family

[`MessageReplyHeader`](/reference/telegram/types/results/message-reply-header/)

## Relationships

- Result family: [`MessageReplyHeader`](/reference/telegram/types/results/message-reply-header/)
- Related constructors: [`messageReplyStoryHeader`](/reference/telegram/types/base/message-reply-story-header/)
- Accepted by: [`ephemeralMessage`](/reference/telegram/types/base/ephemeral-message/), [`message`](/reference/telegram/types/base/message/), [`messageService`](/reference/telegram/types/base/message-service/), [`updateShortChatMessage`](/reference/telegram/types/base/update-short-chat-message/), [`updateShortMessage`](/reference/telegram/types/base/update-short-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
