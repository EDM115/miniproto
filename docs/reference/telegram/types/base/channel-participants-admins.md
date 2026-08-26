---
title: "channelParticipantsAdmins"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelParticipantsAdmins"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb4608969"
---

# `channelParticipantsAdmins`

No description provided by the pinned schema.

## Signature

```tl
channelParticipantsAdmins#b4608969 = ChannelParticipantsFilter;
```

## Result type

`ChannelParticipantsFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import ChannelParticipantsAdmins
```

Public access: `miniproto.raw.types.ChannelParticipantsAdmins`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelParticipantsAdmins

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelParticipantsAdmins
```

## Result family

[`ChannelParticipantsFilter`](/reference/telegram/types/results/channel-participants-filter/)

## Relationships

- Result family: [`ChannelParticipantsFilter`](/reference/telegram/types/results/channel-participants-filter/)
- Related constructors: [`channelParticipantsBanned`](/reference/telegram/types/base/channel-participants-banned/), [`channelParticipantsBots`](/reference/telegram/types/base/channel-participants-bots/), [`channelParticipantsContacts`](/reference/telegram/types/base/channel-participants-contacts/), [`channelParticipantsKicked`](/reference/telegram/types/base/channel-participants-kicked/), [`channelParticipantsMentions`](/reference/telegram/types/base/channel-participants-mentions/), [`channelParticipantsRecent`](/reference/telegram/types/base/channel-participants-recent/), [`channelParticipantsSearch`](/reference/telegram/types/base/channel-participants-search/)
- Accepted by: [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
