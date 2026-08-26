---
title: "channelFull"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelFull"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa04e8d3a"
---

# `channelFull`

No description provided by the pinned schema.

## Signature

```tl
channelFull#a04e8d3a flags:# can_view_participants:flags.3?true can_set_username:flags.6?true can_set_stickers:flags.7?true hidden_prehistory:flags.10?true can_set_location:flags.16?true has_scheduled:flags.19?true can_view_stats:flags.20?true blocked:flags.22?true flags2:# can_delete_channel:flags2.0?true antispam:flags2.1?true participants_hidden:flags2.2?true translations_disabled:flags2.3?true stories_pinned_available:flags2.5?true view_forum_as_messages:flags2.6?true restricted_sponsored:flags2.11?true can_view_revenue:flags2.12?true paid_media_allowed:flags2.14?true can_view_stars_revenue:flags2.15?true paid_reactions_available:flags2.16?true stargifts_available:flags2.19?true paid_messages_available:flags2.20?true has_welcome_messages:flags2.24?true id:long about:string participants_count:flags.0?int admins_count:flags.1?int kicked_count:flags.2?int banned_count:flags.2?int online_count:flags.13?int read_inbox_max_id:int read_outbox_max_id:int unread_count:int chat_photo:Photo notify_settings:PeerNotifySettings exported_invite:flags.23?ExportedChatInvite bot_info:Vector<BotInfo> migrated_from_chat_id:flags.4?long migrated_from_max_id:flags.4?int pinned_msg_id:flags.5?int stickerset:flags.8?StickerSet available_min_id:flags.9?int folder_id:flags.11?int linked_chat_id:flags.14?long location:flags.15?ChannelLocation slowmode_seconds:flags.17?int slowmode_next_send_date:flags.18?int stats_dc:flags.12?int pts:int call:flags.21?InputGroupCall ttl_period:flags.24?int pending_suggestions:flags.25?Vector<string> groupcall_default_join_as:flags.26?Peer theme_emoticon:flags.27?string requests_pending:flags.28?int recent_requesters:flags.28?Vector<long> default_send_as:flags.29?Peer available_reactions:flags.30?ChatReactions reactions_limit:flags2.13?int stories:flags2.4?PeerStories wallpaper:flags2.7?WallPaper boosts_applied:flags2.8?int boosts_unrestrict:flags2.9?int emojiset:flags2.10?StickerSet bot_verification:flags2.17?BotVerification stargifts_count:flags2.18?int send_paid_messages_stars:flags2.21?long main_tab:flags2.22?ProfileTab guard_bot_id:flags2.23?long = ChatFull;
```

## Result type

`ChatFull`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| can_view_participants | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| can_set_username | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| can_set_stickers | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| hidden_prehistory | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| can_set_location | flags.16?true | flags.16 | — | No description provided by the pinned schema. |
| has_scheduled | flags.19?true | flags.19 | — | No description provided by the pinned schema. |
| can_view_stats | flags.20?true | flags.20 | — | No description provided by the pinned schema. |
| blocked | flags.22?true | flags.22 | — | No description provided by the pinned schema. |
| flags2 | # | flag word | — | No description provided by the pinned schema. |
| can_delete_channel | flags2.0?true | flags2.0 | — | No description provided by the pinned schema. |
| antispam | flags2.1?true | flags2.1 | — | No description provided by the pinned schema. |
| participants_hidden | flags2.2?true | flags2.2 | — | No description provided by the pinned schema. |
| translations_disabled | flags2.3?true | flags2.3 | — | No description provided by the pinned schema. |
| stories_pinned_available | flags2.5?true | flags2.5 | — | No description provided by the pinned schema. |
| view_forum_as_messages | flags2.6?true | flags2.6 | — | No description provided by the pinned schema. |
| restricted_sponsored | flags2.11?true | flags2.11 | — | No description provided by the pinned schema. |
| can_view_revenue | flags2.12?true | flags2.12 | — | No description provided by the pinned schema. |
| paid_media_allowed | flags2.14?true | flags2.14 | — | No description provided by the pinned schema. |
| can_view_stars_revenue | flags2.15?true | flags2.15 | — | No description provided by the pinned schema. |
| paid_reactions_available | flags2.16?true | flags2.16 | — | No description provided by the pinned schema. |
| stargifts_available | flags2.19?true | flags2.19 | — | No description provided by the pinned schema. |
| paid_messages_available | flags2.20?true | flags2.20 | — | No description provided by the pinned schema. |
| has_welcome_messages | flags2.24?true | flags2.24 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| about | string | — | — | No description provided by the pinned schema. |
| participants_count | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| admins_count | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| kicked_count | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| banned_count | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| online_count | flags.13?int | flags.13 | — | No description provided by the pinned schema. |
| read_inbox_max_id | int | — | — | No description provided by the pinned schema. |
| read_outbox_max_id | int | — | — | No description provided by the pinned schema. |
| unread_count | int | — | — | No description provided by the pinned schema. |
| chat_photo | Photo | — | — | No description provided by the pinned schema. |
| notify_settings | PeerNotifySettings | — | — | No description provided by the pinned schema. |
| exported_invite | flags.23?ExportedChatInvite | flags.23 | — | No description provided by the pinned schema. |
| bot_info | Vector<BotInfo> | — | — | No description provided by the pinned schema. |
| migrated_from_chat_id | flags.4?long | flags.4 | — | No description provided by the pinned schema. |
| migrated_from_max_id | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| pinned_msg_id | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| stickerset | flags.8?StickerSet | flags.8 | — | No description provided by the pinned schema. |
| available_min_id | flags.9?int | flags.9 | — | No description provided by the pinned schema. |
| folder_id | flags.11?int | flags.11 | — | No description provided by the pinned schema. |
| linked_chat_id | flags.14?long | flags.14 | — | No description provided by the pinned schema. |
| location | flags.15?ChannelLocation | flags.15 | — | No description provided by the pinned schema. |
| slowmode_seconds | flags.17?int | flags.17 | — | No description provided by the pinned schema. |
| slowmode_next_send_date | flags.18?int | flags.18 | — | No description provided by the pinned schema. |
| stats_dc | flags.12?int | flags.12 | — | No description provided by the pinned schema. |
| pts | int | — | — | No description provided by the pinned schema. |
| call | flags.21?InputGroupCall | flags.21 | — | No description provided by the pinned schema. |
| ttl_period | flags.24?int | flags.24 | — | No description provided by the pinned schema. |
| pending_suggestions | flags.25?Vector<string> | flags.25 | — | No description provided by the pinned schema. |
| groupcall_default_join_as | flags.26?Peer | flags.26 | — | No description provided by the pinned schema. |
| theme_emoticon | flags.27?string | flags.27 | — | No description provided by the pinned schema. |
| requests_pending | flags.28?int | flags.28 | — | No description provided by the pinned schema. |
| recent_requesters | flags.28?Vector<long> | flags.28 | — | No description provided by the pinned schema. |
| default_send_as | flags.29?Peer | flags.29 | — | No description provided by the pinned schema. |
| available_reactions | flags.30?ChatReactions | flags.30 | — | No description provided by the pinned schema. |
| reactions_limit | flags2.13?int | flags2.13 | — | No description provided by the pinned schema. |
| stories | flags2.4?PeerStories | flags2.4 | — | No description provided by the pinned schema. |
| wallpaper | flags2.7?WallPaper | flags2.7 | — | No description provided by the pinned schema. |
| boosts_applied | flags2.8?int | flags2.8 | — | No description provided by the pinned schema. |
| boosts_unrestrict | flags2.9?int | flags2.9 | — | No description provided by the pinned schema. |
| emojiset | flags2.10?StickerSet | flags2.10 | — | No description provided by the pinned schema. |
| bot_verification | flags2.17?BotVerification | flags2.17 | — | No description provided by the pinned schema. |
| stargifts_count | flags2.18?int | flags2.18 | — | No description provided by the pinned schema. |
| send_paid_messages_stars | flags2.21?long | flags2.21 | — | No description provided by the pinned schema. |
| main_tab | flags2.22?ProfileTab | flags2.22 | — | No description provided by the pinned schema. |
| guard_bot_id | flags2.23?long | flags2.23 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| can_view_participants | 3 | Controlled by `flags`; present when this bit is set. |
| can_set_username | 6 | Controlled by `flags`; present when this bit is set. |
| can_set_stickers | 7 | Controlled by `flags`; present when this bit is set. |
| hidden_prehistory | 10 | Controlled by `flags`; present when this bit is set. |
| can_set_location | 16 | Controlled by `flags`; present when this bit is set. |
| has_scheduled | 19 | Controlled by `flags`; present when this bit is set. |
| can_view_stats | 20 | Controlled by `flags`; present when this bit is set. |
| blocked | 22 | Controlled by `flags`; present when this bit is set. |
| can_delete_channel | 0 | Controlled by `flags2`; present when this bit is set. |
| antispam | 1 | Controlled by `flags2`; present when this bit is set. |
| participants_hidden | 2 | Controlled by `flags2`; present when this bit is set. |
| translations_disabled | 3 | Controlled by `flags2`; present when this bit is set. |
| stories_pinned_available | 5 | Controlled by `flags2`; present when this bit is set. |
| view_forum_as_messages | 6 | Controlled by `flags2`; present when this bit is set. |
| restricted_sponsored | 11 | Controlled by `flags2`; present when this bit is set. |
| can_view_revenue | 12 | Controlled by `flags2`; present when this bit is set. |
| paid_media_allowed | 14 | Controlled by `flags2`; present when this bit is set. |
| can_view_stars_revenue | 15 | Controlled by `flags2`; present when this bit is set. |
| paid_reactions_available | 16 | Controlled by `flags2`; present when this bit is set. |
| stargifts_available | 19 | Controlled by `flags2`; present when this bit is set. |
| paid_messages_available | 20 | Controlled by `flags2`; present when this bit is set. |
| has_welcome_messages | 24 | Controlled by `flags2`; present when this bit is set. |
| participants_count | 0 | Controlled by `flags`; present when this bit is set. |
| admins_count | 1 | Controlled by `flags`; present when this bit is set. |
| kicked_count | 2 | Controlled by `flags`; present when this bit is set. |
| banned_count | 2 | Controlled by `flags`; present when this bit is set. |
| online_count | 13 | Controlled by `flags`; present when this bit is set. |
| exported_invite | 23 | Controlled by `flags`; present when this bit is set. |
| migrated_from_chat_id | 4 | Controlled by `flags`; present when this bit is set. |
| migrated_from_max_id | 4 | Controlled by `flags`; present when this bit is set. |
| pinned_msg_id | 5 | Controlled by `flags`; present when this bit is set. |
| stickerset | 8 | Controlled by `flags`; present when this bit is set. |
| available_min_id | 9 | Controlled by `flags`; present when this bit is set. |
| folder_id | 11 | Controlled by `flags`; present when this bit is set. |
| linked_chat_id | 14 | Controlled by `flags`; present when this bit is set. |
| location | 15 | Controlled by `flags`; present when this bit is set. |
| slowmode_seconds | 17 | Controlled by `flags`; present when this bit is set. |
| slowmode_next_send_date | 18 | Controlled by `flags`; present when this bit is set. |
| stats_dc | 12 | Controlled by `flags`; present when this bit is set. |
| call | 21 | Controlled by `flags`; present when this bit is set. |
| ttl_period | 24 | Controlled by `flags`; present when this bit is set. |
| pending_suggestions | 25 | Controlled by `flags`; present when this bit is set. |
| groupcall_default_join_as | 26 | Controlled by `flags`; present when this bit is set. |
| theme_emoticon | 27 | Controlled by `flags`; present when this bit is set. |
| requests_pending | 28 | Controlled by `flags`; present when this bit is set. |
| recent_requesters | 28 | Controlled by `flags`; present when this bit is set. |
| default_send_as | 29 | Controlled by `flags`; present when this bit is set. |
| available_reactions | 30 | Controlled by `flags`; present when this bit is set. |
| reactions_limit | 13 | Controlled by `flags2`; present when this bit is set. |
| stories | 4 | Controlled by `flags2`; present when this bit is set. |
| wallpaper | 7 | Controlled by `flags2`; present when this bit is set. |
| boosts_applied | 8 | Controlled by `flags2`; present when this bit is set. |
| boosts_unrestrict | 9 | Controlled by `flags2`; present when this bit is set. |
| emojiset | 10 | Controlled by `flags2`; present when this bit is set. |
| bot_verification | 17 | Controlled by `flags2`; present when this bit is set. |
| stargifts_count | 18 | Controlled by `flags2`; present when this bit is set. |
| send_paid_messages_stars | 21 | Controlled by `flags2`; present when this bit is set. |
| main_tab | 22 | Controlled by `flags2`; present when this bit is set. |
| guard_bot_id | 23 | Controlled by `flags2`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChannelFull
```

Public access: `miniproto.raw.types.ChannelFull`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelFull

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelFull
```

## Result family

[`ChatFull`](/reference/telegram/types/results/chat-full/)

## Relationships

- Result family: [`ChatFull`](/reference/telegram/types/results/chat-full/)
- Related constructors: [`chatFull`](/reference/telegram/types/base/chat-full/), [`communityFull`](/reference/telegram/types/base/community-full/)
- Accepted by: [`messages.chatFull`](/reference/telegram/types/messages/chat-full/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
