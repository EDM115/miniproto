---
title: "channelParticipantsContacts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelParticipantsContacts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xbb6ae88d"
---

# `channelParticipantsContacts`

No description provided by the pinned schema.

## Signature

```tl
channelParticipantsContacts#bb6ae88d q:string = ChannelParticipantsFilter;
```

## Result type

`ChannelParticipantsFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| q | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChannelParticipantsContacts
```

Public access: `miniproto.raw.types.ChannelParticipantsContacts`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelParticipantsContacts

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelParticipantsContacts
```

## Result family

[`ChannelParticipantsFilter`](/reference/telegram/types/results/channel-participants-filter/)

## Relationships

- Result family: [`ChannelParticipantsFilter`](/reference/telegram/types/results/channel-participants-filter/)
- Related constructors: [`channelParticipantsAdmins`](/reference/telegram/types/base/channel-participants-admins/), [`channelParticipantsBanned`](/reference/telegram/types/base/channel-participants-banned/), [`channelParticipantsBots`](/reference/telegram/types/base/channel-participants-bots/), [`channelParticipantsKicked`](/reference/telegram/types/base/channel-participants-kicked/), [`channelParticipantsMentions`](/reference/telegram/types/base/channel-participants-mentions/), [`channelParticipantsRecent`](/reference/telegram/types/base/channel-participants-recent/), [`channelParticipantsSearch`](/reference/telegram/types/base/channel-participants-search/)
- Accepted by: [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
