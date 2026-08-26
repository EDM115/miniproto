---
title: "stickers.suggestedShortName"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "stickers.suggestedShortName"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "stickers"
schema_source: "tdlib"
constructor_id: "0x85fea03f"
---

# `stickers.suggestedShortName`

No description provided by the pinned schema.

## Signature

```tl
stickers.suggestedShortName#85fea03f short_name:string = stickers.SuggestedShortName;
```

## Result type

`stickers.SuggestedShortName`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| short_name | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StickersSuggestedShortName
```

Public access: `miniproto.raw.types.StickersSuggestedShortName`.

## Safe usage shape

```python
from miniproto.raw.types import StickersSuggestedShortName

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StickersSuggestedShortName
```

## Result family

[`stickers.SuggestedShortName`](/reference/telegram/types/results/stickers-suggested-short-name/)

## Relationships

- Result family: [`stickers.SuggestedShortName`](/reference/telegram/types/results/stickers-suggested-short-name/)
- Returned by: [`stickers.suggestShortName`](/reference/telegram/functions/stickers/suggest-short-name/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
