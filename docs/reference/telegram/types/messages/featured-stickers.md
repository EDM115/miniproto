---
title: "messages.featuredStickers"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.featuredStickers"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xbe382906"
---

# `messages.featuredStickers`

No description provided by the pinned schema.

## Signature

```tl
messages.featuredStickers#be382906 flags:# premium:flags.0?true hash:long count:int sets:Vector<StickerSetCovered> unread:Vector<long> = messages.FeaturedStickers;
```

## Result type

`messages.FeaturedStickers`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| premium | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| sets | Vector<StickerSetCovered> | — | — | No description provided by the pinned schema. |
| unread | Vector<long> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| premium | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MessagesFeaturedStickers
```

Public access: `miniproto.raw.types.MessagesFeaturedStickers`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesFeaturedStickers

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesFeaturedStickers
```

## Result family

[`messages.FeaturedStickers`](/reference/telegram/types/results/messages-featured-stickers/)

## Relationships

- Result family: [`messages.FeaturedStickers`](/reference/telegram/types/results/messages-featured-stickers/)
- Related constructors: [`messages.featuredStickersNotModified`](/reference/telegram/types/messages/featured-stickers-not-modified/)
- Returned by: [`messages.getFeaturedEmojiStickers`](/reference/telegram/functions/messages/get-featured-emoji-stickers/), [`messages.getFeaturedStickers`](/reference/telegram/functions/messages/get-featured-stickers/), [`messages.getOldFeaturedStickers`](/reference/telegram/functions/messages/get-old-featured-stickers/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
