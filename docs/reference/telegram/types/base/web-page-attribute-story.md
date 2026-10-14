---
title: "webPageAttributeStory"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webPageAttributeStory"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x2e94c3e7"
---

# `webPageAttributeStory`

No description provided by the pinned schema.

## Signature

```tl
webPageAttributeStory#2e94c3e7 flags:# peer:Peer id:int story:flags.0?StoryItem = WebPageAttribute;
```

## Result type

`WebPageAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| story | flags.0?StoryItem | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| story | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WebPageAttributeStory
```

Public access: `miniproto.raw.types.WebPageAttributeStory`.

## Class reference

```python
from miniproto.raw.types import WebPageAttributeStory

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = WebPageAttributeStory
```

## Result family

[`WebPageAttribute`](/reference/telegram/types/results/web-page-attribute/)

## Relationships

- Result family: [`WebPageAttribute`](/reference/telegram/types/results/web-page-attribute/)
- Related constructors: [`webPageAttributeAiComposeTone`](/reference/telegram/types/base/web-page-attribute-ai-compose-tone/), [`webPageAttributeStarGiftAuction`](/reference/telegram/types/base/web-page-attribute-star-gift-auction/), [`webPageAttributeStarGiftCollection`](/reference/telegram/types/base/web-page-attribute-star-gift-collection/), [`webPageAttributeStickerSet`](/reference/telegram/types/base/web-page-attribute-sticker-set/), [`webPageAttributeTheme`](/reference/telegram/types/base/web-page-attribute-theme/), [`webPageAttributeUniqueStarGift`](/reference/telegram/types/base/web-page-attribute-unique-star-gift/)
- Accepted by: [`webPage`](/reference/telegram/types/base/web-page/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
