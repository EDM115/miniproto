---
title: "payments.uniqueStarGiftValueInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.uniqueStarGiftValueInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x512fe446"
---

# `payments.uniqueStarGiftValueInfo`

No description provided by the pinned schema.

## Signature

```tl
payments.uniqueStarGiftValueInfo#512fe446 flags:# last_sale_on_fragment:flags.1?true value_is_average:flags.6?true currency:string value:long initial_sale_date:int initial_sale_stars:long initial_sale_price:long last_sale_date:flags.0?int last_sale_price:flags.0?long floor_price:flags.2?long average_price:flags.3?long listed_count:flags.4?int fragment_listed_count:flags.5?int fragment_listed_url:flags.5?string = payments.UniqueStarGiftValueInfo;
```

## Result type

`payments.UniqueStarGiftValueInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| last_sale_on_fragment | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| value_is_average | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| value | long | — | — | No description provided by the pinned schema. |
| initial_sale_date | int | — | — | No description provided by the pinned schema. |
| initial_sale_stars | long | — | — | No description provided by the pinned schema. |
| initial_sale_price | long | — | — | No description provided by the pinned schema. |
| last_sale_date | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| last_sale_price | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| floor_price | flags.2?long | flags.2 | — | No description provided by the pinned schema. |
| average_price | flags.3?long | flags.3 | — | No description provided by the pinned schema. |
| listed_count | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| fragment_listed_count | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| fragment_listed_url | flags.5?string | flags.5 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| last_sale_on_fragment | 1 | Controlled by `flags`; present when this bit is set. |
| value_is_average | 6 | Controlled by `flags`; present when this bit is set. |
| last_sale_date | 0 | Controlled by `flags`; present when this bit is set. |
| last_sale_price | 0 | Controlled by `flags`; present when this bit is set. |
| floor_price | 2 | Controlled by `flags`; present when this bit is set. |
| average_price | 3 | Controlled by `flags`; present when this bit is set. |
| listed_count | 4 | Controlled by `flags`; present when this bit is set. |
| fragment_listed_count | 5 | Controlled by `flags`; present when this bit is set. |
| fragment_listed_url | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsUniqueStarGiftValueInfo
```

Public access: `miniproto.raw.types.PaymentsUniqueStarGiftValueInfo`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsUniqueStarGiftValueInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsUniqueStarGiftValueInfo
```

## Result family

[`payments.UniqueStarGiftValueInfo`](/reference/telegram/types/results/payments-unique-star-gift-value-info/)

## Relationships

- Result family: [`payments.UniqueStarGiftValueInfo`](/reference/telegram/types/results/payments-unique-star-gift-value-info/)
- Returned by: [`payments.getUniqueStarGiftValueInfo`](/reference/telegram/functions/payments/get-unique-star-gift-value-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
