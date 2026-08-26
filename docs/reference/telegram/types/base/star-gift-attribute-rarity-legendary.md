---
title: "starGiftAttributeRarityLegendary"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftAttributeRarityLegendary"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xcef7e7a8"
---

# `starGiftAttributeRarityLegendary`

No description provided by the pinned schema.

## Signature

```tl
starGiftAttributeRarityLegendary#cef7e7a8 = StarGiftAttributeRarity;
```

## Result type

`StarGiftAttributeRarity`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import StarGiftAttributeRarityLegendary
```

Public access: `miniproto.raw.types.StarGiftAttributeRarityLegendary`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftAttributeRarityLegendary

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftAttributeRarityLegendary
```

## Result family

[`StarGiftAttributeRarity`](/reference/telegram/types/results/star-gift-attribute-rarity/)

## Relationships

- Result family: [`StarGiftAttributeRarity`](/reference/telegram/types/results/star-gift-attribute-rarity/)
- Related constructors: [`starGiftAttributeRarity`](/reference/telegram/types/base/star-gift-attribute-rarity/), [`starGiftAttributeRarityEpic`](/reference/telegram/types/base/star-gift-attribute-rarity-epic/), [`starGiftAttributeRarityRare`](/reference/telegram/types/base/star-gift-attribute-rarity-rare/), [`starGiftAttributeRarityUncommon`](/reference/telegram/types/base/star-gift-attribute-rarity-uncommon/)
- Accepted by: [`starGiftAttributeBackdrop`](/reference/telegram/types/base/star-gift-attribute-backdrop/), [`starGiftAttributeModel`](/reference/telegram/types/base/star-gift-attribute-model/), [`starGiftAttributePattern`](/reference/telegram/types/base/star-gift-attribute-pattern/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
