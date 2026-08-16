---
title: "payments.getResaleStarGifts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.getResaleStarGifts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0x7a5fa236"
---

# `payments.getResaleStarGifts`

No description provided by the pinned schema.

## Signature

```tl
payments.getResaleStarGifts#7a5fa236 flags:# sort_by_price:flags.1?true sort_by_num:flags.2?true for_craft:flags.4?true stars_only:flags.5?true attributes_hash:flags.0?long gift_id:long attributes:flags.3?Vector<StarGiftAttributeId> offset:string limit:int = payments.ResaleStarGifts;
```

## Result type

`payments.ResaleStarGifts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| sort_by_price | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| sort_by_num | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| for_craft | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| stars_only | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| attributes_hash | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| gift_id | long | — | — | No description provided by the pinned schema. |
| attributes | flags.3?Vector<StarGiftAttributeId> | flags.3 | — | No description provided by the pinned schema. |
| offset | string | — | — | No description provided by the pinned schema. |
| limit | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| sort_by_price | 1 | Controlled by `flags`; present when this bit is set. |
| sort_by_num | 2 | Controlled by `flags`; present when this bit is set. |
| for_craft | 4 | Controlled by `flags`; present when this bit is set. |
| stars_only | 5 | Controlled by `flags`; present when this bit is set. |
| attributes_hash | 0 | Controlled by `flags`; present when this bit is set. |
| attributes | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import PaymentsGetResaleStarGifts
```

Public access: `miniproto.raw.functions.PaymentsGetResaleStarGifts`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsGetResaleStarGifts

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsGetResaleStarGifts
```

## Result family

[`payments.ResaleStarGifts`](/reference/telegram/types/results/payments-resale-star-gifts/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`STARGIFT_ATTRIBUTE_INVALID`](/reference/telegram/errors/stargift-attribute-invalid/) | One of the specified star gift attributes is invalid. |
| 400 | [`STARGIFT_INVALID`](/reference/telegram/errors/stargift-invalid/) | The passed gift is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`StarGiftAttributeId`](/reference/telegram/types/results/star-gift-attribute-id/)
Known selected constructors: [`starGiftAttributeIdBackdrop`](/reference/telegram/types/base/star-gift-attribute-id-backdrop/), [`starGiftAttributeIdModel`](/reference/telegram/types/base/star-gift-attribute-id-model/), [`starGiftAttributeIdPattern`](/reference/telegram/types/base/star-gift-attribute-id-pattern/)

## Returned types

[`payments.ResaleStarGifts`](/reference/telegram/types/results/payments-resale-star-gifts/)
Known selected constructors: [`payments.resaleStarGifts`](/reference/telegram/types/payments/resale-star-gifts/)

## Availability evidence

- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
