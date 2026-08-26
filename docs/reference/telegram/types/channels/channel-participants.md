---
title: "channels.channelParticipants"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channels.channelParticipants"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "channels"
schema_source: "tdlib"
constructor_id: "0x9ab0feaf"
---

# `channels.channelParticipants`

No description provided by the pinned schema.

## Signature

```tl
channels.channelParticipants#9ab0feaf count:int participants:Vector<ChannelParticipant> chats:Vector<Chat> users:Vector<User> = channels.ChannelParticipants;
```

## Result type

`channels.ChannelParticipants`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| participants | Vector<ChannelParticipant> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChannelsChannelParticipants
```

Public access: `miniproto.raw.types.ChannelsChannelParticipants`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelsChannelParticipants

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelsChannelParticipants
```

## Result family

[`channels.ChannelParticipants`](/reference/telegram/types/results/channels-channel-participants/)

## Relationships

- Result family: [`channels.ChannelParticipants`](/reference/telegram/types/results/channels-channel-participants/)
- Related constructors: [`channels.channelParticipantsNotModified`](/reference/telegram/types/channels/channel-participants-not-modified/)
- Returned by: [`channels.getParticipants`](/reference/telegram/functions/channels/get-participants/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
