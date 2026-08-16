---
title: "starGiftAttributeIdModel"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAttributeIdModel"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x48aaae3c"
---

# `starGiftAttributeIdModel`

No description provided by the pinned schema.

## Signature

```tl
starGiftAttributeIdModel#48aaae3c document_id:long = StarGiftAttributeId;
```

## Result type

`StarGiftAttributeId`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| document_id | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarGiftAttributeIdModel
```

Public access: `miniproto.raw.types.StarGiftAttributeIdModel`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAttributeIdModel

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAttributeIdModel
```

## Result family

[`StarGiftAttributeId`](/reference/telegram/types/results/star-gift-attribute-id/)

## Relationships

- Result family: [`StarGiftAttributeId`](/reference/telegram/types/results/star-gift-attribute-id/)
- Related constructors: [`starGiftAttributeIdBackdrop`](/reference/telegram/types/base/star-gift-attribute-id-backdrop/), [`starGiftAttributeIdPattern`](/reference/telegram/types/base/star-gift-attribute-id-pattern/)
- Accepted by: [`payments.getResaleStarGifts`](/reference/telegram/functions/payments/get-resale-star-gifts/), [`starGiftAttributeCounter`](/reference/telegram/types/base/star-gift-attribute-counter/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
