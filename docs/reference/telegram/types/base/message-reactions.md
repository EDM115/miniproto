---
title: "messageReactions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageReactions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x0a339f0b"
---

# `messageReactions`

No description provided by the pinned schema.

## Signature

```tl
messageReactions#0a339f0b flags:# min:flags.0?true can_see_list:flags.2?true reactions_as_tags:flags.3?true results:Vector<ReactionCount> recent_reactions:flags.1?Vector<MessagePeerReaction> top_reactors:flags.4?Vector<MessageReactor> = MessageReactions;
```

## Result type

`MessageReactions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| min | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| can_see_list | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| reactions_as_tags | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| results | Vector<ReactionCount> | — | — | No description provided by the pinned schema. |
| recent_reactions | flags.1?Vector<MessagePeerReaction> | flags.1 | — | No description provided by the pinned schema. |
| top_reactors | flags.4?Vector<MessageReactor> | flags.4 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| min | 0 | Controlled by `flags`; present when this bit is set. |
| can_see_list | 2 | Controlled by `flags`; present when this bit is set. |
| reactions_as_tags | 3 | Controlled by `flags`; present when this bit is set. |
| recent_reactions | 1 | Controlled by `flags`; present when this bit is set. |
| top_reactors | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessageReactions
```

Public access: `miniproto.raw.types.MessageReactions`.

## Safe usage shape

```python
from miniproto.raw.types import MessageReactions

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageReactions
```

## Result family

[`MessageReactions`](/reference/telegram/types/results/message-reactions/)

## Relationships

- Result family: [`MessageReactions`](/reference/telegram/types/results/message-reactions/)
- Accepted by: [`message`](/reference/telegram/types/base/message/), [`messageService`](/reference/telegram/types/base/message-service/), [`updateMessageReactions`](/reference/telegram/types/base/update-message-reactions/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
