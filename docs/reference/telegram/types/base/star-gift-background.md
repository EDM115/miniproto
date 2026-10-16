---
title: "starGiftBackground"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftBackground"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xaff56398"
---

# `starGiftBackground`

No description provided by the pinned schema.

## Signature

```tl
starGiftBackground#aff56398 center_color:int edge_color:int text_color:int = StarGiftBackground;
```

## Result type

`StarGiftBackground`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| center_color | int | — | — | No description provided by the pinned schema. |
| edge_color | int | — | — | No description provided by the pinned schema. |
| text_color | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarGiftBackground
```

Public access: `miniproto.raw.types.StarGiftBackground`.

## Class reference

```python
from miniproto.raw.types import StarGiftBackground

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = StarGiftBackground
```

## Result family

[`StarGiftBackground`](/reference/telegram/types/results/star-gift-background/)

## Relationships

- Result family: [`StarGiftBackground`](/reference/telegram/types/results/star-gift-background/)
- Accepted by: [`starGift`](/reference/telegram/types/base/star-gift/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
