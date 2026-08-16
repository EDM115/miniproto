---
title: "webPage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webPage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xe89c45b2"
---

# `webPage`

No description provided by the pinned schema.

## Signature

```tl
webPage#e89c45b2 flags:# has_large_media:flags.13?true video_cover_photo:flags.14?true id:long url:string display_url:string hash:int type:flags.0?string site_name:flags.1?string title:flags.2?string description:flags.3?string photo:flags.4?Photo embed_url:flags.5?string embed_type:flags.5?string embed_width:flags.6?int embed_height:flags.6?int duration:flags.7?int author:flags.8?string document:flags.9?Document cached_page:flags.10?Page attributes:flags.12?Vector<WebPageAttribute> = WebPage;
```

## Result type

`WebPage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_large_media | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| video_cover_photo | flags.14?true | flags.14 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| display_url | string | — | — | No description provided by the pinned schema. |
| hash | int | — | — | No description provided by the pinned schema. |
| type | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| site_name | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| title | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| description | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| photo | flags.4?Photo | flags.4 | — | No description provided by the pinned schema. |
| embed_url | flags.5?string | flags.5 | — | No description provided by the pinned schema. |
| embed_type | flags.5?string | flags.5 | — | No description provided by the pinned schema. |
| embed_width | flags.6?int | flags.6 | — | No description provided by the pinned schema. |
| embed_height | flags.6?int | flags.6 | — | No description provided by the pinned schema. |
| duration | flags.7?int | flags.7 | — | No description provided by the pinned schema. |
| author | flags.8?string | flags.8 | — | No description provided by the pinned schema. |
| document | flags.9?Document | flags.9 | — | No description provided by the pinned schema. |
| cached_page | flags.10?Page | flags.10 | — | No description provided by the pinned schema. |
| attributes | flags.12?Vector<WebPageAttribute> | flags.12 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_large_media | 13 | Controlled by `flags`; present when this bit is set. |
| video_cover_photo | 14 | Controlled by `flags`; present when this bit is set. |
| type | 0 | Controlled by `flags`; present when this bit is set. |
| site_name | 1 | Controlled by `flags`; present when this bit is set. |
| title | 2 | Controlled by `flags`; present when this bit is set. |
| description | 3 | Controlled by `flags`; present when this bit is set. |
| photo | 4 | Controlled by `flags`; present when this bit is set. |
| embed_url | 5 | Controlled by `flags`; present when this bit is set. |
| embed_type | 5 | Controlled by `flags`; present when this bit is set. |
| embed_width | 6 | Controlled by `flags`; present when this bit is set. |
| embed_height | 6 | Controlled by `flags`; present when this bit is set. |
| duration | 7 | Controlled by `flags`; present when this bit is set. |
| author | 8 | Controlled by `flags`; present when this bit is set. |
| document | 9 | Controlled by `flags`; present when this bit is set. |
| cached_page | 10 | Controlled by `flags`; present when this bit is set. |
| attributes | 12 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WebPage
```

Public access: `miniproto.raw.types.WebPage`.

## Safe usage shape

```python
from miniproto.raw.types import WebPage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebPage
```

## Result family

[`WebPage`](/reference/telegram/types/results/web-page/)

## Relationships

- Result family: [`WebPage`](/reference/telegram/types/results/web-page/)
- Related constructors: [`webPageEmpty`](/reference/telegram/types/base/web-page-empty/), [`webPageNotModified`](/reference/telegram/types/base/web-page-not-modified/), [`webPagePending`](/reference/telegram/types/base/web-page-pending/)
- Accepted by: [`messageMediaWebPage`](/reference/telegram/types/base/message-media-web-page/), [`messages.webPage`](/reference/telegram/types/messages/web-page/), [`updateChannelWebPage`](/reference/telegram/types/base/update-channel-web-page/), [`updateWebPage`](/reference/telegram/types/base/update-web-page/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
