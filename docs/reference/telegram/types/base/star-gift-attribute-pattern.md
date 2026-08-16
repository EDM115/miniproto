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
layer: 228
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

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAttributePattern

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAttributePattern
```

## Result family

[`StarGiftAttribute`](/reference/telegram/types/results/star-gift-attribute/)

## Relationships

- Result family: [`StarGiftAttribute`](/reference/telegram/types/results/star-gift-attribute/)
- Related constructors: [`starGiftAttributeBackdrop`](/reference/telegram/types/base/star-gift-attribute-backdrop/), [`starGiftAttributeModel`](/reference/telegram/types/base/star-gift-attribute-model/), [`starGiftAttributeOriginalDetails`](/reference/telegram/types/base/star-gift-attribute-original-details/)
- Accepted by: [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/), [`payments.starGiftUpgradeAttributes`](/reference/telegram/types/payments/star-gift-upgrade-attributes/), [`payments.starGiftUpgradePreview`](/reference/telegram/types/payments/star-gift-upgrade-preview/), [`starGiftUnique`](/reference/telegram/types/base/star-gift-unique/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
