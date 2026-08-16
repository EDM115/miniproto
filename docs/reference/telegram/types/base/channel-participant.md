---
title: "channelParticipant"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelParticipant"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1bd54456"
---

# `channelParticipant`

No description provided by the pinned schema.

## Signature

```tl
channelParticipant#1bd54456 flags:# user_id:long date:int subscription_until_date:flags.0?int rank:flags.2?string = ChannelParticipant;
```

## Result type

`ChannelParticipant`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| subscription_until_date | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| rank | flags.2?string | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| subscription_until_date | 0 | Controlled by `flags`; present when this bit is set. |
| rank | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChannelParticipant
```

Public access: `miniproto.raw.types.ChannelParticipant`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelParticipant

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelParticipant
```

## Result family

[`ChannelParticipant`](/reference/telegram/types/results/channel-participant/)

## Relationships

- Result family: [`ChannelParticipant`](/reference/telegram/types/results/channel-participant/)
- Related constructors: [`channelParticipantAdmin`](/reference/telegram/types/base/channel-participant-admin/), [`channelParticipantBanned`](/reference/telegram/types/base/channel-participant-banned/), [`channelParticipantCreator`](/reference/telegram/types/base/channel-participant-creator/), [`channelParticipantLeft`](/reference/telegram/types/base/channel-participant-left/), [`channelParticipantSelf`](/reference/telegram/types/base/channel-participant-self/)
- Accepted by: [`channelAdminLogEventActionParticipantInvite`](/reference/telegram/types/base/channel-admin-log-event-action-participant-invite/), [`channelAdminLogEventActionParticipantSubExtend`](/reference/telegram/types/base/channel-admin-log-event-action-participant-sub-extend/), [`channelAdminLogEventActionParticipantToggleAdmin`](/reference/telegram/types/base/channel-admin-log-event-action-participant-toggle-admin/), [`channelAdminLogEventActionParticipantToggleBan`](/reference/telegram/types/base/channel-admin-log-event-action-participant-toggle-ban/), [`channels.channelParticipant`](/reference/telegram/types/channels/channel-participant/), [`channels.channelParticipants`](/reference/telegram/types/channels/channel-participants/), [`updateChannelParticipant`](/reference/telegram/types/base/update-channel-participant/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
