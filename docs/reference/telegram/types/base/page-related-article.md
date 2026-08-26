---
title: "pageRelatedArticle"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "pageRelatedArticle"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb390dc08"
---

# `pageRelatedArticle`

No description provided by the pinned schema.

## Signature

```tl
pageRelatedArticle#b390dc08 flags:# url:string webpage_id:long title:flags.0?string description:flags.1?string photo_id:flags.2?long author:flags.3?string published_date:flags.4?int = PageRelatedArticle;
```

## Result type

`PageRelatedArticle`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| webpage_id | long | — | — | No description provided by the pinned schema. |
| title | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| description | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| photo_id | flags.2?long | flags.2 | — | No description provided by the pinned schema. |
| author | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| published_date | flags.4?int | flags.4 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| title | 0 | Controlled by `flags`; present when this bit is set. |
| description | 1 | Controlled by `flags`; present when this bit is set. |
| photo_id | 2 | Controlled by `flags`; present when this bit is set. |
| author | 3 | Controlled by `flags`; present when this bit is set. |
| published_date | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PageRelatedArticle
```

Public access: `miniproto.raw.types.PageRelatedArticle`.

## Safe usage shape

```python
from miniproto.raw.types import PageRelatedArticle

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PageRelatedArticle
```

## Result family

[`PageRelatedArticle`](/reference/telegram/types/results/page-related-article/)

## Relationships

- Result family: [`PageRelatedArticle`](/reference/telegram/types/results/page-related-article/)
- Accepted by: [`pageBlockRelatedArticles`](/reference/telegram/types/base/page-block-related-articles/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
