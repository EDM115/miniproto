---
title: "messages.reactions"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.reactions"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xeafdf716"
---

# `messages.reactions`

No description provided by the pinned schema.

## Signature

```tl
messages.reactions#eafdf716 hash:long reactions:Vector<Reaction> = messages.Reactions;
```

## Result type

`messages.Reactions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| reactions | Vector<Reaction> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesReactions
```

Public access: `miniproto.raw.types.MessagesReactions`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesReactions

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesReactions
```

## Result family

[`messages.Reactions`](/reference/telegram/types/results/messages-reactions/)

## Relationships

- Result family: [`messages.Reactions`](/reference/telegram/types/results/messages-reactions/)
- Related constructors: [`messages.reactionsNotModified`](/reference/telegram/types/messages/reactions-not-modified/)
- Returned by: [`messages.getDefaultTagReactions`](/reference/telegram/functions/messages/get-default-tag-reactions/), [`messages.getRecentReactions`](/reference/telegram/functions/messages/get-recent-reactions/), [`messages.getTopReactions`](/reference/telegram/functions/messages/get-top-reactions/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
