---
title: "messages.foundStickers"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.foundStickers"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x82c9e290"
---

# `messages.foundStickers`

No description provided by the pinned schema.

## Signature

```tl
messages.foundStickers#82c9e290 flags:# next_offset:flags.0?int hash:long stickers:Vector<Document> = messages.FoundStickers;
```

## Result type

`messages.FoundStickers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| next_offset | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |
| stickers | Vector<Document> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesFoundStickers
```

Public access: `miniproto.raw.types.MessagesFoundStickers`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesFoundStickers

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesFoundStickers
```

## Result family

[`messages.FoundStickers`](/reference/telegram/types/results/messages-found-stickers/)

## Relationships

- Result family: [`messages.FoundStickers`](/reference/telegram/types/results/messages-found-stickers/)
- Related constructors: [`messages.foundStickersNotModified`](/reference/telegram/types/messages/found-stickers-not-modified/)
- Returned by: [`messages.searchStickers`](/reference/telegram/functions/messages/search-stickers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
