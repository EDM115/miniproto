---
title: "page"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "page"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x98657f0d"
---

# `page`

No description provided by the pinned schema.

## Signature

```tl
page#98657f0d flags:# part:flags.0?true rtl:flags.1?true v2:flags.2?true url:string blocks:Vector<PageBlock> photos:Vector<Photo> documents:Vector<Document> views:flags.3?int = Page;
```

## Result type

`Page`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| part | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| rtl | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| v2 | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| blocks | Vector<PageBlock> | — | — | No description provided by the pinned schema. |
| photos | Vector<Photo> | — | — | No description provided by the pinned schema. |
| documents | Vector<Document> | — | — | No description provided by the pinned schema. |
| views | flags.3?int | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| part | 0 | Controlled by `flags`; present when this bit is set. |
| rtl | 1 | Controlled by `flags`; present when this bit is set. |
| v2 | 2 | Controlled by `flags`; present when this bit is set. |
| views | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Page
```

Public access: `miniproto.raw.types.Page`.

## Safe usage shape

```python
from miniproto.raw.types import Page

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Page
```

## Result family

[`Page`](/reference/telegram/types/results/page/)

## Relationships

- Result family: [`Page`](/reference/telegram/types/results/page/)
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
