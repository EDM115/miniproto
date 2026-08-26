---
title: "starGiftCollection"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starGiftCollection"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x9d6b13b0"
---

# `starGiftCollection`

No description provided by the pinned schema.

## Signature

```tl
starGiftCollection#9d6b13b0 flags:# collection_id:int title:string icon:flags.0?Document gifts_count:int hash:long = StarGiftCollection;
```

## Result type

`StarGiftCollection`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| collection_id | int | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| icon | flags.0?Document | flags.0 | — | No description provided by the pinned schema. |
| gifts_count | int | — | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| icon | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import StarGiftCollection
```

Public access: `miniproto.raw.types.StarGiftCollection`.

## Safe usage shape

```python
from miniproto.raw.types import StarGiftCollection

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarGiftCollection
```

## Result family

[`StarGiftCollection`](/reference/telegram/types/results/star-gift-collection/)

## Relationships

- Result family: [`StarGiftCollection`](/reference/telegram/types/results/star-gift-collection/)
- Accepted by: [`payments.starGiftCollections`](/reference/telegram/types/payments/star-gift-collections/)
- Returned by: [`payments.createStarGiftCollection`](/reference/telegram/functions/payments/create-star-gift-collection/), [`payments.updateStarGiftCollection`](/reference/telegram/functions/payments/update-star-gift-collection/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
