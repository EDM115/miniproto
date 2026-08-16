---
title: "payments.savedStarGifts"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.savedStarGifts"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0x95f389b1"
---

# `payments.savedStarGifts`

No description provided by the pinned schema.

## Signature

```tl
payments.savedStarGifts#95f389b1 flags:# count:int chat_notifications_enabled:flags.1?Bool gifts:Vector<SavedStarGift> next_offset:flags.0?string chats:Vector<Chat> users:Vector<User> = payments.SavedStarGifts;
```

## Result type

`payments.SavedStarGifts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |
| chat_notifications_enabled | flags.1?Bool | flags.1 | — | No description provided by the pinned schema. |
| gifts | Vector<SavedStarGift> | — | — | No description provided by the pinned schema. |
| next_offset | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| chat_notifications_enabled | 1 | Controlled by `flags`; present when this bit is set. |
| next_offset | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PaymentsSavedStarGifts
```

Public access: `miniproto.raw.types.PaymentsSavedStarGifts`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsSavedStarGifts

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsSavedStarGifts
```

## Result family

[`payments.SavedStarGifts`](/reference/telegram/types/results/payments-saved-star-gifts/)

## Relationships

- Result family: [`payments.SavedStarGifts`](/reference/telegram/types/results/payments-saved-star-gifts/)
- Returned by: [`payments.getCraftStarGifts`](/reference/telegram/functions/payments/get-craft-star-gifts/), [`payments.getSavedStarGift`](/reference/telegram/functions/payments/get-saved-star-gift/), [`payments.getSavedStarGifts`](/reference/telegram/functions/payments/get-saved-star-gifts/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
