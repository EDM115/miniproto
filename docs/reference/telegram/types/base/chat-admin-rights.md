---
title: "chatAdminRights"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatAdminRights"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5fb224d5"
---

# `chatAdminRights`

No description provided by the pinned schema.

## Signature

```tl
chatAdminRights#5fb224d5 flags:# change_info:flags.0?true post_messages:flags.1?true edit_messages:flags.2?true delete_messages:flags.3?true ban_users:flags.4?true invite_users:flags.5?true pin_messages:flags.7?true add_admins:flags.9?true anonymous:flags.10?true manage_call:flags.11?true other:flags.12?true manage_topics:flags.13?true post_stories:flags.14?true edit_stories:flags.15?true delete_stories:flags.16?true manage_direct_messages:flags.17?true manage_ranks:flags.18?true manage_linked_peers:flags.19?true = ChatAdminRights;
```

## Result type

`ChatAdminRights`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| change_info | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| post_messages | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| edit_messages | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| delete_messages | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| ban_users | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| invite_users | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| pin_messages | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| add_admins | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| anonymous | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| manage_call | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| other | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| manage_topics | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| post_stories | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| edit_stories | flags.15?true | flags.15 | — | No description provided by the pinned schema. |
| delete_stories | flags.16?true | flags.16 | — | No description provided by the pinned schema. |
| manage_direct_messages | flags.17?true | flags.17 | — | No description provided by the pinned schema. |
| manage_ranks | flags.18?true | flags.18 | — | No description provided by the pinned schema. |
| manage_linked_peers | flags.19?true | flags.19 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| change_info | 0 | Controlled by `flags`; present when this bit is set. |
| post_messages | 1 | Controlled by `flags`; present when this bit is set. |
| edit_messages | 2 | Controlled by `flags`; present when this bit is set. |
| delete_messages | 3 | Controlled by `flags`; present when this bit is set. |
| ban_users | 4 | Controlled by `flags`; present when this bit is set. |
| invite_users | 5 | Controlled by `flags`; present when this bit is set. |
| pin_messages | 7 | Controlled by `flags`; present when this bit is set. |
| add_admins | 9 | Controlled by `flags`; present when this bit is set. |
| anonymous | 10 | Controlled by `flags`; present when this bit is set. |
| manage_call | 11 | Controlled by `flags`; present when this bit is set. |
| other | 12 | Controlled by `flags`; present when this bit is set. |
| manage_topics | 13 | Controlled by `flags`; present when this bit is set. |
| post_stories | 14 | Controlled by `flags`; present when this bit is set. |
| edit_stories | 15 | Controlled by `flags`; present when this bit is set. |
| delete_stories | 16 | Controlled by `flags`; present when this bit is set. |
| manage_direct_messages | 17 | Controlled by `flags`; present when this bit is set. |
| manage_ranks | 18 | Controlled by `flags`; present when this bit is set. |
| manage_linked_peers | 19 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatAdminRights
```

Public access: `miniproto.raw.types.ChatAdminRights`.

## Safe usage shape

```python
from miniproto.raw.types import ChatAdminRights

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatAdminRights
```

## Result family

[`ChatAdminRights`](/reference/telegram/types/results/chat-admin-rights/)

## Relationships

- Result family: [`ChatAdminRights`](/reference/telegram/types/results/chat-admin-rights/)
- Accepted by: [`bots.setBotBroadcastDefaultAdminRights`](/reference/telegram/functions/bots/set-bot-broadcast-default-admin-rights/), [`bots.setBotGroupDefaultAdminRights`](/reference/telegram/functions/bots/set-bot-group-default-admin-rights/), [`channels.editAdmin`](/reference/telegram/functions/channels/edit-admin/), [`channel`](/reference/telegram/types/base/channel/), [`channelParticipantAdmin`](/reference/telegram/types/base/channel-participant-admin/), [`channelParticipantCreator`](/reference/telegram/types/base/channel-participant-creator/), [`chat`](/reference/telegram/types/base/chat/), [`community`](/reference/telegram/types/base/community/), [`requestPeerTypeBroadcast`](/reference/telegram/types/base/request-peer-type-broadcast/), [`requestPeerTypeChat`](/reference/telegram/types/base/request-peer-type-chat/), [`userFull`](/reference/telegram/types/base/user-full/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
