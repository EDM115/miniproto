---
title: "communities.participantJoinedChats"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "communities.participantJoinedChats"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "communities"
layer: 228
schema_source: "tdlib"
constructor_id: "0x8d78512a"
---

# `communities.participantJoinedChats`

No description provided by the pinned schema.

## Signature

```tl
communities.participantJoinedChats#8d78512a creator_chat_ids:Vector<long> joined_chat_ids:Vector<long> chats:Vector<Chat> users:Vector<User> = communities.ParticipantJoinedChats;
```

## Result type

`communities.ParticipantJoinedChats`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| creator_chat_ids | Vector<long> | — | — | No description provided by the pinned schema. |
| joined_chat_ids | Vector<long> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import CommunitiesParticipantJoinedChats
```

Public access: `miniproto.raw.types.CommunitiesParticipantJoinedChats`.

## Safe usage shape

```python
from miniproto.raw.types import CommunitiesParticipantJoinedChats

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = CommunitiesParticipantJoinedChats
```

## Result family

[`communities.ParticipantJoinedChats`](/reference/telegram/types/results/communities-participant-joined-chats/)

## Relationships

- Result family: [`communities.ParticipantJoinedChats`](/reference/telegram/types/results/communities-participant-joined-chats/)
- Returned by: [`communities.getParticipantJoinedChats`](/reference/telegram/functions/communities/get-participant-joined-chats/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
