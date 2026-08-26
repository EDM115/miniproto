---
title: "chatReactionsAll"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatReactionsAll"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x52928bca"
---

# `chatReactionsAll`

No description provided by the pinned schema.

## Signature

```tl
chatReactionsAll#52928bca flags:# allow_custom:flags.0?true = ChatReactions;
```

## Result type

`ChatReactions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| allow_custom | flags.0?true | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| allow_custom | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatReactionsAll
```

Public access: `miniproto.raw.types.ChatReactionsAll`.

## Safe usage shape

```python
from miniproto.raw.types import ChatReactionsAll

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatReactionsAll
```

## Result family

[`ChatReactions`](/reference/telegram/types/results/chat-reactions/)

## Relationships

- Result family: [`ChatReactions`](/reference/telegram/types/results/chat-reactions/)
- Related constructors: [`chatReactionsNone`](/reference/telegram/types/base/chat-reactions-none/), [`chatReactionsSome`](/reference/telegram/types/base/chat-reactions-some/)
- Accepted by: [`messages.setChatAvailableReactions`](/reference/telegram/functions/messages/set-chat-available-reactions/), [`channelAdminLogEventActionChangeAvailableReactions`](/reference/telegram/types/base/channel-admin-log-event-action-change-available-reactions/), [`channelFull`](/reference/telegram/types/base/channel-full/), [`chatFull`](/reference/telegram/types/base/chat-full/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
