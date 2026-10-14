---
title: "channelParticipantsRecent"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelParticipantsRecent"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xde3f3c79"
---

# `channelParticipantsRecent`

No description provided by the pinned schema.

## Signature

```tl
channelParticipantsRecent#de3f3c79 = ChannelParticipantsFilter;
```

## Result type

`ChannelParticipantsFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import ChannelParticipantsRecent
```

Public access: `miniproto.raw.types.ChannelParticipantsRecent`.

## Class reference

```python
from miniproto.raw.types import ChannelParticipantsRecent

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ChannelParticipantsRecent
```

## Result family

[`ChannelParticipantsFilter`](/reference/telegram/types/results/channel-participants-filter/)

## Relationships

- Result family: [`ChannelParticipantsFilter`](/reference/telegram/types/results/channel-participants-filter/)
- Related constructors: [`channelParticipantsAdmins`](/reference/telegram/types/base/channel-participants-admins/), [`channelParticipantsBanned`](/reference/telegram/types/base/channel-participants-banned/), [`channelParticipantsBots`](/reference/telegram/types/base/channel-participants-bots/), [`channelParticipantsContacts`](/reference/telegram/types/base/channel-participants-contacts/), [`channelParticipantsKicked`](/reference/telegram/types/base/channel-participants-kicked/), [`channelParticipantsMentions`](/reference/telegram/types/base/channel-participants-mentions/), [`channelParticipantsSearch`](/reference/telegram/types/base/channel-participants-search/)
- Accepted by: [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
