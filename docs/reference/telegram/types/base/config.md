---
title: "config"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "config"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xcc1a241e"
---

# `config`

No description provided by the pinned schema.

## Signature

```tl
config#cc1a241e flags:# default_p2p_contacts:flags.3?true preload_featured_stickers:flags.4?true revoke_pm_inbox:flags.6?true blocked_mode:flags.8?true force_try_ipv6:flags.14?true date:int expires:int test_mode:Bool this_dc:int dc_options:Vector<DcOption> dc_txt_domain_name:string chat_size_max:int megagroup_size_max:int forwarded_count_max:int online_update_period_ms:int offline_blur_timeout_ms:int offline_idle_timeout_ms:int online_cloud_timeout_ms:int notify_cloud_delay_ms:int notify_default_delay_ms:int push_chat_period_ms:int push_chat_limit:int edit_time_limit:int revoke_time_limit:int revoke_pm_time_limit:int rating_e_decay:int stickers_recent_limit:int channels_read_media_period:int tmp_sessions:flags.0?int call_receive_timeout_ms:int call_ring_timeout_ms:int call_connect_timeout_ms:int call_packet_timeout_ms:int me_url_prefix:string autoupdate_url_prefix:flags.7?string gif_search_username:flags.9?string venue_search_username:flags.10?string img_search_username:flags.11?string static_maps_provider:flags.12?string caption_length_max:int message_length_max:int webfile_dc_id:int suggested_lang_code:flags.2?string lang_pack_version:flags.2?int base_lang_pack_version:flags.2?int reactions_default:flags.15?Reaction autologin_token:flags.16?string = Config;
```

## Result type

`Config`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| default_p2p_contacts | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| preload_featured_stickers | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| revoke_pm_inbox | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| blocked_mode | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| force_try_ipv6 | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |
| test_mode | Bool | — | — | No description provided by the pinned schema. |
| this_dc | int | — | — | No description provided by the pinned schema. |
| dc_options | Vector<DcOption> | — | — | No description provided by the pinned schema. |
| dc_txt_domain_name | string | — | — | No description provided by the pinned schema. |
| chat_size_max | int | — | — | No description provided by the pinned schema. |
| megagroup_size_max | int | — | — | No description provided by the pinned schema. |
| forwarded_count_max | int | — | — | No description provided by the pinned schema. |
| online_update_period_ms | int | — | — | No description provided by the pinned schema. |
| offline_blur_timeout_ms | int | — | — | No description provided by the pinned schema. |
| offline_idle_timeout_ms | int | — | — | No description provided by the pinned schema. |
| online_cloud_timeout_ms | int | — | — | No description provided by the pinned schema. |
| notify_cloud_delay_ms | int | — | — | No description provided by the pinned schema. |
| notify_default_delay_ms | int | — | — | No description provided by the pinned schema. |
| push_chat_period_ms | int | — | — | No description provided by the pinned schema. |
| push_chat_limit | int | — | — | No description provided by the pinned schema. |
| edit_time_limit | int | — | — | No description provided by the pinned schema. |
| revoke_time_limit | int | — | — | No description provided by the pinned schema. |
| revoke_pm_time_limit | int | — | — | No description provided by the pinned schema. |
| rating_e_decay | int | — | — | No description provided by the pinned schema. |
| stickers_recent_limit | int | — | — | No description provided by the pinned schema. |
| channels_read_media_period | int | — | — | No description provided by the pinned schema. |
| tmp_sessions | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| call_receive_timeout_ms | int | — | — | No description provided by the pinned schema. |
| call_ring_timeout_ms | int | — | — | No description provided by the pinned schema. |
| call_connect_timeout_ms | int | — | — | No description provided by the pinned schema. |
| call_packet_timeout_ms | int | — | — | No description provided by the pinned schema. |
| me_url_prefix | string | — | — | No description provided by the pinned schema. |
| autoupdate_url_prefix | flags.7?string | flags.7 | — | No description provided by the pinned schema. |
| gif_search_username | flags.9?string | flags.9 | — | No description provided by the pinned schema. |
| venue_search_username | flags.10?string | flags.10 | — | No description provided by the pinned schema. |
| img_search_username | flags.11?string | flags.11 | — | No description provided by the pinned schema. |
| static_maps_provider | flags.12?string | flags.12 | — | No description provided by the pinned schema. |
| caption_length_max | int | — | — | No description provided by the pinned schema. |
| message_length_max | int | — | — | No description provided by the pinned schema. |
| webfile_dc_id | int | — | — | No description provided by the pinned schema. |
| suggested_lang_code | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| lang_pack_version | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| base_lang_pack_version | flags.2?int | flags.2 | — | No description provided by the pinned schema. |
| reactions_default | flags.15?Reaction | flags.15 | — | No description provided by the pinned schema. |
| autologin_token | flags.16?string | flags.16 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| default_p2p_contacts | 3 | Controlled by `flags`; present when this bit is set. |
| preload_featured_stickers | 4 | Controlled by `flags`; present when this bit is set. |
| revoke_pm_inbox | 6 | Controlled by `flags`; present when this bit is set. |
| blocked_mode | 8 | Controlled by `flags`; present when this bit is set. |
| force_try_ipv6 | 14 | Controlled by `flags`; present when this bit is set. |
| tmp_sessions | 0 | Controlled by `flags`; present when this bit is set. |
| autoupdate_url_prefix | 7 | Controlled by `flags`; present when this bit is set. |
| gif_search_username | 9 | Controlled by `flags`; present when this bit is set. |
| venue_search_username | 10 | Controlled by `flags`; present when this bit is set. |
| img_search_username | 11 | Controlled by `flags`; present when this bit is set. |
| static_maps_provider | 12 | Controlled by `flags`; present when this bit is set. |
| suggested_lang_code | 2 | Controlled by `flags`; present when this bit is set. |
| lang_pack_version | 2 | Controlled by `flags`; present when this bit is set. |
| base_lang_pack_version | 2 | Controlled by `flags`; present when this bit is set. |
| reactions_default | 15 | Controlled by `flags`; present when this bit is set. |
| autologin_token | 16 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Config
```

Public access: `miniproto.raw.types.Config`.

## Safe usage shape

```python
from miniproto.raw.types import Config

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Config
```

## Result family

[`Config`](/reference/telegram/types/results/config/)

## Relationships

- Result family: [`Config`](/reference/telegram/types/results/config/)
- Returned by: [`help.getConfig`](/reference/telegram/functions/help/get-config/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
