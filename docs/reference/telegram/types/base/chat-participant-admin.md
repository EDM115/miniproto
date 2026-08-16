---
title: "chatParticipantAdmin"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatParticipantAdmin"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0360d5d2"
---

# `chatParticipantAdmin`

No description provided by the pinned schema.

## Signature

```tl
chatParticipantAdmin#0360d5d2 flags:# user_id:long inviter_id:long date:int rank:flags.0?string = ChatParticipant;
```

## Result type

`ChatParticipant`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |
| inviter_id | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| rank | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| rank | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatParticipantAdmin
```

Public access: `miniproto.raw.types.ChatParticipantAdmin`.

## Safe usage shape

```python
from miniproto.raw.types import ChatParticipantAdmin

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatParticipantAdmin
```

## Result family

[`ChatParticipant`](/reference/telegram/types/results/chat-participant/)

## Relationships

- Result family: [`ChatParticipant`](/reference/telegram/types/results/chat-participant/)
- Related constructors: [`chatParticipant`](/reference/telegram/types/base/chat-participant/), [`chatParticipantCreator`](/reference/telegram/types/base/chat-participant-creator/)
- Accepted by: [`chatParticipants`](/reference/telegram/types/base/chat-participants/), [`chatParticipantsForbidden`](/reference/telegram/types/base/chat-participants-forbidden/), [`updateChatParticipant`](/reference/telegram/types/base/update-chat-participant/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
