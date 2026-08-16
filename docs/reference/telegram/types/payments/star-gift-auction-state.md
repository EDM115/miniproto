---
title: "payments.starGiftAuctionState"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.starGiftAuctionState"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0x6b39f4ec"
---

# `payments.starGiftAuctionState`

No description provided by the pinned schema.

## Signature

```tl
payments.starGiftAuctionState#6b39f4ec gift:StarGift state:StarGiftAuctionState user_state:StarGiftAuctionUserState timeout:int users:Vector<User> chats:Vector<Chat> = payments.StarGiftAuctionState;
```

## Result type

`payments.StarGiftAuctionState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| gift | StarGift | — | — | No description provided by the pinned schema. |
| state | StarGiftAuctionState | — | — | No description provided by the pinned schema. |
| user_state | StarGiftAuctionUserState | — | — | No description provided by the pinned schema. |
| timeout | int | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentsStarGiftAuctionState
```

Public access: `miniproto.raw.types.PaymentsStarGiftAuctionState`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsStarGiftAuctionState

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsStarGiftAuctionState
```

## Result family

[`payments.StarGiftAuctionState`](/reference/telegram/types/results/payments-star-gift-auction-state/)

## Relationships

- Result family: [`payments.StarGiftAuctionState`](/reference/telegram/types/results/payments-star-gift-auction-state/)
- Returned by: [`payments.getStarGiftAuctionState`](/reference/telegram/functions/payments/get-star-gift-auction-state/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
