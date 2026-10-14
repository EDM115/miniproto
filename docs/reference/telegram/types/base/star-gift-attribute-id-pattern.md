---
title: "starGiftAttributeIdPattern"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAttributeIdPattern"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4a162433"
---

# `starGiftAttributeIdPattern`

No description provided by the pinned schema.

## Signature

```tl
starGiftAttributeIdPattern#4a162433 document_id:long = StarGiftAttributeId;
```

## Result type

`StarGiftAttributeId`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| document_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarGiftAttributeIdPattern
```

Public access: `miniproto.raw.types.StarGiftAttributeIdPattern`.

## Class reference

```python
from miniproto.raw.types import StarGiftAttributeIdPattern

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = StarGiftAttributeIdPattern
```

## Result family

[`StarGiftAttributeId`](/reference/telegram/types/results/star-gift-attribute-id/)

## Relationships

- Result family: [`StarGiftAttributeId`](/reference/telegram/types/results/star-gift-attribute-id/)
- Related constructors: [`starGiftAttributeIdBackdrop`](/reference/telegram/types/base/star-gift-attribute-id-backdrop/), [`starGiftAttributeIdModel`](/reference/telegram/types/base/star-gift-attribute-id-model/)
- Accepted by: [`payments.getResaleStarGifts`](/reference/telegram/functions/payments/get-resale-star-gifts/), [`starGiftAttributeCounter`](/reference/telegram/types/base/star-gift-attribute-counter/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
