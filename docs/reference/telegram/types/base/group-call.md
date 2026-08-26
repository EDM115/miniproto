---
title: "groupCall"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "groupCall"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xefb2b617"
---

# `groupCall`

No description provided by the pinned schema.

## Signature

```tl
groupCall#efb2b617 flags:# join_muted:flags.1?true can_change_join_muted:flags.2?true join_date_asc:flags.6?true schedule_start_subscribed:flags.8?true can_start_video:flags.9?true record_video_active:flags.11?true rtmp_stream:flags.12?true listeners_hidden:flags.13?true conference:flags.14?true creator:flags.15?true messages_enabled:flags.17?true can_change_messages_enabled:flags.18?true min:flags.19?true id:long access_hash:long participants_count:int title:flags.3?string stream_dc_id:flags.4?int record_start_date:flags.5?int schedule_date:flags.7?int unmuted_video_count:flags.10?int unmuted_video_limit:int version:int invite_link:flags.16?string send_paid_messages_stars:flags.20?long default_send_as:flags.21?Peer = GroupCall;
```

## Result type

`GroupCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| join_muted | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| can_change_join_muted | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| join_date_asc | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| schedule_start_subscribed | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| can_start_video | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| record_video_active | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| rtmp_stream | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| listeners_hidden | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| conference | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| creator | flags.15?true | flags.15 | — | No description provided by the pinned schema. |
| messages_enabled | flags.17?true | flags.17 | — | No description provided by the pinned schema. |
| can_change_messages_enabled | flags.18?true | flags.18 | — | No description provided by the pinned schema. |
| min | flags.19?true | flags.19 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| participants_count | int | — | — | No description provided by the pinned schema. |
| title | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| stream_dc_id | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| record_start_date | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| schedule_date | flags.7?int | flags.7 | — | No description provided by the pinned schema. |
| unmuted_video_count | flags.10?int | flags.10 | — | No description provided by the pinned schema. |
| unmuted_video_limit | int | — | — | No description provided by the pinned schema. |
| version | int | — | — | No description provided by the pinned schema. |
| invite_link | flags.16?string | flags.16 | — | No description provided by the pinned schema. |
| send_paid_messages_stars | flags.20?long | flags.20 | — | No description provided by the pinned schema. |
| default_send_as | flags.21?Peer | flags.21 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| join_muted | 1 | Controlled by `flags`; present when this bit is set. |
| can_change_join_muted | 2 | Controlled by `flags`; present when this bit is set. |
| join_date_asc | 6 | Controlled by `flags`; present when this bit is set. |
| schedule_start_subscribed | 8 | Controlled by `flags`; present when this bit is set. |
| can_start_video | 9 | Controlled by `flags`; present when this bit is set. |
| record_video_active | 11 | Controlled by `flags`; present when this bit is set. |
| rtmp_stream | 12 | Controlled by `flags`; present when this bit is set. |
| listeners_hidden | 13 | Controlled by `flags`; present when this bit is set. |
| conference | 14 | Controlled by `flags`; present when this bit is set. |
| creator | 15 | Controlled by `flags`; present when this bit is set. |
| messages_enabled | 17 | Controlled by `flags`; present when this bit is set. |
| can_change_messages_enabled | 18 | Controlled by `flags`; present when this bit is set. |
| min | 19 | Controlled by `flags`; present when this bit is set. |
| title | 3 | Controlled by `flags`; present when this bit is set. |
| stream_dc_id | 4 | Controlled by `flags`; present when this bit is set. |
| record_start_date | 5 | Controlled by `flags`; present when this bit is set. |
| schedule_date | 7 | Controlled by `flags`; present when this bit is set. |
| unmuted_video_count | 10 | Controlled by `flags`; present when this bit is set. |
| invite_link | 16 | Controlled by `flags`; present when this bit is set. |
| send_paid_messages_stars | 20 | Controlled by `flags`; present when this bit is set. |
| default_send_as | 21 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import GroupCall
```

Public access: `miniproto.raw.types.GroupCall`.

## Safe usage shape

```python
from miniproto.raw.types import GroupCall

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = GroupCall
```

## Result family

[`GroupCall`](/reference/telegram/types/results/group-call/)

## Relationships

- Result family: [`GroupCall`](/reference/telegram/types/results/group-call/)
- Related constructors: [`groupCallDiscarded`](/reference/telegram/types/base/group-call-discarded/)
- Accepted by: [`phone.groupCall`](/reference/telegram/types/phone/group-call/), [`updateGroupCall`](/reference/telegram/types/base/update-group-call/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
