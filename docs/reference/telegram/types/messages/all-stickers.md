---
title: "messages.allStickers"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.allStickers"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xcdbbcebb"
---

# `messages.allStickers`

No description provided by the pinned schema.

## Signature

```tl
messages.allStickers#cdbbcebb hash:long sets:Vector<StickerSet> = messages.AllStickers;
```

## Result type

`messages.AllStickers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| sets | Vector<StickerSet> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesAllStickers
```

Public access: `miniproto.raw.types.MessagesAllStickers`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesAllStickers

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesAllStickers
```

## Result family

[`messages.AllStickers`](/reference/telegram/types/results/messages-all-stickers/)

## Relationships

- Result family: [`messages.AllStickers`](/reference/telegram/types/results/messages-all-stickers/)
- Related constructors: [`messages.allStickersNotModified`](/reference/telegram/types/messages/all-stickers-not-modified/)
- Returned by: [`messages.getAllStickers`](/reference/telegram/functions/messages/get-all-stickers/), [`messages.getEmojiStickers`](/reference/telegram/functions/messages/get-emoji-stickers/), [`messages.getMaskStickers`](/reference/telegram/functions/messages/get-mask-stickers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
