---
title: "webPageAttributeStarGiftCollection"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webPageAttributeStarGiftCollection"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x31cad303"
---

# `webPageAttributeStarGiftCollection`

No description provided by the pinned schema.

## Signature

```tl
webPageAttributeStarGiftCollection#31cad303 icons:Vector<Document> = WebPageAttribute;
```

## Result type

`WebPageAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| icons | Vector<Document> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WebPageAttributeStarGiftCollection
```

Public access: `miniproto.raw.types.WebPageAttributeStarGiftCollection`.

## Safe usage shape

```python
from miniproto.raw.types import WebPageAttributeStarGiftCollection

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebPageAttributeStarGiftCollection
```

## Result family

[`WebPageAttribute`](/reference/telegram/types/results/web-page-attribute/)

## Relationships

- Result family: [`WebPageAttribute`](/reference/telegram/types/results/web-page-attribute/)
- Related constructors: [`webPageAttributeAiComposeTone`](/reference/telegram/types/base/web-page-attribute-ai-compose-tone/), [`webPageAttributeStarGiftAuction`](/reference/telegram/types/base/web-page-attribute-star-gift-auction/), [`webPageAttributeStickerSet`](/reference/telegram/types/base/web-page-attribute-sticker-set/), [`webPageAttributeStory`](/reference/telegram/types/base/web-page-attribute-story/), [`webPageAttributeTheme`](/reference/telegram/types/base/web-page-attribute-theme/), [`webPageAttributeUniqueStarGift`](/reference/telegram/types/base/web-page-attribute-unique-star-gift/)
- Accepted by: [`webPage`](/reference/telegram/types/base/web-page/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
