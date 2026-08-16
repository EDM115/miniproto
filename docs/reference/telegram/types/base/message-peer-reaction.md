---
title: "messagePeerReaction"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messagePeerReaction"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x8c79b63c"
---

# `messagePeerReaction`

No description provided by the pinned schema.

## Signature

```tl
messagePeerReaction#8c79b63c flags:# big:flags.0?true unread:flags.1?true my:flags.2?true peer_id:Peer date:int reaction:Reaction = MessagePeerReaction;
```

## Result type

`MessagePeerReaction`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| big | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| unread | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| my | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| peer_id | Peer | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| reaction | Reaction | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| big | 0 | Controlled by `flags`; present when this bit is set. |
| unread | 1 | Controlled by `flags`; present when this bit is set. |
| my | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagePeerReaction
```

Public access: `miniproto.raw.types.MessagePeerReaction`.

## Safe usage shape

```python
from miniproto.raw.types import MessagePeerReaction

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagePeerReaction
```

## Result family

[`MessagePeerReaction`](/reference/telegram/types/results/message-peer-reaction/)

## Relationships

- Result family: [`MessagePeerReaction`](/reference/telegram/types/results/message-peer-reaction/)
- Accepted by: [`messageReactions`](/reference/telegram/types/base/message-reactions/), [`messages.messageReactionsList`](/reference/telegram/types/messages/message-reactions-list/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
