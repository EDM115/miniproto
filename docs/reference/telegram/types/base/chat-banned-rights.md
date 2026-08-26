---
title: "chatBannedRights"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatBannedRights"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x9f120418"
---

# `chatBannedRights`

No description provided by the pinned schema.

## Signature

```tl
chatBannedRights#9f120418 flags:# view_messages:flags.0?true send_messages:flags.1?true send_media:flags.2?true send_stickers:flags.3?true send_gifs:flags.4?true send_games:flags.5?true send_inline:flags.6?true embed_links:flags.7?true send_polls:flags.8?true change_info:flags.10?true invite_users:flags.15?true pin_messages:flags.17?true manage_topics:flags.18?true send_photos:flags.19?true send_videos:flags.20?true send_roundvideos:flags.21?true send_audios:flags.22?true send_voices:flags.23?true send_docs:flags.24?true send_plain:flags.25?true edit_rank:flags.26?true send_reactions:flags.27?true manage_linked_peers:flags.28?true until_date:int = ChatBannedRights;
```

## Result type

`ChatBannedRights`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| view_messages | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| send_messages | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| send_media | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| send_stickers | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| send_gifs | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| send_games | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| send_inline | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| embed_links | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| send_polls | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| change_info | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| invite_users | flags.15?true | flags.15 | — | No description provided by the pinned schema. |
| pin_messages | flags.17?true | flags.17 | — | No description provided by the pinned schema. |
| manage_topics | flags.18?true | flags.18 | — | No description provided by the pinned schema. |
| send_photos | flags.19?true | flags.19 | — | No description provided by the pinned schema. |
| send_videos | flags.20?true | flags.20 | — | No description provided by the pinned schema. |
| send_roundvideos | flags.21?true | flags.21 | — | No description provided by the pinned schema. |
| send_audios | flags.22?true | flags.22 | — | No description provided by the pinned schema. |
| send_voices | flags.23?true | flags.23 | — | No description provided by the pinned schema. |
| send_docs | flags.24?true | flags.24 | — | No description provided by the pinned schema. |
| send_plain | flags.25?true | flags.25 | — | No description provided by the pinned schema. |
| edit_rank | flags.26?true | flags.26 | — | No description provided by the pinned schema. |
| send_reactions | flags.27?true | flags.27 | — | No description provided by the pinned schema. |
| manage_linked_peers | flags.28?true | flags.28 | — | No description provided by the pinned schema. |
| until_date | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| view_messages | 0 | Controlled by `flags`; present when this bit is set. |
| send_messages | 1 | Controlled by `flags`; present when this bit is set. |
| send_media | 2 | Controlled by `flags`; present when this bit is set. |
| send_stickers | 3 | Controlled by `flags`; present when this bit is set. |
| send_gifs | 4 | Controlled by `flags`; present when this bit is set. |
| send_games | 5 | Controlled by `flags`; present when this bit is set. |
| send_inline | 6 | Controlled by `flags`; present when this bit is set. |
| embed_links | 7 | Controlled by `flags`; present when this bit is set. |
| send_polls | 8 | Controlled by `flags`; present when this bit is set. |
| change_info | 10 | Controlled by `flags`; present when this bit is set. |
| invite_users | 15 | Controlled by `flags`; present when this bit is set. |
| pin_messages | 17 | Controlled by `flags`; present when this bit is set. |
| manage_topics | 18 | Controlled by `flags`; present when this bit is set. |
| send_photos | 19 | Controlled by `flags`; present when this bit is set. |
| send_videos | 20 | Controlled by `flags`; present when this bit is set. |
| send_roundvideos | 21 | Controlled by `flags`; present when this bit is set. |
| send_audios | 22 | Controlled by `flags`; present when this bit is set. |
| send_voices | 23 | Controlled by `flags`; present when this bit is set. |
| send_docs | 24 | Controlled by `flags`; present when this bit is set. |
| send_plain | 25 | Controlled by `flags`; present when this bit is set. |
| edit_rank | 26 | Controlled by `flags`; present when this bit is set. |
| send_reactions | 27 | Controlled by `flags`; present when this bit is set. |
| manage_linked_peers | 28 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatBannedRights
```

Public access: `miniproto.raw.types.ChatBannedRights`.

## Safe usage shape

```python
from miniproto.raw.types import ChatBannedRights

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatBannedRights
```

## Result family

[`ChatBannedRights`](/reference/telegram/types/results/chat-banned-rights/)

## Relationships

- Result family: [`ChatBannedRights`](/reference/telegram/types/results/chat-banned-rights/)
- Accepted by: [`channels.editBanned`](/reference/telegram/functions/channels/edit-banned/), [`messages.editChatDefaultBannedRights`](/reference/telegram/functions/messages/edit-chat-default-banned-rights/), [`channel`](/reference/telegram/types/base/channel/), [`channelAdminLogEventActionDefaultBannedRights`](/reference/telegram/types/base/channel-admin-log-event-action-default-banned-rights/), [`channelParticipantBanned`](/reference/telegram/types/base/channel-participant-banned/), [`chat`](/reference/telegram/types/base/chat/), [`community`](/reference/telegram/types/base/community/), [`updateChatDefaultBannedRights`](/reference/telegram/types/base/update-chat-default-banned-rights/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
