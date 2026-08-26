---
title: "webPageAttributeStarGiftAuction"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webPageAttributeStarGiftAuction"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x01c641c2"
---

# `webPageAttributeStarGiftAuction`

No description provided by the pinned schema.

## Signature

```tl
webPageAttributeStarGiftAuction#01c641c2 gift:StarGift end_date:int = WebPageAttribute;
```

## Result type

`WebPageAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| gift | StarGift | — | — | No description provided by the pinned schema. |
| end_date | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WebPageAttributeStarGiftAuction
```

Public access: `miniproto.raw.types.WebPageAttributeStarGiftAuction`.

## Safe usage shape

```python
from miniproto.raw.types import WebPageAttributeStarGiftAuction

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebPageAttributeStarGiftAuction
```

## Result family

[`WebPageAttribute`](/reference/telegram/types/results/web-page-attribute/)

## Relationships

- Result family: [`WebPageAttribute`](/reference/telegram/types/results/web-page-attribute/)
- Related constructors: [`webPageAttributeAiComposeTone`](/reference/telegram/types/base/web-page-attribute-ai-compose-tone/), [`webPageAttributeStarGiftCollection`](/reference/telegram/types/base/web-page-attribute-star-gift-collection/), [`webPageAttributeStickerSet`](/reference/telegram/types/base/web-page-attribute-sticker-set/), [`webPageAttributeStory`](/reference/telegram/types/base/web-page-attribute-story/), [`webPageAttributeTheme`](/reference/telegram/types/base/web-page-attribute-theme/), [`webPageAttributeUniqueStarGift`](/reference/telegram/types/base/web-page-attribute-unique-star-gift/)
- Accepted by: [`webPage`](/reference/telegram/types/base/web-page/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
