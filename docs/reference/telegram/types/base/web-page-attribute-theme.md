---
title: "webPageAttributeTheme"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webPageAttributeTheme"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x54b56617"
---

# `webPageAttributeTheme`

No description provided by the pinned schema.

## Signature

```tl
webPageAttributeTheme#54b56617 flags:# documents:flags.0?Vector<Document> settings:flags.1?ThemeSettings = WebPageAttribute;
```

## Result type

`WebPageAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| documents | flags.0?Vector<Document> | flags.0 | — | No description provided by the pinned schema. |
| settings | flags.1?ThemeSettings | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| documents | 0 | Controlled by `flags`; present when this bit is set. |
| settings | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WebPageAttributeTheme
```

Public access: `miniproto.raw.types.WebPageAttributeTheme`.

## Safe usage shape

```python
from miniproto.raw.types import WebPageAttributeTheme

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebPageAttributeTheme
```

## Result family

[`WebPageAttribute`](/reference/telegram/types/results/web-page-attribute/)

## Relationships

- Result family: [`WebPageAttribute`](/reference/telegram/types/results/web-page-attribute/)
- Related constructors: [`webPageAttributeAiComposeTone`](/reference/telegram/types/base/web-page-attribute-ai-compose-tone/), [`webPageAttributeStarGiftAuction`](/reference/telegram/types/base/web-page-attribute-star-gift-auction/), [`webPageAttributeStarGiftCollection`](/reference/telegram/types/base/web-page-attribute-star-gift-collection/), [`webPageAttributeStickerSet`](/reference/telegram/types/base/web-page-attribute-sticker-set/), [`webPageAttributeStory`](/reference/telegram/types/base/web-page-attribute-story/), [`webPageAttributeUniqueStarGift`](/reference/telegram/types/base/web-page-attribute-unique-star-gift/)
- Accepted by: [`webPage`](/reference/telegram/types/base/web-page/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
