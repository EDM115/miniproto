---
title: "starGiftAttributePattern"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAttributePattern"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4e7085ea"
---

# `starGiftAttributePattern`

No description provided by the pinned schema.

## Signature

```tl
starGiftAttributePattern#4e7085ea name:string document:Document rarity:StarGiftAttributeRarity = StarGiftAttribute;
```

## Result type

`StarGiftAttribute`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| name | string | — | — | No description provided by the pinned schema. |
| document | Document | — | — | No description provided by the pinned schema. |
| rarity | StarGiftAttributeRarity | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarGiftAttributePattern
```

Public access: `miniproto.raw.types.StarGiftAttributePattern`.

## Class reference

```python
from miniproto.raw.types import StarGiftAttributePattern

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = StarGiftAttributePattern
```

## Result family

[`StarGiftAttribute`](/reference/telegram/types/results/star-gift-attribute/)

## Relationships

- Result family: [`StarGiftAttribute`](/reference/telegram/types/results/star-gift-attribute/)
- Related constructors: [`starGiftAttributeBackdrop`](/reference/telegram/types/base/star-gift-attribute-backdrop/), [`starGiftAttributeModel`](/reference/telegram/types/base/star-gift-attribute-model/), [`starGiftAttributeOriginalDetails`](/reference/telegram/types/base/star-gift-attribute-original-details/)
- Accepted by: [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.starGiftUpgradeAttributes`](/reference/telegram/types/payments/star-gift-upgrade-attributes/), [`payments.starGiftUpgradePreview`](/reference/telegram/types/payments/star-gift-upgrade-preview/), [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
