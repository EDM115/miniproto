---
title: "messages.reactionsNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.reactionsNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xb06fdbdf"
---

# `messages.reactionsNotModified`

No description provided by the pinned schema.

## Signature

```tl
messages.reactionsNotModified#b06fdbdf = messages.Reactions;
```

## Result type

`messages.Reactions`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import MessagesReactionsNotModified
```

Public access: `miniproto.raw.types.MessagesReactionsNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesReactionsNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesReactionsNotModified
```

## Result family

[`messages.Reactions`](/reference/telegram/types/results/messages-reactions/)

## Relationships

- Result family: [`messages.Reactions`](/reference/telegram/types/results/messages-reactions/)
- Related constructors: [`messages.reactions`](/reference/telegram/types/messages/reactions/)
- Returned by: [`messages.getDefaultTagReactions`](/reference/telegram/functions/messages/get-default-tag-reactions/), [`messages.getRecentReactions`](/reference/telegram/functions/messages/get-recent-reactions/), [`messages.getTopReactions`](/reference/telegram/functions/messages/get-top-reactions/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
