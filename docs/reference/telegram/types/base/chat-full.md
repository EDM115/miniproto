---
title: "chatFull"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatFull"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2633421b"
---

# `chatFull`

No description provided by the pinned schema.

## Signature

```tl
chatFull#2633421b flags:# can_set_username:flags.7?true has_scheduled:flags.8?true translations_disabled:flags.19?true id:long about:string participants:ChatParticipants chat_photo:flags.2?Photo notify_settings:PeerNotifySettings exported_invite:flags.13?ExportedChatInvite bot_info:flags.3?Vector<BotInfo> pinned_msg_id:flags.6?int folder_id:flags.11?int call:flags.12?InputGroupCall ttl_period:flags.14?int groupcall_default_join_as:flags.15?Peer theme_emoticon:flags.16?string requests_pending:flags.17?int recent_requesters:flags.17?Vector<long> available_reactions:flags.18?ChatReactions reactions_limit:flags.20?int = ChatFull;
```

## Result type

`ChatFull`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| can_set_username | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| has_scheduled | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| translations_disabled | flags.19?true | flags.19 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| about | string | — | — | No description provided by the pinned schema. |
| participants | ChatParticipants | — | — | No description provided by the pinned schema. |
| chat_photo | flags.2?Photo | flags.2 | — | No description provided by the pinned schema. |
| notify_settings | PeerNotifySettings | — | — | No description provided by the pinned schema. |
| exported_invite | flags.13?ExportedChatInvite | flags.13 | — | No description provided by the pinned schema. |
| bot_info | flags.3?Vector<BotInfo> | flags.3 | — | No description provided by the pinned schema. |
| pinned_msg_id | flags.6?int | flags.6 | — | No description provided by the pinned schema. |
| folder_id | flags.11?int | flags.11 | — | No description provided by the pinned schema. |
| call | flags.12?InputGroupCall | flags.12 | — | No description provided by the pinned schema. |
| ttl_period | flags.14?int | flags.14 | — | No description provided by the pinned schema. |
| groupcall_default_join_as | flags.15?Peer | flags.15 | — | No description provided by the pinned schema. |
| theme_emoticon | flags.16?string | flags.16 | — | No description provided by the pinned schema. |
| requests_pending | flags.17?int | flags.17 | — | No description provided by the pinned schema. |
| recent_requesters | flags.17?Vector<long> | flags.17 | — | No description provided by the pinned schema. |
| available_reactions | flags.18?ChatReactions | flags.18 | — | No description provided by the pinned schema. |
| reactions_limit | flags.20?int | flags.20 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| can_set_username | 7 | Controlled by `flags`; present when this bit is set. |
| has_scheduled | 8 | Controlled by `flags`; present when this bit is set. |
| translations_disabled | 19 | Controlled by `flags`; present when this bit is set. |
| chat_photo | 2 | Controlled by `flags`; present when this bit is set. |
| exported_invite | 13 | Controlled by `flags`; present when this bit is set. |
| bot_info | 3 | Controlled by `flags`; present when this bit is set. |
| pinned_msg_id | 6 | Controlled by `flags`; present when this bit is set. |
| folder_id | 11 | Controlled by `flags`; present when this bit is set. |
| call | 12 | Controlled by `flags`; present when this bit is set. |
| ttl_period | 14 | Controlled by `flags`; present when this bit is set. |
| groupcall_default_join_as | 15 | Controlled by `flags`; present when this bit is set. |
| theme_emoticon | 16 | Controlled by `flags`; present when this bit is set. |
| requests_pending | 17 | Controlled by `flags`; present when this bit is set. |
| recent_requesters | 17 | Controlled by `flags`; present when this bit is set. |
| available_reactions | 18 | Controlled by `flags`; present when this bit is set. |
| reactions_limit | 20 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatFull
```

Public access: `miniproto.raw.types.ChatFull`.

## Safe usage shape

```python
from miniproto.raw.types import ChatFull

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatFull
```

## Result family

[`ChatFull`](/reference/telegram/types/results/chat-full/)

## Relationships

- Result family: [`ChatFull`](/reference/telegram/types/results/chat-full/)
- Related constructors: [`channelFull`](/reference/telegram/types/base/channel-full/), [`communityFull`](/reference/telegram/types/base/community-full/)
- Accepted by: [`messages.chatFull`](/reference/telegram/types/messages/chat-full/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
