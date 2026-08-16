---
title: "groupCallParticipant"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "groupCallParticipant"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2a3dc7ac"
---

# `groupCallParticipant`

No description provided by the pinned schema.

## Signature

```tl
groupCallParticipant#2a3dc7ac flags:# muted:flags.0?true left:flags.1?true can_self_unmute:flags.2?true just_joined:flags.4?true versioned:flags.5?true min:flags.8?true muted_by_you:flags.9?true volume_by_admin:flags.10?true self:flags.12?true video_joined:flags.15?true peer:Peer date:int active_date:flags.3?int source:int volume:flags.7?int about:flags.11?string raise_hand_rating:flags.13?long video:flags.6?GroupCallParticipantVideo presentation:flags.14?GroupCallParticipantVideo paid_stars_total:flags.16?long = GroupCallParticipant;
```

## Result type

`GroupCallParticipant`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| muted | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| left | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| can_self_unmute | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| just_joined | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| versioned | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| min | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| muted_by_you | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| volume_by_admin | flags.10?true | flags.10 | — | No description provided by the pinned schema. |
| self | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| video_joined | flags.15?true | flags.15 | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| active_date | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| source | int | — | — | No description provided by the pinned schema. |
| volume | flags.7?int | flags.7 | — | No description provided by the pinned schema. |
| about | flags.11?string | flags.11 | — | No description provided by the pinned schema. |
| raise_hand_rating | flags.13?long | flags.13 | — | No description provided by the pinned schema. |
| video | flags.6?GroupCallParticipantVideo | flags.6 | — | No description provided by the pinned schema. |
| presentation | flags.14?GroupCallParticipantVideo | flags.14 | — | No description provided by the pinned schema. |
| paid_stars_total | flags.16?long | flags.16 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| muted | 0 | Controlled by `flags`; present when this bit is set. |
| left | 1 | Controlled by `flags`; present when this bit is set. |
| can_self_unmute | 2 | Controlled by `flags`; present when this bit is set. |
| just_joined | 4 | Controlled by `flags`; present when this bit is set. |
| versioned | 5 | Controlled by `flags`; present when this bit is set. |
| min | 8 | Controlled by `flags`; present when this bit is set. |
| muted_by_you | 9 | Controlled by `flags`; present when this bit is set. |
| volume_by_admin | 10 | Controlled by `flags`; present when this bit is set. |
| self | 12 | Controlled by `flags`; present when this bit is set. |
| video_joined | 15 | Controlled by `flags`; present when this bit is set. |
| active_date | 3 | Controlled by `flags`; present when this bit is set. |
| volume | 7 | Controlled by `flags`; present when this bit is set. |
| about | 11 | Controlled by `flags`; present when this bit is set. |
| raise_hand_rating | 13 | Controlled by `flags`; present when this bit is set. |
| video | 6 | Controlled by `flags`; present when this bit is set. |
| presentation | 14 | Controlled by `flags`; present when this bit is set. |
| paid_stars_total | 16 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import GroupCallParticipant
```

Public access: `miniproto.raw.types.GroupCallParticipant`.

## Safe usage shape

```python
from miniproto.raw.types import GroupCallParticipant

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = GroupCallParticipant
```

## Result family

[`GroupCallParticipant`](/reference/telegram/types/results/group-call-participant/)

## Relationships

- Result family: [`GroupCallParticipant`](/reference/telegram/types/results/group-call-participant/)
- Accepted by: [`channelAdminLogEventActionParticipantMute`](/reference/telegram/types/base/channel-admin-log-event-action-participant-mute/), [`channelAdminLogEventActionParticipantUnmute`](/reference/telegram/types/base/channel-admin-log-event-action-participant-unmute/), [`channelAdminLogEventActionParticipantVolume`](/reference/telegram/types/base/channel-admin-log-event-action-participant-volume/), [`phone.groupCall`](/reference/telegram/types/phone/group-call/), [`phone.groupParticipants`](/reference/telegram/types/phone/group-participants/), [`updateGroupCallParticipants`](/reference/telegram/types/base/update-group-call-participants/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
