---
title: "channelParticipantSelf"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelParticipantSelf"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa9478a1a"
---

# `channelParticipantSelf`

No description provided by the pinned schema.

## Signature

```tl
channelParticipantSelf#a9478a1a flags:# via_request:flags.0?true user_id:long inviter_id:long date:int subscription_until_date:flags.1?int rank:flags.2?string = ChannelParticipant;
```

## Result type

`ChannelParticipant`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| via_request | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |
| inviter_id | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| subscription_until_date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| rank | flags.2?string | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| via_request | 0 | Controlled by `flags`; present when this bit is set. |
| subscription_until_date | 1 | Controlled by `flags`; present when this bit is set. |
| rank | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChannelParticipantSelf
```

Public access: `miniproto.raw.types.ChannelParticipantSelf`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelParticipantSelf

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelParticipantSelf
```

## Result family

[`ChannelParticipant`](/reference/telegram/types/results/channel-participant/)

## Relationships

- Result family: [`ChannelParticipant`](/reference/telegram/types/results/channel-participant/)
- Related constructors: [`channelParticipant`](/reference/telegram/types/base/channel-participant/), [`channelParticipantAdmin`](/reference/telegram/types/base/channel-participant-admin/), [`channelParticipantBanned`](/reference/telegram/types/base/channel-participant-banned/), [`channelParticipantCreator`](/reference/telegram/types/base/channel-participant-creator/), [`channelParticipantLeft`](/reference/telegram/types/base/channel-participant-left/)
- Accepted by: [`channelAdminLogEventActionParticipantInvite`](/reference/telegram/types/base/channel-admin-log-event-action-participant-invite/), [`channelAdminLogEventActionParticipantSubExtend`](/reference/telegram/types/base/channel-admin-log-event-action-participant-sub-extend/), [`channelAdminLogEventActionParticipantToggleAdmin`](/reference/telegram/types/base/channel-admin-log-event-action-participant-toggle-admin/), [`channelAdminLogEventActionParticipantToggleBan`](/reference/telegram/types/base/channel-admin-log-event-action-participant-toggle-ban/), [`channels.channelParticipant`](/reference/telegram/types/channels/channel-participant/), [`channels.channelParticipants`](/reference/telegram/types/channels/channel-participants/), [`updateChannelParticipant`](/reference/telegram/types/base/update-channel-participant/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
