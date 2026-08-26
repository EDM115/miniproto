---
title: "starGiftAttributeBackdrop"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAttributeBackdrop"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x9f2504e4"
---

# `starGiftAttributeBackdrop`

No description provided by the pinned schema.

## Signature

```tl
starGiftAttributeBackdrop#9f2504e4 name:string backdrop_id:int center_color:int edge_color:int pattern_color:int text_color:int rarity:StarGiftAttributeRarity = StarGiftAttribute;
```

## Result type

`StarGiftAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| name | string | — | — | No description provided by the pinned schema. |
| backdrop_id | int | — | — | No description provided by the pinned schema. |
| center_color | int | — | — | No description provided by the pinned schema. |
| edge_color | int | — | — | No description provided by the pinned schema. |
| pattern_color | int | — | — | No description provided by the pinned schema. |
| text_color | int | — | — | No description provided by the pinned schema. |
| rarity | StarGiftAttributeRarity | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarGiftAttributeBackdrop
```

Public access: `miniproto.raw.types.StarGiftAttributeBackdrop`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAttributeBackdrop

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAttributeBackdrop
```

## Result family

[`StarGiftAttribute`](/reference/telegram/types/results/star-gift-attribute/)

## Relationships

- Result family: [`StarGiftAttribute`](/reference/telegram/types/results/star-gift-attribute/)
- Related constructors: [`starGiftAttributeModel`](/reference/telegram/types/base/star-gift-attribute-model/), [`starGiftAttributeOriginalDetails`](/reference/telegram/types/base/star-gift-attribute-original-details/), [`starGiftAttributePattern`](/reference/telegram/types/base/star-gift-attribute-pattern/)
- Accepted by: [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.starGiftUpgradeAttributes`](/reference/telegram/types/payments/star-gift-upgrade-attributes/), [`payments.starGiftUpgradePreview`](/reference/telegram/types/payments/star-gift-upgrade-preview/), [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
