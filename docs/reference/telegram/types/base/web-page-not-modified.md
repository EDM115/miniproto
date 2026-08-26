---
title: "webPageNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webPageNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x7311ca11"
---

# `webPageNotModified`

No description provided by the pinned schema.

## Signature

```tl
webPageNotModified#7311ca11 flags:# cached_page_views:flags.0?int = WebPage;
```

## Result type

`WebPage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| cached_page_views | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| cached_page_views | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WebPageNotModified
```

Public access: `miniproto.raw.types.WebPageNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import WebPageNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebPageNotModified
```

## Result family

[`WebPage`](/reference/telegram/types/results/web-page/)

## Relationships

- Result family: [`WebPage`](/reference/telegram/types/results/web-page/)
- Related constructors: [`webPage`](/reference/telegram/types/base/web-page/), [`webPageEmpty`](/reference/telegram/types/base/web-page-empty/), [`webPagePending`](/reference/telegram/types/base/web-page-pending/)
- Accepted by: [`messageMediaWebPage`](/reference/telegram/types/base/message-media-web-page/), [`messages.webPage`](/reference/telegram/types/messages/web-page/), [`updateChannelWebPage`](/reference/telegram/types/base/update-channel-web-page/), [`updateWebPage`](/reference/telegram/types/base/update-web-page/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
