---
title: "payments.resaleStarGifts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.resaleStarGifts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0x947a12df"
---

# `payments.resaleStarGifts`

No description provided by the pinned schema.

## Signature

```tl
payments.resaleStarGifts#947a12df flags:# count:int gifts:Vector<StarGift> next_offset:flags.0?string attributes:flags.1?Vector<StarGiftAttribute> attributes_hash:flags.1?long chats:Vector<Chat> counters:flags.2?Vector<StarGiftAttributeCounter> users:Vector<User> = payments.ResaleStarGifts;
```

## Result type

`payments.ResaleStarGifts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| gifts | Vector<StarGift> | — | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| attributes | flags.1?Vector<StarGiftAttribute> | flags.1 | — | No description provided by the pinned schema. |
| attributes_hash | flags.1?long | flags.1 | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| counters | flags.2?Vector<StarGiftAttributeCounter> | flags.2 | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |
| attributes | 1 | Controlled by `flags`; present when this bit is set. |
| attributes_hash | 1 | Controlled by `flags`; present when this bit is set. |
| counters | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsResaleStarGifts
```

Public access: `miniproto.raw.types.PaymentsResaleStarGifts`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsResaleStarGifts

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsResaleStarGifts
```

## Result family

[`payments.ResaleStarGifts`](/reference/telegram/types/results/payments-resale-star-gifts/)

## Relationships

- Result family: [`payments.ResaleStarGifts`](/reference/telegram/types/results/payments-resale-star-gifts/)
- Returned by: [`payments.getResaleStarGifts`](/reference/telegram/functions/payments/get-resale-star-gifts/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
