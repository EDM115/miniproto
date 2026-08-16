---
title: "messages.stickersNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.stickersNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf1749a22"
---

# `messages.stickersNotModified`

No description provided by the pinned schema.

## Signature

```tl
messages.stickersNotModified#f1749a22 = messages.Stickers;
```

## Result type

`messages.Stickers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import MessagesStickersNotModified
```

Public access: `miniproto.raw.types.MessagesStickersNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesStickersNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesStickersNotModified
```

## Result family

[`messages.Stickers`](/reference/telegram/types/results/messages-stickers/)

## Relationships

- Result family: [`messages.Stickers`](/reference/telegram/types/results/messages-stickers/)
- Related constructors: [`messages.stickers`](/reference/telegram/types/messages/stickers/)
- Returned by: [`messages.getStickers`](/reference/telegram/functions/messages/get-stickers/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
