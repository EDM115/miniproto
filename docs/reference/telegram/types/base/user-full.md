---
title: "userFull"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "userFull"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x06cbe645"
---

# `userFull`

No description provided by the pinned schema.

## Signature

```tl
userFull#06cbe645 flags:# blocked:flags.0?true phone_calls_available:flags.4?true phone_calls_private:flags.5?true can_pin_message:flags.7?true has_scheduled:flags.12?true video_calls_available:flags.13?true voice_messages_forbidden:flags.20?true translations_disabled:flags.23?true stories_pinned_available:flags.26?true blocked_my_stories_from:flags.27?true wallpaper_overridden:flags.28?true contact_require_premium:flags.29?true read_dates_private:flags.30?true flags2:# sponsored_enabled:flags2.7?true can_view_revenue:flags2.9?true bot_can_manage_emoji_status:flags2.10?true display_gifts_button:flags2.16?true noforwards_my_enabled:flags2.23?true noforwards_peer_enabled:flags2.24?true unofficial_security_risk:flags2.26?true id:long about:flags.1?string settings:PeerSettings personal_photo:flags.21?Photo profile_photo:flags.2?Photo fallback_photo:flags.22?Photo notify_settings:PeerNotifySettings bot_info:flags.3?BotInfo pinned_msg_id:flags.6?int common_chats_count:int folder_id:flags.11?int ttl_period:flags.14?int theme:flags.15?ChatTheme private_forward_name:flags.16?string bot_group_admin_rights:flags.17?ChatAdminRights bot_broadcast_admin_rights:flags.18?ChatAdminRights wallpaper:flags.24?WallPaper stories:flags.25?PeerStories business_work_hours:flags2.0?BusinessWorkHours business_location:flags2.1?BusinessLocation business_greeting_message:flags2.2?BusinessGreetingMessage business_away_message:flags2.3?BusinessAwayMessage business_intro:flags2.4?BusinessIntro birthday:flags2.5?Birthday personal_channel_id:flags2.6?long personal_channel_message:flags2.6?int stargifts_count:flags2.8?int starref_program:flags2.11?StarRefProgram bot_verification:flags2.12?BotVerification send_paid_messages_stars:flags2.14?long disallowed_gifts:flags2.15?DisallowedGiftsSettings stars_rating:flags2.17?StarsRating stars_my_pending_rating:flags2.18?StarsRating stars_my_pending_rating_date:flags2.18?int main_tab:flags2.20?ProfileTab saved_music:flags2.21?Document note:flags2.22?TextWithEntities bot_manager_id:flags2.25?long = UserFull;
```

## Result type

`UserFull`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| blocked | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| phone_calls_available | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| phone_calls_private | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| can_pin_message | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| has_scheduled | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| video_calls_available | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| voice_messages_forbidden | flags.20?true | flags.20 | — | No description provided by the pinned schema. |
| translations_disabled | flags.23?true | flags.23 | — | No description provided by the pinned schema. |
| stories_pinned_available | flags.26?true | flags.26 | — | No description provided by the pinned schema. |
| blocked_my_stories_from | flags.27?true | flags.27 | — | No description provided by the pinned schema. |
| wallpaper_overridden | flags.28?true | flags.28 | — | No description provided by the pinned schema. |
| contact_require_premium | flags.29?true | flags.29 | — | No description provided by the pinned schema. |
| read_dates_private | flags.30?true | flags.30 | — | No description provided by the pinned schema. |
| flags2 | # | flag word | — | No description provided by the pinned schema. |
| sponsored_enabled | flags2.7?true | flags2.7 | — | No description provided by the pinned schema. |
| can_view_revenue | flags2.9?true | flags2.9 | — | No description provided by the pinned schema. |
| bot_can_manage_emoji_status | flags2.10?true | flags2.10 | — | No description provided by the pinned schema. |
| display_gifts_button | flags2.16?true | flags2.16 | — | No description provided by the pinned schema. |
| noforwards_my_enabled | flags2.23?true | flags2.23 | — | No description provided by the pinned schema. |
| noforwards_peer_enabled | flags2.24?true | flags2.24 | — | No description provided by the pinned schema. |
| unofficial_security_risk | flags2.26?true | flags2.26 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| about | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| settings | PeerSettings | — | — | No description provided by the pinned schema. |
| personal_photo | flags.21?Photo | flags.21 | — | No description provided by the pinned schema. |
| profile_photo | flags.2?Photo | flags.2 | — | No description provided by the pinned schema. |
| fallback_photo | flags.22?Photo | flags.22 | — | No description provided by the pinned schema. |
| notify_settings | PeerNotifySettings | — | — | No description provided by the pinned schema. |
| bot_info | flags.3?BotInfo | flags.3 | — | No description provided by the pinned schema. |
| pinned_msg_id | flags.6?int | flags.6 | — | No description provided by the pinned schema. |
| common_chats_count | int | — | — | No description provided by the pinned schema. |
| folder_id | flags.11?int | flags.11 | — | No description provided by the pinned schema. |
| ttl_period | flags.14?int | flags.14 | — | No description provided by the pinned schema. |
| theme | flags.15?ChatTheme | flags.15 | — | No description provided by the pinned schema. |
| private_forward_name | flags.16?string | flags.16 | — | No description provided by the pinned schema. |
| bot_group_admin_rights | flags.17?ChatAdminRights | flags.17 | — | No description provided by the pinned schema. |
| bot_broadcast_admin_rights | flags.18?ChatAdminRights | flags.18 | — | No description provided by the pinned schema. |
| wallpaper | flags.24?WallPaper | flags.24 | — | No description provided by the pinned schema. |
| stories | flags.25?PeerStories | flags.25 | — | No description provided by the pinned schema. |
| business_work_hours | flags2.0?BusinessWorkHours | flags2.0 | — | No description provided by the pinned schema. |
| business_location | flags2.1?BusinessLocation | flags2.1 | — | No description provided by the pinned schema. |
| business_greeting_message | flags2.2?BusinessGreetingMessage | flags2.2 | — | No description provided by the pinned schema. |
| business_away_message | flags2.3?BusinessAwayMessage | flags2.3 | — | No description provided by the pinned schema. |
| business_intro | flags2.4?BusinessIntro | flags2.4 | — | No description provided by the pinned schema. |
| birthday | flags2.5?Birthday | flags2.5 | — | No description provided by the pinned schema. |
| personal_channel_id | flags2.6?long | flags2.6 | — | No description provided by the pinned schema. |
| personal_channel_message | flags2.6?int | flags2.6 | — | No description provided by the pinned schema. |
| stargifts_count | flags2.8?int | flags2.8 | — | No description provided by the pinned schema. |
| starref_program | flags2.11?StarRefProgram | flags2.11 | — | No description provided by the pinned schema. |
| bot_verification | flags2.12?BotVerification | flags2.12 | — | No description provided by the pinned schema. |
| send_paid_messages_stars | flags2.14?long | flags2.14 | — | No description provided by the pinned schema. |
| disallowed_gifts | flags2.15?DisallowedGiftsSettings | flags2.15 | — | No description provided by the pinned schema. |
| stars_rating | flags2.17?StarsRating | flags2.17 | — | No description provided by the pinned schema. |
| stars_my_pending_rating | flags2.18?StarsRating | flags2.18 | — | No description provided by the pinned schema. |
| stars_my_pending_rating_date | flags2.18?int | flags2.18 | — | No description provided by the pinned schema. |
| main_tab | flags2.20?ProfileTab | flags2.20 | — | No description provided by the pinned schema. |
| saved_music | flags2.21?Document | flags2.21 | — | No description provided by the pinned schema. |
| note | flags2.22?TextWithEntities | flags2.22 | — | No description provided by the pinned schema. |
| bot_manager_id | flags2.25?long | flags2.25 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| blocked | 0 | Controlled by `flags`; present when this bit is set. |
| phone_calls_available | 4 | Controlled by `flags`; present when this bit is set. |
| phone_calls_private | 5 | Controlled by `flags`; present when this bit is set. |
| can_pin_message | 7 | Controlled by `flags`; present when this bit is set. |
| has_scheduled | 12 | Controlled by `flags`; present when this bit is set. |
| video_calls_available | 13 | Controlled by `flags`; present when this bit is set. |
| voice_messages_forbidden | 20 | Controlled by `flags`; present when this bit is set. |
| translations_disabled | 23 | Controlled by `flags`; present when this bit is set. |
| stories_pinned_available | 26 | Controlled by `flags`; present when this bit is set. |
| blocked_my_stories_from | 27 | Controlled by `flags`; present when this bit is set. |
| wallpaper_overridden | 28 | Controlled by `flags`; present when this bit is set. |
| contact_require_premium | 29 | Controlled by `flags`; present when this bit is set. |
| read_dates_private | 30 | Controlled by `flags`; present when this bit is set. |
| sponsored_enabled | 7 | Controlled by `flags2`; present when this bit is set. |
| can_view_revenue | 9 | Controlled by `flags2`; present when this bit is set. |
| bot_can_manage_emoji_status | 10 | Controlled by `flags2`; present when this bit is set. |
| display_gifts_button | 16 | Controlled by `flags2`; present when this bit is set. |
| noforwards_my_enabled | 23 | Controlled by `flags2`; present when this bit is set. |
| noforwards_peer_enabled | 24 | Controlled by `flags2`; present when this bit is set. |
| unofficial_security_risk | 26 | Controlled by `flags2`; present when this bit is set. |
| about | 1 | Controlled by `flags`; present when this bit is set. |
| personal_photo | 21 | Controlled by `flags`; present when this bit is set. |
| profile_photo | 2 | Controlled by `flags`; present when this bit is set. |
| fallback_photo | 22 | Controlled by `flags`; present when this bit is set. |
| bot_info | 3 | Controlled by `flags`; present when this bit is set. |
| pinned_msg_id | 6 | Controlled by `flags`; present when this bit is set. |
| folder_id | 11 | Controlled by `flags`; present when this bit is set. |
| ttl_period | 14 | Controlled by `flags`; present when this bit is set. |
| theme | 15 | Controlled by `flags`; present when this bit is set. |
| private_forward_name | 16 | Controlled by `flags`; present when this bit is set. |
| bot_group_admin_rights | 17 | Controlled by `flags`; present when this bit is set. |
| bot_broadcast_admin_rights | 18 | Controlled by `flags`; present when this bit is set. |
| wallpaper | 24 | Controlled by `flags`; present when this bit is set. |
| stories | 25 | Controlled by `flags`; present when this bit is set. |
| business_work_hours | 0 | Controlled by `flags2`; present when this bit is set. |
| business_location | 1 | Controlled by `flags2`; present when this bit is set. |
| business_greeting_message | 2 | Controlled by `flags2`; present when this bit is set. |
| business_away_message | 3 | Controlled by `flags2`; present when this bit is set. |
| business_intro | 4 | Controlled by `flags2`; present when this bit is set. |
| birthday | 5 | Controlled by `flags2`; present when this bit is set. |
| personal_channel_id | 6 | Controlled by `flags2`; present when this bit is set. |
| personal_channel_message | 6 | Controlled by `flags2`; present when this bit is set. |
| stargifts_count | 8 | Controlled by `flags2`; present when this bit is set. |
| starref_program | 11 | Controlled by `flags2`; present when this bit is set. |
| bot_verification | 12 | Controlled by `flags2`; present when this bit is set. |
| send_paid_messages_stars | 14 | Controlled by `flags2`; present when this bit is set. |
| disallowed_gifts | 15 | Controlled by `flags2`; present when this bit is set. |
| stars_rating | 17 | Controlled by `flags2`; present when this bit is set. |
| stars_my_pending_rating | 18 | Controlled by `flags2`; present when this bit is set. |
| stars_my_pending_rating_date | 18 | Controlled by `flags2`; present when this bit is set. |
| main_tab | 20 | Controlled by `flags2`; present when this bit is set. |
| saved_music | 21 | Controlled by `flags2`; present when this bit is set. |
| note | 22 | Controlled by `flags2`; present when this bit is set. |
| bot_manager_id | 25 | Controlled by `flags2`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import UserFull
```

Public access: `miniproto.raw.types.UserFull`.

## Safe usage shape

```python
from miniproto.raw.types import UserFull

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UserFull
```

## Result family

[`UserFull`](/reference/telegram/types/results/user-full/)

## Relationships

- Result family: [`UserFull`](/reference/telegram/types/results/user-full/)
- Accepted by: [`users.userFull`](/reference/telegram/types/users/user-full/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
