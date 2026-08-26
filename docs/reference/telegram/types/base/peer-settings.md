---
title: "peerSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "peerSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf47741f7"
---

# `peerSettings`

No description provided by the pinned schema.

## Signature

```tl
peerSettings#f47741f7 flags:# report_spam:flags.0?true add_contact:flags.1?true block_contact:flags.2?true share_contact:flags.3?true need_contacts_exception:flags.4?true report_geo:flags.5?true autoarchived:flags.7?true invite_members:flags.8?true request_chat_broadcast:flags.10?true business_bot_paused:flags.11?true business_bot_can_reply:flags.12?true geo_distance:flags.6?int request_chat_title:flags.9?string request_chat_date:flags.9?int business_bot_id:flags.13?long business_bot_manage_url:flags.13?string charge_paid_message_stars:flags.14?long registration_month:flags.15?string phone_country:flags.16?string name_change_date:flags.17?int photo_change_date:flags.18?int = PeerSettings;
```

## Result type

`PeerSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| report_spam | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| add_contact | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| block_contact | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| share_contact | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| need_contacts_exception | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| report_geo | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| autoarchived | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| invite_members | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| request_chat_broadcast | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| business_bot_paused | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| business_bot_can_reply | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| geo_distance | flags.6?int | flags.6 | — | No description provided by the pinned schema. |
| request_chat_title | flags.9?string | flags.9 | — | No description provided by the pinned schema. |
| request_chat_date | flags.9?int | flags.9 | — | No description provided by the pinned schema. |
| business_bot_id | flags.13?long | flags.13 | — | No description provided by the pinned schema. |
| business_bot_manage_url | flags.13?string | flags.13 | — | No description provided by the pinned schema. |
| charge_paid_message_stars | flags.14?long | flags.14 | — | No description provided by the pinned schema. |
| registration_month | flags.15?string | flags.15 | — | No description provided by the pinned schema. |
| phone_country | flags.16?string | flags.16 | — | No description provided by the pinned schema. |
| name_change_date | flags.17?int | flags.17 | — | No description provided by the pinned schema. |
| photo_change_date | flags.18?int | flags.18 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| report_spam | 0 | Controlled by `flags`; present when this bit is set. |
| add_contact | 1 | Controlled by `flags`; present when this bit is set. |
| block_contact | 2 | Controlled by `flags`; present when this bit is set. |
| share_contact | 3 | Controlled by `flags`; present when this bit is set. |
| need_contacts_exception | 4 | Controlled by `flags`; present when this bit is set. |
| report_geo | 5 | Controlled by `flags`; present when this bit is set. |
| autoarchived | 7 | Controlled by `flags`; present when this bit is set. |
| invite_members | 8 | Controlled by `flags`; present when this bit is set. |
| request_chat_broadcast | 10 | Controlled by `flags`; present when this bit is set. |
| business_bot_paused | 11 | Controlled by `flags`; present when this bit is set. |
| business_bot_can_reply | 12 | Controlled by `flags`; present when this bit is set. |
| geo_distance | 6 | Controlled by `flags`; present when this bit is set. |
| request_chat_title | 9 | Controlled by `flags`; present when this bit is set. |
| request_chat_date | 9 | Controlled by `flags`; present when this bit is set. |
| business_bot_id | 13 | Controlled by `flags`; present when this bit is set. |
| business_bot_manage_url | 13 | Controlled by `flags`; present when this bit is set. |
| charge_paid_message_stars | 14 | Controlled by `flags`; present when this bit is set. |
| registration_month | 15 | Controlled by `flags`; present when this bit is set. |
| phone_country | 16 | Controlled by `flags`; present when this bit is set. |
| name_change_date | 17 | Controlled by `flags`; present when this bit is set. |
| photo_change_date | 18 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PeerSettings
```

Public access: `miniproto.raw.types.PeerSettings`.

## Safe usage shape

```python
from miniproto.raw.types import PeerSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PeerSettings
```

## Result family

[`PeerSettings`](/reference/telegram/types/results/peer-settings/)

## Relationships

- Result family: [`PeerSettings`](/reference/telegram/types/results/peer-settings/)
- Accepted by: [`messages.peerSettings`](/reference/telegram/types/messages/peer-settings/), [`updatePeerSettings`](/reference/telegram/types/base/update-peer-settings/), [`userFull`](/reference/telegram/types/base/user-full/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
